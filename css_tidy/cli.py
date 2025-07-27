"""
Command-line interface for CSS Tidy.

This module provides the CLI functionality for the css-tidy package.
"""

import os
import sys
import glob
from pathlib import Path
from typing import List, Optional

import click
from colorama import init, Fore, Style

from .tidy import CSSFormatter, CSSMinifier, CSSValidator

# Initialize colorama for cross-platform colored output
init(autoreset=True)


def print_success(message: str) -> None:
    """Print a success message in green."""
    print(f"{Fore.GREEN}✓{Style.RESET_ALL} {message}")


def print_error(message: str) -> None:
    """Print an error message in red."""
    print(f"{Fore.RED}✗{Style.RESET_ALL} {message}")


def print_warning(message: str) -> None:
    """Print a warning message in yellow."""
    print(f"{Fore.YELLOW}⚠{Style.RESET_ALL} {message}")


def print_info(message: str) -> None:
    """Print an info message in blue."""
    print(f"{Fore.BLUE}ℹ{Style.RESET_ALL} {message}")


def get_css_files(input_path: str) -> List[str]:
    """
    Get list of CSS files from input path.
    
    Args:
        input_path: File path or glob pattern
        
    Returns:
        List of CSS file paths
    """
    if os.path.isfile(input_path):
        return [input_path]
    
    # Handle glob patterns
    files = glob.glob(input_path)
    css_files = [f for f in files if f.lower().endswith('.css')]
    
    if not css_files:
        print_warning(f"No CSS files found matching: {input_path}")
    
    return css_files


def process_file(input_file: str, 
                output_file: Optional[str], 
                formatter: CSSFormatter,
                minifier: CSSMinifier,
                validator: CSSValidator,
                verbose: bool = False,
                should_minify: bool = False) -> bool:
    """
    Process a single CSS file.
    
    Args:
        input_file: Input CSS file path
        output_file: Output file path (optional)
        formatter: CSS formatter instance
        minifier: CSS minifier instance
        validator: CSS validator instance
        verbose: Enable verbose output
        
    Returns:
        True if successful, False otherwise
    """
    try:
        if verbose:
            print_info(f"Processing: {input_file}")
        
        # Validate CSS first
        if not validator.validate_file(input_file):
            errors = validator.get_errors()
            warnings = validator.get_warnings()
            
            for error in errors:
                print_error(f"{input_file}: {error}")
            
            for warning in warnings:
                print_warning(f"{input_file}: {warning}")
            
            if errors:
                return False
        
        # Read input file
        with open(input_file, 'r', encoding='utf-8') as f:
            css_code = f.read()
        
        # Count original lines and size
        original_lines = len(css_code.split('\n'))
        original_size = len(css_code.encode('utf-8'))
        
        # Process CSS
        if should_minify:
            processed_css = minifier.minify(css_code)
        else:
            processed_css = formatter.format(css_code)
        
        # Calculate final lines and size
        final_lines = len(processed_css.split('\n'))
        final_size = len(processed_css.encode('utf-8'))
        
        # Show statistics if duplicates were removed
        if formatter.remove_duplicates:
            lines_removed = original_lines - final_lines
            size_removed = original_size - final_size
            
            line_reduction_percent = (lines_removed / original_lines) * 100 if original_lines > 0 else 0
            size_reduction_percent = (size_removed / original_size) * 100 if original_size > 0 else 0
            
            print_info(f"Lines: {original_lines:,} → {final_lines:,} (saved {lines_removed:,} lines, {line_reduction_percent:.1f}%)")
            print_info(f"Size: {original_size:,} → {final_size:,} bytes (saved {size_removed:,} bytes, {size_reduction_percent:.1f}%)")
        
        # Determine output file
        if output_file is None:
            if input_file.endswith('.css'):
                output_file = input_file.replace('.css', '.tidy.css')
            else:
                output_file = input_file + '.tidy'
        
        # Write output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(processed_css)
        
        if verbose:
            print_success(f"Output written to: {output_file}")
        else:
            print_success(f"Processed: {input_file} → {output_file}")
        
        return True
        
    except Exception as e:
        print_error(f"Error processing {input_file}: {str(e)}")
        return False


@click.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('-o', '--output', type=click.Path(), help='Output file path')
@click.option('-i', '--indent', type=int, default=2, help='Indentation size (default: 2)')
@click.option('-m', '--minify', is_flag=True, help='Minify CSS output')
@click.option('-s', '--sort', is_flag=True, help='Sort CSS properties')
@click.option('-c', '--remove-comments', is_flag=True, help='Remove CSS comments')
@click.option('-g', '--group', is_flag=True, help='Group CSS selectors by prefix')
@click.option('-d', '--remove-duplicates', is_flag=True, help='Remove duplicate CSS rules')
@click.option('--duplicate-report', type=click.Path(), help='Generate JSON report of duplicate rules')
@click.option('-v', '--verbose', is_flag=True, help='Enable verbose output')
@click.option('--validate-only', is_flag=True, help='Only validate CSS, do not format')
@click.version_option(version="0.1.3", prog_name='css-tidy')
def main(input_file: str, 
         output: Optional[str], 
         indent: int, 
         minify: bool, 
         sort: bool, 
         remove_comments: bool, 
         group: bool,
         remove_duplicates: bool,
         duplicate_report: Optional[str],
         verbose: bool,
         validate_only: bool) -> None:
    """
    CSS Tidy - Format and validate CSS files.
    
    INPUT_FILE can be a single CSS file or a glob pattern (e.g., *.css)
    """
    try:
        # Get CSS files to process
        css_files = get_css_files(input_file)
        
        if not css_files:
            print_error("No CSS files found to process")
            sys.exit(1)
        
        if verbose:
            print_info(f"Found {len(css_files)} CSS file(s) to process")
        
        # Initialize processors
        formatter = CSSFormatter(
            indent_size=indent,
            sort_properties=sort,
            remove_comments=remove_comments,
            group_selectors=group,
            remove_duplicates=remove_duplicates
        )
        
        minifier = CSSMinifier(
            remove_comments=remove_comments
        )
        
        validator = CSSValidator()
        
        # Handle duplicate detection and reporting
        if duplicate_report or remove_duplicates:
            print_info("Starting duplicate detection...")
            from .tidy import CSSDuplicateDetector
            duplicate_detector = CSSDuplicateDetector()
            
            for css_file in css_files:
                with open(css_file, 'r', encoding='utf-8') as f:
                    css_code = f.read()
                
                # Count original lines and file size
                original_lines = len(css_code.split('\n'))
                original_size = len(css_code.encode('utf-8'))
                
                duplicates = duplicate_detector.detect_duplicates(css_code)
                
                if duplicates:
                    if verbose:
                        print_info(f"Found {len(duplicates)} duplicate rule(s) in {css_file}")
                    
                    if duplicate_report:
                        report_path = duplicate_report if len(css_files) == 1 else f"{duplicate_report}_{Path(css_file).stem}.json"
                        duplicate_detector.generate_report(report_path)
                        print_success(f"Duplicate report saved to: {report_path}")
                    
                    # Show duplicate summary
                    removable_count = len([d for d in duplicates if d.is_removable])
                    print_info(f"Duplicates found: {len(duplicates)} total, {removable_count} removable")
                else:
                    print_info("No duplicates found")
        
        # Process files
        success_count = 0
        total_count = len(css_files)
        
        for css_file in css_files:
            if validate_only:
                # Only validate
                if validator.validate_file(css_file):
                    print_success(f"Valid: {css_file}")
                    success_count += 1
                else:
                    errors = validator.get_errors()
                    warnings = validator.get_warnings()
                    
                    for error in errors:
                        print_error(f"{css_file}: {error}")
                    
                    for warning in warnings:
                        print_warning(f"{css_file}: {warning}")
            else:
                # Format/minify
                if process_file(css_file, output, formatter, minifier, validator, verbose, minify):
                    success_count += 1
        
        # Summary
        if verbose or total_count > 1:
            print_info(f"Processed {success_count}/{total_count} files successfully")
        
        if success_count < total_count:
            sys.exit(1)
            
    except KeyboardInterrupt:
        print_error("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main() 
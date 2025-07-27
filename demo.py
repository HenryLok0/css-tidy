#!/usr/bin/env python3
"""
Demo script for CSS Tidy functionality.

This script demonstrates the various features of the CSS Tidy package.
"""

from css_tidy import CSSFormatter, CSSMinifier, CSSValidator


def demo_formatting():
    """Demonstrate CSS formatting functionality."""
    print("=== CSS Formatting Demo ===")
    
    # Sample messy CSS
    messy_css = """
    body{margin:0;padding:0;font-family:Arial,sans-serif}
    .container{width:100%;max-width:1200px;margin:0 auto;padding:20px}
    .header{background-color:#333;color:white;padding:10px 20px;text-align:center}
    """
    
    print("Original CSS:")
    print(messy_css)
    
    # Basic formatting
    formatter = CSSFormatter()
    formatted_css = formatter.format(messy_css)
    
    print("\nFormatted CSS:")
    print(formatted_css)
    
    # Custom indentation
    formatter_4space = CSSFormatter(indent_size=4)
    formatted_4space = formatter_4space.format(messy_css)
    
    print("\nFormatted CSS (4-space indentation):")
    print(formatted_4space)
    
    # With property sorting
    formatter_sorted = CSSFormatter(sort_properties=True)
    formatted_sorted = formatter_sorted.format(messy_css)
    
    print("\nFormatted CSS (sorted properties):")
    print(formatted_sorted)
    
    # With grouping
    print("\n=== CSS Grouping Demo ===")
    
    grouped_css = """
    .button{background-color:#007bff;color:white;padding:10px 20px}
    .button-primary{background-color:#28a745}
    .button-secondary{background-color:#6c757d}
    .card{background-color:white;border-radius:8px}
    .card-header{padding:20px;border-bottom:1px solid #e9ecef}
    .card-body{padding:20px}
    .nav{background-color:#333;padding:15px}
    .nav-link{color:white;text-decoration:none}
    """
    
    print("Original CSS:")
    print(grouped_css)
    
    # Grouped formatting
    formatter_grouped = CSSFormatter(group_selectors=True)
    formatted_grouped = formatter_grouped.format(grouped_css)
    
    print("\nGrouped CSS:")
    print(formatted_grouped)


def demo_minification():
    """Demonstrate CSS minification functionality."""
    print("\n=== CSS Minification Demo ===")
    
    # Sample formatted CSS
    formatted_css = """
    body {
        margin: 0;
        padding: 0;
        font-family: Arial, sans-serif;
    }
    
    .container {
        width: 100%;
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
    }
    """
    
    print("Original CSS:")
    print(formatted_css)
    
    # Minify
    minifier = CSSMinifier()
    minified_css = minifier.minify(formatted_css)
    
    print("\nMinified CSS:")
    print(minified_css)


def demo_validation():
    """Demonstrate CSS validation functionality."""
    print("\n=== CSS Validation Demo ===")
    
    # Valid CSS
    valid_css = "body { margin: 0; padding: 0; }"
    print("Valid CSS:", valid_css)
    
    validator = CSSValidator()
    is_valid = validator.validate(valid_css)
    print(f"Valid: {is_valid}")
    
    # Invalid CSS
    invalid_css = "body { margin: 0; padding: 0"  # Missing closing brace
    print(f"\nInvalid CSS: {invalid_css}")
    
    is_valid = validator.validate(invalid_css)
    print(f"Valid: {is_valid}")
    
    errors = validator.get_errors()
    warnings = validator.get_warnings()
    
    if errors:
        print("Errors:")
        for error in errors:
            print(f"  - {error}")
    
    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"  - {warning}")


def demo_file_operations():
    """Demonstrate file operations."""
    print("\n=== File Operations Demo ===")
    
    # Create a temporary CSS file
    import tempfile
    import os
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.css', delete=False) as f:
        f.write("body{margin:0;padding:0}.container{width:100%}")
        temp_file = f.name
    
    try:
        print(f"Created temporary file: {temp_file}")
        
        # Format the file
        formatter = CSSFormatter()
        formatted_content = formatter.format_file(temp_file)
        
        print("\nFormatted content:")
        print(formatted_content)
        
        # Minify the file
        minifier = CSSMinifier()
        minified_content = minifier.minify_file(temp_file)
        
        print("\nMinified content:")
        print(minified_content)
        
        # Validate the file
        validator = CSSValidator()
        is_valid = validator.validate_file(temp_file)
        print(f"\nFile is valid: {is_valid}")
        
    finally:
        # Clean up
        os.unlink(temp_file)
        print(f"\nCleaned up temporary file: {temp_file}")


def main():
    """Run all demos."""
    print("CSS Tidy Demo")
    print("=" * 50)
    
    try:
        demo_formatting()
        demo_minification()
        demo_validation()
        demo_file_operations()
        
        print("\n" + "=" * 50)
        print("Demo completed successfully!")
        
    except Exception as e:
        print(f"\nError during demo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main() 
"""
Tests for CSS Tidy functionality.
"""

import tempfile
import os
from css_tidy.tidy import CSSFormatter, CSSMinifier, CSSValidator

# Only import pytest if available
try:
    import pytest  # type: ignore
    PYTEST_AVAILABLE = True
except ImportError:
    PYTEST_AVAILABLE = False


class TestCSSFormatter:
    """Test CSS formatter functionality."""
    
    def test_basic_formatting(self):
        """Test basic CSS formatting."""
        formatter = CSSFormatter()
        css_input = "body{margin:0;padding:0}"
        expected = "body {\n  margin: 0;\n  padding: 0;\n}"
        
        result = formatter.format(css_input)
        assert result == expected
    
    def test_custom_indent(self):
        """Test custom indentation."""
        formatter = CSSFormatter(indent_size=4)
        css_input = "body{margin:0}"
        expected = "body {\n    margin: 0;\n}"
        
        result = formatter.format(css_input)
        assert result == expected
    
    def test_sort_properties(self):
        """Test property sorting."""
        formatter = CSSFormatter(sort_properties=True)
        css_input = "body{padding:0;margin:0}"
        expected = "body {\n  margin: 0;\n  padding: 0;\n}"
        
        result = formatter.format(css_input)
        assert result == expected
    
    def test_remove_comments(self):
        """Test comment removal."""
        formatter = CSSFormatter(remove_comments=True)
        css_input = "/* comment */ body{margin:0}"
        expected = "body {\n  margin: 0;\n}"
        
        result = formatter.format(css_input)
        assert result == expected
    
    def test_empty_input(self):
        """Test empty input handling."""
        formatter = CSSFormatter()
        result = formatter.format("")
        assert result == ""
        
        result = formatter.format("   ")
        assert result == ""


class TestCSSMinifier:
    """Test CSS minifier functionality."""
    
    def test_basic_minification(self):
        """Test basic CSS minification."""
        minifier = CSSMinifier()
        css_input = """
        body {
            margin: 0;
            padding: 0;
        }
        """
        expected = "body{margin:0;padding:0}"
        
        result = minifier.minify(css_input)
        assert result == expected
    
    def test_remove_comments(self):
        """Test comment removal in minification."""
        minifier = CSSMinifier(remove_comments=True)
        css_input = "/* comment */ body{margin:0}"
        expected = "body{margin:0}"
        
        result = minifier.minify(css_input)
        assert result == expected
    
    def test_preserve_comments(self):
        """Test comment preservation."""
        minifier = CSSMinifier(remove_comments=False)
        css_input = "/* comment */ body{margin:0}"
        expected = "/* comment */ body{margin:0}"
        
        result = minifier.minify(css_input)
        assert result == expected


class TestCSSValidator:
    """Test CSS validator functionality."""
    
    def test_valid_css(self):
        """Test valid CSS validation."""
        validator = CSSValidator()
        css_input = "body { margin: 0; }"
        
        result = validator.validate(css_input)
        assert result is True
        assert len(validator.get_errors()) == 0
    
    def test_unbalanced_braces(self):
        """Test unbalanced braces detection."""
        validator = CSSValidator()
        css_input = "body { margin: 0;"
        
        result = validator.validate(css_input)
        assert result is False
        assert len(validator.get_errors()) > 0
    
    def test_missing_semicolon(self):
        """Test missing semicolon detection."""
        validator = CSSValidator()
        css_input = "body { margin: 0 }"
        
        result = validator.validate(css_input)
        assert result is True  # Missing semicolon is a warning, not error
        assert len(validator.get_warnings()) > 0
    
    def test_unclosed_comments(self):
        """Test unclosed comments detection."""
        validator = CSSValidator()
        css_input = "/* comment body { margin: 0; }"
        
        result = validator.validate(css_input)
        assert result is False
        assert len(validator.get_errors()) > 0


class TestFileOperations:
    """Test file operations."""
    
    def test_format_file(self):
        """Test formatting a file."""
        formatter = CSSFormatter()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.css', delete=False) as f:
            f.write("body{margin:0}")
            input_file = f.name
        
        try:
            result = formatter.format_file(input_file)
            expected = "body {\n  margin: 0;\n}"
            assert result == expected
        finally:
            os.unlink(input_file)
    
    def test_minify_file(self):
        """Test minifying a file."""
        minifier = CSSMinifier()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.css', delete=False) as f:
            f.write("body {\n  margin: 0;\n}")
            input_file = f.name
        
        try:
            result = minifier.minify_file(input_file)
            expected = "body{margin:0}"
            assert result == expected
        finally:
            os.unlink(input_file)
    
    def test_validate_file(self):
        """Test validating a file."""
        validator = CSSValidator()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.css', delete=False) as f:
            f.write("body { margin: 0; }")
            input_file = f.name
        
        try:
            result = validator.validate_file(input_file)
            assert result is True
        finally:
            os.unlink(input_file)


if __name__ == '__main__':
    if PYTEST_AVAILABLE:
        pytest.main([__file__])
    else:
        print("pytest not available. Install with: pip install pytest") 
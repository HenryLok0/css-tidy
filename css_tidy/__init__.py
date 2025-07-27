"""
CSS Tidy - A Python tool to tidy and format CSS files.

This module provides functionality to format, minify, and validate CSS code.
"""

__version__ = "0.1.5"
__author__ = "Henry Lok"
__email__ = "henry.lok@example.com"

from .tidy import CSSFormatter, CSSMinifier, CSSValidator

__all__ = [
    "CSSFormatter",
    "CSSMinifier", 
    "CSSValidator",
    "__version__",
    "__author__",
    "__email__",
] 
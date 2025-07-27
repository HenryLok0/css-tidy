try:
    from setuptools import setup, find_packages  # type: ignore
except ImportError:
    from distutils.core import setup  # type: ignore
    from distutils.util import convert_path  # type: ignore
    import os
    
    def find_packages(where='.'):
        """Simple package finder for distutils"""
        packages = []
        for root, dirs, files in os.walk(where):
            if '__init__.py' in files:
                packages.append(root.replace(os.sep, '.'))
        return packages

import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="css-tidy",
    version="0.1.3",
    author="Henry Lok",
    author_email="mail@henrylok.me",
    description="A Python tool to tidy and format CSS files",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/henrylok/css-tidy",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "css-tidy=css_tidy.cli:main",
        ],
    },
    keywords="css, formatting, tidy, beautify, minify",
    project_urls={
        "Bug Reports": "https://github.com/henrylok/css-tidy/issues",
        "Source": "https://github.com/henrylok/css-tidy",
    },
) 
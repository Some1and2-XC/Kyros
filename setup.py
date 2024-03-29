#!/usr/bin/env python3

from setuptools import find_packages, setup

from pathlib import Path

setup(
    name="Kyros",
    packages=find_packages(),
    version="3.1.0",
    description="A Class Based Python Library for Fractal Generation",
    author="@some1and2",
    author_email='04x0xx@gmail.com',
    license="GPL-3.0",
    install_requires=[
        "Pillow == 9.1.0",
        "numba",
        "opencv-python"
    ],
    setup_requires=[],
    long_description = (Path(__file__).parent / "README.md").read_text(),
    long_description_content_type='text/markdown'
)

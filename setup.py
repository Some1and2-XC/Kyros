#!/usr/bin/env python3

from setuptools import find_packages, setup

from pathlib import Path

setup(
	name="Kyros",
	packages=find_packages(include=["Kyros"]),
	version="3.0.4",
	description="A Class Based Python Library for Fractal Generation",
	author="@some1and2",
	license="GPL-3.0",
	install_requires=["pillow >= 9.1.0", "numba"],
	setup_requires=[],
	long_description = ( Path(__file__).parent / "README.md" ).read_text(),
	long_description_content_type='text/markdown'
)
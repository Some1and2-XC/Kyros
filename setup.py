#!/usr/bin/env python3

from setuptools import find_packages, setup

setup(
	name="Kairos",
	packages=find_packages(include=["Kairos"]),
	version="3.0.0",
	description="A Class Based Python Library for Fractal Generation",
	author="@some1and2",
	license="GNUv3.0",
	install_requires=["pillow == 9.1.0", "numba"],
	setup_requires=[]
)
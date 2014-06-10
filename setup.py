#! /usr/bin/env python3
# -*- coding:Utf8 -*-

# from setuptools import find_packages
import setuptools as st
from distutils.core import setup

packages = st.find_packages()

# --------------------------------------------------------------------------------------------------------------
# Call the setup function:
# --------------------------------------------------------------------------------------------------------------
setup(
    name='WallPaperd',
    version='0.2',
    scripts=["wallpaper.py"],
    description='Wallpaper daemon.',
    author='Guillaume Plum, Manuel Duarte',
    packages=packages,
)

# vim:spelllang=

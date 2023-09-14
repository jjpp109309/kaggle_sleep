#!/usr/bin/env python

from distutils.core import setup

setup(
    name='kaggle_child_sleep',
    version='1.0',
    description='Module containing helper functionality competition https://www.kaggle.com/competitions/child-mind-institute-detect-sleep-states?utm_medium=email&utm_source=gamma&utm_campaign=comp-childmind-2023',
    author='jjpp3301',
    package_dir={'': 'src'},
    packages=['kaggle_sleep'],
)

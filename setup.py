#!/usr/bin/env python

from setuptools import setup


setup(
    name='simply-snakes',
    version='0.1.0',
    description='Snakes game using kivy',
    author='Brandon Piatt',
    author_email='branpx@gmail.com',
    url='http://github.com/branpx/simply-snakes',
    license='MIT',
    packages=['simply_snakes'],
    package_data={'simply_snakes': ['*.kv']},
    install_requires=['kivy'],
    entry_points={'gui_scripts': ['simply-snakes=simply_snakes.snakes:main']},
    )

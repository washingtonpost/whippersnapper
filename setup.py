#!/usr/bin/env python

from setuptools import setup

setup(
    name='whippersnapper',
    version='0.0.5',
    author='Kevin Schaul, Katie Park',
    author_email='kevin.schaul@washpost.com, katie.park@washpost.com',
    url='http://github.com/washingtonpost/whippersnapper',
    description='Whippersnapper is an automated screenshot tool to keep a visual history of content on the web.',
    long_description='Check out the project on GitHub for the latest information <http://github.com/washingtonpost/whippersnapper>',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
    ],
    packages=[
        'whippersnapper',
    ],
    entry_points = {
        'console_scripts': [
            'whippersnapper = whippersnapper.whippersnapper:launch_new_instance',
        ],
    },
    install_requires = [
        'PyYAML>=3.11',
        'boto>=2.32.1',
        'wsgiref>=0.1.2'
    ]
)

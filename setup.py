#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from io import open
import os.path as osp
from setuptools import setup, find_packages


HERE = osp.abspath(osp.dirname(__file__))
sys.path.insert(0, HERE)
import pih2o


def main():
    setup(
        name=pih2o.__name__,
        version=pih2o.__version__,
        description=pih2o.__doc__,
        long_description=open(osp.join(HERE, 'README.rst'), encoding='utf-8').read(),
        classifiers=[
            'Development Status :: 2 - Pre-Alpha',
            'Environment :: Other Environment',
            'Intended Audience :: Developers',
            'Intended Audience :: End Users/Desktop',
            'License :: OSI Approved :: MIT License',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Natural Language :: English',
            'Natural Language :: French',
            'Natural Language :: German',
            'Topic :: Multimedia :: Graphics :: Capture :: Digital Camera',
        ],
        author="Antoine Rousseaux",
        url="https://github.com/anxuae/piH2O",
        download_url="https://github.com/anxuae/piH2O.git".format(pih2o.__version__),
        license='MIT license',
        platforms=['unix', 'linux'],
        keywords=[
            'Raspberry Pi',
            'Plant',
            'Watering'
        ],
        packages=find_packages(),
        package_data={
            'pih2o': ['*.ini'],
        },
        include_package_data=True,
        install_requires=[
            'RPi.GPIO',
            'adafruit-ads1x15',
            'croniter',
            'blinker',
            'flask',
            'flask-restful',
            'flask-sqlalchemy'
        ],
        options={
            'bdist_wheel':
                {'universal': True}
        },
        zip_safe=False,  # Don't install the lib as an .egg zipfile
        entry_points={'console_scripts': ["pih2o = pih2o.h2o:main"]},
    )


if __name__ == '__main__':
    main()

import os
from setuptools import setup

setup(
    name = "manifest_generator",
    version = "1.0.0",
    author = "Kevin Dahlhausen",
    author_email = "kevin.dahlhausen@gmail.com",
    description = ("A utility to smartly generate an HTML5 application cache manifest"),
    license = "GPL3",
    keywords = "html5 cache manifest",
    url = "https://github.com/kdahlhaus/manifest_generator",
    packages=['manifestgen',],
    long_description="This package contains a utility to generate the HTML5 application cache manifest file. Running it multiple times only changes the manifest if the manifest contents or contents of files listed in the cache change.",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Internet :: WWW/HTTP",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Environment :: Console",
    ],
    install_requires=["glob2",],
    scripts=['manifest_gen']
)


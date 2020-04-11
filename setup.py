# Copyright (c) 2018, Toby Slight. All rights reserved.
# ISC License (ISCL) - see LICENSE file for details.

import os
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gitforge",
    version="0.0.4",
    author="Toby Slight",
    author_email="tslight@pm.me",
    description="Git Forge API Client..",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tslight/gitforge",
    install_requires=["requests", "chopt"],
    packages=setuptools.find_packages(),
    data_files=[(os.path.expanduser("~/.config/gitforge"), ["config"])],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: ISC License (ISCL)",
        "Operating System :: OS Independent",
    ),
    entry_points={
        "console_scripts": [
            "github = gitforge.github:main",
            "gitlab = gitforge.gitlab:main",
            "gh = gitforge.github:main",
            "gl = gitforge.gitlab:main",
        ],
    },
)

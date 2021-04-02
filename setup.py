# -*- coding: utf-8 -*-

import os

from setuptools import setup, find_packages
from shutil import copy2

with open("requirements.txt", "r") as fp:
    # replace == with >= and remove trailing comments and spaces
    reqs = [x.replace("==", ">=").split("#")[0].strip() for x in fp]
    reqs = [x for x in reqs if x]  # remove empty strings

# load README.md/README.rst file
try:
    if os.path.exists("README.md"):
        with open("README.md", "r") as fp:
            readme = fp.read()
            readme_type = "text/markdown; charset=UTF-8"
    elif os.path.exists("README.rst"):
        with open("README.rst", "r") as fp:
            readme = fp.read()
            readme_type = "text/x-rst; charset=UTF-8"
    else:
        readme = ""
except Exception:
    readme = ""

setup_args = {
    "name": "ndx-mies",
    "version": "0.1.0",
    "description": "An NWB:N extension for data and metadata from the Multichannel Igor Electrophysiology Suite (MIES)",
    "long_description": readme,
    "long_description_content_type": readme_type,
    "author": "Thomas Braun",
    "author_email": "thomas.braun@byte-physics.de",
    "url": "https://github.com/t-b/ndx-MIES",
    "license": "BSD 3-Clause",
    "install_requires": reqs,
    "packages": find_packages("src/pynwb"),
    "package_dir": {"": "src/pynwb"},
    "package_data": {
        "ndx_mies": [
            "spec/ndx-mies.namespace.yaml",
            "spec/ndx-mies.extensions.yaml",
        ]
    },
    "classifiers": [
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
    ],
    "zip_safe": False,
}


def _copy_spec_files(project_dir):
    ns_path = os.path.join(project_dir, "spec", "ndx-mies.namespace.yaml")
    ext_path = os.path.join(project_dir, "spec", "ndx-mies.extensions.yaml")

    dst_dir = os.path.join(project_dir, "src", "pynwb", "ndx_mies", "spec")
    if not os.path.exists(dst_dir):
        os.mkdir(dst_dir)

    copy2(ns_path, dst_dir)
    copy2(ext_path, dst_dir)


if __name__ == "__main__":
    _copy_spec_files(os.path.dirname(__file__))
    setup(**setup_args)

# Copyright (c) 2022 The xlandsat developers.
# Distributed under the terms of the MIT License.
# SPDX-License-Identifier: MIT
"""
Get the automatically generated version information from setuptools_scm and
format it nicely.
"""

# This file is generated automatically by setuptools_scm
from . import _version_generated

# Add a "v" to the version number made by setuptools_scm
__version__ = f"v{_version_generated.version}"

# -*- coding: utf-8 -*-

"""Top-level package for aicsairtable."""

__author__ = "AICS Software"
__email__ = "AICS_SW@alleninstitute"
# Do not edit this string manually, always use bumpversion
# Details in CONTRIBUTING.md
__version__ = "0.0.0"


def get_module_version():
    return __version__


from .example import Example  # noqa: F401

#!/usr/bin/env python3

import os
import sys

import sphinx_rtd_theme

HERE = os.path.dirname(os.path.realpath(__file__))
PROJECT_ROOT = os.path.dirname(HERE)
sys.path.insert(0, PROJECT_ROOT)

from rule30.version import __version__

project = 'rule30'
copyright = '2017, Zhiming Wang'
author = 'Zhiming Wang'
version = release = __version__

extensions = [
    'sphinx.ext.autodoc',
    'numpydoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
]

source_suffix = '.rst'
master_doc = 'index'
exclude_patterns = ['README.rst', '_build']
pygments_style = 'sphinx'

html_favicon = 'favicon.ico'
html_extra_path = [
    'CNAME',
]

# sphinx_rtd_theme
html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

# autodoc
autodoc_member_order = 'bysource'

# numpydoc
numpydoc_show_class_members = False

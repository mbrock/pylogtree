# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.abspath('logtree'))

project = 'logtree'
copyright = '2019, Zensum AB'
author = 'Mikael Brockman'

version = '1.1'
release = '1.1'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
]

source_suffix = '.rst'
master_doc = 'index'
language = None
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
pygments_style = 'sphinx'
html_theme = 'alabaster'
autodoc_member_order = 'bysource'

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}

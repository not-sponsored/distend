"""Distend - build small targeted wordlists from an existing wordlist

Import example for the 'io_utils' module:

    >>> from io_utils import is_comment
    >>> is_comment('# This is a comment')
    True

See https://github.com/not-sponsored/distend for source, license, and tests.

Disclaimer: please refrain from malicious use of the software. For more
information view the LICENSE on the github repository linked above.
"""

# Distend version
__version__ = '1.1.0'

# allow tests to run
from .modifier import (
    prepend_list,
    postpend_list,
    prepend_str,
    postpend_str,
    multi_transform,
    single_transform,
    fuse_list_prepend_list_postpend,
    fuse_list_prepend_str_postpend,
    fuse_str_prepend_list_postpend,
    fuse_str_prepend_str_postpend,
    fuse_list_prepend_no_postpend,
    fuse_str_prepend_no_postpend,
    fuse_no_prepend_list_postpend,
    fuse_no_prepend_str_postpend,
)

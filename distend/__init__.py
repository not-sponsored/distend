"""Distend - build small targeted wordlists from an existing wordlist

Import example for the 'io_utils' module:

    >>> from io_utils import is_comment
    >>> is_comment('# This is a comment')
    True

See https://github.com/not-sponsored/distend for full source"""

# Distend version
__version__ = '1.0.0'

# allow tests to run
from .modifier import (
    pre_list,
    post_list,
    pre_str,
    post_str,
    multi_transform,
    single_transform,
    fuse_lp_lp,
    fuse_lp_sp,
    fuse_sp_lp,
    fuse_sp_sp,
    fuse_lp_np,
    fuse_sp_np,
    fuse_np_lp,
    fuse_np_sp,
)

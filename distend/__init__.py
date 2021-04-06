"""Distend - build small targeted wordlists from an existing wordlist

# insert example usage here

See https://github.com/hanzuo123/munch for more details"""

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

'''from .io_utils import (
    reduce_list,
    is_comment,
    rule_reader,
    pp_reader,
    duplicate_check,
    unique_file_name,
    file_exists,
    create_wordlist,
    append_list,
    append_str,
    rename_file,
    banner_title
)'''

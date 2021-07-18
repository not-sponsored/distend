"""serialize the command line arguments"""

# internal distend imports
import distend.modifier

# standard library
from typing import Tuple, Callable

# change function definition
def serialize_args(multi_rule: bool, verbose: bool,
                   prepend, postpend) -> Tuple[Callable, Callable]:
    """takes bool:multi_rule, bool:verbose flag, prepend, postpend
    note that prepend and postpend could be either a list or str,
    return a tuple of (transform, fuse) functions
    """
    transform = get_multi_rule_function(multi_rule)
    fuse = get_pre_postpend_function(prepend, postpend)
    return transform, fuse

# name change
def get_multi_rule_function(multi_rule: bool) -> Callable:
    """given bool:multi_rule flag, return transform function from modifier"""
    if multi_rule:
        return distend.modifier.multi_transform
    else:
        return distend.modifier.single_transform

# name change
def get_pre_postpend_function(prepend, postpend) -> Callable:
    """given pre and postpends, return fuse function from modifier"""
    attributes = (
        bool(prepend),                          # True if not ''
        bool(postpend),
        isinstance(prepend, list),
        isinstance(postpend, list)
    )
    fuse_function_lookup = {
        (1,1,1,1): distend.modifier.fuse_list_prepend_list_postpend,
        (1,1,1,0): distend.modifier.fuse_list_prepend_str_postpend,
        (1,1,0,1): distend.modifier.fuse_str_prepend_list_postpend,
        (1,1,0,0): distend.modifier.fuse_str_prepend_str_postpend,
        (1,0,1,0): distend.modifier.fuse_list_prepend_no_postpend,
        (1,0,0,0): distend.modifier.fuse_str_prepend_no_postpend,
        (0,1,0,1): distend.modifier.fuse_no_prepend_list_postpend,
        (0,1,0,0): distend.modifier.fuse_no_prepend_str_postpend,
        (0,0,0,0): None
    }
    return fuse_function_lookup.get(attributes, None)

"""serialize the command line arguments"""

# internal distend imports
import distend.modifier

# standard library
from typing import Tuple, Callable

# change function definition
def serialize_args(multi_rule: bool, verbose: bool,
                   prepend, postpend) -> Tuple[Callable, Callable, Callable]:
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

# may change depending on modifier, name change
def get_pre_postpend_function(prepend, postpend) -> Callable:
    """given pre and postpends, return fuse function from modifier"""
    attributes = (
        bool(prepend),                          # True if not ''
        bool(postpend),
        isinstance(prepend, list),
        isinstance(postpend, list)
    )
    fuse_function_lookup = {
        (1,1,1,1): distend.modifier.fuse_lp_lp,
        (1,1,1,0): distend.modifier.fuse_lp_sp,
        (1,1,0,1): distend.modifier.fuse_sp_lp,
        (1,1,0,0): distend.modifier.fuse_sp_sp,
        (1,0,1,0): distend.modifier.fuse_lp_np,
        (1,0,0,0): distend.modifier.fuse_sp_np,
        (0,1,0,1): distend.modifier.fuse_np_lp,
        (0,1,0,0): distend.modifier.fuse_np_sp,
        (0,0,0,0): None
    }
    return fuse_function_lookup.get(attributes, None)

"""serialize the command line arguments"""

# internal distend imports
import distend.modifier
import distend.drive

# standard library
from typing import Tuple, Callable

def serialize_args(multi_rule: bool, verbose: bool,
                   pre_postpend: tuple) -> Tuple[Callable, Callable, Callable]:
    """take bool:multi_rule and bool:verbose flag as well as tuple:pre_postpend,
    note tuple:pre_postpend could be two lists or two strings or one of each,
    return a tuple of (translation, fuse, drive) functions
    """
    translation = get_multi_rule_function(multi_rule)
    fuse = get_pre_postpend_function(pre_postpend[0], pre_postpend[1])
    drive = get_drive_function(verbose, pre_postpend[0], pre_postpend[1])
    return (translation, fuse, drive)

def get_multi_rule_function(multi_rule: bool) -> Callable:
    """given bool:multi_rule flag, return transform function from modifier"""
    if multi_rule:
        return distend.modifier.multi_transform
    else:
        return distend.modifier.single_transform

def get_pre_postpend_function(prepend, postpend) -> Callable:
    """given pre and postpends, return the fuse function from modifier"""
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
    """if prepend and postpend:
        if isinstance(prepend, list) and isinstance(postpend, list):
            return mod.fuse_lp_lp
        if isinstance(prepend, list) and isinstance(postpend, str):
            return mod.fuse_lp_sp
        if isinstance(prepend, str) and isinstance(postpend, list):
            return mod.fuse_sp_lp
        if isinstance(prepend, str) and isinstance(postpend, str):
            return mod.fuse_sp_sp
    elif prepend:
        if isinstance(prepend, list):
            return mod.fuse_lp_np
        if isinstance(prepend, str):
            return mod.fuse_sp_np
    elif postpend:
        if isinstance(postpend, list):
            return mod.fuse_np_lp
        if isinstance(postpend, str):
            return mod.fuse_np_sp
    else:
        return None"""

# may change depending on
def get_drive_function(verbose: bool, prepend, postpend) -> Callable:
    """given bool:verbose and pre and postpends, return drive function"""
    attributes = (
        verbose,
        bool(prepend),                               # True if not ''
        bool(postpend)
    )
    drive_function_lookup = {
        (1,1,1): distend.drive.verbose_pre_post,
        (1,1,0): distend.drive.verbose_single_pend,
        (1,0,1): distend.drive.verbose_single_pend,
        (1,0,0): distend.drive.verbose_no_pend,
        (0,1,1): distend.drive.concise_pre_post,
        (0,1,0): distend.drive.concise_single_pend,
        (0,0,1): distend.drive.concise_single_pend,
        (0,0,0): distend.drive.concise_no_pend
    }
    return drive_function_lookup.get(attributes, None)
    """if verbose:
        if prepend and postpend:
            return drive.verbose_pre_post
        elif prepend or postpend:
            return drive.verbose_single_pend
        else:
            return drive.verbose_no_pend
    else:
        if prepend and postpend:
            return drive.concise_pre_post
        elif prepend or postpend:
            return drive.concise_single_pend
        else:
            return drive.concise_no_pend"""

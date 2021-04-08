"""serialize the command line arguments"""

# internal distend imports
import distend.modifier as mod
import distend.drive as drive

def serialize_args(multi_rule, verbose, pends):
    """take bool:multi_rule and bool:verbose flag as well as tuple:pends,
    return fncts serialized according to inputs in tuple
    """
    trn_fnct = get_multi_rule(multi_rule)
    fuse_fnct = get_pends(pends[0], pends[1])
    drive_fnct = get_drive(verbose, pends[0], pends[1])
    return (trn_fnct, fuse_fnct, drive_fnct)

def get_multi_rule(multi_rule):
    """given bool:multi_rule flag, return transform fnct from modifier"""
    if multi_rule:
        return mod.multi_transform
    else:
        return mod.single_transform

def get_pends(prepend, postpend):
    """given pre and post pends, return fuse fnct from modifier"""
    if prepend and postpend:
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
        return None

def get_drive(verbose, prepend, postpend):
    """given bool:verbose and pre and post pends, return drive fnct"""
    if verbose:
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
            return drive.concise_no_pend

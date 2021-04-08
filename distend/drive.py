"""loops over the word list calling the modification fncts"""

# internal distend
import distend.io_utils as iou

def verbose_pre_post(fin, fncts, rules, pends, dupe):
    """verbose with both pre and post pends, return nothing"""
    for line in fin:
        base = line.strip()
        print(f'currently at [{base:^20}]', end='\r', flush=True)
        iou.append_list(fncts[1](fncts[0](base, rules), pends[0], pends[1]),
                        dupe)

def concise_pre_post(fin, fncts, rules, pends, dupe):
    """minimal verbosity with both pre and post pends, return nothing"""
    for line in fin:
        iou.append_list(fncts[1](fncts[0](line.strip(), rules), pends[0],
                        pends[1]), dupe)

def verbose_single_pend(fin, fncts, rules, pends, dupe):
    """verbose with either pre or post pend, return nothing"""
    pend = pends[0] if pends[0] else pends[1]
    for line in fin:
        base = line.strip()
        print(f'currently at [{base:^20}]', end='\r', flush=True)
        iou.append_list(fncts[1](fncts[0](base, rules), pend), dupe)

def concise_single_pend(fin, fncts, rules, pends, dupe):
    """minimal verbosity with either pre or post pend, return nothing"""
    pend = pends[0] if pends[0] else pends[1]
    for line in fin:
        iou.append_list(fncts[1](fncts[0](line.strip(), rules), pend),
                        dupe)

def verbose_no_pend(fin, fncts, rules, no_pend, dupe):
    """verbose with no pre or post pends, return nothing"""
    for line in fin:
        base = line.strip()
        print(f'currently at [{base:^20}]', end='\r', flush=True)
        iou.append_list(fncts[0](base, rules)[1:], dupe)

def concise_no_pend(fin, fncts, rules, no_pend, dupe):
    """minimal verbosity with no pre or post pends, return nothing"""
    for line in fin:
        iou.append_list(fncts[0](line.strip(), rules)[1:], dupe)

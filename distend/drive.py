"""loops over the wordlists doing most of the work"""

# internal distend
import distend.io_utils as iou

def verbose_pre_post(fin, fncts, rules, pends, dupe):
    for line in fin:
        base = line.strip()
        print(f'currently at [{base:^20}]', end='\r', flush=True)
        iou.append_list(fncts[1](fncts[0](base, rules), pends[0], pends[1]),
                        dupe)

def concise_pre_post(fin, fncts, rules, pends, dupe):
    for line in fin:
        iou.append_list(fncts[1](fncts[0](line.strip(), rules), pends[0],
                        pends[1]), dupe)

def verbose_single_pend(fin, fncts, rules, pends, dupe):
    pend = pends[0] if pends[0] else pends[1]
    for line in fin:
        base = line.strip()
        print(f'currently at [{base:^20}]', end='\r', flush=True)
        iou.append_list(fncts[1](fncts[0](base, rules), pend), dupe)

def concise_single_pend(fin, fncts, rules, pends, dupe):
    pend = pends[0] if pends[0] else pends[1]
    for line in fin:
        iou.append_list(fncts[1](fncts[0](line.strip(), rules), pend),
                        dupe)

def verbose_no_pend(fin, fncts, rules, no_pend, dupe):
    for line in fin:
        base = line.strip()
        print(f'currently at [{base:^20}]', end='\r', flush=True)
        iou.append_list(fncts[0](base, rules)[1:], dupe)

def concise_no_pend(fin, fncts, rules, no_pend, dupe):
    for line in fin:
        iou.append_list(fncts[0](line.strip(), rules)[1:], dupe)

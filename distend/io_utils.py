"""input/output utilities to read and display data"""

# TODO potentially write an custom error class
# TODO maybe check for file collision to prevent overwriting in create_wordlist?

# standard library
import os
import shutil
import pkg_resources

def reduce_list(arg):
    """reduce single element list:arg to string, return str:arg"""
    if len(arg) == 1:
        return str(arg[0])
    return arg

def is_comment(line):
    """check if str:line has '#' as first char, return a bool"""
    return line.strip().startswith('#')

def rule_reader(rules_file, verbose=False):
    """given file location str:rules_file, return a dict:rules"""
    if not rules_file:
        path = 'rules.conf'
        rules_file = pkg_resources.resource_filename(__name__, path)
    rules = {}
    try:
        with open(rules_file, 'r') as f:
            for line in f:
                if is_comment(line):
                    pass
                # check if rule is valid
                else:
                    if '=' in line:
                        single_rule = [x.strip() for x in line.split('=')]
                        if len(single_rule) >= 2:
                            rules[single_rule[0]] = single_rule[1]
    except FileNotFoundError:
        raise SystemExit(f'ERROR file does not exist: {rules_file}')
    except Exception as other:
        raise SystemExit(f'Error {other}')
    # extra verbosity
    if verbose:
        print(f'substitution rules from {rules_file}: {rules}')
    return rules

def pp_reader(rules_file, verbose=False):
    """pre_post_reader given file location str:rules_file, return str:prepend
    and str:postpend
    or may return list:prepend and/or list:postpend depending on str:rules_file
    see rules.conf for more information
    """
    if not rules_file:
        path = 'rules.conf'
        rules_file = pkg_resources.resource_filename(__name__, path)
    prepend = postpend = ''
    try:
        with open(rules_file, 'r') as f:
            for line in f:
                if is_comment(line):
                    pass
                # check for pre and post pend
                else:
                    if ',' in line:
                        pends = [x.strip() for x in line.split(',')]
                        if len(pends) >= 2 and pends[0] == 'postpend':
                            postpend = pends[1:]
                        elif len(pends) >= 2 and pends[0] == 'prepend':
                            prepend = pends[1:]
    except FileNotFoundError:
        raise SystemExit(f'ERROR file does not exist: {rules_file}')
    except Exception as other:
        raise SystemExit(f'ERROR: {other}')
    # reduce to single string or keep as a list
    prepend = reduce_list(prepend)
    postpend = reduce_list(postpend)
    # extra verbosity
    if verbose:
        print(f'prepend(s) from {rules_file}: {prepend}')
        print(f'postpend(s) from {rules_file}: {postpend}')
    return prepend, postpend

def unique_file_name(file_name, cnt):
    """create a random temp file name, return a str"""
    return f'{file_name}_wordlist({cnt}).temp'

def file_exists(test_file):
    """check if file location str:test_file exists, return a bool"""
    return os.path.exists(test_file)

def create_wordlist(infile, outfile, concat=False):
    """given str:infile, str:outfile and bool:concat creates a new file for the
    wordlist, returns str:infile unmodified if infile != outfile
    """
    # check infile != outfile because cannot perform read/write on same file
    if infile == outfile:
        file_name = outfile.split('.')[0]
        cnt = 1
        outfile = unique_file_name(file_name, cnt)
        while file_exists(outfile):
            cnt += 1
            outfile = unique_file_name(file_name, cnt)
    # copy infile to outfile
    if concat:
        try:
            shutil.copy(infile, outfile)
        except:
            raise SystemExit(f'ERROR could not copy {infile}')
    else:
        try:
            open(outfile, 'x').close()
        except FileExistsError:
            print(f'WARNING file already exists: {outfile}')
            overwrite = str(input(f'overwrite with new {outfile} (Y/N)? '))
            if overwrite.upper() == 'Y' or overwrite.upper() == 'YES':
                pass
            else:
                raise SystemExit()
        except:
            raise SystemExit(f'ERROR could not create: {outfile}')
    return outfile

def read_file_generator(infile):
    try:
        for line in open(infile, 'r'):
            yield line
    except FileNotFoundError:
        raise SystemExit(f'ERROR file does not exist: {infile}')
    except Exception as other:
        raise SystemExit(f'ERROR: {other}')

def append_list(lines, outfile):
    """takes a lst:lines and str:outfile, appends to outfile returns nothing"""
    try:
        with open(outfile, 'a') as f:
            f.write('\n'.join(lines) + '\n')
    except:
        raise SystemExit(f'ERROR could not append lst to {outfile}')

def rename_file(tempfile, rn_file):
    """take str:tempfile and str:rn_file then move tempfile to rn_file
    return nothing
    """
    try:
        overwrite = str(input(f'WARNING: overwrite {rn_file} with {tempfile} (Y/N)? '))
        if overwrite.upper() == 'Y' or overwrite.upper() == 'YES':
            shutil.move(tempfile, rn_file)
            print(f'Renamed {tempfile} to {rn_file}')
    except:
        raise SystemExit(f"ERROR temp file {tempfile} move to {rn_file} failed")

def generator_file_check(infile):
    if file_exists(infile):
        return True
    else:
        raise SystemExit(f'ERROR file does not exist: {infile}')

def banner_title(vrsn):
    """special thanks to textkool.com for the ascii text
    takes a str:vrsn, returns a string of ascii art and version number
    """
    banner = '''
    ██████╗ ██╗███████╗████████╗███████╗███╗   ██╗██████╗
    ██╔══██╗██║██╔════╝╚══██╔══╝██╔════╝████╗  ██║██╔══██╗
    ██║  ██║██║███████╗   ██║   █████╗  ██╔██╗ ██║██║  ██║
    ██║  ██║██║╚════██║   ██║   ██╔══╝  ██║╚██╗██║██║  ██║
    ██████╔╝██║███████║   ██║   ███████╗██║ ╚████║██████╔╝
    ╚═════╝ ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═══╝╚═════╝ '''
    vrsn_num = f'version {vrsn}'
    return f'{banner}\n\n{vrsn_num:>56}'

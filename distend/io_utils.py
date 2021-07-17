"""input/output utilities to read and display data

symbolic meaning of output prefixes:
[*] regular output
[+] using a default
[!] warning or caution
"""

# TODO potentially write an custom error class

# standard library
import os
import shutil
from typing import List, Dict, Generator
try:
    from importlib.resources import files
except ImportError:
    from importlib_resources import files

def reduce_list(arg: List[str]):
    """reduces single element list:arg to a string or returns unmodified for a
    list:arg with many elements, returns str:arg or unmodified list:arg,
    returns an empty string if given an empty string
    """
    if len(arg) == 1:
        return str(arg[0])
    return arg

def is_comment(line: str) -> bool:
    """checks for '#' as first char in str:line, returns a bool"""
    return line.strip().startswith('#')

def rule_reader(rules_file: str, verbose: bool=False) -> Dict[str, str]:
    """given a file location str:rules_file, returns a dict:rules"""
    rules: Dict[str, str] = {}
    if not rules_file:
        rules_file = files('distend').joinpath('rules.conf') # default location
        print(f'[+] default rules file: {rules_file}')
    try:
        with open(rules_file, 'r') as f:
            for line in f:
                if is_comment(line):
                    pass
                else:                            # check if the rule is valid
                    if '=' in line:
                        single_rule = [x.strip() for x in line.split('=')]
                        if len(single_rule) >= 2:
                            rules[single_rule[0]] = single_rule[1]
    except FileNotFoundError:
        raise SystemExit(f'[!] ERROR file does not exist: {rules_file}')
    except Exception as other:
        raise SystemExit(f'[!] Error: {other}')
    if verbose:                                  # extra verbosity
        print(f'[+] substitution rules from {rules_file}: {rules}')
    return rules

def pre_post_reader(rules_file: str, verbose: bool=False) -> tuple:
    """given file location str:rules_file, returns str:prepend and str:postpend
    or may return list:prepend and/or list:postpend depending on str:rules_file
    see rules.conf for more information
    """
    prepend = postpend = ''
    if not rules_file:
        rules_file = files('distend').joinpath('rules.conf') # default location
    try:
        with open(rules_file, 'r') as f:
            for line in f:
                if is_comment(line):
                    pass
                else:                   # check for valid pre and postpend(s)
                    if ',' in line:
                        pends = [x.strip() for x in line.split(',')]
                        if len(pends) >= 2 and pends[0] == 'postpend':
                            postpend = pends[1:]
                        elif len(pends) >= 2 and pends[0] == 'prepend':
                            prepend = pends[1:]
    except FileNotFoundError:
        raise SystemExit(f'[!] ERROR file does not exist: {rules_file}')
    except Exception as other:
        raise SystemExit(f'[!] ERROR: {other}')
    prepend = reduce_list(prepend)          # turns single element list to str
    postpend = reduce_list(postpend)
    if verbose:                             # extra verbosity
        print(f'[+] prepend(s) from {rules_file}: {prepend}')
        print(f'[+] postpend(s) from {rules_file}: {postpend}')
    return prepend, postpend

def unique_file_name(file_name: str, cnt: int) -> str:
    """creates a random temporary file name, returns a str"""
    return f'{file_name}_wordlist({cnt}).temp'

def file_exists(test_file: str) -> bool:
    """checks if file location str:test_file exists, returns a bool"""
    return os.path.exists(test_file)

def create_wordlist(infile: str, outfile: str, concatenate=False) -> str:
    """given str:infile, str:outfile and bool:concatenate creates a new file for
    the wordlist, returns str:infile unmodified if infile is not outfile
    """
    # check infile != outfile because cannot perform read/write on same file
    if infile == outfile:
        file_name = outfile.split('.')[0]             # removes file extension
        cnt = 1
        outfile = unique_file_name(file_name, cnt)
        while file_exists(outfile):                   # creates a unique name
            cnt += 1
            outfile = unique_file_name(file_name, cnt)
    if concatenate:                                 # copy infile text to outfile
        try:
            shutil.copy(infile, outfile)
        except:
            raise SystemExit(f'[!] ERROR could not copy: {infile}')
    else:
        try:
            open(outfile, 'x').close()               # create a blank file
        except FileExistsError:
            print(f'[!] WARNING file already exists: {outfile}')
            overwrite = str(input(f'overwrite with new {outfile} (Y/N)? '))
            if overwrite.upper() == 'Y' or overwrite.upper() == 'YES':
                pass               # another function will overwrite
            else:
                raise SystemExit()
        except:
            raise SystemExit(f'[!] ERROR could not create: {outfile}')
    return outfile

def read_file_generator(infile: str) -> Generator[str, None, None]:
    """given str:infile, return a generator of str:line elements"""
    try:
        for line in open(infile, 'r'):
            yield line
    except FileNotFoundError:
        raise SystemExit(f'[!] ERROR file does not exist: {infile}')
    except Exception as other:
        raise SystemExit(f'[!] ERROR: {other}')

# add an option for standard out in cli
def append_list(lines: List[str], outfile: str) -> None:
    """takes lst:lines and str:outfile, append to outfile return nothing
    if outfile is None then outputs to standard output
    """
    try:                                          # write to a file
        with open(outfile, 'a') as f:
            f.write('\n'.join(lines) + '\n')
    except TypeError:                             # stdout with outfile as None
        print('\n'.join(lines) + '\n')
    except:
        raise SystemExit(f'[!] ERROR could not append list to {outfile}')

def rename_file(temp_file: str, rn_file: str) -> None:
    """takes str:tempfile and str:rn_file then moves temp_file to rn_file
    returns nothing
    """
    try:
        warning = f'[!] WARNING: overwrite {rn_file} with {temp_file} (Y/N)? '
        overwrite = str(input(warning))
        if overwrite.upper() == 'Y' or overwrite.upper() == 'YES':
            shutil.move(temp_file, rn_file)
            print(f'[!] Renamed {temp_file} to {rn_file}')
    except:
        raise SystemExit(f"[!] ERROR could not move {temp_file} to {rn_file}")

def generator_file_check(infile: str) -> bool:
    """given str:infile check if infile exists, returns a bool or exits"""
    if file_exists(infile):
        return True
    else:
        raise SystemExit(f'[!] ERROR file does not exist: {infile}')

def banner_title(vrsn: str) -> str:
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
    version = f'version {vrsn}'
    return f'{banner}\n\n{version:>56}'

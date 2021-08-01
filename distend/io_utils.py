"""input/output utilities to read and display data

symbolic meaning of output prefixes:
[*] regular output
[+] using a default
[!] warning or caution

unless otherwise noted all files should be in text format
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
    cleans up malformed '' pre and postpends from a list
    returns an empty string if given an empty string
    """
    no_empty_pre_postpends = [pre_post for pre_post in arg if pre_post]
    if not no_empty_pre_postpends:  # returns empty string given empty list
        return ''
    if len(no_empty_pre_postpends) == 1:  # single element list into a string
        return str(no_empty_pre_postpends[0])
    return no_empty_pre_postpends   # normal list of pre or postpends

def is_comment(line: str) -> bool:
    """checks for '#' as first char in str:line, returns a bool"""
    return line.strip().startswith('#')

def get_default_configuration_location():
    """returns default configuration file location"""
    return files('distend').joinpath('configuration.txt')

# add parameter out_stream
def read_replacements(configuration_file: str, verbose: bool=False,
                      out_stream=None) -> Dict[str, str]:
    """given a file location str:configuration_file, returns a dict:replacements
    example of how replacements would appear in a configuration file:
    a = 4
    t = 7
    ...
    for more information see configuration.txt included with the package
    """
    replacements: Dict[str, str] = {}
    delimiter = '='                    # character to split at
    if not configuration_file:
        configuration_file = get_default_configuration_location()
        print(f'[+] replacements from: {configuration_file}', file=out_stream)
    try:
        with open(configuration_file, 'r') as f:
            for line in f:
                if is_comment(line):
                    pass
                else:  # check if the replacement is valid
                    if delimiter in line:
                        single_replace = [x.strip() for x in\
                                              line.split(delimiter)]
                        if len(single_replace) >= 2:
                            replacements[single_replace[0]] = single_replace[1]
    except FileNotFoundError:
        raise SystemExit(f'[!] ERROR file does not exist: {configuration_file}')
    except Exception as other:
        raise SystemExit(f'[!] Error: {other}')
    if verbose:                                  # extra verbosity
        print(f'[*] replacements from {configuration_file}: {replacements}')
    return replacements

def read_pre_post(configuration_file: str, verbose: bool=False,
                    out_stream=None) -> tuple:
    """given file location str:configuration_file,
    returns str:prepend, str:postpend
    or may return list:prepend and/or list:postpend depending on file
    example of list:prepends and postpends as it would appear in a file:
    prepend, prepend1, prepend2
    postpend, postpend1, postpend2
    for more information see configuration.txt included with the package
    """
    prepend = postpend = ''
    keyword_prepend = 'prepend'    # keyword for prepend line
    keyword_postpend = 'postpend'  # keyword for postpend line
    delimiter = ','                # character to split at
    if not configuration_file:
        configuration_file = get_default_configuration_location()
        print(f'[+] pre and postpends from: {configuration_file}',
              file=out_stream)
    try:
        with open(configuration_file, 'r') as f:
            for line in f:
                if is_comment(line):
                    pass
                else:  # check for valid pre and postpends named 'pre_post'
                    if delimiter in line:
                        pre_post = [x.strip() for x in line.split(delimiter)]
                        if len(pre_post) >= 2 and pre_post[0] ==\
                                                  keyword_prepend:
                            prepend = pre_post[1:]
                        elif len(pre_post) >= 2 and pre_post[0] ==\
                                                    keyword_postpend:
                            postpend = pre_post[1:]
    except FileNotFoundError:
        raise SystemExit(f'[!] ERROR file does not exist: {configuration_file}')
    except Exception as other:
        raise SystemExit(f'[!] ERROR: {other}')
    prepend = reduce_list(prepend)          # turns single element list to str
    postpend = reduce_list(postpend)
    if verbose:                             # extra verbosity
        print(f'[*] prepend(s) from {configuration_file}: {prepend}')
        print(f'[*] postpend(s) from {configuration_file}: {postpend}')
    return prepend, postpend

def unique_file_name(file_name: str, cnt: int) -> str:
    """creates a random temporary file name, returns a str"""
    return f'{file_name}_wordlist({cnt}).temp'

def file_exists(test_file: str) -> bool:
    """checks if file location str:test_file exists, returns a bool"""
    return os.path.exists(test_file)

# add parameter force
def create_wordlist(infile: str, outfile: str, concatenate: bool=False,
                    force: bool=False) -> str:
    """given str:infile, str:outfile and bool:concatenate creates a new file for
    the wordlist, returns str:infile unmodified if infile is not outfile
    """
    if outfile == 'None':  # printing to stdout no need for a file
        if concatenate:
            with open(infile, 'r') as f:
                print(f.read(), end='')
        return
    # check infile != outfile because cannot perform read/write on same file
    if infile == outfile:
        file_name = outfile.split('.')[0]             # removes file extension
        cnt = 1
        outfile = unique_file_name(file_name, cnt)
        while file_exists(outfile):                   # creates a unique name
            cnt += 1
            outfile = unique_file_name(file_name, cnt)
    if concatenate:                             # copy infile text to outfile
        try:
            shutil.copy(infile, outfile)
        except:
            raise SystemExit(f'[!] ERROR could not copy: {infile}')
    else:
        try:
            open(outfile, 'x').close()               # create a blank text file
        except FileExistsError:
            print(f'[!] WARNING file already exists: {outfile}')
            overwrite = str(input(f'overwrite with new {outfile} (Y/N)? '))
            if overwrite.upper() == 'Y' or overwrite.upper() == 'YES' or force:
                open(outfile, 'w').close()           # erase contents
            else:
                raise SystemExit()
        except:
            raise SystemExit(f'[!] ERROR could not create: {outfile}')
    return outfile

def read_file_generator(infile: str) -> Generator[str, None, None]:
    """given str:infile, returns a generator of str:line elements
    the infile should be in text and have one word per line
    """
    try:
        for line in open(infile, 'r'):
            yield line
    except FileNotFoundError:
        raise SystemExit(f'[!] ERROR file does not exist: {infile}')
    except Exception as other:
        raise SystemExit(f'[!] ERROR: {other}')

def append_list(lines: List[str], outfile: str) -> None:
    """takes lst:lines and str:outfile, append to outfile return nothing
    if outfile is None then outputs to standard output
    """
    try:                                          # write to a file
        with open(outfile, 'a') as f:
            f.write('\n'.join(lines) + '\n')
    except TypeError:                             # stdout with outfile as None
        print('\n'.join(lines) + '\n', end='')
    except:
        raise SystemExit(f'[!] ERROR could not append list to {outfile}')

# add parameter force
def rename_file(temporary_file: str, rename_file: str,
               force: bool=False) -> None:
    """takes str:temporary_file and str:rename_file then moves temporary_file to
    rename_file, returns nothing
    """
    if temporary_file is None:  # no file to move temporary_file is None
        return
    try:
        warning = (f'[!] WARNING: overwrite {rename_file} '
                   f'with {temporary_file} (Y/N)? ')
        overwrite = str(input(warning))
        if overwrite.upper() == 'Y' or overwrite.upper() == 'YES' or force:
            shutil.move(temporary_file, rename_file)
            print(f'[!] Renamed {temporary_file} to {rename_file}')
    except:
        raise SystemExit(f'[!] ERROR could not move {temporary_file} '
                         f'to {rename_file}')

def check_infile(infile: str) -> bool:
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
    return f'{banner}\n\n{version:>58}'

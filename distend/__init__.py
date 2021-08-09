"""Distend - build targeted wordlists from an existing wordlist

---User Guide---
basic usage:

    distend infile.txt outfile.txt

to find the default configuration file after an install use locate_default:

    distend infile.txt outfile.txt -ld

or just directly input prepend, postpend, and replacements:

    distend infile.txt outfile.txt -pr pre1,pre2 -po post1,post2 -r "{'a':'@'}"

if the arguments have spaces wrap them in quotes:

    distend infile.txt outfile.txt -pr "pre1, pre2" -r "{'a': '@', 't', '7'}"

with a non-default configuration file:

    distend infile.txt outfile.txt -cf 'new_configuration.txt'

to output directly to stdout for use in a password cracker set outfile to None:

    distend infile.txt None

with verbose, concatenate, replace_multiple flags set as True:

    distend infile.txt outfile.txt -v -c -rm

with quiet flag no output except for errors or when infile is None
quiet is mutually exclusive with verbose:

    distend infile.txt outfile.txt -q

with a period separator to add between prepends and postpends:

    distend infile.txt outfile.txt -s '.'

---Import---
Import example from the 'io_utils' module:

    >>> from distend.io_utils import is_comment
    >>> is_comment('# This is a comment')
    True

---Contact---
developer email: HanwenZuo1@gmail.com

See https://github.com/not-sponsored/distend for source, license, and tests.

---Disclaimer---
please refrain from malicious use of the software. For more
information view the LICENSE on the github repository linked above.
"""

# Distend version
__version__ = '1.1.1'

# allow tests to run
from .modifier import (
    prepend_list,
    postpend_list,
    prepend_str,
    postpend_str,
    replace_multiple,
    replace_single,
    fuse_list_prepend_list_postpend,
    fuse_list_prepend_str_postpend,
    fuse_str_prepend_list_postpend,
    fuse_str_prepend_str_postpend,
    fuse_list_prepend_no_postpend,
    fuse_str_prepend_no_postpend,
    fuse_no_prepend_list_postpend,
    fuse_no_prepend_str_postpend,
)

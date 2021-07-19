"""Distend - wordlist generator
------
Usage:
------
basic usage:

    distend infile.txt outfile.txt

with verbose, concatenate, multi_rule_only flags set as True:

    distend infile.txt outfile.txt -v -c -m

with non-default rules file:

    distend infile.txt outfile.txt -r 'new_rules.conf'

with a period separator:

    distend infile.txt outfile.txt -s '.'

Contact:

- developer email: HanwenZuo1@gmail.com

"""
# standard library
import sys
import argparse
import time
import os

# internal distend imports
import distend.__init__
import distend.serializer
import distend.io_utils

def main(passed_arguments: list=[]) -> None:
    """generates the wordlist, returns None"""
    if not passed_arguments:                          # increases flexibility
        passed_arguments = sys.argv[1:]
    args = parser(passed_arguments)                   # parse arguments

    OUT_STREAM = sys.stdout
    if args.quiet:       # silences output except for errors and append_list
        OUT_STREAM = open(os.devnull, 'w')

    start_time = time.perf_counter()                  # start timer
    version = distend.__init__.__version__
    print(f'{distend.io_utils.banner_title(version)}\n', file=OUT_STREAM)

    distend.io_utils.generator_file_check(args.infile)  # check infile
    rules = distend.io_utils.rule_reader(args.rules_file, args.verbose,
                                         OUT_STREAM)
    prepend, postpend = distend.io_utils.pre_post_reader(args.rules_file,
                                                         args.verbose)
    lines = distend.io_utils.read_file_generator(args.infile)
    output = distend.io_utils.create_wordlist(args.infile, args.outfile,
                                              args.concatenate)

    transform, fuse = distend.serializer.serialize_args(args.multi_rule_only,
                            args.verbose, prepend, postpend)


    print('[*] Running ...', file=OUT_STREAM)
    # loop through generator:lines and apply fuse and transform functions
    line_count = 0
    if prepend and postpend:
        for index, word in enumerate(lines, start=1):
            # fuse applies pre and postpends, transform replaces strings
            distend.io_utils.append_list(
                                         fuse(
                                              transform(word.strip(), rules),
                                         prepend, postpend, args.separator
                                         ),
                                         output)
            line_count += 1
    elif prepend or postpend:
        pre_or_post = prepend if prepend else postpend # get pre or postpend
        for index, word in enumerate(lines, start=1):
            # fuse applies pre_or_post
            distend.io_utils.append_list(
                                         fuse(
                                              transform(word.strip(), rules),
                                         pre_or_post, args.separator
                                         ),
                                         output)
            line_count += 1
    else:
        for index, word in enumerate(lines, start=1):
            distend.io_utils.append_list(
                                         transform(word.strip(), rules)[1:],
                                         output)
            line_count += 1
    print(f'\n[*] => Generated wordlist at {output}', file=OUT_STREAM)

    if args.outfile != output:       # renames temporary file to outfile
        distend.io_utils.rename_file(output, args.outfile)

    end_time = time.perf_counter()  # end timer
    number_of_prepends = number_of_postpends = 0  # assume no pre or postpends
    if prepend:
        number_of_prepends = len(prepend) if isinstance(prepend, list)\
                                          else 1
    if postpend:
        number_of_postpends = len(postpend) if isinstance(postpend, list)\
                                            else 1
    stats = (f'[*] transformed {line_count} line(s) with '
            f'{number_of_prepends} prepend(s) and '
            f'{number_of_postpends} postpend(s) '
            f'\n in {end_time - start_time:0.3f} seconds')
    print(stats, file=OUT_STREAM)

def parser(args: list):
    """parse arguments with lst:args return lst"""
    parser = argparse.ArgumentParser(description='distend - generate a\
    targeted wordlist from an existing file with rules')
    parser.add_argument('infile', help='input file to read from')
    parser.add_argument('outfile', help='output file to write to, enter None\
                        to print to stdout')
    parser.add_argument('-c', '--concatenate', action='store_true',
                        default=False,
                        help='outfile copies infile then concatenates generated\
                        words to the copied infile words, by default does not\
                        concatenate')
    parser.add_argument('-r', '--rules_file', default=None,
                        help='specify location of alternate rules file, default\
                        file is rules.conf included with package')
    parser.add_argument('-m', '--multi_rule_only', action='store_true',
                        default=False, help='only apply multiple rules at once\
                        single substitutions skipped i.e.\
                        password -> p@ssw0rd\
                        instead of\
                        password -> p@ssword -> p@ssw0rd')
    parser.add_argument('-s', '--separator', default='',
                        help='separator between pre and postpends with base')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-v', '--verbose', action='store_true', default=False,
                        help='display more information as program runs')
    group.add_argument('-q', '--quiet', action='store_true', default=False,
                        help='no output except on errors or outfile is None')
    return parser.parse_args(args)

if __name__ == '__main__':
    main()

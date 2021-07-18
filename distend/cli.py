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

Contact:

- developer email: HanwenZuo1@gmail.com

"""
# standard library
import sys
import argparse
import time

# internal distend imports
import distend.__init__
import distend.serializer
import distend.io_utils

def main(passed_arguments: list=None) -> None:
    """generate the wordlist return nothing"""
    if not passed_arguments:                          # increases flexibility
        passed_arguments = sys.argv[1:]
    start_time = time.perf_counter()                  # start timer
    args = parser(passed_arguments)                   # parse arguments
    print(f'{distend.io_utils.banner_title(distend.__init__.__version__)}\n')

    distend.io_utils.generator_file_check(args.infile)  # check infile
    rules = distend.io_utils.rule_reader(args.rules_file, args.verbose)
    prepend, postpend = distend.io_utils.pre_post_reader(args.rules_file,
                                                         args.verbose)
    lines = distend.io_utils.read_file_generator(args.infile)
    output = distend.io_utils.create_wordlist(args.infile, args.outfile,
                                              args.concatenate)

    transform, fuse = distend.serializer.serialize_args(args.multi_rule_only,
                            args.verbose, prepend, postpend)

    # loop through generator:lines and apply fuse and transform functions
    line_count = 0
    print('[*] Running ...')
    if prepend and postpend:
        for index, word in enumerate(lines, start=1):
            # fuse applies pre and postpends, transform replaces strings
            distend.io_utils.append_list(
                                         fuse(
                                              transform(word.strip(), rules),
                                         prepend, postpend
                                         ),
                                         output)
        else:
            line_count = index        # get the number of lines in the infile
    elif prepend or postpend:
        pre_or_post = prepend if prepend else postpend # get pre or postpend
        for index, word in enumerate(lines, start=1):
            # fuse applies pre_or_post
            distend.io_utils.append_list(
                                         fuse(
                                              transform(word.strip(), rules),
                                         pre_or_post
                                         ),
                                         output)
        else:
            line_count = index
    else:
        for index, word in enumerate(lines, start=1):
            distend.io_utils.append_list(
                                         transform(word.strip(), rules)[1:],
                                         output)
        else:
            line_count = index
    """end new code"""
    print(f'\n[*] => Generated wordlist at {output}')

    if args.outfile != output:       # renames temporary file to outfile
        distend.io_utils.rename_file(output, args.outfile)

    end_time = time.perf_counter()  # end timer
    stats = (f'[*] transformed {line_count} line(s) with '
            f'{len(prepend)} prepend(s) and {len(postpend)} postpend(s) '
            f'\n in {end_time - start_time:0.3f} seconds')
    print(stats)

# maybe add new argument for the separator
def parser(args: list):
    """parse arguments with lst:args return lst"""
    parser = argparse.ArgumentParser(description='distend - generate a\
    targeted wordlist from an existing file with rules')
    parser.add_argument('infile', help='input file to read from')
    parser.add_argument('outfile', help='output file to write to')
    parser.add_argument('-c', '--concatenate', action='store_true',
                        default=False,
                        help='outfile copies infile then concatenates generated\
                        words to the copied infile words, by default does not\
                        concatenate')
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        help='display more information as program runs')
    parser.add_argument('-r', '--rules_file', default=None,
                        help='specify location of alternate rules file, default\
                        file is rules.conf included with package')
    parser.add_argument('-m', '--multi_rule_only', action='store_true',
                        default=False, help='only apply multiple rules at once\
                        single substitutions skipped i.e.\
                        password -> p@ssw0rd\
                        instead of\
                        password -> p@ssword -> p@ssw0rd')
    return parser.parse_args(args)

if __name__ == '__main__':
    main()

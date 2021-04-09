"""Distend - wordlist generator
------
Usage:
------
basic usage:

    distend infile.txt outfile.txt

with verbose, concatenate, multi_rule only flags set as True:

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
import distend.serializer as serializer
import distend.io_utils as iou

def main():
    """generate the wordlist return nothing"""
    # start timer + args + banner
    start_time = time.perf_counter()
    args = parser(sys.argv[1:])
    print(f'{iou.banner_title(distend.__init__.__version__)}\n')

    # run checks, parse rules and pends, get file generator, create outfile
    iou.generator_file_check(args.infile)
    rules = iou.rule_reader(args.rules_file, args.verbose)
    pends = iou.pp_reader(args.rules_file, args.verbose)
    read_gen = iou.read_file_generator(args.infile)
    dupe = iou.create_wordlist(args.infile, args.outfile, args.concatenate)

    # serialize options into tuple + call drive + display success message
    fncts = serializer.serialize_args(args.multi_rule_only, args.verbose,
                                      pends)
    fncts[2](read_gen, fncts[:2], rules, pends, dupe)
    print(f'\n=> Generated wordlist at {dupe}')

    # if duplicate file exists, attempts to move dupe to original outfile
    if args.outfile != dupe:
        iou.rename_file(dupe, args.outfile)

    # show elapsed time
    end_time = time.perf_counter()
    print(f'Elapsed time: {end_time - start_time:0.3f}s')

def parser(args):
    """parse arguments with lst:args return lst"""
    parser = argparse.ArgumentParser(description='distend - generate a targeted\
    wordlist from an existing file with rules')
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

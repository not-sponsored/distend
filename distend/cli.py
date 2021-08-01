"""parse arguments and run the main function to generate the wordlist"""

# standard library
import sys
import argparse
import time
import os
import ast

# internal distend imports
import distend.__init__
import distend.serializer
import distend.io_utils

def main(passed_arguments: list=[]) -> None:
    """generates the wordlist, returns None"""
    if not passed_arguments:                          # increases flexibility
        passed_arguments = sys.argv[1:]
    args = parser(passed_arguments)

    if args.locate_default:  # locate default configuration file after install
        default_file = distend.io_utils.get_default_configuration_location()
        print(f'[+] default configuration file: {default_file}')
        return 0

    out_stream = None         # output to stdout
    if args.quiet:            # no output except for errors and append_list
        out_stream = open(os.devnull, 'w')      # devnull to silence output

    start_timer = time.perf_counter()
    version = distend.__init__.__version__
    print(f'{distend.io_utils.banner_title(version)}\n', file=out_stream)

    distend.io_utils.check_infile(args.infile)

    replacements = args.replacements  # assume given replacements
    if not args.replacements:  # read the replacements when not given
        replacements = distend.io_utils.read_replacements(
                            args.configuration_file, args.verbose, out_stream)

    prepend, postpend = args.prepend, args.postpend  # assume given both
    if not prepend and not postpend:    # neither pre nor postpend given
        prepend, postpend = distend.io_utils.read_pre_post(
                            args.configuration_file, args.verbose, out_stream)
    elif not prepend:  # prepend not given so read from file
        prepend, _ = distend.io_utils.read_pre_post(args.configuration_file,
                                                    args.verbose, out_stream)
    elif not postpend: # postpend not given so read from file
        _, postpend = distend.io_utils.read_pre_post(args.configuration_file,
                                                     args.verbose, out_stream)

    if args.verbose:  # display cli inputs or inputs from a file
        print(f'[*] prepend(s): {prepend} postpend(s): {postpend} '
              f'replacements: {replacements}', file=out_stream)

    lines = distend.io_utils.read_file_generator(args.infile)
    output = distend.io_utils.create_wordlist(args.infile, args.outfile,
                                              args.concatenate, args.force)

    # replace applies replacements, fuse inserts/appends pre and postpends
    replace, fuse = distend.serializer.serialize_args(args.replace_multiple,
                            args.verbose, prepend, postpend)


    print('[*] Running ...', file=out_stream)
    # loop through generator:lines and run replace and fuse functions
    line_count = 0
    if prepend and postpend:
        for word in lines:
            distend.io_utils.append_list(
                                         fuse(
                                           replace(word.strip(), replacements),
                                         prepend, postpend, args.separator
                                         ),
                                         output)
            line_count += 1
    elif prepend or postpend:
        pre_or_post = prepend if prepend else postpend # get pre or postpend
        for word in lines:
            distend.io_utils.append_list(
                                         fuse(
                                           replace(word.strip(), replacements),
                                         pre_or_post, args.separator
                                         ),
                                         output)
            line_count += 1
    else:
        for word in lines:
            distend.io_utils.append_list(
                    replace(word.strip(), replacements)[1:], output)
            line_count += 1
    print(f'\n[*] => Generated wordlist at {output}', file=out_stream)

    if output != args.outfile:       # renames temporary file output to outfile
        distend.io_utils.rename_file(output, args.outfile, args.force)

    stop_timer = time.perf_counter()
    number_of_prepends = number_of_postpends = 0  # assume no pre or postpends
    if prepend:
        number_of_prepends = 1 if isinstance(prepend, str) else len(prepend)
    if postpend:
        number_of_postpends = 1 if isinstance(postpend, str) else len(postpend)
    statistics = (f'[*] transformed {line_count} line(s) with '
                  f'{number_of_prepends} prepend(s), '
                  f'{number_of_postpends} postpend(s), '
                  f'and {len(replacements)} replacement(s)\n'
                  f'    in {stop_timer - start_timer:0.3f} seconds')
    print(statistics, file=out_stream)

    if out_stream is not None:
        out_stream.close()
    return 0

# changed rules_file to configuration_file, -> multi_rule_only replace_multiple
def parser(args: list):
    """parse arguments with lst:args return lst"""
    # get the documentation from the package document string
    distend_doc_str = distend.__init__.__doc__.split('\n')[2:]
    examples = '\n'.join(distend_doc_str)
    parser = argparse.ArgumentParser(
        description='distend - build a targeted wordlist from an existing one',
        epilog=examples,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('infile', help='input file to read from')
    parser.add_argument('outfile', help='output file to write to, enter None\
                        to print to stdout')
    parser.add_argument('-c', '--concatenate', action='store_true',
                        default=False,
                        help='outfile copies infile then concatenates generated\
                        words to the copied infile words, by default does not\
                        concatenate')
    parser.add_argument('-cf', '--configuration_file', default=None,
                        help='specify location of alternate configuration file,\
                        default is configuration.txt included with the package')
    parser.add_argument('-rm', '--replace_multiple', action='store_true',
                        default=False, help='apply multiple replacements at\
                        once single substitutions skipped i.e.\
                        password -> p@ssw0rd\
                        instead of default single substitutions\
                        password -> p@ssword -> passw0rd -> p@ssw0rd')
    parser.add_argument('-s', '--separator', default='',
                        help='separator between pre and postpends with base')
    parser.add_argument('-f', '--force', action='store_true', default=False,
                        help='force answer yes to every prompt')
    parser.add_argument('-ld', '--locate_default', action='store_true',
                        default=False,
                        help='show default configuration.txt location\
                        and exit')
    parser.add_argument('-r', '--replacements', default='{}',
                        help='replacements i.e. {"a": "@"} replaces\
                        a with @ in password -> p@ssword enter as a python\
                        dictionary -r \'{"s": "5", "t": "7"}\'')
    parser.add_argument('-pr', '--prepend', default='',
                        help='prepend to apply to base word i.e. prepend =\
                        1984 on password -> 1984password for multiple\
                        prepends use commas -pr prepend1,prepend2')
    parser.add_argument('-po', '--postpend', default='',
                        help='postpend to apply to base word i.e. postpend =\
                        1985 on password -> password1985 for multiple\
                        postpends use commas -po postpend1,postpend2')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-v', '--verbose', action='store_true', default=False,
                        help='display more information as program runs')
    group.add_argument('-q', '--quiet', action='store_true', default=False,
                        help='no output except on errors or outfile is None')
    secondary_parse = parser.parse_args(args)
    secondary_parse.prepend = [prepend.strip() for prepend\
                               in secondary_parse.prepend.split(',')]
    secondary_parse.postpend = [postpend.strip() for postpend\
                                in secondary_parse.postpend.split(',')]
    secondary_parse.prepend = distend.io_utils.reduce_list(
                                        secondary_parse.prepend)
    secondary_parse.postpend = distend.io_utils.reduce_list(
                                        secondary_parse.postpend)
    secondary_parse.replacements = ast.literal_eval(
                                        secondary_parse.replacements)
    return secondary_parse

if __name__ == '__main__':
    main()

# standard library
import unittest
from unittest.mock import patch, mock_open
import os
os.chdir('..')  # change for default configuration file location output test

# internal distend imports
from distend import cli
import distend.__init__
import distend.io_utils

class TestCli(unittest.TestCase):

    def setUp(self):
        # infile configurations
        self.blank_infile = ""
        self.infile = "polecat"  # replacement variety: t=7, l=1, o=0, a=4, e=3
        # mocked return values for io_utils
        self.replacements = {'a':'4', 'e':'3'}
        self.single_replace = {'a':'4'}
        self.no_replace = {}
        self.list_pre_postpend = (['prepend1', 'prepend2'],
                                  ['postpend1', 'postpend2'])
        self.str_pre_postpend = ('prepend1', 'postpend1')
        self.prepend = ('prepend1', '')
        self.postpend = ('', 'postpend1')
        self.no_pre_postpend = ('', '')


    def test_parser_all_options(self):
        """cli.parse_args all options on except for mutually exclusive -q"""
        options = ['in.txt', 'out.txt', '-c', '-v', '-rm', '-cf',
                   'configuration.txt', '-s', '.', '-f', '-ld', '-pr',
                   'prepend1, prepend2', '-po', 'postpend1, postpend2',
                   '-r', '{"a": "4"}']
        prepends = ['prepend1', 'prepend2']
        postpends = ['postpend1', 'postpend2']
        replacements = {"a": "4"}
        args = cli.parser(options)
        self.assertEqual(args.infile, 'in.txt', 'parses infile incorrectly')
        self.assertEqual(args.outfile, 'out.txt', 'parses outfile incorrectly')
        self.assertEqual(args.concatenate, True,
                         'parses concatenate flag incorrectly')
        self.assertEqual(args.verbose, True, 'parses verbose flag incorrectly')
        self.assertEqual(args.replace_multiple, True,
                         'parses replace_multiple flag incorrectly')
        self.assertEqual(args.configuration_file, 'configuration.txt',
                         'parses configuration_file incorrectly')
        self.assertEqual(args.separator, '.', 'parses separator incorrectly')
        self.assertEqual(args.force, True, 'parses force flag incorrectly')
        self.assertEqual(args.quiet, False, 'parses quiet flag incorrectly')
        self.assertEqual(args.locate_default, True,
                         'parses locate_default flag incorrectly')
        self.assertEqual(args.prepend, prepends, 'parses prepends incorrectly')
        self.assertEqual(args.postpend, postpends,
                         'parses postpends incorrectly')
        self.assertEqual(args.replacements, replacements,
                         'parses replacements incorrectly')

    def test_parser_default_options(self):
        """cli.parse_args no options on"""
        options = ['in.txt', 'out.txt']
        default_prepends = ''
        default_postpends = ''
        default_replacements = {}
        args = cli.parser(options)
        self.assertEqual(args.infile, 'in.txt', 'parses infile incorrectly')
        self.assertEqual(args.outfile, 'out.txt', 'parses outfile incorrectly')
        self.assertEqual(args.concatenate, False,
                         'parses concatenate flag incorrectly')
        self.assertEqual(args.verbose, False, 'parses verbose flag incorrectly')
        self.assertEqual(args.replace_multiple, False,
                         'parses replace_multiple flag incorrectly')
        self.assertEqual(args.configuration_file, None,
                         'parses configuration incorrectly')
        self.assertEqual(args.separator, '', 'parses separator incorrectly')
        self.assertEqual(args.force, False, 'parses force flag incorrectly')
        self.assertEqual(args.quiet, False, 'parses quiet flag incorrectly')
        self.assertEqual(args.locate_default, False,
                         'parses locate_default flag incorrectly')
        self.assertEqual(args.prepend, default_prepends,
                         'parses prepends incorrectly')
        self.assertEqual(args.postpend, default_postpends,
                         'parses postpends incorrectly')
        self.assertEqual(args.replacements, default_replacements,
                         'parses replacement incorrectly')

    def test_parser_mutually_exclusive_verbose_and_quiet(self):
        """cli.parse_args test verbose and quiet flag are mutually exclusive"""
        options = ['in.txt', 'out.txt', '-v', '-q']
        try:
            #args = cli.parser(options)  # should fail and trigger except
            args = cli.parser(options)
        except:
            return
        error_notice = "failed to prevent mutually exclusive -v and -q options"
        # if both options are True then assert is false printing error_notice
        assert not (args.verbose and args.quiet), error_notice

    @patch('distend.io_utils.file_exists')
    @patch('distend.io_utils.read_file_generator')
    def test_main_when_outfile_is_none_and_quiet(self, mock_file_generator,
                                                  mock_exists):
        """cli.main check output when outfile is none and quiet enabled"""
        null_stream = open(os.devnull, 'w') # open stream to devnull
        mock_exists.return_value = True
        mock_file_generator.return_value = (w for w in self.infile.split('\n'))
        quiet_options = ['in.txt', 'None', '-q',
                         '-pr', ', '.join(self.list_pre_postpend[0]),
                         '-po', ', '.join(self.list_pre_postpend[1]),
                         '-r', str(self.single_replace)]

        version = distend.__init__.__version__
        banner = distend.io_utils.banner_title(version) + '\n'
        output = ('prepend1polecat\nprepend2polecat\npolecatpostpend1\n'
                  'polecatpostpend2\nprepend1polecatpostpend1\n'
                  'prepend1polecatpostpend2\nprepend2polecatpostpend1\n'
                  'prepend2polecatpostpend2\nprepend1polec4t\n'
                  'prepend2polec4t\npolec4tpostpend1\npolec4tpostpend2\n'
                  'prepend1polec4tpostpend1\nprepend1polec4tpostpend2\n'
                  'prepend2polec4tpostpend1\nprepend2polec4tpostpend2\n'
                  'polec4t\n')

        # test quiet options

        with patch('builtins.print') as mock_print:
            return_code = cli.main(quiet_options)

        calls_text = [banner, '[*] Running ...', '',
                      '\n[*] => Generated wordlist at None',
                      ('[*] transformed 1 line(s) with 2 prepend(s), '
                       '2 postpend(s), and 1 replacement(s)\n    in ')
                      ]

        mock_print.assert_any_call(output, end='')

        # manually check each call's text and file stream
        for call, expected_text in zip(mock_print.call_args_list, calls_text):
            text_printed = call[0][0]
            if text_printed == output:  # already tested by assert_any
                continue
            error_text = f'Printed: {text_printed} Expected: {expected_text}'
            assert expected_text in text_printed, error_text

            file_stream = call[1]['file']
            error_stream = f'Stream: {file_stream} Expected: {null_stream}'
            assert str(file_stream) == str(null_stream), error_stream

        null_stream.close()
        self.assertEqual(return_code, 0, 'wrong exit code')

    @patch('distend.io_utils.read_pre_post')
    @patch('distend.io_utils.read_replacements')
    @patch('distend.io_utils.file_exists')
    @patch('distend.io_utils.read_file_generator')
    def test_main_outfile_is_none_quiet_concatenate(self, mock_file_generator,
                                                   mock_exists, mock_replace,
                                                   mock_pre_post):
        """test cli.main when outfile is None with quiet and concatenate"""
        # no pre or postpend and no replacements but with -c and -q
        # reset the generator
        mock_file_generator.return_value = (w for w in self.infile.split('\n'))
        mock_exists.return_value = True
        mock_replace.return_value = self.no_replace
        mock_pre_post.return_value = self.no_pre_postpend
        concatenate_option = ['in.txt', 'None', '-c', '-q']

        concatenate_output = 'polecat'

        with patch('builtins.open', mock_open(read_data=self.infile)) as mf:
            with patch('builtins.print') as mock_print:
                return_code = cli.main(concatenate_option)

        mock_print.assert_any_call(concatenate_output, end='')
        self.assertEqual(return_code, 0, 'wrong exit code')

    @patch('distend.io_utils.file_exists')
    @patch('distend.io_utils.read_file_generator')
    @patch('distend.io_utils.read_pre_post')
    @patch('distend.io_utils.read_replacements')
    def test_main_minimal_options(self, mock_read_replacements,
                                    mock_read_pre_post, mock_file_generator,
                                    mock_exists):
        """cli.main check correct output"""
        mock_exists.return_value = True
        mock_file_generator.return_value = (w for w in self.infile.split('\n'))
        mock_read_replacements.return_value = self.replacements
        mock_read_pre_post.return_value = self.str_pre_postpend
        outfile = 'out.txt'
        minimal_options = ['in.txt', outfile, '-s', '.']

        output = ('prepend1.polecat\npolecat.postpend1\n'
                  'prepend1.polecat.postpend1\nprepend1.polec4t\n'
                  'polec4t.postpend1\nprepend1.polec4t.postpend1\n'
                  'prepend1.pol3cat\npol3cat.postpend1\n'
                  'prepend1.pol3cat.postpend1\nprepend1.pol3c4t\n'
                  'pol3c4t.postpend1\nprepend1.pol3c4t.postpend1\n'
                  'polec4t\npol3cat\npol3c4t\n'
                  )

        with patch('builtins.open', mock_open()) as mock_file:
            return_code = cli.main(minimal_options)

        mock_file.assert_any_call(outfile, 'a')
        mock_file.return_value.write.assert_called_once_with(output)
        self.assertEqual(return_code, 0, 'wrong exit code')

    @patch('distend.io_utils.file_exists')
    @patch('distend.io_utils.read_file_generator')
    @patch('distend.io_utils.read_pre_post')
    @patch('distend.io_utils.read_replacements')
    def test_main_edge_cases(self, mock_read_replacements, mock_read_pre_post,
                             mock_file_generator, mock_exists):
        """cli.main check output on edge cases"""
        # no lines in the infile
        mock_exists.return_value = True
        mock_file_generator.return_value = (w for w in\
                                           self.blank_infile.split('\n'))
        mock_read_replacements.return_value = self.no_replace
        mock_read_pre_post.return_value = self.no_pre_postpend
        outfile = 'out.txt'
        minimal_options = ['in.txt', outfile]

        blank_output = '\n'

        with patch('builtins.open', mock_open()) as mock_file:
            return_code = cli.main(minimal_options)

        mock_file.assert_any_call(outfile, 'a')
        mock_file.return_value.write.assert_called_once_with(blank_output)
        self.assertEqual(return_code, 0, 'wrong exit code')

        # single replacement and no pre or postpend
        mock_file_generator.return_value = (w for w in self.infile.split('\n'))
        mock_read_replacements.return_value = self.single_replace

        single_output = 'polec4t\n'

        with patch('builtins.open', mock_open()) as mock_file:
            return_code = cli.main(minimal_options)

        mock_file.assert_any_call(outfile, 'a')
        mock_file.return_value.write.assert_called_once_with(single_output)
        self.assertEqual(return_code, 0, 'wrong exit code')

        # prepend and no replacement
        mock_file_generator.return_value = (w for w in self.infile.split('\n'))
        mock_read_replacements.return_value = self.no_replace
        mock_read_pre_post.return_value = self.prepend

        prepend_output = 'prepend1polecat\n'

        with patch('builtins.open', mock_open()) as mock_file:
            return_code = cli.main(minimal_options)

        mock_file.assert_any_call(outfile, 'a')
        mock_file.return_value.write.assert_called_once_with(prepend_output)
        self.assertEqual(return_code, 0, 'wrong exit code')

        # postpend and no replacement
        mock_file_generator.return_value = (w for w in self.infile.split('\n'))
        mock_read_pre_post.return_value = self.postpend

        postpend_output = 'polecatpostpend1\n'

        with patch('builtins.open', mock_open()) as mock_file:
            return_code = cli.main(minimal_options)

        mock_file.assert_any_call(outfile, 'a')
        mock_file.return_value.write.assert_called_once_with(postpend_output)
        self.assertEqual(return_code, 0, 'wrong exit code')

    def test_main_locate_default(self):
        """test cli.main with locate_default flag"""
        default_location = os.getcwd() + '/distend/configuration.txt'
        options = ['in.txt', 'out.txt', '-ld']

        with patch('builtins.print') as mock_print:
            return_code = cli.main(options)

        call_text = f'[+] default configuration file: {default_location}'
        mock_print.assert_called_once_with(call_text)
        self.assertEqual(return_code, 0, 'wrong exit code')

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()

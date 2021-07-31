# standard library
import unittest
from unittest.mock import patch, mock_open
import os
os.chdir('..')  # changes location for default configuration file tests

# internal distend imports
from distend import io_utils

class TestIoUtils(unittest.TestCase):

    def setUp(self):
        # configuration file test setups
        self.file = """
                      # replacements
                      a = 4
                      e = 3
                      # prepend
                      prepend, 1972
                      # postpend
                      postpend, 1984"""
        self.single_replace = """
                              # replacements
                              a = 4
                              # prepend
                              prepend, 1972
                              # postpend
                              postpend, 1984"""
        self.no_replace = """
                          # replacements
                          # prepend
                          prepend, 1972
                          # postpend
                          postpend, 1984"""
        self.list_pre_postpend = """
                                    # replacements
                                    a = 4
                                    e = 3
                                    # prepend
                                    prepend, 1972, 1973
                                    # postpend
                                    postpend, 1984, 1985"""
        self.blank_pre_postpend = """
                                     # replacements
                                     a = 4
                                     e = 3
                                     # prepend
                                     prepend,
                                     # postpend
                                     postpend,"""
        self.no_pre_postpend = """
                                  # replacements
                                  a = 4
                                  e = 3
                                  # prepend
                                  # postpend"""
        self.removal_replace = """
                                 # replacements
                                 a =
                                 """
        self.malformed_pre_postpend = """
                                         # prepend, postpend
                                         prepend,, ,
                                         postpend, , 1984,,1985"""

    def test_reduce_list_maintains_list(self):
        """io_utils.reduce_list returns a list given a list"""
        input = ['1984', '1985']
        empty_inputs = ['', '1984', '', '1985', '', '']
        result = io_utils.reduce_list(input)
        empty_result = io_utils.reduce_list(empty_inputs)
        self.assertIsInstance(result, list, 'does not return datatype list')
        self.assertIsInstance(empty_result, list,
                              'does not return datatype list')
        self.assertEqual(result, input, 'does not maintain list')
        self.assertEqual(empty_result, input, 'does not maintain list')

    def test_reduce_list_reduces_to_str(self):
        """io_utils.reduce_list returns a str given a single element"""
        single_element_input = ['1984']
        no_element_input = ['']
        default_input = ''
        multiple_empty = ['', '']
        empty_and_single = ['', '1984', '']
        single_element_result = io_utils.reduce_list(single_element_input)
        no_element_result = io_utils.reduce_list(no_element_input)
        default_input_result = io_utils.reduce_list(default_input)
        multiple_empty_result = io_utils.reduce_list(multiple_empty)
        empty_single_result = io_utils.reduce_list(empty_and_single)
        self.assertIsInstance(single_element_result, str,
                              'does not return datatype str')
        self.assertIsInstance(no_element_result, str,
                              'does not return datatype str')
        self.assertIsInstance(default_input_result, str,
                              'does not return datatype str')
        self.assertIsInstance(multiple_empty_result, str,
                              'does not return datatype str')
        self.assertIsInstance(empty_single_result, str,
                              'does not return datatype str')
        self.assertEqual(single_element_result, '1984',
                         'does not reduce to str')
        self.assertEqual(no_element_result, '', 'does not reduce to str')
        self.assertEqual(default_input_result, '', 'does not reduce to str')
        self.assertEqual(multiple_empty_result, '', 'does not reduce to str')
        self.assertEqual(empty_single_result, '1984',
                         'does not reduce to str')

    def test_is_comment_identifies_comment(self):
        """io_utils.is_comment catches a comment, returns bool:true"""
        perfect_comment = '# This is a comment line'
        atypical_comment = '     #a weird comment  '
        multiple_hash = '### Multi hash mark headline comment'
        perfect_comment_result = io_utils.is_comment(perfect_comment)
        atypical_comment_result = io_utils.is_comment(atypical_comment)
        multiple_hash_result = io_utils.is_comment(multiple_hash)
        self.assertIsInstance(perfect_comment_result, bool,
                              'does not return datatype bool')
        self.assertIsInstance(atypical_comment_result, bool,
                              'does not return datatype bool')
        self.assertIsInstance(multiple_hash_result, bool,
                              'does not return datatype bool')
        self.assertEqual(perfect_comment_result, True,
                         'does not identify comment')
        self.assertEqual(atypical_comment_result, True,
                         'does not identify comment')
        self.assertEqual(multiple_hash_result, True,
                         'does not identify comment')

    def test_is_comment_does_not_identify_regular_text(self):
        """io_utils.is_comment does not catch regular text, returns false"""
        line = 'This is a regular line'
        prepend_line = 'prepend, 1984, 1985'
        replacement_line = 'a = 4'
        false_comment = 'This is not a comment # other text'
        result = io_utils.is_comment(line)
        prepend_result = io_utils.is_comment(prepend_line)
        replacement_result = io_utils.is_comment(replacement_line)
        false_comment_result = io_utils.is_comment(false_comment)
        self.assertIsInstance(result, bool, 'does not return datatype bool')
        self.assertIsInstance(prepend_result, bool,
                              'does not return datatype bool')
        self.assertIsInstance(replacement_result, bool,
                              'does not return datatype bool')
        self.assertIsInstance(false_comment_result, bool,
                              'does not return datatype bool')
        self.assertEqual(result, False, 'incorrectly catches regular text')
        self.assertEqual(prepend_result, False,
                         'incorrectly catches regular text')
        self.assertEqual(replacement_result, False,
                         'incorrectly catches regular text')
        self.assertEqual(false_comment_result, False,
                         'incorrectly catches regular text')

    def test_read_replacements_parses_replacements(self):
        """io_utils.read_replacements parses replacements,
        returns replacements in a dictionary
        """
        with patch("builtins.open",
                   mock_open(read_data=self.file)) as mock_file:
                result = io_utils.read_replacements(None)
        self.assertIsInstance(result, dict, 'does return a dictionary')
        self.assertEqual(result, {'a':'4', 'e':'3'},
                         'does not parse the replacements correctly')

    def test_read_replacements_single_replace_and_no_replace(self):
        """io_utils.read_replacements parses, returns a dictionary"""
        with patch("builtins.open",
                   mock_open(read_data=self.single_replace)) as mock_file:
                single_result = io_utils.read_replacements(None)
        with patch("builtins.open",
                   mock_open(read_data=self.no_replace)) as mock_file:
                no_replace_result = io_utils.read_replacements(None)
        self.assertIsInstance(single_result, dict, 'does return a dictionary')
        self.assertIsInstance(no_replace_result, dict,
                              'does return a dictionary')
        self.assertEqual(single_result, {'a':'4'},
                         'does not parse the replacements correctly')
        self.assertEqual(no_replace_result, {},
                         'does not parse the replacements correctly')

    def test_read_replacements_removal_replace(self):
        """io_utils.read_replacements parses malformed replacement,
        returns a dictionary
        """
        with patch("builtins.open",
                   mock_open(read_data=self.removal_replace)) as mock_file:
                malformed_result = io_utils.read_replacements(None)
        self.assertIsInstance(malformed_result, dict,
                              'does return a dictionary')
        self.assertEqual(malformed_result, {'a': ''},
                         'does not parse the replacement correctly')

    @patch('builtins.print')
    def test_read_replacements_default_reminder_and_out_stream(self,
                                                               mock_print):
        """io_utils.read_replacements test output of default reminder"""
        blank_stream = open(os.devnull, 'w')  # open stream to devnull
        default_location = os.getcwd() + '/distend/configuration.txt'
        default_call = f'[+] replacements from: {default_location}'
        with patch("builtins.open", mock_open(read_data=self.file)) as default:
                result = io_utils.read_replacements(None)
                mock_print.assert_called_with(default_call, file=None)
        with patch("builtins.open", mock_open(read_data=self.file)) as silent:
                silent_result = io_utils.read_replacements(None, False,
                                                           blank_stream)
                mock_print.assert_called_with(default_call, file=blank_stream)
        blank_stream.close()

    def test_get_default_configuration_location(self):
        """io_utils.get_default_configuration_location
        returns correct location
        """
        default_location = os.getcwd() + '/distend/configuration.txt'
        self.assertEqual(str(io_utils.get_default_configuration_location()),
                         default_location,
                         'does not return the default configuration location')

    def test_read_pre_post_parses_single_prepend_and_postpend(self):
        """io_utils.read_pre_post parses file,
        returns tuple:(str:prepend, str:postpend)
        """
        with patch("builtins.open", mock_open(read_data=self.file)) as mock_file:
                result = io_utils.read_pre_post(None)
        self.assertIsInstance(result, tuple, 'does return a tuple')
        self.assertIsInstance(result[0], str, 'element zero is not a str')
        self.assertIsInstance(result[1], str, 'element one is not a str')
        self.assertEqual(result, ('1972', '1984'),
                         'does not parse single pre and postpend correctly')

    def test_read_pre_post_parses_multiple_prepends_and_postpends(self):
        """io_utils.read_pre_post parses,
        returns tuple:(list:prepends, list:postpends)
        """
        with patch("builtins.open",
                   mock_open(read_data=self.list_pre_postpend)) as mock_file:
                result = io_utils.read_pre_post(None)
        self.assertIsInstance(result, tuple, 'does return a tuple')
        self.assertIsInstance(result[0], list, 'element zero is not a list')
        self.assertIsInstance(result[1], list, 'element one is not a list')
        self.assertEqual(result, (['1972', '1973'], ['1984', '1985']),
                         'does not parse multiple pre and postpends correctly')

    def test_read_pre_post_parses_no_and_blank_prepends_and_postpends(self):
        """io_utils.read_pre_post parses,
        returns tuple:(str:prepends, str:postpends)
        """
        with patch("builtins.open",
                   mock_open(read_data=self.blank_pre_postpend)) as mock_file:
                blank_result = io_utils.read_pre_post(None)
        with patch("builtins.open",
                   mock_open(read_data=self.no_pre_postpend)) as mock_file:
                no_result = io_utils.read_pre_post(None)
        self.assertIsInstance(blank_result, tuple, 'does return a tuple')
        self.assertIsInstance(blank_result[0], str,
                              'element zero is not a str')
        self.assertIsInstance(blank_result[1], str,
                              'element one is not a str')
        self.assertIsInstance(no_result, tuple, 'does return a tuple')
        self.assertIsInstance(no_result[0], str,
                              'element zero is not a str')
        self.assertIsInstance(no_result[1], str,
                              'element one is not a str')
        self.assertEqual(blank_result, ('', ''),
                         'does not parse blank pre and postpends correctly')
        self.assertEqual(no_result, ('', ''),
                         'does not parse no pre and postpends case correctly')

    def test_read_pre_post_parses_malformed_pre_postpends(self):
        """io_utils.read_pre_post parses,
        returns tuple(str:prepend, list:postpend)"""
        with patch("builtins.open",
                mock_open(read_data=self.malformed_pre_postpend)) as mock_file:
                malformed_result = io_utils.read_pre_post(None)
        self.assertIsInstance(malformed_result, tuple, 'does return a tuple')
        self.assertIsInstance(malformed_result[0], str,
                              'element zero is not a str')
        self.assertIsInstance(malformed_result[1], list,
                              'element one is not a list')
        self.assertEqual(malformed_result, ('', ['1984', '1985']),
                         'does not parse malformed pre postpends correctly')

    @patch('builtins.print')
    def test_read_pre_post_default_reminder_and_out_stream(self, mock_print):
        """io_utils.read_pre_post test output of default reminder"""
        blank_stream = open(os.devnull, 'w')  # open stream to devnull
        default_location = os.getcwd() + '/distend/configuration.txt'
        default_call = f'[+] pre and postpends from: {default_location}'
        with patch("builtins.open", mock_open(read_data=self.file)) as default:
                result = io_utils.read_pre_post(None)
                mock_print.assert_called_with(default_call, file=None)
        with patch("builtins.open", mock_open(read_data=self.file)) as silent:
                silent_result = io_utils.read_pre_post(None, False,
                                                         blank_stream)
                mock_print.assert_called_with(default_call, file=blank_stream)
        blank_stream.close()

    def test_unique_file_name_formats_correctly(self):
        """io_utils.unique_file_name returns correct string given input"""
        infile = 'duplicate'
        cnt = 1
        result = io_utils.unique_file_name(infile, cnt)
        self.assertIsInstance(result, str, 'does not return a str')
        self.assertEqual(result, 'duplicate_wordlist(1).temp',
                         'does not format duplicate file name correctly')

    # no need to test file_exists, basically just the standard lib function

    def test_create_wordlist_infile_equals_outfile(self):
        """io_utils.create_wordlist returns alternate file name"""
        infile = outfile = 'duplicate'
        with patch('builtins.open', mock_open()) as mock_file:
            result = io_utils.create_wordlist(infile, outfile)
        mock_file.assert_called_once_with('duplicate_wordlist(1).temp', 'x')
        self.assertEqual(result, 'duplicate_wordlist(1).temp',
                         'does not return an alternate outfile name')

    def test_create_wordlist_infile_does_not_equal_outfile(self):
        """io_utils.create_wordlist returns outfile str"""
        infile = 'unique.txt'
        outfile = 'out.txt'
        with patch('builtins.open', mock_open()) as mock_file:
            result = io_utils.create_wordlist(infile, outfile)
        mock_file.assert_called_once_with(outfile, 'x')
        self.assertEqual(result, outfile,
                         'does not return the correct outfile name')

    @patch('distend.io_utils.shutil.copy')
    def test_create_wordlist_infile_equals_outfile_concat_true(self, mock_copy):
        """io_utils.create_wordlist returns alternate file name"""
        infile = outfile = 'duplicate'
        mock_copy.return_value = 'duplicate_wordlist(1).temp'
        result = io_utils.create_wordlist(infile, outfile, True)
        mock_copy.assert_called_once_with('duplicate',
                                          'duplicate_wordlist(1).temp')
        self.assertEqual(result, mock_copy.return_value,
                         'failed to cat and return the correct outfile name')

    @patch('distend.io_utils.shutil.copy')
    def test_create_wordlist_in_not_equal_to_out_concat_true(self, mock_copy):
        """io_utils.create_wordlist returns outfile name"""
        infile = 'unique.txt'
        outfile = 'out.txt'
        mock_copy.return_value = 'out.txt'
        result = io_utils.create_wordlist(infile, outfile, True)
        mock_copy.assert_called_once_with('unique.txt', 'out.txt')
        self.assertEqual(result, mock_copy.return_value,
                         'failed to cat and return the correct outfile name')

    @patch('builtins.open')
    def test_create_wordlist_throws_FileExistsError(self, mock_open):
        """io_utils.create_wordlist handles FileExistsError"""
        infile = 'unique.txt'
        outfile = 'out.txt'
        verbose = False
        force = True
        mock_open.side_effect = [FileExistsError, mock_open.DEFAULT]
        with patch('builtins.input', return_value='y'):
            result = io_utils.create_wordlist(infile, outfile)
            mock_open.assert_called_with(outfile, 'w')
        mock_open.reset_mock()
        mock_open.side_effect = [FileExistsError, mock_open.DEFAULT]
        with patch('builtins.input', return_value='blank_answer'):
            result = io_utils.create_wordlist(infile, outfile, verbose, force)
            mock_open.assert_called_with(outfile, 'w')


    def test_read_file_generator_works(self):
        """io_utils.read_file_generator works and returns a generator"""
        infile = 'unique.txt'
        file_data = 'first_word\nsecond_word\nthird_word'
        generator_type = type(0 for i in [])
        with patch("builtins.open",
                   mock_open(read_data=file_data)) as mock_file:
                result = io_utils.read_file_generator(infile)
                self.assertEqual(type(result), generator_type,
                                 'does not return a generator')
                self.assertEqual(list(result), ['first_word\n', 'second_word\n',
                                 'third_word'], 'does not return a generator')

    def test_append_list(self):
        """io_utils.append_list returns nothing and writes to file"""
        lines = ['first', 'second']
        single_element = ['sin']
        outfile = 'out.txt'
        with patch('builtins.open', mock_open()) as mock_file:
            io_utils.append_list(lines, outfile)
        with patch('builtins.open', mock_open()) as single_element_mock:
            io_utils.append_list(single_element, outfile)
        mock_file.assert_called_once_with(outfile, 'a')
        single_element_mock.assert_called_once_with(outfile, 'a')
        mock_file.return_value.write.assert_called_once_with('first\nsecond\n')
        single_element_mock.return_value.write.assert_called_once_with('sin\n')

    @patch('builtins.print')
    def test_append_list_stdout(self, mock_print):
        """io_utils.append_list returns nothing and prints to stdout"""
        lines = ['first', 'second']
        single_element = ['first']
        io_utils.append_list(lines, None)
        mock_print.assert_called_with('first\nsecond\n', end='')
        io_utils.append_list(single_element, None)
        mock_print.assert_called_with('first\n', end='')

    @patch('distend.io_utils.shutil.move')
    def test_rename_file(self, mock_move):
        """io_utils.rename_file returns nothing and moves temp_file to rn_file"""
        temp_file = 'duplicate_wordlist(1).txt'
        rn_file = 'renamed.txt'
        mock_move.return_value = rn_file
        force = True
        with patch('builtins.input', return_value='y'):
            io_utils.rename_file(temp_file, rn_file)
            mock_move.assert_called_once_with(temp_file, rn_file)
        mock_move.reset_mock()
        with patch('builtins.input', return_value='blank_answer'):
            io_utils.rename_file(temp_file, rn_file, force)
            mock_move.assert_called_once_with(temp_file, rn_file)

    def test_check_infile(self):
        """io_utils.check_infile checks if a file exists
        returns bool:True or raises a systemexit if a file does not exist
        """
        infile = 'existing_file.txt'
        with patch('distend.io_utils.file_exists', return_value=True):
            assert io_utils.check_infile(infile)

    def test_version_appears_in_banner_title(self):
        """io_utils.banner_title returns a banner with the version in it"""
        version = '1.0.0'
        result = io_utils.banner_title(version)
        self.assertIn(version, result, 'did not return version in banner')

    def tearDown(self):
        pass

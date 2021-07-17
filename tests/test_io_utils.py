# workaround
import sys
sys.path.append('..')

# standard library
import unittest
from unittest.mock import patch, mock_open

# internal distend imports
from distend import io_utils

class Test_io_utils(unittest.TestCase):

    def setUp(self):
        # example file configurations
        self.file = """
                      # rules
                      a = 4
                      e = 3
                      # prepend
                      prepend, 1972
                      # postpend
                      postpend, 1984"""
        self.single_rule = """
                              # rules
                              a = 4
                              # prepend
                              prepend, 1972
                              # postpend
                              postpend, 1984"""
        self.no_rule = """
                          # rules
                          # prepend
                          prepend, 1972
                          # postpend
                          postpend, 1984"""
        self.list_pre_postpend = """
                                    # rules
                                    a = 4
                                    e = 3
                                    # prepend
                                    prepend, 1972, 1973
                                    # postpend
                                    postpend, 1984, 1985"""
        self.blank_pre_postpend = """
                                     # rules
                                     a = 4
                                     e = 3
                                     # prepend
                                     prepend,
                                     # postpend
                                     postpend,"""
        self.no_pre_postpend = """
                                  # rules
                                  a = 4
                                  e = 3
                                  # prepend
                                  # postpend"""

    def test_reduce_list_maintains_list(self):
        """io_utils.reduce_list returns a list given a list"""
        input = ['1984', '1985']
        result = io_utils.reduce_list(input)
        self.assertIsInstance(result, list, 'does not return datatype list')
        self.assertEqual(result, input, 'does not maintain list')

    def test_reduce_list_reduces_to_str(self):
        """io_utils.reduce_list returns a str given a single element"""
        single_element_input = ['1984']
        no_element_input = ['']
        default_input = ''
        single_element_result = io_utils.reduce_list(single_element_input)
        no_element_result = io_utils.reduce_list(no_element_input)
        default_input_result = io_utils.reduce_list(default_input)
        self.assertIsInstance(single_element_result, str,
                              'does not return datatype str')
        self.assertIsInstance(no_element_result, str,
                              'does not return datatype str')
        self.assertIsInstance(default_input_result, str,
                              'does not return datatype str')
        self.assertEqual(single_element_result, '1984',
                         'does not reduce to str')
        self.assertEqual(no_element_result, '',
                         'does not reduce to str')
        self.assertEqual(default_input_result, '',
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
        rule_line = 'a = 4'
        false_comment = 'This is not a comment # other text'
        result = io_utils.is_comment(line)
        prepend_result = io_utils.is_comment(prepend_line)
        rule_result = io_utils.is_comment(rule_line)
        false_comment_result = io_utils.is_comment(false_comment)
        self.assertIsInstance(result, bool, 'does not return datatype bool')
        self.assertIsInstance(prepend_result, bool,
                              'does not return datatype bool')
        self.assertIsInstance(rule_result, bool,
                              'does not return datatype bool')
        self.assertIsInstance(false_comment_result, bool,
                              'does not return datatype bool')
        self.assertEqual(result, False, 'incorrectly catches regular text')
        self.assertEqual(prepend_result, False,
                         'incorrectly catches regular text')
        self.assertEqual(rule_result, False,
                         'incorrectly catches regular text')
        self.assertEqual(false_comment_result, False,
                         'incorrectly catches regular text')

    def test_rule_reader_parses_rules(self):
        """io_utils.rule_reader parses rules, returns rules in a dictionary"""
        with patch("builtins.open", mock_open(read_data=self.file)) as mock_file:
                result = io_utils.rule_reader(None)
        self.assertIsInstance(result, dict, 'does return a dictionary')
        self.assertEqual(result, {'a':'4', 'e':'3'},
                         'does not parse the rules correctly')

    def test_rule_reader_single_rule_and_no_rule(self):
        """io_utils.rule_reader parses, returns a dictionary"""
        with patch("builtins.open", mock_open(read_data=self.single_rule)) as mock_file:
                single_result = io_utils.rule_reader(None)
        with patch("builtins.open", mock_open(read_data=self.no_rule)) as mock_file:
                no_rule_result = io_utils.rule_reader(None)
        self.assertIsInstance(single_result, dict, 'does return a dictionary')
        self.assertIsInstance(no_rule_result, dict, 'does return a dictionary')
        self.assertEqual(single_result, {'a':'4'},
                         'does not parse the rules correctly')
        self.assertEqual(no_rule_result, {},
                         'does not parse the rules correctly')

    def test_pre_post_reader_parses_single_prepend_and_postpend(self):
        """io_utils.pre_post_reader parses file,
        returns tuple:(str:prepend, str:postpend)
        """
        with patch("builtins.open", mock_open(read_data=self.file)) as mock_file:
                result = io_utils.pre_post_reader(None)
        self.assertIsInstance(result, tuple, 'does return a tuple')
        self.assertIsInstance(result[0], str, 'element zero is not a str')
        self.assertIsInstance(result[1], str, 'element one is not a str')
        self.assertEqual(result, ('1972', '1984'),
                         'does not parse single pre and postpend correctly')

    def test_pre_post_reader_parses_multiple_prepends_and_postpends(self):
        """io_utils.pre_post_reader parses,
        returns tuple:(list:prepends, list:postpends)
        """
        with patch("builtins.open", mock_open(read_data=self.list_pre_postpend)) as mock_file:
                result = io_utils.pre_post_reader(None)
        self.assertIsInstance(result, tuple, 'does return a tuple')
        self.assertIsInstance(result[0], list, 'element zero is not a list')
        self.assertIsInstance(result[1], list, 'element one is not a list')
        self.assertEqual(result, (['1972', '1973'], ['1984', '1985']),
                         'does not parse multiple pre and postpends correctly')

    def test_pre_post_reader_parses_no_and_blank_prepends_and_postpends(self):
        """io_utils.pre_post_reader parses,
        returns tuple:(str:prepends, str:postpends)
        """
        with patch("builtins.open", mock_open(read_data=self.blank_pre_postpend)) as mock_file:
                blank_result = io_utils.pre_post_reader(None)
        with patch("builtins.open", mock_open(read_data=self.no_pre_postpend)) as mock_file:
                no_result = io_utils.pre_post_reader(None)
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

    def test_read_file_generator_works(self):
        """io_utils.read_file_generator works and returns a generator"""
        infile = 'unique.txt'
        file_data = 'first_word\nsecond_word\nthird_word'
        generator_type = type(1 for i in "")
        with patch("builtins.open", mock_open(read_data=file_data)) as mock_file:
                result = io_utils.read_file_generator(infile)
                self.assertEqual(type(result), generator_type,
                                 'does not return a generator')
                self.assertEqual(list(result), ['first_word\n', 'second_word\n',
                                 'third_word'], 'does not return a generator')

    def test_append_list(self):
        """io_utils.append_list returns nothing and writes to file"""
        lines = ['first', 'second']
        single_element = ['first']
        outfile = 'out.txt'
        with patch('builtins.open', mock_open()) as mock_file:
            io_utils.append_list(lines, outfile)
        with patch('builtins.open', mock_open()) as single_element_mock:
            io_utils.append_list(single_element, outfile)
        mock_file.assert_called_once_with(outfile, 'a')
        single_element_mock.assert_called_once_with(outfile, 'a')
        mock_file.return_value.write.assert_called_once_with('first\nsecond\n')
        single_element_mock.return_value.write.assert_called_once_with('first\n')

    @patch('builtins.print')
    def test_append_list_stdout(self, mock_print):
        """io_utils.append_list returns nothing and prints to stdout"""
        lines = ['first', 'second']
        single_element = ['first']
        io_utils.append_list(lines, None)
        mock_print.assert_called_with('first\nsecond\n')
        io_utils.append_list(single_element, None)
        mock_print.assert_called_with('first\n')

    @patch('distend.io_utils.shutil.move')
    def test_rename_file(self, mock_move):
        """io_utils.rename_file returns nothing and moves temp_file to rn_file"""
        temp_file = 'duplicate_wordlist(1).txt'
        rn_file = 'renamed.txt'
        mock_move.return_value = rn_file
        with patch('builtins.input', return_value='y'):
            io_utils.rename_file(temp_file, rn_file)
            mock_move.assert_called_once_with(temp_file, rn_file)

    def test_generator_file_check(self):
        """io_utils.generator_file_check checks if a file exists
        returns bool:True or raises a systemexit if a file does not exist
        """
        infile = 'existing_file.txt'
        with patch('distend.io_utils.file_exists', return_value=True):
            assert io_utils.generator_file_check(infile)

    def test_version_appears_in_banner_title(self):
        """io_utils.banner_title returns a banner with the version in it"""
        version = '1.0.0'
        result = io_utils.banner_title(version)
        self.assertIn(version, result, 'did not return version in banner')

    def tearDown(self):
        pass

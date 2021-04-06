# workaround
import sys
sys.path.append('..')

# standard library
import unittest
from unittest.mock import patch, mock_open

# internal distend imports
from distend import io_utils as iou

class TestIoUtils(unittest.TestCase):

    def setUp(self):
        self.file = """
                      # rules
                      a = 4
                      e = 3
                      # prepend
                      prepend, 1972
                      # postpend
                      postpend, 1984"""

    def test_reduce_list_returns_list(self):
        """iou.reduce_list returns datatype list given a list"""
        input = ['1984', '1985']
        result = iou.reduce_list(input)
        self.assertIsInstance(result, list, 'does not return datatype list')

    def test_reduce_list_returns_str(self):
        """iou.reduce_list returns datatype str given single element"""
        input = ['1984']
        result = iou.reduce_list(input)
        self.assertIsInstance(result, str, 'does not return datatype str')

    def test_reduce_list_reduces_to_str(self):
        """iou.reduce_list reduces single element list to str"""
        input = ['1984']
        result = iou.reduce_list(input)
        self.assertEqual(result, '1984', 'does not reduce to str')

    def test_reduce_list_maintains_list(self):
        """iou.reduce_list maintains list with more than one element"""
        input = ['1984', '1985']
        result = iou.reduce_list(input)
        self.assertEqual(result, input, 'does not maintain list')

    def test_is_comment_returns_bool(self):
        """iou.is_comment returns a bool"""
        line = '# This is a comment line'
        result = iou.is_comment(line)
        self.assertIsInstance(result, bool, 'does not return a bool')

    def test_is_comment_identifies_comment(self):
        """iou.is_comment catches a comment and returns true"""
        line = '# This is a comment line'
        result = iou.is_comment(line)
        self.assertEqual(result, True, 'does not identify comment')

    def test_is_comment_does_not_identify_regular_text(self):
        """iou.is_comment does not catch regular text and returns false"""
        line = 'This is a regular line'
        result = iou.is_comment(line)
        self.assertEqual(result, False, 'incorrectly catches regular text')

    def test_rule_reader_returns_dictionary(self):
        """iou.rule_reader returns a dictionary"""
        with patch("builtins.open", mock_open(read_data=self.file)) as mock_file:
                result = iou.rule_reader(None)
        mock_file.assert_called_once_with("../distend/rules.conf", "r")
        self.assertIsInstance(result, dict, 'does return a dictionary')

    def test_rule_reader_parses_rules(self):
        """iou.rule_reader parses rules and returns in a dictionary"""
        with patch("builtins.open", mock_open(read_data=self.file)) as mock_file:
                result = iou.rule_reader(None)
        mock_file.assert_called_once_with("../distend/rules.conf", "r")
        self.assertEqual(result, {'a':'4', 'e':'3'},
                         'does not parse the rules correctly')

    def test_pp_reader_returns_tuple(self):
        """iou.pp_reader returns datatype tuple"""
        with patch("builtins.open", mock_open(read_data=self.file)) as mock_file:
                result = iou.pp_reader(None)
        mock_file.assert_called_once_with("../distend/rules.conf", "r")
        self.assertIsInstance(result, tuple, 'does return a tuple')

    def test_pp_reader_parses_single_prepend_and_postpend(self):
        """iou.pp_reader parses and returns tuple:(prepend, postpend)"""
        with patch("builtins.open", mock_open(read_data=self.file)) as mock_file:
                result = iou.pp_reader(None)
        mock_file.assert_called_once_with("../distend/rules.conf", "r")
        self.assertEqual(result, ('1972', '1984'),
                         'does not parse single pre and postpend correctly')

    def test_pp_reader_parses_multiple_prepends_and_postpends(self):
        """iou.pp_reader parses and returns tuple:([prepends], [postpends])"""
        self.file = self.file.replace('prepend, 1972', 'prepend, 1972, 1973')
        self.file = self.file.replace('postpend, 1984', 'postpend, 1984, 1985')
        with patch("builtins.open", mock_open(read_data=self.file)) as mock_file:
                result = iou.pp_reader(None)
        mock_file.assert_called_once_with("../distend/rules.conf", "r")
        self.assertEqual(result, (['1972', '1973'], ['1984', '1985']),
                         'does not parse multiple pre and postpends correctly')

    def test_unique_file_name_returns_str(self):
        """iou.unique_file_name returns datatype str"""
        infile = 'duplicate'
        cnt = 1
        result = iou.unique_file_name(infile, cnt)
        self.assertIsInstance(result, str, 'does not return a str')

    def test_unique_file_name_formats_correctly(self):
        """iou.unique_file_name returns correct string given input"""
        infile = 'duplicate'
        cnt = 1
        result = iou.unique_file_name(infile, cnt)
        self.assertEqual(result, 'duplicate_wordlist(1).temp',
                         'does not format inputs correctly')

    # do not need to test file_exists is basically the standard lib function

    def test_create_wordlist_infile_equals_outfile(self):
        """iou.create_wordlist returns alternate file name"""
        infile = outfile = 'duplicate'
        with patch('builtins.open', mock_open()) as mock_file:
            result = iou.create_wordlist(infile, outfile)
        mock_file.assert_called_once_with('duplicate_wordlist(1).temp', 'x')
        self.assertEqual(result, 'duplicate_wordlist(1).temp',
                         'does not return an alternate outfile name')

    def test_create_wordlist_infile_does_not_equal_outfile(self):
        """iou.create_wordlist returns outfile str"""
        infile = 'unique.txt'
        outfile = 'out.txt'
        with patch('builtins.open', mock_open()) as mock_file:
            result = iou.create_wordlist(infile, outfile)
        mock_file.assert_called_once_with(outfile, 'x')
        self.assertEqual(result, outfile,
                         'does not return the correct outfile name')

    @patch('distend.io_utils.shutil.copy')
    def test_create_wordlist_infile_equals_outfile_concat_true(self, mock_copy):
        """iou.create_wordlist returns alternate file name"""
        infile = outfile = 'duplicate'
        mock_copy.return_value = 'duplicate_wordlist(1).temp'
        result = iou.create_wordlist(infile, outfile, True)
        mock_copy.assert_called_once_with('duplicate',
                                          'duplicate_wordlist(1).temp')
        self.assertEqual(result, mock_copy.return_value,
                         'failed to cat and return the correct outfile name')

    @patch('distend.io_utils.shutil.copy')
    def test_create_wordlist_in_not_equal_to_out_concat_true(self, mock_copy):
        """iou.create_wordlist returns alternate file name"""
        infile = 'unique.txt'
        outfile = 'out.txt'
        mock_copy.return_value = 'out.txt'
        result = iou.create_wordlist(infile, outfile, True)
        mock_copy.assert_called_once_with('unique.txt', 'out.txt')
        self.assertEqual(result, mock_copy.return_value,
                         'failed to cat and return the correct outfile name')

    def test_read_file_generator_returns_generator(self):
        """iou.read_file_generator returns datatype generator"""
        infile = 'unique.txt'
        file_data = 'first_word\nsecond_word\nthird_word'
        with patch("builtins.open", mock_open(read_data=file_data)) as mock_file:
                result = iou.read_file_generator(infile)
        gentype = type(1 for i in "")
        self.assertEqual(type(result), gentype, 'does not return a generator')

    def test_read_file_generator_works(self):
        """iou.read_file_generator works as intended"""
        infile = 'unique.txt'
        file_data = 'first_word\nsecond_word\nthird_word'
        with patch("builtins.open", mock_open(read_data=file_data)) as mock_file:
                result = iou.read_file_generator(infile)
                self.assertEqual(list(result), ['first_word\n', 'second_word\n',
                                 'third_word'], 'does not return a generator')

    def test_append_list(self):
        """iou.append_list returns nothing writes to file"""
        lines = ['first', 'second']
        outfile = 'out.txt'
        with patch('builtins.open', mock_open()) as mock_file:
            iou.append_list(lines, outfile)

        mock_file.assert_called_once_with(outfile, 'a')
        mock_file.return_value.write.assert_called_once_with('first\nsecond\n')

    @patch('distend.io_utils.shutil.move')
    def test_rename_file(self, mock_move):
        """iou.rename_file returns nothing and moves tempfile to rn_file"""
        tempfile = 'duplicate_wordlist(1).txt'
        rn_file = 'renamed.txt'
        mock_move.return_value = rn_file
        with patch('builtins.input', return_value='y'):
            iou.rename_file(tempfile, rn_file)
            mock_move.assert_called_once_with(tempfile, rn_file)

    def test_generator_file_check(self):
        infile = 'existing_file.txt'
        with patch('distend.io_utils.file_exists', return_value=True):
            assert iou.generator_file_check(infile)

    def test_banner_title(self):
        vrsn = '1.0.0'
        result = iou.banner_title(vrsn)
        self.assertIn(vrsn, result, 'did not return version in banner')

    def tearDown(self):
        pass

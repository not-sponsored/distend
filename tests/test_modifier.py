# standard library
import unittest

# distend
from distend import modifier

class Testmodifier(unittest.TestCase):

    def test_prepend_list_against_prepends(self):
        """test modifier.prepend_list against an expected result"""
        base = 'test'
        prepend = ['1984', '1985']
        separator = '.'
        result = modifier.prepend_list(base, prepend)
        separator_result = modifier.prepend_list(base, prepend, separator)
        self.assertIsInstance(result, list, 'does not return a list')
        self.assertIsInstance(separator_result, list, 'does not return a list')
        self.assertEqual(result, ['1984test', '1985test'],
                         'list of prepends inserted incorrectly before base')
        self.assertEqual(separator_result, ['1984.test', '1985.test'],
                         'incorrect list of prepends with separator and base')

    def test_postpend_list_against_postpends(self):
        """test modifier.postpend_list against an expected result"""
        base = 'test'
        postpend = ['1984', '1985']
        separator = '.'
        result = modifier.postpend_list(base, postpend)
        separator_result = modifier.postpend_list(base, postpend, separator)
        self.assertIsInstance(result, list, 'does not return a list')
        self.assertIsInstance(separator_result, list, 'does not return a list')
        self.assertEqual(result, ['test1984', 'test1985'],
                         'list of postpends appended incorrectly on base')
        self.assertEqual(separator_result, ['test.1984', 'test.1985'],
                         'incorrect list of postpends with separator and base')

    def test_prepend_str_against_prepend_string(self):
        """test modifier.prepend_str returns expected string"""
        base = 'test'
        prepend = '1984'
        separator = '.'
        result = modifier.prepend_str(base, prepend)
        separator_result = modifier.prepend_str(base, prepend, separator)
        self.assertIsInstance(result, str, 'does not return a string')
        self.assertIsInstance(separator_result, str,
                              'does not return a string')
        self.assertEqual(result, '1984test',
                         'string prepend inserted incorrectly before base')
        self.assertEqual(separator_result, '1984.test',
                         'incorrect str of prepend with separator and base')

    def test_postpend_str_against_postpend(self):
        """test modifier.postpend_str returns expected string"""
        base = 'test'
        postpend = '1984'
        separator = '.'
        result = modifier.postpend_str(base, postpend)
        separator_result = modifier.postpend_str(base, postpend, separator)
        self.assertIsInstance(result, str, 'does not return a string')
        self.assertIsInstance(separator_result, str,
                              'does not return a string')
        self.assertEqual(result, 'test1984',
                         'string postpend appended incorrectly after base')
        self.assertEqual(separator_result, 'test.1984',
                         'incorrect str of prepend with separator and base')

    def test_replace_multiple_returns_at_least_base(self):
        """test modifier.replace_multiple returns at least the base string"""
        base = 'test'
        replacements = {'a':'4', 'l':'1'}
        blank_replacements = {}
        result = modifier.replace_multiple(base, replacements)
        blank_replacements_result = modifier.replace_multiple(base, blank_replacements)
        self.assertIsInstance(result, list, 'does not return a list')
        self.assertIsInstance(blank_replacements_result, list,
                              'does not return a list')
        self.assertEqual(len(result), 1, 'returns more elements than expected')
        self.assertEqual(len(blank_replacements_result), 1,
                         'returns more elements than expected')
        self.assertIn(base, result, 'does not return base string')
        self.assertIn(base, blank_replacements_result, 'does not return base string')

    def test_replace_multiple_against_replacements(self):
        """test modifier.replace_multiple returns at most a list of length two"""
        base = 'test'
        replacements = {'t':'7', 'e':'3'}
        single_replacement = {'s': '5'}
        result = modifier.replace_multiple(base, replacements)
        single_replacement_result = modifier.replace_multiple(base, single_replacement)
        self.assertIsInstance(result, list, 'does not return a list')
        self.assertIsInstance(single_replacement_result, list,
                              'does not return a list')
        self.assertEqual(len(result), 2, 'returns more than 2 elements')
        self.assertEqual(len(single_replacement_result), 2,
                         'returns more than 2 elements')
        self.assertEqual(result, ['test', '73s7'],
                         'does not return expected list')
        self.assertEqual(single_replacement_result, ['test', 'te5t'],
                         'does not return expected list')

    def test_replace_single_returns_at_least_base(self):
        """test modifier.replace_single returns at least the base string"""
        base = 'test'
        replacements = {'a':'4', 'l':'1'}
        blank_replacements = {}
        result = modifier.replace_single(base, replacements)
        blank_replacements_result = modifier.replace_single(base, blank_replacements)
        self.assertIsInstance(result, list, 'does not return a list')
        self.assertIsInstance(blank_replacements_result, list,
                              'does not return a list')
        self.assertEqual(len(result), 1, 'returns more elements than expected')
        self.assertEqual(len(blank_replacements_result), 1,
                         'returns more elements than expected')
        self.assertIn(base, result, 'does not return base string')
        self.assertIn(base, blank_replacements_result, 'does not return base string')

    def test_replace_single_against_replacements(self):
        """test modifier.replace_single returns expected list"""
        base = 'test'
        replacements = {'t':'7', 'e':'3'}
        single_replacement = {'s': '5'}
        result = modifier.replace_single(base, replacements)
        single_replacement_result = modifier.replace_multiple(base, single_replacement)
        self.assertIsInstance(result, list, 'does not return a list')
        self.assertIsInstance(single_replacement_result, list,
                              'does not return a list')
        self.assertEqual(result, ['test', '7es7', 't3st', '73s7'],
                         'does not return expected list')
        self.assertEqual(single_replacement_result, ['test', 'te5t'],
                         'does not return expected list')

    def test_fuse_list_prepend_list_postpend_returns_correct_list(self):
        """test modifier.fuse_list_prepend_list_postpend
        returns the correct modifications in a list
        """
        transformed = ['test', '73s7']
        prepends = ['1984', '1985']
        postpends = ['1974', '1975']
        separator = '.'
        result = modifier.fuse_list_prepend_list_postpend(transformed, prepends,
                                                         postpends)
        separator_result = modifier.fuse_list_prepend_list_postpend(transformed,
                                prepends, postpends, separator)
        self.assertIsInstance(result, list, 'does not return a list')
        self.assertIsInstance(separator_result, list, 'does not return a list')
        self.assertEqual(result, ['1984test', '1985test', 'test1974',
        'test1975', '1984test1974', '1984test1975', '1985test1974',
        '1985test1975', '198473s7', '198573s7', '73s71974', '73s71975',
        '198473s71974', '198473s71975', '198573s71974', '198573s71975',
        '73s7'],
        'does not modify list:prepend and list:postpend correctly')
        self.assertEqual(separator_result, ['1984.test', '1985.test',
        'test.1974', 'test.1975', '1984.test.1974', '1984.test.1975',
        '1985.test.1974', '1985.test.1975', '1984.73s7', '1985.73s7',
        '73s7.1974', '73s7.1975', '1984.73s7.1974', '1984.73s7.1975',
        '1985.73s7.1974', '1985.73s7.1975', '73s7'],
        'does not modify prepends and postpends with a separator correctly')

    def test_fuse_list_prepend_str_postpend_returns_correct_list(self):
        """test if modifier.fuse_list_prepend_str_postpend
        returns the correct modifications in a list
        """
        transformed = ['test', '73s7']
        prepends = ['1984', '1985']
        postpend = '1974'
        separator = '.'
        result = modifier.fuse_list_prepend_str_postpend(transformed, prepends,
                                                        postpend)
        separator_result = modifier.fuse_list_prepend_str_postpend(transformed,
                                prepends, postpend, separator)
        self.assertIsInstance(result, list, 'does not return a list')
        self.assertIsInstance(separator_result, list, 'does not return a list')
        self.assertEqual(result, ['1984test', '1985test', 'test1974',
        '1984test1974', '1985test1974', '198473s7', '198573s7', '73s71974',
        '198473s71974', '198573s71974', '73s7'],
        'does not modify list:prepend and str:postpend correctly')
        self.assertEqual(separator_result, ['1984.test', '1985.test',
        'test.1974', '1984.test.1974', '1985.test.1974', '1984.73s7',
        '1985.73s7', '73s7.1974', '1984.73s7.1974', '1985.73s7.1974', '73s7'],
        'does not modify prepends and postpend with a separator correctly')

    def test_fuse_str_prepend_list_postpend_returns_correct_list(self):
        """test if modifier.fuse_str_prepend_list_postpend
        returns the correct modifications in a list
        """
        transformed = ['test', '73s7']
        prepend = '1984'
        postpends = ['1974', '1975']
        separator = '.'
        result = modifier.fuse_str_prepend_list_postpend(transformed, prepend,
                                                        postpends)
        separator_result = modifier.fuse_str_prepend_list_postpend(transformed,
                                prepend, postpends, separator)
        self.assertIsInstance(result, list, 'does not return a list')
        self.assertIsInstance(separator_result, list, 'does not return a list')
        self.assertEqual(result, ['1984test', 'test1974', 'test1975',
        '1984test1974', '1984test1975', '198473s7', '73s71974', '73s71975',
        '198473s71974', '198473s71975', '73s7'],
        'does not modify str:prepend and list:postpend correctly')
        self.assertEqual(separator_result, ['1984.test', 'test.1974',
        'test.1975', '1984.test.1974', '1984.test.1975', '1984.73s7',
        '73s7.1974', '73s7.1975', '1984.73s7.1974', '1984.73s7.1975', '73s7'],
        'does not modify prepend and postpends with a separator correctly')

    def test_fuse_str_prepend_str_postpend_returns_correct_list(self):
        """test if modifier.fuse_str_prepend_str_postpend
        returns the correct modifications in a list
        """
        transformed = ['test', '73s7']
        prepend = '1984'
        postpend = '1974'
        separator = '.'
        result = modifier.fuse_str_prepend_str_postpend(transformed, prepend,
                                                       postpend)
        separator_result = modifier.fuse_str_prepend_str_postpend(transformed,
                                prepend, postpend, separator)
        self.assertIsInstance(result, list, 'does not return a list')
        self.assertIsInstance(separator_result, list, 'does not return a list')
        self.assertEqual(result, ['1984test', 'test1974', '1984test1974',
        '198473s7', '73s71974', '198473s71974', '73s7'],
        'does not modify str:prepend and str:postpend correctly')
        self.assertEqual(separator_result, ['1984.test', 'test.1974',
        '1984.test.1974', '1984.73s7', '73s7.1974', '1984.73s7.1974', '73s7'],
        'does not modify prepend and postpend with a separator correctly')

    def test_fuse_list_prepend_no_postpend_returns_correct_list(self):
        """test if modifier.fuse_list_prepend_no_postpend
        returns the correct modifications in a list
        """
        transformed = ['test', '73s7']
        prepends = ['1984', '1985']
        separator = '.'
        result = modifier.fuse_list_prepend_no_postpend(transformed, prepends)
        separator_result = modifier.fuse_list_prepend_no_postpend(transformed,
                                prepends, separator)
        self.assertIsInstance(result, list, 'does not return a list')
        self.assertIsInstance(separator_result, list, 'does not return a list')
        self.assertEqual(result, ['1984test', '198473s7', '1985test',
        '198573s7', '73s7'],
        'does not modify list:prepend correctly')
        self.assertEqual(separator_result, ['1984.test', '1984.73s7',\
        '1985.test', '1985.73s7', '73s7'],
        'does not modify list:prepend correctly')

    def test_fuse_str_prepend_no_postpend_returns_correct_list(self):
        """test if modifier.fuse_str_prepend_no_postpend
        returns the correct modifications in a list
        """
        transformed = ['test', '73s7']
        prepend = '1984'
        separator = '.'
        result = modifier.fuse_str_prepend_no_postpend(transformed, prepend)
        separator_result = modifier.fuse_str_prepend_no_postpend(transformed,
                                prepend, separator)
        self.assertIsInstance(result, list, 'does not return a list')
        self.assertIsInstance(separator_result, list, 'does not return a list')
        self.assertEqual(result, ['1984test', '198473s7', '73s7'],
        'does not modify list:prepend correctly')
        self.assertEqual(separator_result, ['1984.test', '1984.73s7', '73s7'],
        'does not modify prepends with a separator correctly')

    def test_fuse_no_prepend_list_postpend_returns_correct_list(self):
        """test if modifier.fuse_no_prepend_list_postpend
        returns the correct modifications in a list
        """
        transformed = ['test', '73s7']
        postpends = ['1974', '1975']
        separator = '.'
        result = modifier.fuse_no_prepend_list_postpend(transformed, postpends)
        separator_result = modifier.fuse_no_prepend_list_postpend(transformed,
                                postpends, separator)
        self.assertIsInstance(result, list, 'does not return a list')
        self.assertIsInstance(separator_result, list, 'does not return a list')
        self.assertEqual(result, ['test1974',  '73s71974', 'test1975',
        '73s71975', '73s7'],
        'does not modify list:prepend correctly')
        self.assertEqual(separator_result, ['test.1974',  '73s7.1974',
        'test.1975', '73s7.1975', '73s7'],
        'does not modify prepends with a separator correctly')

    def test_fuse_no_prepend_str_postpend_returns_correct_list(self):
        """test if modifier.fuse_no_prepend_str_postpend
        returns the correct modifications in a list
        """
        transformed = ['test', '73s7']
        postpend = '1974'
        separator = '.'
        result = modifier.fuse_no_prepend_str_postpend(transformed, postpend)
        separator_result = modifier.fuse_no_prepend_str_postpend(transformed,
                                postpend, separator)
        self.assertIsInstance(result, list, 'does not return a list')
        self.assertIsInstance(separator_result, list, 'does not return a list')
        self.assertEqual(result, ['test1974',  '73s71974', '73s7'],
        'does not modify str:prepend correctly')
        self.assertEqual(separator_result, ['test.1974',  '73s7.1974', '73s7'],
        'does not modify prepend with a separator correctly')

if __name__ == '__main__':
    unittest.main()

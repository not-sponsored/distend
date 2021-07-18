# hacky way to get tests to run
import sys
sys.path.append('..')

# standard library
import unittest

# distend
from distend import modifier

class Testmodifier(unittest.TestCase):

    def test_prepend_list_against_prepends(self):
        """test modifier.prepend_list against an expected result"""
        base = 'test'
        prepend = ['1984', '1985']
        result = modifier.prepend_list(base, prepend)
        self.assertIsInstance(result, list, 'does not return a list')
        self.assertEqual(result, ['1984test', '1985test'],
                         'list of prepends inserted incorrectly before base')

    def test_postpend_list_against_postpends(self):
        """test modifier.postpend_list against an expected result"""
        base = 'test'
        postpend = ['1984', '1985']
        result = modifier.postpend_list(base, postpend)
        self.assertIsInstance(result, list, 'does not return a list')
        self.assertEqual(result, ['test1984', 'test1985'],
                         'list of postpends appended incorrectly on base')

    def test_prepend_str_against_prepend_string(self):
        """test modifier.prepend_str returns expected string"""
        base = 'test'
        prepend = '1984'
        result = modifier.prepend_str(base, prepend)
        self.assertIsInstance(result, str, 'does not return a string')
        self.assertEqual(result, '1984test',
                         'string prepend inserted incorrectly before base')

    def test_postpend_str_against_postpend(self):
        """test modifier.postpend_str returns expected string"""
        base = 'test'
        postpend = '1984'
        result = modifier.postpend_str(base, postpend)
        self.assertIsInstance(result, str, 'does not return a string')
        self.assertEqual(result, 'test1984',
                         'string postpend appended incorrectly after base')

    def test_multi_transform_returns_at_least_base(self):
        """test modifier.multi_transform returns at least the base string"""
        base = 'test'
        rules = {'a':'4', 'l':'1'}
        blank_rules = {}
        result = modifier.multi_transform(base, rules)
        blank_rules_result = modifier.multi_transform(base, blank_rules)
        self.assertIsInstance(result, list, 'does not return a list')
        self.assertIsInstance(blank_rules_result, list,
                              'does not return a list')
        self.assertEqual(len(result), 1, 'returns more elements than expected')
        self.assertEqual(len(blank_rules_result), 1,
                         'returns more elements than expected')
        self.assertIn(base, result, 'does not return base string')
        self.assertIn(base, blank_rules_result, 'does not return base string')

    def test_multi_transform_against_rules(self):
        """test modifier.multi_transform returns at most a list of length two"""
        base = 'test'
        rules = {'t':'7', 'e':'3'}
        single_rule = {'s': '5'}
        result = modifier.multi_transform(base, rules)
        single_rule_result = modifier.multi_transform(base, single_rule)
        self.assertIsInstance(result, list, 'does not return a list')
        self.assertIsInstance(single_rule_result, list,
                              'does not return a list')
        self.assertEqual(len(result), 2, 'returns more than 2 elements')
        self.assertEqual(len(single_rule_result), 2,
                         'returns more than 2 elements')
        self.assertEqual(result, ['test', '73s7'],
                         'does not return expected list')
        self.assertEqual(single_rule_result, ['test', 'te5t'],
                         'does not return expected list')

    def test_single_transform_returns_at_least_base(self):
        """test modifier.single_transform returns at least the base string"""
        base = 'test'
        rules = {'a':'4', 'l':'1'}
        blank_rules = {}
        result = modifier.single_transform(base, rules)
        blank_rules_result = modifier.single_transform(base, blank_rules)
        self.assertIsInstance(result, list, 'does not return a list')
        self.assertIsInstance(blank_rules_result, list,
                              'does not return a list')
        self.assertEqual(len(result), 1, 'returns more elements than expected')
        self.assertEqual(len(blank_rules_result), 1,
                         'returns more elements than expected')
        self.assertIn(base, result, 'does not return base string')
        self.assertIn(base, blank_rules_result, 'does not return base string')

    def test_single_transform_against_rules(self):
        """test modifier.single_transform returns expected list"""
        base = 'test'
        rules = {'t':'7', 'e':'3'}
        single_rule = {'s': '5'}
        result = modifier.single_transform(base, rules)
        single_rule_result = modifier.multi_transform(base, single_rule)
        self.assertIsInstance(result, list, 'does not return a list')
        self.assertIsInstance(single_rule_result, list,
                              'does not return a list')
        self.assertEqual(result, ['test', '7es7', 't3st', '73s7'],
                         'does not return expected list')
        self.assertEqual(single_rule_result, ['test', 'te5t'],
                         'does not return expected list')

    def test_fuse_list_prepend_list_postpend_returns_correct_list(self):
        """test modifier.fuse_list_prepend_list_postpend
        returns the correct modifications in a list
        """
        transformed = ['test', '73s7']
        prepends = ['1984', '1985']
        postpends = ['1974', '1975']
        result = modifier.fuse_list_prepend_list_postpend(transformed, prepends,
                                                         postpends)
        self.assertIsInstance(result, list, 'does not return a list')
        self.assertEqual(result, ['1984test', '1985test', 'test1974',
        'test1975', '1984test1974', '1984test1975', '1985test1974',
        '1985test1975', '198473s7', '198573s7', '73s71974', '73s71975',
        '198473s71974', '198473s71975', '198573s71974', '198573s71975',
        '73s7'],
        'does not modify list:prepend and list:postpend correctly')

    def test_fuse_list_prepend_str_postpend_returns_correct_list(self):
        """test if modifier.fuse_list_prepend_str_postpend
        returns the correct modifications in a list
        """
        transformed = ['test', '73s7']
        prepends = ['1984', '1985']
        postpend = '1974'
        result = modifier.fuse_list_prepend_str_postpend(transformed, prepends,
                                                        postpend)
        self.assertIsInstance(result, list, 'does not return a list')
        self.assertEqual(result, ['1984test', '1985test', 'test1974',
        '1984test1974', '1985test1974', '198473s7', '198573s7', '73s71974',
        '198473s71974', '198573s71974', '73s7'],
        'does not modify list:prepend and str:postpend correctly')

    def test_fuse_str_prepend_list_postpend_returns_correct_list(self):
        """test if modifier.fuse_str_prepend_list_postpend
        returns the correct modifications in a list
        """
        transformed = ['test', '73s7']
        prepend = '1984'
        postpends = ['1974', '1975']
        result = modifier.fuse_str_prepend_list_postpend(transformed, prepend,
                                                        postpends)
        self.assertIsInstance(result, list, 'does not return a list')
        self.assertEqual(result, ['1984test', 'test1974', 'test1975',
        '1984test1974', '1984test1975', '198473s7', '73s71974', '73s71975',
        '198473s71974', '198473s71975', '73s7'],
        'does not modify str:prepend and list:postpend correctly')

    def test_fuse_str_prepend_str_postpend_returns_correct_list(self):
        """test if modifier.fuse_str_prepend_str_postpend
        returns the correct modifications in a list
        """
        transformed = ['test', '73s7']
        prepend = '1984'
        postpend = '1974'
        result = modifier.fuse_str_prepend_str_postpend(transformed, prepend,
                                                       postpend)
        self.assertIsInstance(result, list, 'does not return a list')
        self.assertEqual(result, ['1984test', 'test1974', '1984test1974',
        '198473s7', '73s71974', '198473s71974', '73s7'],
        'does not modifierify str:prepend and str:postpend correctly')

    def test_fuse_list_prepend_no_postpend_returns_correct_list(self):
        """test if modifier.fuse_list_prepend_no_postpend
        returns the correct modifications in a list
        """
        transformed = ['test', '73s7']
        prepends = ['1984', '1985']
        result = modifier.fuse_list_prepend_no_postpend(transformed, prepends)
        self.assertIsInstance(result, list, 'does not return a list')
        self.assertEqual(result, ['1984test', '198473s7', '1985test',
        '198573s7', '73s7'], 'does not modify list:prepend correctly')

    def test_fuse_str_prepend_no_postpend_returns_correct_list(self):
        """test if modifier.fuse_str_prepend_no_postpend
        returns the correct modifications in a list
        """
        transformed = ['test', '73s7']
        prepend = '1984'
        result = modifier.fuse_str_prepend_no_postpend(transformed, prepend)
        self.assertIsInstance(result, list, 'does not return a list')
        self.assertEqual(result, ['1984test', '198473s7', '73s7'],
        'does not modify list:prepend correctly')

    def test_fuse_no_prepend_list_postpend_returns_correct_list(self):
        """test if modifier.fuse_no_prepend_list_postpend
        returns the correct modifications in a list
        """
        transformed = ['test', '73s7']
        postpends = ['1974', '1975']
        result = modifier.fuse_no_prepend_list_postpend(transformed, postpends)
        self.assertIsInstance(result, list, 'does not return a list')
        self.assertEqual(result, ['test1974',  '73s71974', 'test1975',
        '73s71975', '73s7'], 'does not modify list:prepend correctly')

    def test_fuse_no_prepend_str_postpend_returns_correct_list(self):
        """test if modifier.fuse_no_prepend_str_postpend
        returns the correct modifications in a list
        """
        transformed = ['test', '73s7']
        postpend = '1974'
        result = modifier.fuse_no_prepend_str_postpend(transformed, postpend)
        self.assertIsInstance(result, list, 'does not return a list')
        self.assertEqual(result, ['test1974',  '73s71974', '73s7'],
        'does not modifierify str:prepend correctly')

# hacky way to get tests to run
import sys
sys.path.append('..')

# standard library
import unittest

# distend
from distend import modifier as mod

class TestModifier(unittest.TestCase):
    def test_pre_list_returns_list(self):
        """test mod.pre_list returns datatype list"""
        base = 'test'
        prepend = ['1984', '1985']
        result = mod.pre_list(base, prepend)
        self.assertIsInstance(result, list, 'does not return a list')

    def test_pre_list_against_prepend_list(self):
        """test mod.pre_list against an expected result"""
        base = 'test'
        prepend = ['1984', '1985']
        result = mod.pre_list(base, prepend)
        self.assertEqual(result, ['1984test', '1985test'],
                         'list of prepends inserted incorrectly before base')

    def test_post_list_returns_list(self):
        """tset mod.post_list returns datatype list"""
        base = 'test'
        postpend = ['1984', '1985']
        result = mod.post_list(base, postpend)
        self.assertIsInstance(result, list, 'does not return a list')

    def test_post_list_against_postpend_list(self):
        """test mod.post_list against an expected result"""
        base = 'test'
        postpend = ['1984', '1985']
        result = mod.post_list(base, postpend)
        self.assertEqual(result, ['test1984', 'test1985'],
                         'list of postpends appended incorrectly on base')

    def test_pre_str_returns_string(self):
        """test mod.pre_str returns datatype string"""
        base = 'test'
        prepend = '1984'
        result = mod.pre_str(base, prepend)
        self.assertIsInstance(result, str, 'does not return a string')

    def test_pre_str_against_prepend_string(self):
        """test mod.pre_str returns expected string"""
        base = 'test'
        prepend = '1984'
        result = mod.pre_str(base, prepend)
        self.assertEqual(result, '1984test',
                         'string prepend inserted incorrectly before base')

    def test_post_str_returns_string(self):
        """test mod.post_str returns datatype string"""
        base = 'test'
        postpend = '1984'
        result = mod.post_str(base, postpend)
        self.assertIsInstance(result, str, 'does not return a string')

    def test_post_str_against_postpend_string(self):
        """test mod.post_str returns expected string"""
        base = 'test'
        postpend = '1984'
        result = mod.post_str(base, postpend)
        self.assertEqual(result, 'test1984',
                         'string postpend appended incorrectly after base')

    def test_multi_transform_returns_list(self):
        """test mod.multi_transform returns datatype list"""
        base = 'test'
        rules = {'t':'7', 'e':'3'}
        result = mod.multi_transform(base, rules)
        self.assertIsInstance(result, list, 'does not return a list')

    def test_multi_transform_min_return_base(self):
        """test mod.multi_transform returns at least the base string"""
        base = 'test'
        rules = {'a':'4', 'l':'1'}
        result = mod.multi_transform(base, rules)
        self.assertEqual(len(result), 1, 'returns more elements than expected')
        self.assertIn(base, result, 'does not return base string')

    def test_multi_transform_max_return_len_two(self):
        """test mod.multi_transform returns at most a list of length two"""
        base = 'test'
        rules = {'t':'7', 'e':'3'}
        result = mod.multi_transform(base, rules)
        self.assertEqual(len(result), 2, 'returns more than 2 elements')

    def test_multi_transform_against_rules(self):
        """test mod.multi_transform returns expected list"""
        base = 'test'
        rules = {'t':'7', 'e':'3'}
        result = mod.multi_transform(base, rules)
        self.assertEqual(result, ['test', '73s7'],
                         'does not return expected list')

    def test_single_transform_returns_list(self):
        """test mod.single_transform returns datatype list"""
        base = 'test'
        rules = {'t':'7', 'e':'3'}
        result = mod.single_transform(base, rules)
        self.assertIsInstance(result, list, 'does not return a list')

    def test_single_transform_min_return_base(self):
        """test mod.single_transform returns at least the base string"""
        base = 'test'
        rules = {'a':'4', 'l':'1'}
        result = mod.single_transform(base, rules)
        self.assertEqual(len(result), 1, 'returns more elements than expected')
        self.assertIn(base, result, 'does not return base string')

    def test_single_transform_against_rules(self):
        """test mod.single_transform returns expected list"""
        base = 'test'
        rules = {'t':'7', 'e':'3'}
        result = mod.single_transform(base, rules)
        self.assertEqual(result, ['test', '7es7', 't3st', '73s7'],
                         'does not return expected list')

    def test_fuse_lp_lp_returns_list(self):
        """test mod.fuse_lp_lp returns datatype list"""
        transformed = ['test', '73s7']
        lpre = ['1984', '1985']
        lpost = ['1974', '1975']
        result = mod.fuse_lp_lp(transformed, lpre, lpost)
        self.assertIsInstance(result, list, 'does not return a list')

    def test_fuse_lp_lp_returns_correct_list(self):
        """test if mod.fuse_lp_lp modifies and returns correctly"""
        transformed = ['test', '73s7']
        lpre = ['1984', '1985']
        lpost = ['1974', '1975']
        result = mod.fuse_lp_lp(transformed, lpre, lpost)
        self.assertEqual(result, ['1984test', '1985test', 'test1974',
        'test1975', '1984test1974', '1984test1975', '1985test1974',
        '1985test1975', '198473s7', '198573s7', '73s71974', '73s71975',
        '198473s71974', '198473s71975', '198573s71974', '198573s71975',
        '73s7'],
        'does not modify lst:prepend and lst:postpend correctly')

    def test_fuse_lp_sp_returns_list(self):
        """test mod.fuse_lp_sp returns datatype list"""
        transformed = ['test', '73s7']
        lpre = ['1984', '1985']
        spost = '1974'
        result = mod.fuse_lp_sp(transformed, lpre, spost)
        self.assertIsInstance(result, list, 'does not return a list')

    def test_fuse_lp_sp_returns_correct_list(self):
        """test if mod.fuse_lp_sp modifies and returns correctly"""
        transformed = ['test', '73s7']
        lpre = ['1984', '1985']
        spost = '1974'
        result = mod.fuse_lp_sp(transformed, lpre, spost)
        self.assertEqual(result, ['1984test', '1985test', 'test1974',
        '1984test1974', '1985test1974', '198473s7', '198573s7', '73s71974',
        '198473s71974', '198573s71974', '73s7'],
        'does not modify lst:prepend and str:postpend correctly')

    def test_fuse_sp_lp_returns_list(self):
        """test mod.fuse_sp_lp returns datatype list"""
        transformed = ['test', '73s7']
        spre = '1984'
        lpost = ['1974', '1975']
        result = mod.fuse_sp_lp(transformed, spre, lpost)
        self.assertIsInstance(result, list, 'does not return a list')

    def test_fuse_sp_lp_returns_correct_list(self):
        """test if mod.fuse_sp_lp returns the correct list"""
        transformed = ['test', '73s7']
        spre = '1984'
        lpost = ['1974', '1975']
        result = mod.fuse_sp_lp(transformed, spre, lpost)
        self.assertEqual(result, ['1984test', 'test1974', 'test1975',
        '1984test1974', '1984test1975', '198473s7', '73s71974', '73s71975',
        '198473s71974', '198473s71975', '73s7'],
        'does not modify str:prepend and lst:postpend correctly')

    def test_fuse_sp_sp_returns_list(self):
        """test mod.fuse_sp_sp returns datatype list"""
        transformed = ['test', '73s7']
        spre = '1984'
        spost = '1974'
        result = mod.fuse_sp_sp(transformed, spre, spost)
        self.assertIsInstance(result, list, 'does not return a list')

    def test_fuse_sp_sp_returns_correct_list(self):
        """test if mod.fuse_sp_sp returns the correct list"""
        transformed = ['test', '73s7']
        spre = '1984'
        spost = '1974'
        result = mod.fuse_sp_sp(transformed, spre, spost)
        self.assertEqual(result, ['1984test', 'test1974', '1984test1974',
        '198473s7', '73s71974', '198473s71974', '73s7'],
        'does not modify str:prepend and str:postpend correctly')

    def test_fuse_lp_np_returns_list(self):
        """test mod.fuse_lp_np returns datatype list"""
        transformed = ['test', '73s7']
        lpre = ['1984', '1985']
        result = mod.fuse_lp_np(transformed, lpre)
        self.assertIsInstance(result, list, 'does not return a list')

    def test_fuse_lp_np_returns_correct_list(self):
        """test if mod.fuse_lp_np modifies and returns correctly"""
        transformed = ['test', '73s7']
        lpre = ['1984', '1985']
        result = mod.fuse_lp_np(transformed, lpre)
        self.assertEqual(result, ['1984test', '198473s7', '1985test',
        '198573s7', '73s7'], 'does not modify lst:prepend correctly')

    def test_fuse_sp_np_returns_list(self):
        """test mod.fuse_sp_np returns datatype list"""
        transformed = ['test', '73s7']
        spre = '1984'
        result = mod.fuse_sp_np(transformed, spre)
        self.assertIsInstance(result, list, 'does not return a list')

    def test_fuse_sp_np_returns_correct_list(self):
        """test if mod.fuse_sp_np modifies and returns correctly"""
        transformed = ['test', '73s7']
        spre = '1984'
        result = mod.fuse_sp_np(transformed, spre)
        self.assertEqual(result, ['1984test', '198473s7', '73s7'],
        'does not modify lst:prepend correctly')

    def test_fuse_np_lp_returns_list(self):
        """test mod.fuse_np_lp returns datatype list"""
        transformed = ['test', '73s7']
        lpost = ['1974', '1975']
        result = mod.fuse_np_lp(transformed, lpost)
        self.assertIsInstance(result, list, 'does not return a list')

    def test_fuse_np_lp_returns_correct_list(self):
        """test if mod.fuse_np_lp returns the correct list"""
        transformed = ['test', '73s7']
        lpost = ['1974', '1975']
        result = mod.fuse_np_lp(transformed, lpost)
        self.assertEqual(result, ['test1974',  '73s71974', 'test1975',
        '73s71975', '73s7'],
        'does not modify lst:prepend correctly')

    def test_fuse_np_sp_returns_list(self):
        """test mod.fuse_np_sp returns datatype list"""
        transformed = ['test', '73s7']
        spost = '1974'
        result = mod.fuse_np_sp(transformed, spost)
        self.assertIsInstance(result, list, 'does not return a list')

    def test_fuse_np_sp_returns_correct_list(self):
        """test if mod.fuse_np_sp returns the correct list"""
        transformed = ['test', '73s7']
        spost = '1974'
        result = mod.fuse_np_sp(transformed, spost)
        self.assertEqual(result, ['test1974',  '73s71974', '73s7'],
        'does not modify str:prepend correctly')

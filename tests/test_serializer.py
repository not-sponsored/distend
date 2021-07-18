# workaround
import sys
sys.path.append('..')

# standard library
import unittest

# internal distend imports
from distend import serializer

class TestSerializer(unittest.TestCase):

    def test_get_multi_rule_function(self):
        """test serializer.get_multi_rule_function,
        returns multi_transform function
        """
        multi_rule_true = True
        multi_rule_false = False
        transform_true = serializer.get_multi_rule_function(multi_rule_true)
        transform_false = serializer.get_multi_rule_function(multi_rule_false)
        self.assertTrue(callable(transform_true), 'return is not callable')
        self.assertTrue(callable(transform_false), 'return is not callable')
        self.assertEqual(transform_true.__name__, 'multi_transform',
                         "not multi_transform when multi_rule is true")
        self.assertEqual(transform_false.__name__, 'single_transform',
                         "not single_transform when multi_rule is false")

    def test_get_pre_postpend_function_with_list_prepend_list_postpend(self):
        """test serializer.get_pre_postpend_function,
        returns fuse_list_prepend_list_postpend
        """
        prepend, postpend = (['1972', '1973'], ['1984', '1985'])
        fuse = serializer.get_pre_postpend_function(prepend, postpend)
        self.assertTrue(callable(fuse), 'return is not callable')
        self.assertEqual(fuse.__name__, 'fuse_list_prepend_list_postpend',
                         "expected fuse_list_prepend_list_postpend")

    def test_get_pre_postpend_function_with_list_prepend_str_postpend(self):
        """test serializer.get_pre_postpend_function,
        returns fuse_list_prepend_str_postpend
        """
        prepend, postpend = (['1972', '1973'], '1984')
        fuse = serializer.get_pre_postpend_function(prepend, postpend)
        self.assertTrue(callable(fuse), 'return is not callable')
        self.assertEqual(fuse.__name__, 'fuse_list_prepend_str_postpend',
                         "expected fuse_list_prepend_str_postpend")

    def test_get_pre_postpend_function_with_str_prepend_str_postpend(self):
        """test serializer.get_pre_postpend_function,
        returns fuse_str_prepend_str_postpend
        """
        prepend, postpend = ('1972', '1984')
        fuse = serializer.get_pre_postpend_function(prepend, postpend)
        self.assertTrue(callable(fuse), 'return is not callable')
        self.assertEqual(fuse.__name__, 'fuse_str_prepend_str_postpend',
                         "expected fuse_str_prepend_str_postpend")

    def test_get_pre_postpend_function_with_str_prepend_list_postpend(self):
        """test serializer.get_pre_postpend_function,
        returns fuse_str_prepend_list_postpend
        """
        prepend, postpend = ('1972', ['1984', '1985'])
        fuse = serializer.get_pre_postpend_function(prepend, postpend)
        self.assertTrue(callable(fuse), 'return is not callable')
        self.assertEqual(fuse.__name__, 'fuse_str_prepend_list_postpend',
                         "expected fuse_str_prepend_list_postpend")

    def test_get_pre_postpend_function_with_list_prepend_no_postpend(self):
        """test serializer.get_pre_postpend_function
        returns fuse_list_prepend_no_postpend
        """
        prepend, postpend = (['1972', '1973'], '')
        fuse = serializer.get_pre_postpend_function(prepend, postpend)
        self.assertTrue(callable(fuse), 'return is not callable')
        self.assertEqual(fuse.__name__, 'fuse_list_prepend_no_postpend',
                         "expected fuse_list_prepend_no_postpend")

    def test_get_pre_postpend_function_with_str_prepend_no_postpend(self):
        """test serializer.get_pre_postpend_function,
        returns fuse_str_prepend_no_postpend
        """
        prepend, postpend = ('1972', '')
        fuse = serializer.get_pre_postpend_function(prepend, postpend)
        self.assertTrue(callable(fuse), 'return is not callable')
        self.assertEqual(fuse.__name__, 'fuse_str_prepend_no_postpend',
                         "expected fuse_str_prepend_no_postpend")

    def test_get_pre_postpend_function_with_no_prepend_list_postpend(self):
        """test serializer.get_pre_postpend_function,
        returns fuse_no_prepend_list_postpend
        """
        prepend, postpend = ('', ['1984', '1985'])
        fuse = serializer.get_pre_postpend_function(prepend, postpend)
        self.assertTrue(callable(fuse), 'return is not callable')
        self.assertEqual(fuse.__name__, 'fuse_no_prepend_list_postpend',
                         "expected fuse_no_prepend_list_postpend")

    def test_get_pre_postpend_function_with_no_prepend_str_postpend(self):
        """test serializer.get_pre_postpend_function,
        returns fuse_no_prepend_str_postpend
        """
        prepend, postpend = ('', '1984')
        fuse = serializer.get_pre_postpend_function(prepend, postpend)
        self.assertTrue(callable(fuse), 'return is not callable')
        self.assertEqual(fuse.__name__, 'fuse_no_prepend_str_postpend',
                         "expected fuse_no_prepend_str_postpend")

    def test_get_pre_postpend_function_with_no_prepend_no_postpend(self):
        """test serializer.get_pre_postpend_function, returns none"""
        prepend, postpend = ('', '')
        fuse = serializer.get_pre_postpend_function(prepend, postpend)
        self.assertIsNone(fuse, "expected none")

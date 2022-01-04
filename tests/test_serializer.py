# standard library
import unittest

# internal distend imports
from distend import serializer

class TestSerializer(unittest.TestCase):

    def test_get_replace_function(self):
        """test serializer.get_replace_function,
        returns replace_multiple function
        """
        replace_multiple_true = True
        replace_multiple_false = False
        replace_true = serializer.get_replace_function(replace_multiple_true)
        replace_false = serializer.get_replace_function(replace_multiple_false)
        self.assertTrue(callable(replace_true), 'return is not callable')
        self.assertTrue(callable(replace_false), 'return is not callable')
        self.assertEqual(replace_true.__name__, 'replace_multiple',
                         "not replace_multiple when flag is true")
        self.assertEqual(replace_false.__name__, 'replace_single',
                         "not replace_single when flag is false")

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

if __name__ == '__main__':
    unittest.main()

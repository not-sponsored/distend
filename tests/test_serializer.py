# workaround
import sys
sys.path.append('..')

# standard library
import unittest

# internal distend imports
from distend import serializer

class TestSerializer(unittest.TestCase):

    def test_get_multi_rule_returns_fnct(self):
        """test serializer.get_multi_rule returns datatype function"""
        multi_rule = False
        trn_fnct = serializer.get_multi_rule(multi_rule)
        self.assertTrue(callable(trn_fnct), 'return is not callable')

    def test_get_multi_rule_with_multi_rule_true(self):
        """test serializer.get_multi_rule returns multi_transform function"""
        multi_rule = True
        trn_fnct = serializer.get_multi_rule(multi_rule)
        self.assertEqual(trn_fnct.__name__, 'multi_transform',
                         "does not return multi_transform as expected")

    def test_get_multi_rule_with_multi_rule_false(self):
        """test serializer.get_multi_rule returns single_transform function"""
        multi_rule = False
        trn_fnct = serializer.get_multi_rule(multi_rule)
        self.assertEqual(trn_fnct.__name__, 'single_transform',
                         "does not return single_transform as expected")

    def test_get_pends_returns_fnct(self):
        """test serializer.get_pends returns datatype function"""
        pends = ('prepend', 'postpend')
        fuse_fnct = serializer.get_pends(pends[0], pends[1])
        self.assertTrue(callable(fuse_fnct), 'return is not callable')

    def test_get_pends_with_list_pre_list_post(self):
        """test serializer.get_pends returns fuse_lp_lp"""
        pends = (['1972', '1973'], ['1984', '1985'])
        fuse_fnct = serializer.get_pends(pends[0], pends[1])
        self.assertEqual(fuse_fnct.__name__, 'fuse_lp_lp',
                         "expected fuse_lp_lp")

    def test_get_pends_with_list_pre_str_post(self):
        """test serializer.get_pends returns fuse_lp_sp"""
        pends = (['1972', '1973'], '1984')
        fuse_fnct = serializer.get_pends(pends[0], pends[1])
        self.assertEqual(fuse_fnct.__name__, 'fuse_lp_sp',
                         "expected fuse_lp_sp")

    def test_get_pends_with_str_pre_str_post(self):
        """test serializer.get_pends returns fuse_sp_sp"""
        pends = ('1972', '1984')
        fuse_fnct = serializer.get_pends(pends[0], pends[1])
        self.assertEqual(fuse_fnct.__name__, 'fuse_sp_sp',
                         "expected fuse_sp_sp")

    def test_get_pends_with_str_pre_list_post(self):
        """test serializer.get_pends returns fuse_sp_lp"""
        pends = ('1972', ['1984', '1985'])
        fuse_fnct = serializer.get_pends(pends[0], pends[1])
        self.assertEqual(fuse_fnct.__name__, 'fuse_sp_lp',
                         "expected fuse_sp_lp")

    def test_get_pends_with_list_pre_no_post(self):
        """test serializer.get_pends returns fuse_lp_np"""
        pends = (['1972', '1973'], '')
        fuse_fnct = serializer.get_pends(pends[0], pends[1])
        self.assertEqual(fuse_fnct.__name__, 'fuse_lp_np',
                         "expected fuse_lp_np")

    def test_get_pends_with_str_pre_no_post(self):
        """test serializer.get_pends returns fuse_sp_np"""
        pends = ('1972', '')
        fuse_fnct = serializer.get_pends(pends[0], pends[1])
        self.assertEqual(fuse_fnct.__name__, 'fuse_sp_np',
                         "expected fuse_sp_np")

    def test_get_pends_with_no_pre_list_post(self):
        """test serializer.get_pends returns fuse_np_lp"""
        pends = ('', ['1984', '1985'])
        fuse_fnct = serializer.get_pends(pends[0], pends[1])
        self.assertEqual(fuse_fnct.__name__, 'fuse_np_lp',
                         "expected fuse_np_lp")

    def test_get_pends_with_no_pre_str_post(self):
        """test serializer.get_pends returns fuse_np_sp"""
        pends = ('', '1984')
        fuse_fnct = serializer.get_pends(pends[0], pends[1])
        self.assertEqual(fuse_fnct.__name__, 'fuse_np_sp',
                         "expected fuse_np_sp")

    def test_get_pends_with_no_pre_no_post(self):
        """test serializer.get_pends returns none"""
        pends = ('', '')
        fuse_fnct = serializer.get_pends(pends[0], pends[1])
        self.assertIsNone(fuse_fnct, "expected none")

    def test_get_drive_returns_fnct(self):
        """test serializer.get_drive returns datatype function"""
        pends = ('prepend', 'postpend')
        verbose = False
        drive_fnct = serializer.get_drive(verbose, pends[0], pends[1])
        self.assertTrue(callable(drive_fnct), 'return is not callable')

    def test_get_drive_with_str_pre_str_post_verbose_as_true(self):
        """test serializer.get_drive returns verbose_pre_post"""
        pends = ('prepend', 'postpend')
        verbose = True
        drive_fnct = serializer.get_drive(verbose, pends[0], pends[1])
        self.assertEqual(drive_fnct.__name__, 'verbose_pre_post',
                         "expected verbose_pre_post")

    def test_get_drive_with_str_pre_no_post_verbose_as_true(self):
        """test serializer.get_drive returns verbose_single_pend"""
        pends = ('prepend', '')
        verbose = True
        drive_fnct = serializer.get_drive(verbose, pends[0], pends[1])
        self.assertEqual(drive_fnct.__name__, 'verbose_single_pend',
                         "expected verbose_single_pend")

    def test_get_drive_with_no_pre_str_post_verbose_as_true(self):
        """test serializer.get_drive returns verbose_single_pend"""
        pends = ('', 'postpend')
        verbose = True
        drive_fnct = serializer.get_drive(verbose, pends[0], pends[1])
        self.assertEqual(drive_fnct.__name__, 'verbose_single_pend',
                         "expected verbose_single_pend")

    def test_get_drive_with_no_pre_no_post_verbose_as_true(self):
        """test serializer.get_drive returns verbose_no_pend"""
        pends = ('', '')
        verbose = True
        drive_fnct = serializer.get_drive(verbose, pends[0], pends[1])
        self.assertEqual(drive_fnct.__name__, 'verbose_no_pend',
                         "expected verbose_single_pend")

    def test_get_drive_with_str_pre_str_post_verbose_as_false(self):
        """test serializer.get_drive returns verbose_pre_post"""
        pends = ('prepend', 'postpend')
        verbose = False
        drive_fnct = serializer.get_drive(verbose, pends[0], pends[1])
        self.assertEqual(drive_fnct.__name__, 'concise_pre_post',
                         "expected concise_pre_post")

    def test_get_drive_with_str_pre_no_post_verbose_as_true(self):
        """test serializer.get_drive returns concise_single_pend"""
        pends = ('prepend', '')
        verbose = False
        drive_fnct = serializer.get_drive(verbose, pends[0], pends[1])
        self.assertEqual(drive_fnct.__name__, 'concise_single_pend',
                         "expected concise_single_pend")

    def test_get_drive_with_no_pre_str_post_verbose_as_true(self):
        """test serializer.get_drive returns concise_single_pend"""
        pends = ('', 'postpend')
        verbose = False
        drive_fnct = serializer.get_drive(verbose, pends[0], pends[1])
        self.assertEqual(drive_fnct.__name__, 'concise_single_pend',
                         "expected concise_single_pend")

    def test_get_drive_with_no_pre_no_post_verbose_as_true(self):
        """test serializer.get_drive returns concise_single_pend"""
        pends = ('', '')
        verbose = False
        drive_fnct = serializer.get_drive(verbose, pends[0], pends[1])
        self.assertEqual(drive_fnct.__name__, 'concise_no_pend',
                         "expected concise_single_pend")

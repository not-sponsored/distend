# work around
import sys
sys.path.append('..')

# standard library
import unittest
from unittest.mock import patch, mock_open

# distend internal imports
from distend import drive
from distend import modifier

class TestDrive(unittest.TestCase):

    @patch('builtins.print')
    def test_verbose_pre_post(self, mock_print):
        """drive.verbose_pre_post returns list correctly and prints"""
        fncts = (modifier.multi_transform, modifier.fuse_lp_lp,
                 drive.verbose_pre_post)
        fin = (x for x in ['polecat\n'])
        rules = {'a':'4', 'e':'3', 'o':'0'}
        pends = (['1972', '1973'], ['1984', '1985'])
        dupe = 'out.txt'
        with patch('distend.io_utils.append_list') as mock_append:
            fncts[2](fin, fncts, rules, pends, dupe)
            mock_append.assert_called_once_with(['1972polecat', '1973polecat',
            'polecat1984', 'polecat1985', '1972polecat1984', '1972polecat1985',
            '1973polecat1984', '1973polecat1985', '1972p0l3c4t', '1973p0l3c4t',
            'p0l3c4t1984', 'p0l3c4t1985', '1972p0l3c4t1984', '1972p0l3c4t1985',
            '1973p0l3c4t1984', '1973p0l3c4t1985', 'p0l3c4t'], dupe)
        mock_print.assert_called_once_with('currently at [      polecat       ]', end='\r', flush=True)

    def test_concise_pre_post(self):
        """drive.concise_pre_post returns list correctly"""
        fncts = (modifier.multi_transform, modifier.fuse_lp_lp,
                 drive.concise_pre_post)
        fin = (x for x in ['polecat\n'])
        rules = {'a':'4', 'e':'3', 'o':'0'}
        pends = (['1972', '1973'], ['1984', '1985'])
        dupe = 'out.txt'
        with patch('distend.io_utils.append_list') as mock_append:
            fncts[2](fin, fncts, rules, pends, dupe)
            mock_append.assert_called_once_with(['1972polecat', '1973polecat',
            'polecat1984', 'polecat1985', '1972polecat1984', '1972polecat1985',
            '1973polecat1984', '1973polecat1985', '1972p0l3c4t', '1973p0l3c4t',
            'p0l3c4t1984', 'p0l3c4t1985', '1972p0l3c4t1984', '1972p0l3c4t1985',
            '1973p0l3c4t1984', '1973p0l3c4t1985', 'p0l3c4t'], dupe)

    @patch('builtins.print')
    def test_verbose_single_pend(self, mock_print):
        """drive.verbose_single_pend returns list correctly and prints"""
        fncts = (modifier.multi_transform, modifier.fuse_lp_np,
                 drive.verbose_single_pend)
        fin = (x for x in ['polecat\n'])
        rules = {'a':'4', 'e':'3', 'o':'0'}
        pends = (['1972', '1973'], '')
        dupe = 'out.txt'
        with patch('distend.io_utils.append_list') as mock_append:
            fncts[2](fin, fncts, rules, pends, dupe)
            mock_append.assert_called_once_with(['1972polecat', '1972p0l3c4t',
            '1973polecat', '1973p0l3c4t', 'p0l3c4t'], dupe)
        mock_print.assert_called_once_with('currently at [      polecat       ]', end='\r', flush=True)

    def test_concise_single_pend(self):
        """drive.concise_single_pend returns list correctly"""
        fncts = (modifier.multi_transform, modifier.fuse_lp_np,
                 drive.concise_single_pend)
        fin = (x for x in ['polecat\n'])
        rules = {'a':'4', 'e':'3', 'o':'0'}
        pends = (['1972', '1973'], '')
        dupe = 'out.txt'
        with patch('distend.io_utils.append_list') as mock_append:
            fncts[2](fin, fncts, rules, pends, dupe)
            mock_append.assert_called_once_with(['1972polecat', '1972p0l3c4t',
            '1973polecat', '1973p0l3c4t', 'p0l3c4t'], dupe)

    @patch('builtins.print')
    def test_verbose_no_pend(self, mock_print):
        """drive.verbose_no_pend returns list correctly and prints"""
        fncts = (modifier.single_transform, None, drive.verbose_no_pend)
        fin = (x for x in ['polecat\n'])
        rules = {'a':'4', 'e':'3', 'o':'0'}
        pends = ('', '')
        dupe = 'out.txt'
        with patch('distend.io_utils.append_list') as mock_append:
            fncts[2](fin, fncts, rules, pends, dupe)
            mock_append.assert_called_once_with(['polec4t', 'pol3cat',
            'p0lecat', 'p0l3c4t'], dupe)
        mock_print.assert_called_once_with('currently at [      polecat       ]', end='\r', flush=True)

    def test_concise_no_pend(self):
        """drive.concise_no_pend returns list correctly"""
        fncts = (modifier.single_transform, None, drive.concise_no_pend)
        fin = (x for x in ['polecat\n'])
        rules = {'a':'4', 'e':'3', 'o':'0'}
        pends = ('', '')
        dupe = 'out.txt'
        with patch('distend.io_utils.append_list') as mock_append:
            fncts[2](fin, fncts, rules, pends, dupe)
            mock_append.assert_called_once_with(['polec4t', 'pol3cat',
            'p0lecat', 'p0l3c4t'], dupe)

# workaround
import sys
sys.path.append('..')

# standard library
import unittest
from unittest.mock import patch

# internal distend imports
from distend import cli

class TestCli(unittest.TestCase):

    def test_parser_all_options(self):
        """cli.parse_args all options on"""
        options = ['in.txt', 'out.txt', '-c', '-v', '-m', '-r', 'rules.conf']
        args = cli.parser(options)
        self.assertEqual(args.infile, 'in.txt', 'parses infile incorrectly')
        self.assertEqual(args.outfile, 'out.txt', 'parses outfile incorrectly')
        self.assertEqual(args.concatenate, True,
                         'parses concatenate flag incorrectly')
        self.assertEqual(args.verbose, True, 'parses verbose flag incorrectly')
        self.assertEqual(args.multi_rule_only, True,
                         'parses multi_rule_only flag incorrectly')
        self.assertEqual(args.rules_file, 'rules.conf',
                         'parses rules_file incorrectly')

    def test_parser_no_options(self):
        """cli.parse_args no options on"""
        options = ['in.txt', 'out.txt']
        args = cli.parser(options)
        self.assertEqual(args.infile, 'in.txt', 'parses infile incorrectly')
        self.assertEqual(args.outfile, 'out.txt', 'parses outfile incorrectly')
        self.assertEqual(args.concatenate, False, 
                         'parses concatenate flag incorrectly')
        self.assertEqual(args.verbose, False, 'parses verbose flag incorrectly')
        self.assertEqual(args.multi_rule_only, False,
                         'parses multi_rule_only flag incorrectly')
        self.assertEqual(args.rules_file, None, 'parses rules_file incorrectly')

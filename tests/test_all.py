# standard library
import unittest

if __name__ == '__main__':
    test_suite = unittest.TestLoader().discover('.', 'test*.py')
    runner = unittest.TextTestRunner()
    runner.run(test_suite)

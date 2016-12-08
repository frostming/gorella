# -*- coding: utf-8 -*-
import gorella
import unittest
import re


class GorellaTestSuite(unittest.TestCase):
    def test_extension_methods(self):
        self.assertTrue(hasattr(str, 'match'))
        self.assertTrue(hasattr(str, 'search'))
        self.assertTrue(hasattr(str, 'find'))
        self.assertTrue(hasattr(str, 'finditer'))

    def test_replace(self):
        self.assertEqual('hello world'.replace('world', 'bitch'), 'hello bitch')
        pat = re.compile('\d+')
        self.assertEqual('I am 5 years old'.replace(pat, '6'),
                         'I am 6 years old')
        self.assertEqual('I am 5 years old'.replace(
            pat, lambda m: str(int(m.group()) * 2)), 'I am 10 years old')
        self.assertEqual('5 people and 3 apples'.replace(pat, '6', 1),
                         '6 people and 3 apples')

    def test_split(self):
        self.assertEqual('hello world'.split(), ['hello', 'world'])
        self.assertEqual('hello_world'.split('_'), ['hello', 'world'])
        pat = re.compile('[^a-zA-Z]')
        self.assertEqual('I have3apples'.split(pat), ['I', 'have', 'apples'])
        self.assertEqual('I have3apples'.split(pat, 1), ['I', 'have3apples'])

    def test_rsplit(self):
        self.assertEqual('hello world'.rsplit(), ['hello', 'world'])
        self.assertEqual('hello_world'.rsplit('_'), ['hello', 'world'])
        pat = re.compile('[^a-zA-Z]')
        self.assertEqual('I have3apples'.rsplit(pat), ['I', 'have', 'apples'])
        self.assertEqual('I have3apples'.rsplit(pat, 1), ['I have', 'apples'])

    def test_find(self):
        self.assertEqual('hello world'.find('hell'), 0)
        self.assertEqual('hello world'.find('hell', 2, 6), -1)
        self.assertEqual('hello world'.find('heaven'), -1)
        nums = re.compile('\d+')
        spaces = re.compile('\s+')
        self.assertEqual('hello world'.find(nums), -1)
        self.assertEqual('hello world'.find(spaces), 5)
        self.assertEqual('hello world'.find(spaces, 6, 9), -1)

    def test_rfind(self):
        self.assertEqual('I have 3 apples'.rfind(' '), 8)
        self.assertEqual('I have 3 apples'.rfind(' ', 0, 7), 6)
        self.assertEqual('I have 3 apples'.rfind('banana'), -1)
        nums = re.compile('\d+')
        spaces = re.compile('\s+')
        self.assertEqual('I have 3 apples'.rfind(nums), 7)
        self.assertEqual('I have 3 apples'.rfind(nums, 3, 5), -1)
        self.assertEqual('I have 3 apples'.rfind(spaces), 8)
        self.assertEqual('I have 3 apples'.rfind(spaces, 0, 7), 6)

    def test_index(self):
        self.assertEqual('hello world'.index('hell'), 0)
        self.assertRaises(ValueError, 'hello world'.index, 'hell', 2, 6)
        self.assertRaises(ValueError, 'hello world'.index, 'heaven')
        nums = re.compile('\d+')
        spaces = re.compile('\s+')
        self.assertRaises(ValueError, 'hello world'.index, nums)
        self.assertEqual('hello world'.index(spaces), 5)
        self.assertRaises(ValueError, 'hello world'.index, spaces, 6, 9)

    def test_rindex(self):
        self.assertEqual('I have 3 apples'.rindex(' '), 8)
        self.assertEqual('I have 3 apples'.rindex(' ', 0, 7), 6)
        self.assertRaises(ValueError, 'I have 3 apples'.rindex, 'banana')
        nums = re.compile('\d+')
        spaces = re.compile('\s+')
        self.assertEqual('I have 3 apples'.rindex(nums), 7)
        self.assertRaises(ValueError, 'I have 3 apples'.rindex, nums, 3, 5)
        self.assertEqual('I have 3 apples'.rindex(spaces), 8)
        self.assertEqual('I have 3 apples'.rindex(spaces, 0, 7), 6)

    def test_count(self):
        self.assertEqual('I have 3 apples'.count('a'), 2)
        self.assertEqual('I have 3 apples'.count('de'), 0)
        nums = re.compile('\d+')
        self.assertEqual('5 people and 3 apples'.count(nums), 2)
        self.assertEqual('hello world'.count(nums), 0)

    def test_partition(self):
        self.assertEqual('I have 3 apples'.partition('have'),
                         ('I ', 'have', ' 3 apples'))
        self.assertEqual('I have 3 apples'.partition('no'),
                         ('I have 3 apples', '', ''))
        nums = re.compile('\d+')
        self.assertEqual('I have 3 apples'.partition(nums),
                         ('I have ', '3', ' apples'))
        self.assertEqual('I have no apple'.partition(nums),
                         ('I have no apple', '', ''))

    def test_rpartition(self):
        self.assertEqual('I have 3 apples'.rpartition(' '),
                         ('I have 3', ' ', 'apples'))
        self.assertEqual('I have 3 apples'.rpartition('no'),
                         ('', '', 'I have 3 apples'))
        nums = re.compile('\d+')
        self.assertEqual('5 people and 3 apples'.rpartition(nums),
                         ('5 people and ', '3', ' apples'))
        self.assertEqual('I have no apple'.rpartition(nums),
                         ('', '', 'I have no apple'))

    def test_startswith(self):
        self.assertTrue('>>> import gorella'.startswith('>>>'))
        self.assertTrue('>>> import gorella'.startswith(('>', '<')))
        self.assertFalse('>>> import gorella'.startswith('<<<'))
        prefix = re.compile('[><]')
        self.assertTrue('>>> import gorella'.startswith(prefix))
        self.assertFalse('import gorella'.startswith(prefix))
        self.assertTrue('>>> import gorella'.startswith((prefix, ' ')))

    def test_endswith(self):
        self.assertTrue("What's your name?".endswith('?'))
        self.assertFalse("What's your name?".endswith('!'))
        self.assertTrue("What's your name?".endswith(('?', '!')))
        suffix = re.compile(r'[?!\.,:;]')
        self.assertTrue("What's your name?".endswith(suffix))
        self.assertFalse("What's your name".endswith(suffix))
        self.assertTrue("What's your name".endswith((suffix, 'e')))


if __name__ == '__main__':
    unittest.main()

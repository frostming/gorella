# -*- coding: utf-8 -*-
import gorella
import unittest
import re


class GorellaTestSuite(unittest.TestCase):
    def test_extension_methods(self):
        self.assertTrue(hasattr(unicode, u'match'))
        self.assertTrue(hasattr(unicode, u'search'))
        self.assertTrue(hasattr(unicode, u'find'))
        self.assertTrue(hasattr(unicode, u'finditer'))

    def test_replace(self):
        self.assertEqual(u'hello world'.replace(u'world', u'bitch'), u'hello bitch')
        pat = re.compile(u'\d+')
        self.assertEqual(u'I am 5 years old'.replace(pat, u'6'),
                         u'I am 6 years old')
        self.assertEqual(u'I am 5 years old'.replace(
            pat, lambda m: unicode(int(m.group()) * 2)), u'I am 10 years old')
        self.assertEqual(u'5 people and 3 apples'.replace(pat, u'6', 1),
                         u'6 people and 3 apples')

    def test_split(self):
        self.assertEqual(u'hello world'.split(), [u'hello', u'world'])
        self.assertEqual(u'hello_world'.split(u'_'), [u'hello', u'world'])
        pat = re.compile(u'[^a-zA-Z]')
        self.assertEqual(u'I have3apples'.split(pat), [u'I', u'have', u'apples'])
        self.assertEqual(u'I have3apples'.split(pat, 1), [u'I', u'have3apples'])

    def test_rsplit(self):
        self.assertEqual(u'hello world'.rsplit(), [u'hello', u'world'])
        self.assertEqual(u'hello_world'.rsplit(u'_'), [u'hello', u'world'])
        pat = re.compile(u'[^a-zA-Z]')
        self.assertEqual(u'I have3apples'.rsplit(pat), [u'I', u'have', u'apples'])
        self.assertEqual(u'I have3apples'.rsplit(pat, 1), [u'I have', u'apples'])

    def test_find(self):
        self.assertEqual(u'hello world'.find(u'hell'), 0)
        self.assertEqual(u'hello world'.find(u'hell', 2, 6), -1)
        self.assertEqual(u'hello world'.find(u'heaven'), -1)
        nums = re.compile(u'\d+')
        spaces = re.compile(u'\s+')
        self.assertEqual(u'hello world'.find(nums), -1)
        self.assertEqual(u'hello world'.find(spaces), 5)
        self.assertEqual(u'hello world'.find(spaces, 6, 9), -1)

    def test_rfind(self):
        self.assertEqual(u'I have 3 apples'.rfind(u' '), 8)
        self.assertEqual(u'I have 3 apples'.rfind(u' ', 0, 7), 6)
        self.assertEqual(u'I have 3 apples'.rfind(u'banana'), -1)
        nums = re.compile(u'\d+')
        spaces = re.compile(u'\s+')
        self.assertEqual(u'I have 3 apples'.rfind(nums), 7)
        self.assertEqual(u'I have 3 apples'.rfind(nums, 3, 5), -1)
        self.assertEqual(u'I have 3 apples'.rfind(spaces), 8)
        self.assertEqual(u'I have 3 apples'.rfind(spaces, 0, 7), 6)

    def test_index(self):
        self.assertEqual(u'hello world'.index(u'hell'), 0)
        self.assertRaises(ValueError, u'hello world'.index, u'hell', 2, 6)
        self.assertRaises(ValueError, u'hello world'.index, u'heaven')
        nums = re.compile(u'\d+')
        spaces = re.compile(u'\s+')
        self.assertRaises(ValueError, u'hello world'.index, nums)
        self.assertEqual(u'hello world'.index(spaces), 5)
        self.assertRaises(ValueError, u'hello world'.index, spaces, 6, 9)

    def test_rindex(self):
        self.assertEqual(u'I have 3 apples'.rindex(u' '), 8)
        self.assertEqual(u'I have 3 apples'.rindex(u' ', 0, 7), 6)
        self.assertRaises(ValueError, u'I have 3 apples'.rindex, u'banana')
        nums = re.compile(u'\d+')
        spaces = re.compile(u'\s+')
        self.assertEqual(u'I have 3 apples'.rindex(nums), 7)
        self.assertRaises(ValueError, u'I have 3 apples'.rindex, nums, 3, 5)
        self.assertEqual(u'I have 3 apples'.rindex(spaces), 8)
        self.assertEqual(u'I have 3 apples'.rindex(spaces, 0, 7), 6)

    def test_count(self):
        self.assertEqual(u'I have 3 apples'.count(u'a'), 2)
        self.assertEqual(u'I have 3 apples'.count(u'de'), 0)
        nums = re.compile(u'\d+')
        self.assertEqual(u'5 people and 3 apples'.count(nums), 2)
        self.assertEqual(u'hello world'.count(nums), 0)

    def test_partition(self):
        self.assertEqual(u'I have 3 apples'.partition(u'have'),
                         (u'I ', u'have', u' 3 apples'))
        self.assertEqual(u'I have 3 apples'.partition(u'no'),
                         (u'I have 3 apples', u'', u''))
        nums = re.compile(u'\d+')
        self.assertEqual(u'I have 3 apples'.partition(nums),
                         (u'I have ', u'3', u' apples'))
        self.assertEqual(u'I have no apple'.partition(nums),
                         (u'I have no apple', u'', u''))

    def test_rpartition(self):
        self.assertEqual(u'I have 3 apples'.rpartition(u' '),
                         (u'I have 3', u' ', u'apples'))
        self.assertEqual(u'I have 3 apples'.rpartition(u'no'),
                         (u'', u'', u'I have 3 apples'))
        nums = re.compile(u'\d+')
        self.assertEqual(u'5 people and 3 apples'.rpartition(nums),
                         (u'5 people and ', u'3', u' apples'))
        self.assertEqual(u'I have no apple'.rpartition(nums),
                         (u'', u'', u'I have no apple'))

    def test_startswith(self):
        self.assertTrue(u'>>> import gorella'.startswith(u'>>>'))
        self.assertTrue(u'>>> import gorella'.startswith((u'>', u'<')))
        self.assertFalse(u'>>> import gorella'.startswith(u'<<<'))
        prefix = re.compile(u'[><]')
        self.assertTrue(u'>>> import gorella'.startswith(prefix))
        self.assertFalse(u'import gorella'.startswith(prefix))
        self.assertTrue(u'>>> import gorella'.startswith((prefix, u' ')))

    def test_endswith(self):
        self.assertTrue(u"What's your name?".endswith(u'?'))
        self.assertFalse(u"What's your name?".endswith(u'!'))
        self.assertTrue(u"What's your name?".endswith((u'?', u'!')))
        suffix = re.compile(r'[?!\.,:;]')
        self.assertTrue(u"What's your name?".endswith(suffix))
        self.assertFalse(u"What's your name".endswith(suffix))
        self.assertTrue(u"What's your name".endswith((suffix, u'e')))


if __name__ == '__main__':
    unittest.main()

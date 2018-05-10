# -*- coding: utf-8 -*-


import unittest

from aspwrapper import answer_set
from aspwrapper import literal


__author__ = "Patrick Hohenecker"
__copyright__ = (
        "Copyright (c) 2018 Patrick Hohenecker\n"
        "\n"
        "Permission is hereby granted, free of charge, to any person obtaining a copy\n"
        "of this software and associated documentation files (the \"Software\"), to deal\n"
        "in the Software without restriction, including without limitation the rights\n"
        "to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n"
        "copies of the Software, and to permit persons to whom the Software is\n"
        "furnished to do so, subject to the following conditions:\n"
        "\n"
        "The above copyright notice and this permission notice shall be included in all\n"
        "copies or substantial portions of the Software.\n"
        "\n"
        "THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n"
        "IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n"
        "FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n"
        "AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n"
        "LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n"
        "OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n"
        "SOFTWARE."
)
__license__ = "MIT License"
__version__ = "2018.1"
__date__ = "May 10, 2018"
__maintainer__ = "Patrick Hohenecker"
__email__ = "mail@paho.at"
__status__ = "Development"


class AnswerSetTest(unittest.TestCase):
    
    def test_eq(self):
        # CHECK: equality checks work as expected
        self.assertTrue(
                answer_set.AnswerSet([literal.Literal("fact-1"), literal.Literal("fact-2")], []) ==
                answer_set.AnswerSet([literal.Literal("fact-2"), literal.Literal("fact-1")], [])
        )
        self.assertFalse(
                answer_set.AnswerSet([literal.Literal("fact-1")], [literal.Literal("fact-2")]) ==
                answer_set.AnswerSet([literal.Literal("fact-2")], [literal.Literal("fact-1")])
        )
    
    def test_init(self):
        # CHECK: facts has to be an iterable of literals -> otherwise a TypeError is raised
        with self.assertRaises(TypeError):
            answer_set.AnswerSet("facts", [])
            answer_set.AnswerSet(literal.Literal("fact"), [])
        with self.assertRaises(TypeError):
            answer_set.AnswerSet(["fact"], [])
        with self.assertRaises(TypeError):
            answer_set.AnswerSet((literal.Literal("test"), "fact"), [])

        # CHECK: inferences has to be an iterable of literals -> otherwise a TypeError is raised
        with self.assertRaises(TypeError):
            answer_set.AnswerSet([], "facts")
            answer_set.AnswerSet([], literal.Literal("fact"))
        with self.assertRaises(TypeError):
            answer_set.AnswerSet([], ["fact"])
        with self.assertRaises(TypeError):
            answer_set.AnswerSet([], (literal.Literal("test"), "fact"))
        
        # CHECK: providing legal values causes no issues
        answer_set.AnswerSet([], [])
        answer_set.AnswerSet([literal.Literal("fact-1")], [])
        answer_set.AnswerSet({literal.Literal("fact-1"), literal.Literal("fact-2")}, [])
        answer_set.AnswerSet([], [literal.Literal("fact-1")])
        answer_set.AnswerSet([], (literal.Literal("fact-1"), literal.Literal("fact-2")))
        answer_set.AnswerSet([literal.Literal("fact-1")], [literal.Literal("fact-2")])
        
        # CHECK: attributes are defined correctly
        ans = answer_set.AnswerSet(
                [literal.Literal("fact-1"), literal.Literal("fact-2")],
                (literal.Literal("fact-3"), literal.Literal("fact-4"), literal.Literal("fact-5"))
        )
        self.assertEqual(
                {literal.Literal("fact-1"), literal.Literal("fact-2")},
                ans.facts
        )
        self.assertEqual(
                {literal.Literal("fact-3"), literal.Literal("fact-4"), literal.Literal("fact-5")},
                ans.inferences
        )
    
    def test_iter(self):
        # CHECK: iterating over an answer sets covers all facts and inferences
        ans = answer_set.AnswerSet(
                [literal.Literal("fact-1"), literal.Literal("fact-2")],
                [literal.Literal("fact-3")]
        )
        self.assertEqual(
                {literal.Literal("fact-1"), literal.Literal("fact-2"), literal.Literal("fact-3")},
                set(ans)
        )

# -*- coding: utf-8 -*-


import unittest

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


class LiteralTest(unittest.TestCase):
    
    def test_eq(self):
        # CHECK: equality checks work as expected
        self.assertTrue(literal.Literal("person", ["patrick"]) == literal.Literal("person", ["patrick"]))
        self.assertTrue(literal.Literal("person", positive=False) == literal.Literal("person", positive=False))
        self.assertFalse(literal.Literal("person", ["patrick"]) == literal.Literal("person"))
        self.assertFalse(literal.Literal("person", positive=False) == literal.Literal("person", positive=True))
    
    def test_init(self):
        # CHECK: the predicate symbol must not be the empty string
        with self.assertRaises(ValueError):
            literal.Literal("")
        
        # CHECK: none of the terms can be the empty string
        with self.assertRaises(ValueError):
            literal.Literal("pred", [""])
        with self.assertRaises(ValueError):
            literal.Literal("pred", ["abc", "def", "", "jkl"])
        
        # CHECK: legal args do not cause any issues
        literal.Literal("person")
        literal.Literal("person", [], positive=False)
        literal.Literal("person", ["patrick"])
        literal.Literal(1)     # -> translated to "1"
        literal.Literal(None)  # -> translated to "None"
        
        # CHECK: attributes are created correctly
        lit = literal.Literal("pred", ["a", "b", "c"], positive=False)
        self.assertEqual("pred", lit.predicate)
        self.assertEqual(("a", "b", "c"), lit.terms)
        self.assertFalse(lit.positive)

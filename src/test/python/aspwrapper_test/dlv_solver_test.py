# -*- coding: utf-8 -*-


import unittest

import aspwrapper_test

from aspwrapper import answer_set
from aspwrapper import dlv_solver
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


class DlvSolverTest(unittest.TestCase):
    
    def setUp(self):
        self.ontology = aspwrapper_test.ONTOLOGY
        self.solver = dlv_solver.DlvSolver(aspwrapper_test.DLV_PATH)
    
    def test_init(self):
        # CHECK: providing an illegal path causes a ValueError
        with self.assertRaises(ValueError):
            dlv_solver.DlvSolver("/not/a/valid/path")
        with self.assertRaises(ValueError):
            dlv_solver.DlvSolver(None)

        # CHECK: providing legal args causes no problems whatsoever
        dlv_solver.DlvSolver(aspwrapper_test.DLV_PATH)

    def test_run(self):
        # CHECK: providing a non-existing ontology path causes a ValueError
        with self.assertRaises(ValueError):
            self.solver.run("/not/a/valid/path", [])
        with self.assertRaises(ValueError):
            self.solver.run(None, [])
        
        # CHECK: providing a non-iterable as facts causes a TypeError
        with self.assertRaises(TypeError):
            self.solver.run(self.ontology, "no facts")
        with self.assertRaises(TypeError):
            self.solver.run(self.ontology, None)
        with self.assertRaises(TypeError):
            self.solver.run(self.ontology, 123)
        
        # CHECK: if facts contains instances of a type other than Literal, then a TypeError is raised
        with self.assertRaises(TypeError):
            self.solver.run(self.ontology, [literal.Literal("person", ["patrick"]), 0])
        with self.assertRaises(TypeError):
            self.solver.run(self.ontology, [None, literal.Literal("person", ["patrick"])])
        
        # CHECK: correct invocations of run do not causes any issues
        self.solver.run(self.ontology, [])
        self.solver.run(self.ontology, (literal.Literal("person", ["patrick"]), literal.Literal("hero", ["patrick"])))
    
    def test_run_multiple_answer_sets(self):
        facts = [literal.Literal("person", ["patrick"])]
        target_1 = answer_set.AnswerSet(facts, [literal.Literal("hero", ["patrick"])])
        target_2 = answer_set.AnswerSet(facts, [literal.Literal("hero", ["patrick"], positive=False)])
        result = self.solver.run(self.ontology, facts)
        self.assertEqual(2, len(result))
        self.assertTrue(
                (target_1 == result[0] and target_2 == result[1]) or
                (target_1 == result[1] and target_2 == result[0])
        )

    def test_run_no_answer_sets(self):
        facts = [
                literal.Literal("person", ["patrick"]),
                literal.Literal("person", ["patrick"], positive=False)
        ]
        result = self.solver.run(self.ontology, facts)
        self.assertEqual([], result)

    def test_run_single_answer_sets(self):
        facts = [literal.Literal("hero", ["patrick"])]
        target = answer_set.AnswerSet(facts, [literal.Literal("person", ["patrick"])])
        result = self.solver.run(self.ontology, facts)
        self.assertEqual(1, len(result))
        self.assertEqual(target, result[0])
    
    def test_sanitize_literals(self):
        # CHECK: illegal predicate of term symbols cause a ValueError
        with self.assertRaises(ValueError):
            self.solver._sanitize_literals([literal.Literal("Person", ["patrick"])])
        with self.assertRaises(ValueError):
            self.solver._sanitize_literals([literal.Literal("1person", ["patrick"])])
        with self.assertRaises(ValueError):
            self.solver._sanitize_literals([literal.Literal("per-son", ["patrick"])])
        with self.assertRaises(ValueError):
            self.solver._sanitize_literals([literal.Literal("_person", ["patrick"])])
        with self.assertRaises(ValueError):
            self.solver._sanitize_literals([literal.Literal("person", ["Patrick"])])
        with self.assertRaises(ValueError):
            self.solver._sanitize_literals([literal.Literal("person", ["1patrick"])])
        with self.assertRaises(ValueError):
            self.solver._sanitize_literals([literal.Literal("person", ["pat-rick"])])
        with self.assertRaises(ValueError):
            self.solver._sanitize_literals([literal.Literal("person", ["_patrick"])])
        with self.assertRaises(ValueError):
            self.solver._sanitize_literals([literal.Literal("person", ["patrick", "Patrick"])])
        
        # CHECK: legal literals do not cause any issues
        self.solver._sanitize_literals([literal.Literal("person", ["patrick"])])
        self.solver._sanitize_literals([literal.Literal("person1", ["patrick1"])])
        self.solver._sanitize_literals([literal.Literal("per_son", ["pat_rick"])])
        self.solver._sanitize_literals([literal.Literal("personPerson", ["patrickPatrick"])])

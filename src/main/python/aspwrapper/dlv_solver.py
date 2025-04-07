# -*- coding: utf-8 -*-


import collections
import os
import re
import subprocess
import typing

import insanity

from aspwrapper import answer_set
from aspwrapper import base_solver
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
__date__ = "May 09, 2018"
__maintainer__ = "Patrick Hohenecker"
__email__ = "mail@paho.at"
__status__ = "Development"


class DlvSolver(base_solver.BaseSolver):
    """A wrapper class for the DLV system."""
    
    LITERAL_PATTERN = r"^(?P<sign>[-~]?)(?P<predicate>.+)\((?P<terms>.+)\)$"
    """str: A regular expression for parsing literals provided by DLV."""

    PREDICATE_PATTERN = "^[a-z][a-zA-Z0-9_]*$"
    """str: A regular expression that describes legal predicate symbols."""

    TERM_PATTERN = PREDICATE_PATTERN
    """str: A regular expression that describes legal terms."""
    
    #  CONSTRUCTOR  ####################################################################################################
    
    def __init__(self, dlv_path: str):
        """Creates a new instance of ``DlvSolver``.

        Args:
            dlv_path (str): The path to the DLV executable.
        """
        dlv_path = str(dlv_path)
        if not os.path.isfile(dlv_path):
            raise ValueError("The provided <dlv_path> does not refer to an existing file: '{}'".format(dlv_path))
        
        # if the provided path is relative, then prefix it with "./"
        # otherwise, relative paths in the same directory (i.e., just filenames) cause errors on invoking DLV
        if not os.path.isabs(dlv_path):
            dlv_path = os.path.join(".", dlv_path)

        self._dlv_path = dlv_path
    
    #  METHODS  ########################################################################################################
    
    def _sanitize_literals(self, literals: typing.Iterable[literal.Literal]) -> None:
        """Examines the predicate and term symbols that appear in any of the provided literals.
        
        This function ensures that all of the used literals comply with syntax that is used by the DLV system.
        
        Args:
            literals (iterable[:class:`literal.Literal`): The literals to check.
        
        Raises:
            ValueError: If any illegal predicate or term symbols is encountered.
        """
        for l in literals:  # iterate over all of the provided literals
            
            # sanitize the predicate symbol
            if not re.match(self.PREDICATE_PATTERN, l.predicate):
                raise ValueError("Encountered an illegal predicate symbol: '{}'".format(l.predicate))
            
            # sanitize the literal's terms
            for t in l.terms:
                if not re.match(self.TERM_PATTERN, t):
                    raise ValueError("Encountered an illegal term: '{}'".format(t))
    
    def run(self, path: str, facts: typing.Iterable[literal.Literal]) -> typing.List[answer_set.AnswerSet]:
        # sanitize args
        path = str(path)
        if not os.path.isfile(path):
            raise ValueError("The provided <path> does not refer to an existing file: '{}'!".format(path))
        insanity.sanitize_type("facts", facts, collections.Iterable)
        facts = set(facts)
        insanity.sanitize_iterable("facts", facts, elements_type=literal.Literal)
        self._sanitize_literals(facts)
        
        # prepare list of facts to pass into temporary file
        if len(facts) == 0:
            str_facts = ""
        else:
            str_facts = [str(f) + '.' for f in facts if f]
            
        # create a temporary file combining facts with the mapping
        temp_file = os.path.join(input_dir, "temp.asp")
        with open(temp_file, "w") as f:
            for x in str_facts:
                f.write(x + "\n")
            f.write("\n")
            with open(path, "r") as mapping:
                f.write(mapping.read())
        f.close()
        
        
        # run DLV
        cmd = "{} {} --silent".format(
                self._dlv_path,
                temp_file
        )
        result = str(subprocess.check_output(cmd, shell=True, universal_newlines=True)).strip()
        
        # delete the temp file
        os.remove(temp_file)
        
        # check if any answer set has been provided at all
        if result == "":
            return []
        
        # split result into parts representing single answer sets
        result = [r.strip()[1:-1] for r in result.split("\n")]
        
        # create answer sets
        result_sets = []
        for r in result:  # iterate over all answer sets (i.e., string representations of them)
            
            # collect inferences
            inferences = set()
            if r != "":
                for x in r.split(", "):
                    m = re.match(self.LITERAL_PATTERN, x)
                    lit = literal.Literal(
                            m.group("predicate"),
                            m.group("terms").split(","),
                            positive=m.group("sign") == ""
                    )
                    if lit not in facts:
                        inferences.add(lit)

            # create answer set
            result_sets.append(answer_set.AnswerSet(facts, inferences))
        
        return result_sets

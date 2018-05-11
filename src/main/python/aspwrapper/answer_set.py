# -*- coding: utf-8 -*-


import collections
import itertools
import typing

import insanity

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


class AnswerSet(object):
    """Instances of this class represent single answer sets."""
    
    def __init__(self, facts: typing.Iterable[literal.Literal], inferences: typing.Iterable[literal.Literal]):
        """Creates a new instance of ``AnswerSet``.

        Args:
            facts (list[:class:`literal.Literal`]): The facts contained in the answer set.
            inferences (list[:class:`literal.Literal`]): The inferences contained in the answer set.

        Raises:
            TypeError: If any of ``facts`` and ``inferences`` is not an ``Iterable`` of instances of type
                :class:`literal.Literal`.
        """
        # sanitize args
        insanity.sanitize_type("facts", facts, collections.Iterable)
        facts = set(facts)
        insanity.sanitize_iterable("facts", facts, elements_type=literal.Literal)
        insanity.sanitize_type("inferences", inferences, collections.Iterable)
        inferences = set(inferences)
        insanity.sanitize_iterable("inferences", inferences, elements_type=literal.Literal)
        
        # define attributes
        self._facts = facts
        self._inferences = inferences
    
    #  MAGIC FUNCTIONS  ################################################################################################
    
    def __eq__(self, other) -> bool:
        return (
                isinstance(other, AnswerSet) and
                other.facts == self._facts and
                other.inferences == self._inferences
        )
    
    def __iter__(self) -> typing.Iterator[literal.Literal]:
        return itertools.chain(self._facts, self._inferences)
    
    def __str__(self) -> str:
        return "AnswerSet(\n\tfacts      = {{ {} }},\n\tinferences = {{ {} }}\n)".format(
                ", ".join((str(f) for f in self._facts)),
                ", ".join((str(i) for i in self._inferences))
        )
    
    #  PROPERTIES  #####################################################################################################
    
    @property
    def facts(self) -> typing.Set[literal.Literal]:
        """set[:class:`literal.Literal`]: The facts contained in the answer set."""
        return self._facts
    
    @property
    def inferences(self) -> typing.Set[literal.Literal]:
        """set[:class:`literal.Literal`]: The inferences contained in the answer set."""
        return self._inferences

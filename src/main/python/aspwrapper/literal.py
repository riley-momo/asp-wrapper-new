# -*- coding: utf-8 -*-


import collections
import re
import typing


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


class Literal(object):
    """Instances of this class represent single literals."""
    
    #  CONSTRUCTORS  ###################################################################################################
    
    def __init__(self, predicate: str, terms: typing.Iterable[str] = None, positive: bool = True):
        """Creates a new instance of ``Literal``.

        An example of a positive literal is ``country(austria)``, and a negative one is ``~locatedIn(germany, africa)``.
        The predicates that appear in these literals are ``country`` and ``locatedIn``, respectively, and the terms are
        ``austria`` in the former example and both ``germany`` and ``africa`` in the latter.

        Args:
            predicate (str): The predicate symbol that appears in the literal.
            terms (iterable[str], optional): The terms that appear in the literal in the order that they can be iterated
                over.
            positive (bool, optional): Indicates whether the literal is positive or negative, i.e., an atom or a negated
                atom. By default, this parameters is ``True``.

        Raises:
            TypeError: If ``terms``, given that it has been provided, is not iterable.
            ValueError: If ``predicate`` or any element in ``terms`` is the empty string.
        """
        # sanitize args
        predicate = str(predicate)
        if len(predicate) == 0:
            raise ValueError("The parameter <predicate> must not be the empty string!")
        if terms is not None:
            if not isinstance(terms, collections.Iterable):
                raise TypeError("The parameter <terms> has to be iterable!")
            terms = tuple(str(t) for t in terms)
            for t in terms:
                if len(t) == 0:
                    raise ValueError("None of the terms can be the empty string!")
        else:
            terms = tuple()
        positive = bool(positive)
        
        # define attributes
        self._positive = positive
        self._predicate = predicate
        self._terms = terms
    
    #  MAGIC FUNCTIONS  ################################################################################################
    
    def __eq__(self, other) -> bool:
        return isinstance(other, Literal) and str(other) == str(self)
    
    def __hash__(self) -> int:
        return hash(str(self))
    
    def __str__(self) -> str:
        return "{}{}({})".format(
                "" if self._positive else "~",
                self._predicate,
                ",".join(self._terms)
        )
    
    #  PROPERTIES  #####################################################################################################
    
    @property
    def positive(self) -> bool:
        """bool: Indicates whether the literal is a positive one."""
        return self._positive
    
    @property
    def predicate(self) -> str:
        """str: The predicate symbol that appears in the literal."""
        return self._predicate
    
    @property
    def terms(self) -> typing.Tuple[str]:
        """tuple: The terms that appear in the literal."""
        return self._terms


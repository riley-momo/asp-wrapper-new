# -*- coding: utf-8 -*-


import abc
import typing

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
__date__ = "May 09, 2018"
__maintainer__ = "Patrick Hohenecker"
__email__ = "mail@paho.at"
__status__ = "Development"


class BaseSolver(metaclass=abc.ABCMeta):
    """An abstract base class for wrappers that provide access to ASP solvers."""
    
    @abc.abstractmethod
    def run(self, path, facts: typing.Iterable[literal.Literal]) -> typing.List[answer_set.AnswerSet]:
        """Runs the ASP program at the provided path, and provides the created answer set.

        Args:
            path (str): The path of the ASP program to run.
            facts (iterable[:class:`literal.Literal`]): The facts to provide to the solver in addition to the ASP
                program.

        Returns:
            :class:`answer_set.AnswerSet`: The created answer set.

        Raises:
            CalledProcessError: If the invoked ASP solver raises any error.
            TypeError: If ``facts`` is not an ``Iterable`` of instances of type :class:`literal.Literal`.
            ValueError: If ``path`` does not refer to an existing path.
        """


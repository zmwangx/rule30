#!/usr/bin/env python3

import bitarray

from . import visualize

class Automaton(object):
    """
    An elementary cellular automaton with an initial state of a single 1.

    The number of rows, `rows`, is given at class instantiation, and the
    automaton is only simulated to that depth. Horizontally, we only
    keep the states of the 2 * `rows` - 1 cells centered around the
    initial 1.

    One can access the history matrix via `matrix` or as a numpy array
    via `nparray`, or as a printable string via `string`, or as an image
    via `image`.

    Parameters
    ----------
    rows : int
    rule : int, optional
        The Wolfram code for the rule (in the range [0, 255]). See
        `Wolfram code <https://en.wikipedia.org/wiki/Wolfram_code>`_ on
        Wikipedia. Default is 30.

    """

    def __init__(self, rows, rule=30):
        if rows <= 0:
            raise ValueError("The number of rows should be positive.")
        self._rows = rows
        self._columns = rows * 2 - 1

        if not 0 <= rule <= 255:
            raise ValueError("The rule should be an integer in the range 0-255.")
        self._rule = rule
        # Unpack rule
        u = [bit == '1' for bit in reversed('{:08b}'.format(rule))]
        # Wolfram code is big-endian in terms of the bit position of
        # each of the 2^3=8 configurations (just like how we write
        # numbers in a left-to-right system); we map the ruleset to
        # little-endian form, so that, for instance, the rule for 110 is
        # stored in 0b011.
        self._rule_unpacked = [
            u[0b000],  # 000
            u[0b100],  # 001
            u[0b010],  # 010
            u[0b110],  # 011
            u[0b001],  # 100
            u[0b101],  # 101
            u[0b011],  # 110
            u[0b111],  # 111
        ]

        self._matrix = []
        self._generate()

    def __str__(self):
        return self.string()

    @property
    def rows(self):
        """Number of rows in the history matrix.

        Returns
        -------
        int

        """
        return self._rows

    @property
    def columns(self):
        """Number of columns in the history matrix.

        Always equals 2 * `rows` - 1.

        Returns
        -------
        int

        """
        return self._columns

    @property
    def rule(self):
        """Wolfram code for the rule.

        Returns
        -------
        int

        """
        return self._rule

    @property
    def matrix(self):
        """The history matrix.

        This is a list of `rows` rows, where each row is a bitarray of
        length `columns`. See `bitarray's reference
        <https://pypi.python.org/pypi/bitarray>`_ for more details.

        This is the internal representation of the `Automaton` class.

        Returns
        -------
        List[bitarray]

        """
        return self._matrix

    def string(self, zero='0', one='1'):
        """Returns a printable string representation of the matrix.

        Parameters
        ----------
        zero : str, optional
            The character to print for a cell of value 0. Default is '0'.
        one : str, optional
            The character to print for a cell of value 1. Default is '1'.

        Returns
        -------
        str

        Examples
        --------
        >>> import rule30
        >>> print(rule30.Automaton(5, rule=30).string())
        000010000
        000111000
        001100100
        011011110
        110010001

        """
        return '\n'.join([''.join([one if bit else zero for bit in row])
                          for row in self._matrix])

    def nparray(self):
        """Returns the matrix as a numpy array of dtype bool.

        Requires numpy.

        Returns
        -------
        numpy.ndarray

        """
        import numpy
        rows = self._rows
        columns = self._columns
        matrix = self._matrix
        array = numpy.ndarray((rows, columns), dtype=bool)
        for i in range(rows):
            buf = matrix[i].unpack(zero=b'\x00', one=b'\x01')
            array[i] = numpy.frombuffer(buf, dtype=bool)
        return array

    def image(self, block_size=1):
        """Returns an image for the matrix.

        Parameters
        ----------
        block_size : int, optional
            Size in pixels of each cell (drawn as a square). Default is 1.

        Returns
        -------
        PIL.Image.Image

        """
        return visualize.image_from_matrix(self._matrix, block_size=block_size)

    @staticmethod
    def _zeros(length):
        # Returns a zeroed little-endian bitarray of specified length
        buf = bitarray.bitarray(length, endian='little')
        buf.setall(0)
        return buf

    def _generate(self):
        if self.rule % 2 == 0:
            self._generate_even()
        else:
            self._generate_odd()

    def _generate_even(self):
        rows = self._rows
        columns = self._columns
        rule_unpacked = self._rule_unpacked

        # Initial state, with a single 1 in the middle
        row = self._zeros(columns)
        row[rows-1] = 1
        self._matrix.append(row)

        # Evolution
        for i in range(1, rows):
            lastrow = row
            row = self._zeros(columns)
            for j in range(max(rows-i-1, 1), max(rows+i, columns-1)):
                row[j] = rule_unpacked[int.from_bytes(lastrow[j-1:j+2].tobytes(), 'little')]

            # The left and right endpoints of the last row need special
            # attention because we don't have all three neighbors from
            # the previous row.
            if i == rows - 1:
                row[0] = rule_unpacked[lastrow[0] * 2 + lastrow[1] * 4]
                row[columns-1] = rule_unpacked[lastrow[columns-2] + lastrow[columns-1] * 2]

            self._matrix.append(row)

    def _generate_odd(self):
        rows = self._rows
        columns = self._columns
        rule_unpacked = self._rule_unpacked

        # In order to compute the states of the middle (2n-1) cells on
        # the n-th row, we need to start from the states of the middle
        # (4n-3) cells on the first row, and step by step compute the
        # middle (4n-3-2i) cells on the (i+1)-th row.

        # Initial state, with a single 1 in the middle
        row = self._zeros(4 * rows - 3)
        row[2*rows-2] = 1
        self._matrix.append(row[rows-1:rows-1+columns])

        # Evolution
        for i in range(1, rows):
            lastrow = row
            columns_to_compute = 4 * rows - 3 - 2 * i
            row = self._zeros(columns_to_compute)
            for j in range(columns_to_compute):
                row[j] = rule_unpacked[int.from_bytes(lastrow[j:j+3].tobytes(), 'little')]

            self._matrix.append(row[rows-1-i:rows-1-i+columns])

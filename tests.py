import unittest
from unittest import TestCase

from compound_interest import getFile, getPrincipal, getMonths


class TestFileInput(TestCase):

    def test_no_input_file(self):
        import sys
        sys.argv = []
        self.assertRaises(SystemExit, getFile)

    def test_no_csv_format(self):
        import sys
        values = ['asdf', '', 'file.exe', 'csv']
        for value in values:
            sys.argv = ['', value]
            self.assertRaises(SystemExit, getFile)

    def test_correct_file_input(self):
        import sys
        values = ['file.csv', '.csv']
        for value in values:
            sys.argv = ['', value]
            file = getFile()
            self.assertEqual(file, value)


class TestBorrowInput(TestCase):

    def test_no_input_borrow(self):
        import sys
        sys.argv = ['', 'csv']
        self.assertRaises(SystemExit, getPrincipal)

    def test_no_digit_input(self):
        import sys
        sys.argv = ['', 'csv', 'asdf']
        self.assertRaises(SystemExit, getPrincipal)

    def test_0_input(self):
        import sys
        sys.argv = ['', 'csv', '0']
        self.assertRaises(SystemExit, getPrincipal)

    def test_not_divisible_100(self):
        import sys
        values = ['1', '13', '1222']
        for value in values:
            sys.argv = ['', 'csv', value]
            self.assertRaises(SystemExit, getPrincipal)

    def test_borrow_more_than_15000(self):
        import sys
        sys.argv = ['1000000']
        self.assertRaises(SystemExit, getPrincipal)

    def test_correct_borrow_input(self):
        import sys
        values = ['100', '1500', '1100']
        for value in values:
            sys.argv = ['', 'csv', value]
            borrowing = getPrincipal()
            self.assertEqual(borrowing, float(value))


class TestMonthsInput(TestCase):

    def test_no_month_input(self):
        import sys
        sys.argv = ['', 'csv', 'borrowing']
        month = getMonths()
        self.assertEqual(month, 12)

    def test_no_digit_input(self):
        import sys
        sys.argv = ['', 'csv', 'borrowing', 'asdf']
        self.assertRaises(SystemExit, getMonths)

    def test_negative_or_0_or_decimal_input(self):
        import sys
        values = ['-12', '0.5', '0']
        for value in values:
            sys.argv = ['', 'csv', 'asdf', value]
            self.assertRaises(SystemExit, getMonths)

    def test_correct_month_input(self):
        import sys
        sys.argv = ['', 'csv', 'asdf', '3']
        months = getMonths()
        self.assertEqual(months, float('3'))


if __name__ == '__main__':
    unittest.main()
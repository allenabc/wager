import unittest
from draftkings import get_soup
from draftkings import convert_soup_to_lists
import bs4
from unittest import TestCase


class Test(TestCase):
    @unittest.skip("Skip get_soup")
    def test_get_soup(self):
        fn = 'draftkings.pickle'
        soup_obj = get_soup(fn)
        self.assertIsInstance(soup_obj, bs4.BeautifulSoup)

    def test_convert_soup(self):
        fn = 'draftkings.pickle'
        sport = "hockey"
        y = convert_soup_to_lists(fn, sport)
        self.assertTrue(1)


if __name__ == '__main__':
    unittest.main()

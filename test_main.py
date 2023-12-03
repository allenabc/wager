import unittest
from unittest import TestCase
from main import access_website
from main import access_pickle
from mysql import create_db_outfile
from mysql import create_cursor
from main import write_pickle
from main import convert_soup_to_lists
from main import download_website_and_save

import bs4
import os


class Test(TestCase):
    @unittest.skip("Skip access_website")
    def test_access_website(self):
        url = "https://www.ibm.com/"
        expecting = "College Football Computer Picks"
        expecting = "IBM"
        # returns a soup object
        title = str(access_website(url).title)
        print("Title is ***{}***".format(title))
        self.assertIn(expecting, title)

    @unittest.skip("Skip pickle1")
    def test_pickle(self):
        # Download website into pickle file
        url = "https://www.ibm.com/"
        fn = "ibm"
        test_file = "ibm.pickle"
        if os.path.isfile(test_file):
            os.remove(test_file)
        access_to_pickle(url, test_file)
        file_stats = os.stat(test_file)
        print(file_stats.st_size)
        self.assertTrue(os.path.isfile(test_file))
        self.assertTrue(file_stats.st_size > 1000)

    @unittest.skip("Skip it")
    # Check create csv file
    def test_it(self):
        cursor = create_cursor()
        sport = "nba"
        fn = create_db_outfile(sport, cursor)
        self.assertIn(sport, fn)

    @unittest.skip("Skip create_file")
    def test_create_pickle(self):
        url = "https://www.ibm.com/"
        fn = "ibm"
        test_file = "ibm.pickle"
        try:
            os.remove(test_file)
        except OSError:
            pass
        soup_obj = ""
        write_pickle(url, soup_obj, fn)
        file_stats = os.stat(test_file)
        self.assertTrue(file_stats.st_size > 1000)

    @unittest.skip("Skip open_pickle_file")
    def test_open_pickle_file(self):
        fn = "ibm.pickle"
        soup_obj = access_pickle(fn)
        self.assertIsInstance(soup_obj, bs4.BeautifulSoup)

    @unittest.skip("Skip process_sport_soup")
    def test_process_sport_soup(self):
        pickle_file = "hockey.pickle"
        sport = "hockey"
        sport, teams, times, dates, scores, totals = convert_soup_to_lists(pickle_file, sport)
        self.assertTrue(len(totals) > 5)
        pass

    def test_download_save(self):
        pickle_file = "ibm.pickle"
        os.remove(pickle_file)
        url = "https://www.ibm.com/us-en"
        download_website_and_save(url, "ibm")
        file_stats = os.stat(pickle_file)
        self.assertTrue(os.path.isfile(pickle_file))
        print("*** Downloaded {} {} ***".format(pickle_file,file_stats.st_size))
        self.assertTrue(file_stats.st_size > 10000)

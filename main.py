import datetime
from mysql import create_cursor
from bs4 import BeautifulSoup as bs
import os
import sys
import pickle
from urllib.request import urlopen


def access_website(url):
    print("************ Accessed ********* " + url)
    html = urlopen(url)
    soup_obj = bs(html, "lxml")
    return soup_obj


def access_pickle(pickle_file):
    soup_obj = ""
    if os.path.isfile(pickle_file):
        with open(pickle_file, "rb") as file1:
            f1 = pickle.load(file1)
    else:
        print("{} does not exist".format(pickle_file))
        return
    print("******* {} accessed *********".format(pickle_file) )
    return f1


def download_website_and_save(url, pickle_file):
    soup_obj = access_website(url)
    write_pickle(soup_obj, pickle_file)


def write_pickle(soup_obj, fn):
    # download website and pickle dump it
    sys.setrecursionlimit(8000)
    fn = fn+".pickle"
    try:
        os.remove(fn)
    except OSError:
        pass
    with open(fn, "wb") as fn:
        pickle.dump(soup_obj, fn)


def convert_soup_to_lists(pickle_file, sport):
    soup = access_pickle(pickle_file)
    teams = []
    timesx = []
    datesx = []
    scores_list = []
    totals = []
    team_names = soup.find_all("span", class_="teamName")
    for team_name in team_names:
        teams.append(team_name.text)
    dates = soup.find_all("span", class_="date")
    for dte in dates:
        datesx.append(dte)
    times = soup.find_all("span", class_="time")
    for tm in times:
        timesx.append(tm.text)
    scores = soup.find_all("span", class_="score")
    for score in scores:
        scores_list.append(score.text)
    t_scores = soup.find_all("span", class_="totalScore")
    for t_score in t_scores:
        totals.append(t_score.text)
    return sport, teams, timesx, datesx, scores_list, totals


def write_lists_to_database(sport, team, times, dates, scores, totals):
    cursor = create_cursor()
    # away, home, away_score, home_score,total_score,d_date, t_time
    print("Truncating " + sport)
    cursor.execute("truncate table " + sport)
    sql = ""
    if sport == "nba":
        sql = ("INSERT INTO nba("  "away, home, a_score, h_score, total, t_time,d_date)"
               "VALUES( (%s),(%s),(%s),(%s),(%s),(%s),(%s) )")
    if sport == "hockey":
        sql = ("INSERT INTO hockey("  "away, home, a_score, h_score, total, t_time,d_date)"
               "VALUES( (%s),(%s),(%s),(%s),(%s),(%s),(%s) )")
    if sport == "ncaab":
        sql = ("INSERT INTO ncaab("  "away, home, a_score, h_score, total, t_time,d_date)"
               "VALUES( (%s),(%s),(%s),(%s),(%s),(%s),(%s) )")
    if sport == "ncaaf":
        sql = ("INSERT INTO ncaaf("  "away, home, a_score, h_score, total, t_time,d_date)"
               "VALUES( (%s),(%s),(%s),(%s),(%s),(%s),(%s) )")
    if sport == "nfl":
        sql = ("INSERT INTO nfl("  "away, home, a_score, h_score, total, t_time,d_date)"
               "VALUES( (%s),(%s),(%s),(%s),(%s),(%s),(%s) )")
    for t_time in times:
        home = team.pop(0)
        away = team.pop(0)
        a_score = scores.pop(0)
        h_score = scores.pop(0)
        t_score = totals.pop(0)
        d_date = dates.pop(0)
        val = (home, away, a_score, h_score, t_score, t_time, d_date)
        cursor.execute(sql, val)
    cursor.commit()


def create_sport_table(sport):
    if sport == "ncaab":
        pickle_file = "ncaab.pickle"
        url = "https://www.oddstrader.com/ncaa-college-basketball/picks/"
    elif sport == "hockey":
        pickle_file = "hockey.pickle"
        url = "https://www.oddstrader.com/nhl/picks/"
    elif sport == "ncaaf":
        pickle_file = "ncaaf.pickle"
        url = "https://www.oddstrader.com/ncaa-college-football/picks/"
    elif sport == "nfl":
        pickle_file = "nfl.pickle"
        url = "https://www.oddstrader.com/nfl/picks/"
    elif sport == "nba":
        pickle_file = "nba.pickle"
        url = "https://www.oddstrader.com/nba/picks/"
    else:
        print("unknown sport > " + sport)
        return
    print('Running * {0} *'.format(sport))
    convert_soup_to_lists(url, pickle_file, sport)


#sp = 'hockey'
#create_sport_table(sp)

# Notes
#   game = re.sub('boxscore|div|br|class=|"|<|>|span|=|style|float', '', game)
# today = date.today()
# create table games(id MEDIUMINT not null auto_increment,home char(30)
# not null,away char(30) not null,time char(30), primary key(id) );
# 
# INSERT INTO games  (home,away,time) VALUES(('rangers'),('wild'),('the time'));
# """
# SELECT * FROM data.employees INTO OUTFILE 'employees.csv';
# mysqldump - u allen - p - -databases trader > ~ / PycharmProjects / Hockey / Save / sql_backup.sql
# current database ? select database();
# repeat copy cell  copy cell, choose cells, control D

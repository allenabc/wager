import datetime
import pymysql
import os


def create_cursor():
    connection = pymysql.connect(host='localhost', user='allen', password='Vagrant',
                                 database='trader', cursorclass=pymysql.cursors.DictCursor)
    return connection.cursor()


def create_db_outfile(sport, cursor):
    now = datetime.now()
    dt_string = now.strftime("%d-%m")
    fn = "/tmp/" + sport + "-" + dt_string + ".csv"
    if os.path.isfile(fn):
        print("CSV file for this sport already exists " + fn)
    else:
        my_cmd = "SELECT * FROM trader." + sport + " " + "INTO OUTFILE  " + "'" + fn + "'"
        cursor.execute(my_cmd)
        print(my_cmd)
    return fn

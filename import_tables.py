""" Imports data from a csv file into the sqlite database table """

import csv, sqlite3
import pandas

database = r"C:\Users\Artiom\Documents\Python Scripts\Tests\my_test.db"
csvfile = 'archive\all_countries.csv'
con = sqlite3.connect(database)
cur = con.cursor()
cur.execute("CREATE TABLE countries (country);") # use your column names here

df = pandas.read_csv(csvfile)
df.to_sql("countries", con, if_exists='append', index=False)
con.commit()
con.close()




import csv, sqlite3
import pandas

database = r"C:\Users\Artiom\Documents\Python Scripts\Tests\my_test.db"
csvfile = 'archive\all_countries.csv'
con = sqlite3.connect(database)
cur = con.cursor()
cur.execute("CREATE TABLE countries (country);") # use your column names here

# with open('all_countries.csv','r') as fin: # `with` statement available in 2.5+
#     # csv.DictReader uses first line in file for column headings by default
#     dr = csv.DictReader(fin) # comma is default delimiter
#     to_db = [(i['country']) for i in dr]
df = pandas.read_csv(csvfile)
df.to_sql("countries", con, if_exists='append', index=False)
#cur.executemany("INSERT INTO countries (country) VALUES (?);", to_db)
con.commit()
con.close()


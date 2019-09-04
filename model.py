import sqlite3
from sqlite3 import Error


class DbModel:
    """ Allows connection to the database """

    database = r"C:\Users\Artiom\Documents\Python Scripts\Tests\my_test.db"

    def __init__(self):
        pass

    def __enter__(self):
        self.connection = sqlite3.connect(self.database)
        #self.create_table_if_not_exists()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()
        print("Exiting Db instance")

    def create_base_table_if_not_exists(self):
        """ If the tables doesn't exist yet, create it """
        sql = '''CREATE TABLE IF NOT EXISTS entities (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                                      entity,
                                                      country,
                                                      partner,
                                                      parent);'''
        self.cur = self.connection.cursor()
        self.cur.execute(sql)
        self.connection.commit()
        self.cur.close()

    # def create_tree_table_if_not_exists1(self):
    #     """ If the tables doesn't exist yet, create it """
    #     sql = ''' SELECT A.entity,
    #                      A.country,
    #                      A.partner,
    #                      A.parent,
    #                      B.partner AS partner_B,
    #                      B.parent AS parent_B,
    #                      CASE WHEN A.partner=B.parent THEN A.partner
    #                      END AS PARENT_CHILD_NODE,
    #                      CASE WHEN A.parent=B.partner THEN A.parent
    #                      END AS CHILD_PARENT_NODE
    #               FROM entities  A
    #               CROSS JOIN entities B
    #               WHERE PARENT_CHILD_NODE NOT NULL OR CHILD_PARENT_NODE NOT NULL
    #               '''
    #     self.cur = self.connection.cursor()
    #     self.cur.execute(sql)
    #     rows = self.cur.fetchall()
    #     for row in rows:
    #         print(row)
    #     return rows

    def create_tree_table_if_not_exists(self):
        """ If the tables doesn't exist yet, create it """
        sql_drop = '''DROP TABLE IF EXISTS parent_child_relations;'''
        sql_create = '''CREATE TABLE parent_child_relations AS
                  SELECT distinct(parent) AS parent, group_concat(A.partner) AS child
                  FROM entities  A
                  GROUP BY parent
                  '''
        self.cur = self.connection.cursor()
        self.cur.execute(sql_drop)
        self.cur.execute(sql_create)
        rows = self.cur.fetchall()
        for row in rows:
            print(row)
        return rows

    def display_all_content(self):
        """ Show the content of the table """
        sql = ''' SELECT entity,
                         country,
                         partner,
                         parent 
                  FROM entities 
                  ORDER BY entity'''
        self.cur = self.connection.cursor()
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        return rows

    def display_all_entities(self):
        """ Display all entities available in the database """
        sql = ''' SELECT distinct(entity ) 
                  FROM entities'''
        self.cur = self.connection.cursor()
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        return rows

    def display_all_countries(self):
        """ Display all countries available in the database """
        sql = ''' SELECT country
                  FROM countries'''
        self.cur = self.connection.cursor()
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        return rows

    def insert_content(self, row):
        """ Insert a new row into the table """
        sql = ''' INSERT INTO entities(entity,country,partner,parent)
                  VALUES(?,?,?,?) '''
        self.cur = self.connection.cursor()
        self.cur.execute(sql, row)
        print("Row inserted")

        self.connection.commit()
        print("Record inserted successfully into SqliteDb_developers table ")
        self.cur.close()

        return self.cur.lastrowid

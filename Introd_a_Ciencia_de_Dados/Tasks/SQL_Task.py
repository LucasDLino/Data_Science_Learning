import pymysql
import pandas as pd

class SQL_Class(object):

    def __init__(self, stations):
        self.stations = stations

    def sql_task(self):
        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                     user='ICD_user',
                                     password='icd2020',
                                     db='rain_data')

        # create cursor
        cursor = connection.cursor()

        # Insert Stations in Table 'stations'
        for i in self.stations:
            sql = "INSERT INTO `stations` (`Name`) VALUES (%s)"
            cursor.execute(sql, (i.name))
            # the connection is not auto committed by default, so we must commit to save our changes
            connection.commit()

        # Insert DataFrame data one by one - Table 'rain'
        count = 1
        for i in self.stations:
            for index, value in i.items():
                sql = "INSERT INTO `rain` (`date`, `precipitation`, `ID_stations`) VALUES (%s, %f, %d)"
                cursor.execute(sql, (index.strftime('%Y-%m-%d'), value, count))
                # the connection is not auto committed by default, so we must commit to save our changes
                connection.commit()
            count += 1

        # Execute query - table 2
        sql = "SELECT * FROM `rain`"
        cursor.execute(sql)

        # Fetch all the records
        result = cursor.fetchall()
        for i in result:
            print(i)

        #Execute query - table 1
        sql = "SELECT * FROM stations WHERE ID_stations=1"
        result = cursor.fetchall()
        for i in result:
            print(i)



        connection.close()
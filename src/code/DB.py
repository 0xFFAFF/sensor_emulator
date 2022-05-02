# # -*- coding: utf-8 -*-
# '''
# Created on 2022-04-29   09:47:47
# @author: TA
# '''
# import sqlite3

# # DROP_SQL = '''DROP TABLE IF EXISTS sensor_data'''
# # CREATE_SQL = '''CREATE TABLE IF NOT EXISTS sensor_data
# # (ID INTEGER PRIMARY KEY AUTOINCREMENT, data_value TEXT)'''

# class DataBase():
#     def __init__(self,db):
#         self.db = db
#         self.db = sqlite3.connect(self.db)
#         pass
    
#     def create_table(self,*args):
#         cursor = self.db.cursor()
#         for sql in args:
#             cursor.execute(sql)
#         self.db.commit()
#         pass
    
#     def insert_data(self,param):
#         cursor = self.db.cursor()
#         cursor.execute(param)
#         self.db.commit()
#         pass
    
#     def delete_data(self,param):
#         cursor = self.db.cursor()
#         cursor.execute(param)
#         self.db.commit()
#         pass
    
#     def query_data(self,param):
#         cursor = self.db.cursor()
#         cursor.execute(param)
#         result = cursor.fetchall()
#         return result
#         pass
    
# if __name__ == '__main__':
#     db = DataBase('test.db')
#     db.create_table(DROP_SQL,CREATE_SQL)
#     db.insert_data('INSERT INTO sensor_data(data_value) VALUES (\'youhsdn\')')
#     db.insert_data('INSERT INTO sensor_data(data_value) VALUES (\'youhsdn\')')
#     result = db.query_data('SELECT * FROM sensor_data')
#     print(result)
    
from datetime import datetime
import csv
import sqlite3 as sql
import os
import pandas as pd
from flask import request

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class DBManage():

	def __init__(self):

		self.db_path = r'database\db.db'
		self.WIP_path = r"\\ad.numatic.co.uk\group\Operations\Production Assembly\Metal Shop\Supply_sheet_all_departments\Supply All Departments.csv"
		self.weekly_supply_db_path = r'database\weekly_supply.db'

	def updateWIPTable(self):

		#connect to database
		conn = sql.connect(self.db_path)
		cur = conn.cursor()
		#drop table
		cur.execute("""
		DROP TABLE IF EXISTS WIP;""")
		#create table
		cur.execute("""
		CREATE TABLE "WIP" (
			"WEEK_NUMBER" TEXT NOT NULL,
		    "WIP_ENTITY_NAME" TEXT NOT NULL,
		    "PART_NUMBER" TEXT NOT NULL,
		    "PART_DESCRIPTION" TEXT NOT NULL,
		    "START_QUANTITY" TEXT NOT NULL,
		    "DEPARTMENT_CLASS" TEXT NOT NULL,
		    "DEPARTMENT" TEXT,
		    OPERATION_DESCRIPTION TEXT NOT NULL);
		""")
		conn.commit()

		#load new table
		with open(self.WIP_path,"r") as csvfile:
		    file = csv.reader(csvfile)
		    for row in file:
		    	if (row[6] == 'METAL SHOP') and (row[6] != 'PAINT SHOP'):
		        	cur.execute('INSERT INTO WIP VALUES (?,?,?,?,?,?,?,?)',(row[0],row[1],row[2],row[3],row[4],row[6],row[7],row[11]))
		    conn.commit()
		    print(f"WIP updated on {datetime.now()}" )
		conn.close()	    
		

	def loadWeekSupply(self, file, file_name, week_no):

		conn = sql.connect(self.weekly_supply_db_path)
		cur = conn.cursor()

		cur.execute(f"""
		DROP TABLE IF EXISTS {file_name};""")

		cur.execute(f"""
		CREATE TABLE {file_name} (
		    "WEEK_NUMBER" TEXT NOT NULL,
		    "JOB_NUMBER" TEXT NOT NULL,
		    "PART_NUMBER" TEXT NOT NULL,
		    "PART_DESCRIPTION" TEXT NOT NULL,
		    "ROUTING_CODE" TEXT NOT NULL,
		    "QUANTITY" TEXT NOT NULL);
		    """)

		for row in file.iterrows():
		    if (row[1][0] == int(week_no)) and (row[1][7] != 'WELD DEPT') and (row[1][7] !='PAINT CELL'):
		        cur.execute(f'INSERT INTO {file_name} VALUES (?,?,?,?,?,?)',(row[1][0],row[1][1],row[1][2],row[1][3],row[1][11],row[1][4]))
		  
		conn.commit()
		conn.close()
		

	def refreshWIPTable(self):
		wip_data = []
		t2 = []
		
		conn = sql.connect(self.db_path)
		cur = conn.cursor()

		cur.execute(f"SELECT * FROM JOB_DETAILS WHERE STAGE = 'In Progress';")
		c = cur.fetchall()
		wip_data.append(c)
		t1 = [list(i) for i in c]
		
		for row in wip_data[0]:
			cur.execute(f"SELECT * FROM JOB_ROUTING WHERE WIP_ENTITY_NAME = '{row[1]}';")
			t2.append([list(i) for i in cur.fetchall()])

		conn.commit()
		conn.close()
		
		wip_data = [list(i) for i in zip(t1,t2)]

		return wip_data

	def insertToWIPcompletion(self,job_details,job_qty,job_routing):

		conn = sql.connect(self.db_path)
		cur = conn.cursor()
		cur.execute(f'INSERT INTO WIP_COMPLETION VALUES (?,?,?,?,?,?)',(int(job_details[3]),int(job_details[0])
			,int(job_details[1]),job_routing,int(job_qty),str(datetime.now().strftime("%Y-%m-%d %H:%M"))))
	
		conn.commit()
		conn.close()

	def loadPlanTable(self,session):
		conn = sql.connect(self.weekly_supply_db_path)
		conn.row_factory = dict_factory
		cur = conn.cursor()
		cur.execute(f"""ATTACH DATABASE "{self.db_path}" AS db2;""")

		cur.execute(f"""
							SELECT WEEK_NUMBER, JOB_NUMBER,PART_NUMBER, PART_DESCRIPTION, QUANTITY,COMPLETE ,ROUTING_CODE, STATUS FROM {session}
							LEFT JOIN
							db2.JOB_ROUTING ON db2.JOB_ROUTING.WIP_ENTITY_NAME = {session}.JOB_NUMBER
							AND db2.JOB_ROUTING.ROUTING = {session}.ROUTING_CODE							
			""")
		file_data = cur.fetchall()

		conn.commit()
		conn.close()

		return file_data

	def planCompletion(self,session):

		conn = sql.connect(self.weekly_supply_db_path)
		# Cursor returns dictionary
		conn.row_factory = dict_factory
		#Attache second database
		cur = conn.cursor()
		cur.execute(f"""ATTACH DATABASE "{self.db_path}" AS db2;""")
		plan_updated = cur.execute(f"""
							SELECT WEEK_NUMBER, JOB_NUMBER,PART_NUMBER, PART_DESCRIPTION, QUANTITY ,ROUTING_CODE, STATUS FROM {session}
							LEFT JOIN
							db2.JOB_ROUTING ON db2.JOB_ROUTING.WIP_ENTITY_NAME = {session}.JOB_NUMBER
							AND db2.JOB_ROUTING.ROUTING = {session}.ROUTING_CODE 
							WHERE {session}.ROUTING_CODE = 'BLAST DEPT'

			""").fetchall()
		print(plan_updated)
		conn.close()
		return plan_updated

	def routing_details(self):

		conn = sql.connect(self.db_path)
		# Cursor returns dictionary
		conn.row_factory = dict_factory
		#Attache second database
		cur = conn.cursor()
		#cur.execute(f"""ATTACH DATABASE "{self.db_path}" AS db2;""")
		routing_details = cur.execute(f"""
							SELECT DETAILS.WIP_ENTITY_NAME, DETAILS.STAGE, DETAILS.QUANTITY, ROUTES.ROUTING, ROUTES.COMPLETE, ROUTES.STATUS FROM JOB_DETAILS AS DETAILS
							INNER JOIN JOB_ROUTING AS ROUTES ON
							ROUTES.WIP_ENTITY_NAME = DETAILS.WIP_ENTITY_NAME
							

			""").fetchall()
		print(routing_details)
		conn.close()
		return routing_details










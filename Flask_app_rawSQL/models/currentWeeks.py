import sqlite3 as sql




class getCurrentWeeks():

	def __init__(self):

		self.weekly_supply_db_path = r'database\weekly_supply.db'
		self.weekList = []
	def getWeekList(self):

		conn = sql.connect(self.weekly_supply_db_path)
		cur = conn.cursor()
		cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
		tables = cur.fetchall()

		for table in tables:
			self.weekList.append(table[0])


		conn.close()
		return sorted(self.weekList)

		
import sqlite3 as sql
#from app import app

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class routingFilter():
	def __init__(self):
		self.db_path = r'database\db.db'
		self.conn = sql.connect(r'database\weekly_supply.db')
		self.conn.row_factory = dict_factory
		self.cur = self.conn.cursor()
		self.data = None

	def saw(self,session):

		self.cur.execute(f"SELECT * FROM {session['current_week']} WHERE ROUTING_CODE = 'SAW DEPT'")
		self.data = self.cur.fetchall()
		self.conn.close()

		return self.data


	def cncPunch(self,session):

		self.cur.execute(f"SELECT * FROM {session['current_week']} WHERE ROUTING_CODE = 'CNC PUNCH'")
		self.data = self.cur.fetchall()
		self.conn.close()
			
		return self.data

	def blastDept(self,session):

		self.cur.execute(f"""ATTACH DATABASE "{self.db_path}" AS db2;""")

		self.cur.execute(f"""
							SELECT WEEK_NUMBER, JOB_NUMBER,PART_NUMBER, PART_DESCRIPTION, QUANTITY,COMPLETE ,ROUTING_CODE, STATUS FROM {session}
							LEFT JOIN
							db2.JOB_ROUTING ON db2.JOB_ROUTING.WIP_ENTITY_NAME = {session}.JOB_NUMBER
							AND db2.JOB_ROUTING.ROUTING = {session}.ROUTING_CODE 
							WHERE {session}.ROUTING_CODE = 'BLAST DEPT'""")
		self.data = self.cur.fetchall()


		print(self.data)
		return self.data

	def laserFold(self,session):

		self.cur.execute(f"SELECT * FROM {session['current_week']} WHERE ROUTING_CODE = 'LASER FOLD'")
		self.data = self.cur.fetchall()
		self.conn.close()
			
		return self.data

	def drillDept(self,session):

		self.cur.execute(f"SELECT * FROM {session['current_week']} WHERE ROUTING_CODE = 'DRILL DEPT'")
		self.data = self.cur.fetchall()
		self.conn.close()
			
		return self.data

	def drumDept(self,session):

		self.cur.execute(f"SELECT * FROM {session['current_week']} WHERE ROUTING_CODE = 'DRUM DEPT'")
		self.data = self.cur.fetchall()
		self.conn.close()
			
		return self.data

	def wandWipe(self,session):

		self.cur.execute(f"SELECT * FROM {session['current_week']} WHERE ROUTING_CODE = 'WAND WIPE'")
		self.data = self.cur.fetchall()
		self.conn.close()
			
		return self.data


	def wandLoad(self,session):

		self.cur.execute(f"SELECT * FROM {session['current_week']} WHERE ROUTING_CODE = 'WAND LOAD'")
		self.data = self.cur.fetchall()
		self.conn.close()
			
		return self.data

	def wvc001(self,session):

		self.cur.execute(f"SELECT * FROM {session['current_week']} WHERE ROUTING_CODE = 'WVC-001'")
		self.data = self.cur.fetchall()
		self.conn.close()
			
		return self.data

	def wdc001(self,session):

		self.cur.execute(f"SELECT * FROM {session['current_week']} WHERE ROUTING_CODE = 'WDC-001'")
		self.data = self.cur.fetchall()
		self.conn.close()
			
		return self.data

	def wcim001(self,session):

		self.cur.execute(f"SELECT * FROM {session['current_week']} WHERE ROUTING_CODE = 'WCIM-001'")
		self.data = self.cur.fetchall()
		self.conn.close()
			
		return self.data

	def vcp001(self,session):

		self.cur.execute(f"SELECT * FROM {session['current_week']} WHERE ROUTING_CODE = 'VCP-001'")
		self.data = self.cur.fetchall()
		self.conn.close()
			
		return self.data

	def vcp002(self,session):

		self.cur.execute(f"SELECT * FROM {session['current_week']} WHERE ROUTING_CODE = 'VCP-002'")
		self.data = self.cur.fetchall()
		self.conn.close()
			
		return self.data

	def uww001(self,session):

		self.cur.execute(f"SELECT * FROM {session['current_week']} WHERE ROUTING_CODE = 'UWW-001'")
		self.data = self.cur.fetchall()
		self.conn.close()
			
		return self.data
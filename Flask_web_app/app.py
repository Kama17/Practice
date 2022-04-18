from flask import Flask, render_template, request,redirect,session, url_for
import os
import pandas as pd
from databaseManage import DBManage 
import sqlite3 as sql
from models.currentWeeks import getCurrentWeeks
from models.routingFilter import routingFilter
from datetime import datetime
from bookin import bookIn
import webbrowser
from waitress import serve
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine


app = Flask(__name__)
app.secret_key = '125987'

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

WIP_path = (r'Supply All Departments.csv')
#weekly_supply_db_path = create_engine(r'sqlite:///database\weekly_supply.db')
weekly_supply_db_path = (r'database\weekly_supply.db')
#db_path = create_engine(r'sqlite:///database\db.db')
db_path = (r'database\db.db')


@app.route('/')
def login():
	session.clear()
	return render_template('login.html')


@app.route('/index')
def index():

	wip_modif = datetime.fromtimestamp(os.stat(WIP_path).st_mtime).strftime('%d-%m-%Y %H:%M')

	availableWeeks = getCurrentWeeks().getWeekList()
	
	if request.method == 'POST':
		
		
		return render_template('index.html',wip_modif = wip_modif,routings = update_wip[1], update_wip =  DBManage().refreshWIPTable(),weeks = availableWeeks)
	
	return render_template('index.html', wip_modif = wip_modif,update_wip =  DBManage().refreshWIPTable(),weeks = availableWeeks)

@app.route('/bend', methods = ['GET', 'POST'])
def bend():

	availableWeeks = getCurrentWeeks().getWeekList()
	if request.method == 'POST':

		#Loading complately new week
		file = request.files['plan']
		week = int(file.filename.split()[1])
		file_name = file.filename.split('.')[0].replace(" ","_")
		
		# Connect to db
		conn = sql.connect(weekly_supply_db_path)
		conn.row_factory = dict_factory 
		cur = conn.cursor()
		# Get list of available tables
		cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
		tables = cur.fetchall()
		
		# Set session to current week table
		session['current_week'] = file_name

		# Load week
		for table in tables:
			if table['name'] == file_name:

				file_data = DBManage().loadPlanTable(file_name)		
		
				return render_template('bend.html',file_value = file, name = file_name, file = file_data, title = file_name, weeks = availableWeeks)
		
		# if table not exists readl and load
		# read from html file tag as pandas dataframe
		new_plan = pd.read_excel(file)
		# create new table
		DBManage().loadWeekSupply(new_plan, file_name, week)
		# read from database
		file_data = DBManage().loadPlanTable(file_name)

		return render_template('bend.html',file_value = file, name = file_name, file = file_data, title = file_name,weeks = availableWeeks)

	# Upload week for current session variable
	else:
		if session:
			#IMPORTANT GET UNIQUE VALUES FORM ROUTING_CODE FOR NAVBAR BUTTONS
			conn = sql.connect(weekly_supply_db_path)
			cur = conn.cursor()
			dep_routing = cur.execute(f"SELECT DISTINCT ROUTING_CODE FROM {session['current_week']}").fetchall()
			########################
			# SORT ROUTINGS
			dep_routing.sort()
			#If the the session is available then load the current week 
			file_data = DBManage().loadPlanTable(session['current_week'])
			availableWeeks = getCurrentWeeks().getWeekList()

			#detail = DBManage().routing_details()
			#print(detail)
			return render_template('bend.html', file = file_data, weeks = availableWeeks, dep_routing = dep_routing)

		availableWeeks = getCurrentWeeks().getWeekList()
		return render_template('bend.html', weeks = availableWeeks)


#load available week form html
@app.route('/loading', methods = ['POST', 'GET'])
def loadweek():

	week_request = request.args['no1']
	conn = sql.connect(weekly_supply_db_path)
	conn.row_factory = dict_factory
	file_data = DBManage().loadPlanTable(week_request)
	conn.close()
	availableWeeks = getCurrentWeeks().getWeekList()

	#Set new week after loading
	session['current_week'] = week_request

	return render_template('bend.html', file = file_data, current_week = session['current_week'],weeks = availableWeeks)


@app.route('/booking', methods = ['GET', 'POST'])
def booking():
	#complete = 0
	action = ""
	job_no =  request.args['job_no']

	# Check if job in JOB_DETAILS table
	job_rec = bookIn().search_weekly_supply(job_no)
	
	# If record not exists. Srearch WIP
	if job_rec == None:
		action = "insert"
		data = bookIn().searchWIP(job_no)

		# if job not found in WIP
		if data == []:
			return render_template('index.html',message = 'Job not found in database' ,update_wip = DBManage().refreshWIPTable())
			

		routing = []
		for route in data:
			routing.append([route[1],route[7],0])
	
		return render_template('index.html', 
			job_rec = routing, 
			#wip_modif = wip_modif, 
			data0 = data[0][0],
			data1 = data[0][1],
			data2 = data[0][2],
			data3 = data[0][3],
			data4 = int(data[0][4]),
			action = action, # Set value action to insert and pass to submit route
			update_wip =  DBManage().refreshWIPTable())

	# If record exists 	
	elif job_rec != None:
		action = "update" # Set te value action to update and pass to submit route
	
		return render_template('index.html', 
			job_rec = job_rec[1],
			#wip_modif = wip_modif, 
			data0 = job_rec[0][0][0],
			data1 = job_rec[0][0][1],
			data2 = job_rec[0][0][2],
			data3 = job_rec[0][0][3],
			data4 = job_rec[0][0][4],
			action = action,update_wip =  DBManage().refreshWIPTable())


@app.route('/<action>/bookout', methods = ['GET', 'POST'])
def bookout(action):
	job_no_out =  request.args.get('job_no_book_out')
	
	job_rec_book_out = bookIn().search_weekly_supply(job_no_out)
	
	
	if action == 'search':
		print('Search')
		return render_template('index.html', 
				job_rec_book_out = job_rec_book_out[1],
				update_wip = DBManage().refreshWIPTable(), 
				data0_out = job_rec_book_out[0][0][0],
				data1_out = job_rec_book_out[0][0][1],
				data2_out = job_rec_book_out[0][0][2],
				data3_out = job_rec_book_out[0][0][3],
				data4_out = job_rec_book_out[0][0][4],
				action = 'search')
	
	elif action == 'bookin_out':

		job_no_out =  request.args.get('no')
		job_out_routing =  request.args.get('job_bookout_routing')
		job_out_qty =  request.args.get('job_bookout_qty')
		job_details = request.args.getlist('no')

		# Insert to WIP_Completion
		job_details = request.args.getlist('no')
		
		DBManage().insertToWIPcompletion(job_details,job_out_qty,job_out_routing)

		#conn = sql.connect(db_path)
		conn = sql.connect(db_path)
		cur = conn.cursor()

		cur.execute(f"""

					SELECT * FROM JOB_ROUTING
					WHERE ROUTING = '{job_out_routing}' AND WIP_ENTITY_NAME = '{job_no_out}' AND STATUS = 'In Progress';
			""")
		job_out_rec = cur.fetchall()

		# if qty completed is == total qty
		if (job_out_rec[0][2] + int(job_out_qty)) == job_out_rec[0][3]:
		
			cur.execute(f"""
				
					UPDATE JOB_ROUTING SET STATUS = 'Complete', COMPLETE = '{job_out_rec[0][2] + int(job_out_qty)}'
					WHERE ROUTING = '{job_out_routing}' AND WIP_ENTITY_NAME = '{job_no_out}';
			""")

			cur.execute(f"""
				
					UPDATE JOB_DETAILS SET STAGE = 'Complete'
					WHERE  WIP_ENTITY_NAME = '{job_no_out}';
			""")

			conn.commit()
		# if qty compelet is != totla qty
		else:
			
			cur.execute(f"""
				
					UPDATE JOB_ROUTING SET STATUS = '', COMPLETE = {job_out_rec[0][2] + int(job_out_qty)}
					WHERE ROUTING = '{job_out_routing}' AND WIP_ENTITY_NAME = '{job_no_out}';
			""")

			cur.execute(f"""
				
					UPDATE JOB_DETAILS SET STAGE = ''
					WHERE  WIP_ENTITY_NAME = '{job_no_out}';
			""")

			conn.commit()	
		conn.close()

	render_template('index.html', update_wip = DBManage().refreshWIPTable())
	#wip_modif = wip_modif,
	return redirect('/index')

@app.route('/<action>/submit', methods = ['POST','GET'])
def submit(action):

	sub = request.args.getlist('no')
	sub1 = request.args.getlist('no_1')
	sub2 = request.args.getlist('no_2')
	sub_routings = dict(zip(sub1,sub2))
	sub_check = request.args.get('check_box')
	
	#Check if routing check box was selected
	if sub_check == None:
		
		return render_template('index.html', message = 'Please select routing.' ,update_wip = DBManage().refreshWIPTable())

	conn = sql.connect(db_path)
	cur = conn.cursor()

	#Check if job already started
	cur.execute(f"""
				SELECT WIP_ENTITY_NAME,STAGE FROM JOB_DETAILS
				WHERE WIP_ENTITY_NAME = {sub[0]} AND STAGE == 'In Progress' 
		""")
	check = cur.fetchall()

	if check != []:
		conn.close()
		return render_template('index.html',message = 'Job already started.' ,update_wip = DBManage().refreshWIPTable())
	
	if action == 'insert':
		print('Insert')
		cur.execute(f"""
						INSERT INTO JOB_DETAILS (WEEK_NUMBER,WIP_ENTITY_NAME,PART_NUMBER,DESCRIPTION,QUANTITY,STAGE)
					VALUES ({sub[3]},'{sub[0]}',{sub[1]},'{sub[4]}',{sub[2]},'In Progress');
			""")

		for key, val in sub_routings.items():
						# Set routing to in Progress otherwise set to none
			if sub_check == key:
				('True')
				cur.execute(f"""	
					INSERT INTO JOB_ROUTING (WIP_ENTITY_NAME,ROUTING,COMPLETE,DATE_TIME,STATUS)
					VALUES ('{sub[0]}','{key}',{val},'{sub[2]}','In Progress');
				""")
		
			else:
				cur.execute(f"""	
					INSERT INTO JOB_ROUTING (WIP_ENTITY_NAME,ROUTING,COMPLETE,DATE_TIME,STATUS)
					VALUES ('{sub[0]}','{key}',{val},'{sub[2]}','');
					""")			
		conn.commit()
		conn.close()
		
	elif action == 'update':
		print('Update')
		cur.execute(f"""
				
					UPDATE JOB_ROUTING SET STATUS = 'In Progress'
					WHERE ROUTING = '{sub_check}' AND WIP_ENTITY_NAME = '{sub[0]}';
			""")
		cur.execute(f"""
				
					UPDATE JOB_DETAILS SET STAGE = 'In Progress' WHERE WIP_ENTITY_NAME = '{sub[0]}';
			""")
		conn.commit()
		conn.close()
	
	render_template('index.html', update_wip = DBManage().refreshWIPTable())#, routings = update_wip[1:])
	#wip_modif = wip_modif,
	return redirect('/index')

@app.route('/trans', methods = ['GET'])
def trans():
	conn = sql.connect(db_path)
	cur = conn.cursor()
	wip = cur.execute(f"""SELECT * FROM WIP_COMPLETION""").fetchall()
	conn.close()
	
	return render_template('transaction.html', wip = wip)
 
#webbrowser.open_new('http://127.0.0.1:5000')

if __name__ == '__main__':
	webbrowser.open('http://127.0.0.1:5000', new = 2)
	app.run(debug = True,threaded=True)
	#serve(app, port = 5000)
#shutdown_func = request.environ.get('werkzeug.server.shutdown')
#shutdown_func()

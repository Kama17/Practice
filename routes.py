#import sqlite3 as sql
from app import app
from models.routingFilter import routingFilter
from models.routingFilter import routingFilter


@app.route('/cncpunch')
def cncPunch():
	file_data = routingFilter().cncPunch(session)

	return render_template('bend.html', file = file_data, weeks = availableWeeks, current_week =session['current_week'] ) 


@app.route('/blastdept')
def blastDept():
	file_data = routingFilter().blastDept(session)

	return render_template('bend.html', file = file_data, weeks = availableWeeks, current_week =session['current_week'] ) 

@app.route('/laserfold')
def laserFold():
	file_data = routingFilter().laserFold(session)

	return render_template('bend.html', file = file_data, weeks = availableWeeks, current_week =session['current_week'] ) 

@app.route('/drilldept')
def drillDept():
	file_data = routingFilter().drillDept(session)

	return render_template('bend.html', file = file_data, weeks = availableWeeks, current_week =session['current_week'] )

@app.route('/drumDept')
def drumDept():
	file_data = routingFilter().drumDept(session)

	return render_template('bend.html', file = file_data, weeks = availableWeeks, current_week =session['current_week'] )


@app.route('/wandwipe')
def wandWipe():
	file_data = routingFilter().wandWipe(session)

	return render_template('bend.html', file = file_data, weeks = availableWeeks, current_week =session['current_week'] )

@app.route('/wandload')
def wandLoad():
	file_data = routingFilter().wandLoad(session)

	return render_template('bend.html', file = file_data, weeks = availableWeeks, current_week =session['current_week'] )

@app.route('/wvc001')
def wvc001():
	file_data = routingFilter().wvc001(session)

	return render_template('bend.html', file = file_data, weeks = availableWeeks, current_week =session['current_week'] )

@app.route('/wdc001')
def wdc001():
	file_data = routingFilter().wdc001(session)

	return render_template('bend.html', file = file_data, weeks = availableWeeks, current_week =session['current_week'] )

@app.route('/wcim001')
def wcim001():
	file_data = routingFilter().wcim001(session)

	return render_template('bend.html', file = file_data, weeks = availableWeeks, current_week =session['current_week'] )

@app.route('/vcp001')
def vcp001():
	file_data = routingFilter().vcp001(session)

	return render_template('bend.html', file = file_data, weeks = availableWeeks, current_week =session['current_week'] )	

@app.route('/vcp002')
def vcp002():
	file_data = routingFilter().vcp002(session)

	return render_template('bend.html', file = file_data, weeks = availableWeeks, current_week =session['current_week'] )

@app.route('/uww001')
def uww001():
	file_data = routingFilter().uww001(session)

	return render_template('bend.html', file = file_data, weeks = availableWeeks, current_week =session['current_week'] )
 
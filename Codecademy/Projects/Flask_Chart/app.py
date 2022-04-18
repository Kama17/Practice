from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
	labels = ['01-09-2021','02-09-2021','03-09-2021','04-09-2021']
	data = [10,50,40, 100]

	return render_template('index.html', data = data, labels = labels)


if __name__ == '__main__':
	app.run(debug= True)
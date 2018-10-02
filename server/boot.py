from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
	return "Root"

@app.route('/test/<input>')
def test(input=None):
	data = {'input': input}
	return render_template('index.html', data=data)
	

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)

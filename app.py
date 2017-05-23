from flask import Flask, render_template, request;
import recommendLocation
import json 

with open('./key/test.json') as test_json:
    test = json.load(test_json)



app = Flask(__name__)

@app.route('/')
def index():
	return render_template('accounts.html', name = "refgjin")

@app.route('/analysis', methods = ['POST'])
def analysisEvent():
	#analysisList=nlp.listFromAccount(request.form['account']) # origin
	#analysisList=nlp.listFromAccount(test['calendar-hashkey']['1'])
	analysisList=recommendLocation.listFromAccountByCalendarHashkey(test['calendar-hashkey']['1'])
	#print(request.form)
	return render_template('analysisEvents.html', analysisList=analysisList)

if __name__ == '__main__':
	app.run('0.0.0.0',8585);
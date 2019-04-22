from flask import Flask, render_template,redirect,url_for,request,flash,session,jsonify
import os
from subprocess import call
import pandas as pd
app = Flask(__name__)
app.secret_key="ajsdykjdjash bkas dha sd"

@app.route('/')
def index():
		return render_template('index.html')

@app.route('/analyse',methods=['GET','POST'])
def analyse():
	data = open('input.json').read()
	result = pd.read_csv('out.csv',index_col=0)
	out = result['cuisine'].unique()
	return render_template('analyse.html',data=data,out=out)

@app.route('/try',methods=['GET','POST'])
def test():
	jsondata = {}
	if request.method == 'POST':
		ingredients=request.form.get("ingredients")
		jsondata["ingredients"]=ingredients.split(', ')
		jsondata['id']=1
		with open('input.json','w') as f:
			data=str(jsondata).replace("'",'"')
			f.write(f'[{data}]')
		command= "python cuisine_classification.py --predict input.json --out-file out.csv"
		try:
			retcode=call(command.split(),shell=True)
			flash('successfully predicted','success')
			return redirect('/analyse')
		except Exception as e:
			print('command error',e)
			flash('error in prediction','success')
	return render_template('test.html')


if __name__ == '__main__':
	app.run(host='127.0.0.1', port=8000, debug=True)

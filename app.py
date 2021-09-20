import os
from datetime import date
import re
from flask import Flask, render_template, url_for, json


minDate = date.today().strftime("%Y-%m-%d")

app = Flask(__name__)

json_url = os.path.join(app.static_folder,"data\\mca.json")
jData = json.load(open(json_url))

@app.route("/")
def index(fjsonData=jData,fmDate=minDate):
    return render_template('index.html',jsonData=fjsonData,mDate=fmDate)

if __name__=='__main__':
    app.run(debug=True)
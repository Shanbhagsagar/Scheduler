import requests
from datetime import date
from flask import Flask, render_template, request, redirect



minDate = date.today().strftime("%Y-%m-%d")

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home(mDate=minDate):
    return render_template("index.html",mDate=mDate)    


@app.route("/", methods=["POST"])
def scheduleData():

    batchName = request.form.get("batchName")
    semName = request.form.get("semName")
    subject = request.form.get("subject")
    facultyName = request.form.get("facultyName")
    lectDate = request.form.get("lectDate")
    fromTime = request.form.get("fromTime")
    toTime = request.form.get("toTime")
    message = request.form.get("message")

    return render_template("index.html",batchName=batchName,semName=semName,subject=subject,facultyName=facultyName,lectDate=lectDate,fromTime=fromTime,toTime=toTime,message=message,compSent=True)

@app.route('/background_process_test', methods=["POST"])
def background_process_test():

    batchName = request.form.get("batchName")
    semName = request.form.get("semName")
    subject = request.form.get("subject")
    facultyName = request.form.get("facultyName")
    lectDate = request.form.get("lectDate")
    fromTime = request.form.get("fromTime")
    toTime = request.form.get("toTime")
    message = request.form.get("message")

    base_url = 'https://api.telegram.org/bot1943744198:AAG_RIG8396YKaJ6Ya_1r1lmMkLIwZ7OAcs/sendMessage?chat_id=-592983235&text=Batch%20Name:%20{0}\nSemester:%20{1}\nSubject:%20{2}\nFaculty%20Name:%20{3}\nLecture%20Date:%20{4}\nFrom%20Time:%20{5}\nTo%20Time:%20{6}\nLink:%20{7}'.format(batchName,semName,subject,facultyName,lectDate,fromTime,toTime,message)
    print(base_url)
    requests.get(base_url)

    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)
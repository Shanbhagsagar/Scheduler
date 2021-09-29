import requests
import smtplib
import pickle
import secrets1 
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from datetime import date,datetime
from flask import Flask, render_template, request, redirect


minDate = date.today().strftime("%Y-%m-%d")

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home(mDate=minDate):
    return render_template("index.html", mDate=mDate)


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
    return render_template("index.html", batchName=batchName, semName=semName, subject=subject, facultyName=facultyName, lectDate=lectDate, fromTime=fromTime, toTime=toTime, message=message, compSent=True)


@app.route('/background_process_test', methods=["POST"])
def background_process_test():

    batchName = request.form.get("batchName")
    semName = request.form.get("semName")
    subject = request.form.get("subject")
    facultyName = request.form.get("facultyName")
    lectDate = request.form.get("lectDate")
    fromTime = request.form.get("fromTime")
    toTime = request.form.get("toTime")
    link = request.form.get("message")
      
    sch_gmail_id = secrets1.sch_gmail_id
    sch_gmail_pass = secrets1.sch_gmail_pass
    chatid = secrets1.chatid
    tel_api_token = secrets1.tel_api_token

    recieve = ['kasturismitha05@gmail.com', 'nmitdscheduler2021@gmail.com',
               'shettymegha098@gmail.com', "sagarshanbhag09@gmail.com", "thomasbenjohnson@gmail.com"]

    message = 'Subject: Lecture details of Subject - {}\n\nBatch Name: {}\nSemester: {} \nFaculty Name: {}\nLecture Date: {} \nTime: {} - {} \nLink: {} '.format(subject, batchName, semName, facultyName, lectDate, fromTime, toTime, link)
 

    # To schedule lecture in google calendar

    scopes = ['https://www.googleapis.com/auth/calendar']
    flow = InstalledAppFlow.from_client_secrets_file(
        "client_secret1.json", scopes=scopes)
    credentials = flow.run_local_server()
    credentials

    pickle.dump(credentials, open("token.pkl", "wb"))
    credentials = pickle.load(open("token.pkl", "rb"))
    service = build("calendar", "v3", credentials=credentials)

    # To retrieve individual date(date,month,year) and time(hour,minute)
    year, month, date = lectDate.split('-')
    start_hour, start_min = fromTime.split(':')
    end_hour, end_min = toTime.split(':')
    start_time = datetime(int(year), int(month), int(
        date), int(start_hour), int(start_min), 0)
    end_time = datetime(int(year), int(month), int(date),
                        int(end_hour), int(end_min), 0)
    timezone = 'Asia/Kolkata'
    event = {
        'summary': 'Lecture Details of  '+semName+' Subject '+subject+' '+' Faculty name '+facultyName,
        'location': 'NMITD, Dadar',
        'description': 'Lecture Link '+link,
        'start': {
            'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': timezone,
        },
        'end': {
            'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': timezone,
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }
    result = service.calendarList().list().execute()
    calendar_id = result['items'][0]['id']
    service.events().insert(calendarId=calendar_id, body=event).execute()

    # To send email
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(sch_gmail_id , sch_gmail_pass)
    server.sendmail(sch_gmail_id, recieve, message)

    server.quit()

    base_url = 'https://api.telegram.org/bot{0}/sendMessage?chat_id={1}&text=Batch%20Name:%20{2}\nSemester:%20{3}\nSubject:%20{4}\nFaculty%20Name:%20{5}\nLecture%20Date:%20{6}\nTime:%20{7}%20To%20{8}\nLink:%20{9}'.format(
        tel_api_token,chatid,batchName, semName, subject, facultyName, lectDate, fromTime, toTime, link)
    requests.get(base_url)

    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)

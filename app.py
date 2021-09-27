import requests,smtplib,pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from datetime import date
from flask import Flask, render_template, request, redirect
from datetime import datetime, timedelta



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
    print(lectDate)
    print(fromTime)
    print(toTime)
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
    link = request.form.get("message")

    recieve = ['kasturismitha05@gmail.com', 'nmitdscheduler2021@gmail.com', 'shettymegha098@gmail.com',"sagarshanbhag09@gmail.com","thomasbenjohnson@gmail.com"]

    message = """
        Subject: Lecture details of Subject %s
        Batch Name: %s
        Semester: %s
        Faculty Name:%s
        Lecture Date:%s
        Time: %s - %s
        Link: %s
        """
    # To schedule lecture in google calendar
    message = message % (subject, batchName, semName, facultyName, lectDate, fromTime, toTime, link)
    print(message)
    scopes = ['https://www.googleapis.com/auth/calendar']
    flow = InstalledAppFlow.from_client_secrets_file("client_secret1.json", scopes=scopes)
    credentials = flow.run_local_server()
    credentials
    
    pickle.dump(credentials, open("token.pkl", "wb"))
    credentials = pickle.load(open("token.pkl", "rb"))
    service = build("calendar", "v3", credentials=credentials)

    #To retrieve individual date(date,month,year) and time(hour,minute)
    year,month,date=lectDate.split('-')
    start_hour,start_min=fromTime.split(':')
    end_hour,end_min=toTime.split(':')
    start_time = datetime(int(year), int(month), int(date), int(start_hour), int(start_min), 0)
    end_time = datetime(int(year), int(month), int(date), int(end_hour), int(end_min), 0)
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

    #To send email
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login("nmitdscheduler2021@gmail.com", "Scheduler@2021")
    server.sendmail("nmitdscheduler2021@gmail.com",recieve, message)

    server.quit()

    #Telegram message
    # base_url = 'https://api.telegram.org/bot1943744198:AAG_RIG8396YKaJ6Ya_1r1lmMkLIwZ7OAcs/sendMessage?chat_id=-592983235&text=Batch%20Name:%20%7B0%7D/nSemester:%20%7B1%7D/nSubject:%20%7B2%7D/nFaculty%20Name:%20%7B3%7D/nLecture%20Date:%20%7B4%7D/nFrom%20Time:%20%7B5%7D/nTo%20Time:%20%7B6%7D/nLink:%20%7B7%7D%27'.format(batchName,semName,subject,facultyName,lectDate,fromTime,toTime,link)
    # print(base_url)
    # requests.get(base_url)

    base_url = 'https://api.telegram.org/bot1943744198:AAG_RIG8396YKaJ6Ya_1r1lmMkLIwZ7OAcs/sendMessage?chat_id=-592983235&text=Batch%20Name:%20{0}\nSemester:%20{1}\nSubject:%20{2}\nFaculty%20Name:%20{3}\nLecture%20Date:%20{4}\nFrom%20Time:%20{5}\nTo%20Time:%20{6}\nLink:%20{7}'.format(batchName,semName,subject,facultyName,lectDate,fromTime,toTime,link)
    print(base_url)
    requests.get(base_url)

    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask,render_template,redirect,request,session,url_for
from flask_sqlalchemy import SQLAlchemy
import secrets
import hashlib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
import random
import math


app = Flask(__name__)

db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.sqlite3'
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = '#@$#erSammy'


def send_to_email(r):
      from_address = 'imagesunsplash@gmail.com'
      user = r
      msg = MIMEMultipart()
      msg['From']=formataddr((str(Header('Unsplash Images', 'utf-8')), 'imagesunsplash@gmail.com'))
      
      msg['Subject']='Your Password Change Request OTP'
      html ='''<html>
      <head>
      <style>
      .title
      {
            
            color:red;
            font-size:2rem;
      }
      .subtitle
      {
            color:#000;
            font-size:18px;
      }
      a
      {
            text-decoration:none;
      }
      
      </style>
      </head>
      <body bgcolor="red">
      '''
      digits = "0123456789"
      OTP = "" 
      for i in range(4) : 
        OTP += digits[math.floor(random.random() * 10)]
      html+=f'<h1> Unsplash Password Reset Request</h1><br/><br/><p class="subtitle">Your OTP is : {OTP}</p></body></html>'
      msg.attach(MIMEText(html,'html'))
      # creates SMTP session 
      s = smtplib.SMTP('smtp.gmail.com', 587) 
      s.ehlo()
      s.starttls()
      s.ehlo()
      s.login(from_address,'#@$#erSammy')
      text = msg.as_string()
      s.sendmail(from_address,user,text)
      s.quit()
      return OTP
      


    


class Photo(db.Model):
      __tablename__ = 'unsplash_upload'
      id = db.Column(db.Integer,primary_key=True)
      type = db.Column(db.String(50))
      img_url = db.Column(db.String(1100))
      upload_by = db.Column(db.String(80))
      



class User(db.Model):
      __tablename__ = 'user'
      id = db.Column(db.Integer, primary_key=True)
      username = db.Column(db.String(30))
      password = db.Column(db.String(50))
      useremail = db.Column(db.String(30))
      otp = db.Column(db.String(60))


all_topics = [
    {"name":"Current Events","count":Photo.query.filter_by(type="Current Events").count()},
    {"name":"Covid-19","count":Photo.query.filter_by(type="Covid-19").count()},
    {"name":"Travel","count":Photo.query.filter_by(type="Travel").count()},
    {"name":"Nature","count":Photo.query.filter_by(type="Nature").count()},
    {"name":"Wallpapers","count":Photo.query.filter_by(type="Wallpapers").count()},
    {"name":"Textures","count":Photo.query.filter_by(type="Textures").count()},
    {"name":"Patterns","count":Photo.query.filter_by(type="Patterns").count()},
    {"name":"People","count":Photo.query.filter_by(type="People").count()},
    {"name":"Business","count":Photo.query.filter_by(type="Business").count()},
    {"name":"Work","count":Photo.query.filter_by(type="Work").count()},
    {"name":"Technology","count":Photo.query.filter_by(type="Technology").count()},
    {"name":"Animals","count":Photo.query.filter_by(type="Animals").count()},
    {"name":"Interiors","count":Photo.query.filter_by(type="Interiors").count()},
    {"name":"Architecture","count":Photo.query.filter_by(type="Architecture").count()},
    {"name":"Food","count":Photo.query.filter_by(type="Food").count()},
    {"name":"Athletics","count":Photo.query.filter_by(type="Athletics").count()},
    {"name":"Health","count":Photo.query.filter_by(type="Health").count()},
    {"name":"Wellness","count":Photo.query.filter_by(type="Wellness").count()},
    {"name":"Film","count":Photo.query.filter_by(type="Film").count()},
    {"name":"Fashion","count":Photo.query.filter_by(type="Fashion").count()},
    {"name":"Experimental","count":Photo.query.filter_by(type="Experimental").count()},
    {"name":"Art","count":Photo.query.filter_by(type="Art").count()},
    {"name":"Culture","count":Photo.query.filter_by(type="Culture").count()},
    {"name":"History","count":Photo.query.filter_by(type="History").count()},
    

]



@app.route('/',methods=["GET"])
def index():
    if not session.get("user") is None:
        return render_template('index.html',uname=session["user"],data=Photo.query.all(),category=all_topics)
    else:
        return render_template('index.html',uname=False,data=Photo.query.all(),category=all_topics)

@app.route('/<string:type>',methods=["GET"])
def type(type):
    if not session.get("user") is None:
        return render_template('type.html',uname=session["user"],data=Photo.query.filter_by(type=type),typeimage=type,count=Photo.query.filter_by(type=type).count())
    else:
        return render_template('type.html',uname=False,data=Photo.query.filter_by(type=type),typeimage=type,count=Photo.query.filter_by(type=type).count())



@app.route('/view/viewid=<string:pid>',methods=["GET"])
def view(pid):
    count=Photo.query.filter_by(id=pid).count()
    if count > 0:
        if not session.get("user") is None:
            return render_template('viewimage.html',uname=session["user"],data=Photo.query.filter_by(id=pid))
        else:
            return render_template('viewimage.html',uname=False,data=Photo.query.filter_by(id=pid))
    else:
        return redirect(url_for('index'))

    


@app.route("/all",methods=["GET"])
def all():
    if not session.get("user") is None:
        return render_template('all.html',data=all_topics,uname=session["user"],category=all_topics)
    else:
        return render_template('all.html',data=all_topics,uname=False,category=all_topics)

@app.route('/login', methods=["GET","POST"])
def login():
      if request.method == "POST":
            uemail = request.form.get('uemail')
            password = request.form.get('password')
            if len(uemail) == 0 and len(password) == 0:
                  return render_template('login.html',error="All Fields Required")
            else:
                  password = hashlib.md5(f'{password}'.encode()).hexdigest()
                  count = User.query.filter_by(useremail=uemail,password=password).count()
                  if count > 0 :
                        data=User.query.filter_by(useremail=uemail).first()
                        session["user"] = data.username
                        session["email"] = data.useremail
                        return redirect(url_for('index'))
                  else:
                        
                        return render_template('login.html',error="Invalid Username & Password")
      else:
            if not session.get("user") is None:
                return redirect(url_for('index'))
            else:
                return render_template('login.html')


@app.route('/profile',methods=["GET","POST"])
def profile():
    if request.method == "POST":
        pass
    else:
        if not session.get("user") is None:
            return render_template('profile.html',data=Photo.query.filter_by(upload_by=session["user"]),uname=session["user"],count=Photo.query.filter_by(upload_by=session["user"]).count())
        else:
            return render_template('login.html',error="You must be Signed In!");


@app.route('/logout', methods=["GET"])
def logout():
      session.pop("user", None)
      return redirect(url_for('index'))


@app.route("/upload",methods=["GET","POST"])
def upload():
    if request.method == "POST":
        imgUrl = request.form.get('imgUrl');
        imgType= request.form.get('type');
        postBy = request.form.get('uname');
        data = Photo(img_url=imgUrl,type=imgType,upload_by=postBy)
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        if not session.get("user") is None:
            return render_template('upload.html',uname=session["user"],options=all_topics)
        else:
            return render_template("login.html",error="You must be loggined before uploading...")


@app.route('/join',methods=["GET","POST"])
def create_account():
      if request.method == "POST":
            uname = request.form.get('uname')
            pass1 = request.form.get('pass1')
            pass2 = request.form.get('pass2')
            uemail = request.form.get('email')
            count = User.query.filter_by(username=uname).count()
            if len(uname) < 6 and len(pass1) <6 and len(uemail) <15:
                  error = "You must choose a username and password of 6 letter long"
                  return render_template('create_account.html',error=error)
            elif pass1!=pass2:
                error = "You must choose a username and password of 6 letter long"
                return render_template('create_account.html',error=error)
            elif count > 0 :
                  error = f"User with {uname} Already Exist"
                  return render_template('create_account.html', error=error)
            
            else:
                  data = User(username=uname,password = hashlib.md5(f'{pass1}'.encode()).hexdigest(),useremail=uemail)
                  db.session.add(data)
                  db.session.commit()
                  return render_template('login.html')
      else:
            if not session.get("user") is None:
                return redirect(url_for('index'))
            else:
                return render_template('create.html')



@app.route('/forget',methods=["GET","POST"])
def forget():
    if request.method == "POST":
        uemail = request.form.get("uemail");
        count = User.query.filter_by(useremail=uemail).count()
        if count > 0:
            otp=send_to_email(uemail)
            user = User.query.filter_by(useremail=uemail).first()
            user.otp=otp
            db.session.commit()
            return render_template('check_otp.html',message='Your OTP is sented to your email!')
        else:
            return render_template('forget.html',error="No User Found With this email!")


    else:
        return render_template('forget.html')



@app.route('/checkotp',methods=["GET","POST"])
def check_otp():
    if request.method == "POST":
        otp = request.form.get('otp')
        if len(otp) <0:
            return render_template('check_otp.html',error="Please Enter OTP")
        else:
            user = User.query.filter_by(otp=otp).first()
            if user.otp == otp:
                user.otp = ''
                return render_template('change.html')
            else:
                return render_template('check_otp.html',error="Invalid OTP")
       
    else:
        return render_template('check_otp.html')


@app.route('/change',methods=["GET","POST"])
def change():
    if request.method == "POST":
        pass1 = request.form.get('pass1')
        pass2 = request.form.get('pass2')
        umail = request.form.get('uemail')
        if pass1!=pass2:
            return render_template('change.html',error="Two Password Not Matched! Try Again!")
        else:
            user = User.query.filter_by(useremail=umail).first()
            user.password = str(hashlib.md5(f'{pass1}'.encode()).hexdigest())
            db.session.commit()
            return render_template('login.html',message="Password Reset Successfully")
        

    else:
        return render_template('change.html',error="Error in Changing Password")


if __name__ == "__main__":
    app.run(debug=True)

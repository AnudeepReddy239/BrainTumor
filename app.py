from flask import Flask, request, render_template, send_from_directory,session,flash
import pandas as pd
import os
import mysql.connector
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model

app = Flask(_name_)
app.config['SECRET_KEY'] = 'the random string'
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/user")
def user():
    return render_template("user.html")

@app.route("/reg")
def reg():
    return render_template("ureg.html")
@app.route('/regback',methods = ["POST"])
def regback():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        pwd=request.form['pwd']
        pno=request.form['pno']



    #email = request.form["email"]


        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="brain_tumor"
        )
        mycursor = mydb.cursor()
        sql = "select * from ureg"
        result = pd.read_sql_query(sql, mydb)
        email1 = result['email'].values
        print(email1)
        if email in email1:
            flash("email already existed","warning")
            return render_template('ureg.html', msg="email existed")
        sql = "INSERT INTO ureg (name,email,pwd,pno) VALUES(%s,%s,%s,%s)"
        val = (name, email, pwd, pno)
        mycursor.execute(sql, val)
        mydb.commit()
        flash("Your registration successfully completed", "success")

    return render_template('user.html', msg="registered successfully")
    print("Successfully Registered")

@app.route('/userlog',methods=['POST', 'GET'])
def userlog():
    global name, name1
    global user
    if request.method == "POST":

        username = request.form['email']
        password1 = request.form['pwd']
        print('p')
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="", database="brain_tumor")
        cursor = mydb.cursor()
        sql = "select * from ureg where email='%s' and pwd='%s'" % (username, password1)
        print('q')
        x = cursor.execute(sql)
        print(x)
        results = cursor.fetchall()
        print(results)
        if len(results) > 0:
            print('r')
            # session['user'] = username
            # session['id'] = results[0][0]
            # print(id)
            # print(session['id'])
            flash("Welcome to website", "success")
            return render_template('userhome.html', msg=results[0][1])
        else:
            flash("Invalid Email/password", "danger")
            return render_template('user.html', msg="Login Failure!!!")

    return render_template('user.html')
@app.route("/userhome")
def userhome():
    return render_template("userhome.html")

@app.route("/upload", methods=["POST", "GET"])
def upload():
    if request.method == 'POST':
        myfile = request.files['file']
        fn = myfile.filename
        mypath = os.path.join('images/', fn)
        myfile.save(mypath)

        print("{} is the file name".format(fn))
        print("Accept incoming file:", fn)
        print("Save it to:", mypath)

        classes = ['No Tumor', 'Tumor']

        new_model = load_model(r"alg\CNN.h5")
        test_image = image.load_img(mypath, target_size=(256, 256))
        test_image = image.img_to_array(test_image)
        test_image = test_image / 255
        test_image = np.expand_dims(test_image, axis=0)
        result = new_model.predict(test_image)

        print("Result:", result)
        print("Argmax of result:", np.argmax(result))

        prediction = classes[np.argmax(result)]  # Define prediction based on the result
        msg = ''
        if prediction == 'Tumor':
            msg = 'Chemotherapy uses drugs to kill tumor cells, Physical therapy, Occupational therapy, Speech therapy and Tutoring for school-age children.'

        return render_template("template.html", image_name=fn, text=prediction, msg=msg)
    else:
        return "Please upload an image."

@app.route('/upload/<filename>')
def send_image(filename):
        return send_from_directory("images", filename)
@app.route('/upload1')
def upload1():
    return render_template("upload.html")


@app.route("/about")
def about():
    return render_template("about.html")

if _name_ == "_main_":
    app.run(debug=True)
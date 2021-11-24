import json
from flask import Flask, render_template , request
from flask.wrappers import Response
from  get_ocr import  get_ocr
import os
import datetime
from werkzeug.utils import secure_filename
import csv
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route("/upload",methods=['POST','GET'])    
def upload():
    if request.method == 'POST':
        img = request.files.get('imagefile', '')
        img.save(os.path.join(os.getcwd() , "static" , secure_filename('img_test' + '.jpg')))
        img_path  = 'static/img_test.jpg'
        data , text , textnew , newpath= get_ocr(img_path)
    return render_template('edit_details.html' , data= data , text=text , img = newpath , textnew=textnew )

current_uid = {}
current_uid['id'] = "None"


@app.route("/submit",methods=['POST','GET'])    
def sub():
    if request.method == 'POST':
        global updated_data 
        updated_data = {}
        updated_data['DOC_type'] =  request.form.get('doctype')
        updated_data['Name'] =  request.form.get('name')
        updated_data['Gender']  = request.form.get('gender')
        updated_data['Birth year'] =  request.form.get('byear')
        updated_data['Uid'] = request.form.get('uid')
        current_uid['id'] = updated_data['Uid'] 
    return render_template('jsonify.html' , data = updated_data)



@app.route("/insert",methods=['POST','GET'])    
def insert():
    date = str(datetime.datetime.now())
    f = open("records.csv", "a")
    f.write(f"{updated_data['DOC_type']},{updated_data['Uid']},{updated_data['Name']},{updated_data['Birth year']},{updated_data['Gender']}, {date[0:10]},{date[11:19]}\n")
    f.close()
    return render_template('jsonify.html' , data = updated_data , msg=1)


@app.route("/downlaod",methods=['POST','GET'])    
def download():
    uid  = current_uid['id']
    json_file_path = f"static/document/{uid}.json"
    with open(json_file_path, 'r') as fp:
        json_data = json.load(fp)
    return Response(
            json_data,
            mimetype="text/json",
            headers={"Content-disposition":
                    f"attachment; filename={uid}.json"})

@app.route("/record", methods=['POST','GET'])     # page to view record of all users
def rec():
    val = []
    with open("records.csv", "r") as f:
        reader = csv.reader(f)
        for i in reader:
            val.append(i)
    return render_template('/records.html' , val = val)

if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host='0.0.0.0')

import os
from flask import Flask, flash, request, redirect, url_for, render_template
from flask import send_from_directory
from secret import access_key, secret_access_key, s3_bucket
from werkzeug.utils import secure_filename
import PIL
from PIL import Image, ImageFilter 
import cv2
import numpy as np
import boto3

s3 = boto3.client('s3',
                        aws_access_key_id = access_key,
                        aws_secret_access_key = secret_access_key)

# UPLOAD_FOLDER = '/home/subhan-khaliq/Downloads/uploads'
app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        # check if the post request has the file part
        if filename == "":
            return render_template('index1.html')
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
            # return render_template('index.html')
        if file:
            select = request.form.get('options')
            file = Image.open(file)
            if str(select) == "Guassian Blur":
                file = file.filter(ImageFilter.GaussianBlur)
            elif str(select) == "Median Filter":
                # applying the median filter 
                file = file.filter(ImageFilter.MedianFilter(size = 3)) 
            else:
                file = file.convert("L")
                # Detecting Edges on the Image using the argument ImageFilter.FIND_EDGES
                file = file.filter(ImageFilter.FIND_EDGES)
            aws_link = "put your aws s3 bucket link" + filename
            file.save(filename)
            s3.upload_file(
                        Bucket = s3_bucket,
                        Filename = filename,
                        Key = filename,
                    
                        )
            return redirect(aws_link)


    return redirect(request.url)




if __name__ == '__main__':
   app.run()

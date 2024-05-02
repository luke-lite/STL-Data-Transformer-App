from app import app
import os
from flask import render_template, flash, jsonify, request
from werkzeug.utils import secure_filename
from app.forms import UploadForm
import sqlite3
from utils import DataTransformer

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/upload_page', methods=['GET', 'POST'])
def upload_page():
    form = UploadForm()
    if form.validate_on_submit():
        month = form.month.data
        year = form.year.data
        csv_file = form.csv_file.data
        filename = f"Crime_{month}_{year}"  # Construct the filename
        filesrc = f"Crime_{month}_{year}.csv"
        upload_path = os.path.join('uploads', secure_filename(filesrc))
        csv_file.save(upload_path)

        with sqlite3.connect('database.db') as conn:
            DT = DataTransformer(filename='Crime_01_2024',
                                 upload_path='uploads/Crime_01_2024.csv',
                                 conn=conn)
            DT.full_update()

        flash('File uploaded successfully!')

        return "File uploaded successfully!"

    return render_template('upload_page.html', form=form)



@app.route('/check_file', methods=['GET'])
def check_file():
    filename = request.args.get('filename', None)
    if filename:
        upload_path = os.path.join('uploads', filename)
        file_exists = os.path.exists(upload_path)
        return jsonify({'exists': file_exists})
    else:
        return jsonify({'error': 'No filename provided'}), 400
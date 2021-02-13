import os

from possat3d import app
from possat3d.RINEXparser import satpos

from flask import render_template, request, flash, redirect, jsonify, send_file
from werkzeug.utils import secure_filename

@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route("/get_data", methods=['GET'])
def get_model():
    filename = os.path.join(app.config['RINEX_FILES_FOLDER'], 'gmez0380.21n')
    processed_pos = satpos.process_RINEX_file(filename)
    return jsonify(processed_pos)
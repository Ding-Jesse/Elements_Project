from multiprocessing import allow_connection_pickling
import os
from time import sleep
from flask import Flask, request, redirect, url_for, render_template,send_from_directory
from werkzeug.utils import secure_filename
from main import main_function
import time
app = Flask(__name__, template_folder='./')
UPLOAD_FOLDER = 'C:/Users/User/Desktop/BeamQC/INPUT'
OUTPUT_FOLDER = 'C:/Users/User/Desktop/BeamQC/OUTPUT'
ALLOWED_EXTENSIONS = set(['dwg'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 60 * 1024 * 1024  # 60MB

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html', template_folder='./')

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        uploaded_beam = request.files["file1"]
        uploaded_plan = request.files["file2"]
        beam_type = '大梁'
        sbeam_type = '小梁'
        beam_file =''
        plan_file = ''
        txt_file =''
        project_name = request.form['project_name']
        beam_ok = False
        plan_ok = False
        if uploaded_beam and allowed_file(uploaded_beam.filename):
            filename_beam = secure_filename(uploaded_beam.filename)
            beam_file = os.path.join(app.config['UPLOAD_FOLDER'], f'{project_name}-{filename_beam}')
            uploaded_beam.save(beam_file)
            beam_ok = True
        if uploaded_plan and allowed_file(uploaded_plan.filename):
            filename_plan = secure_filename(uploaded_plan.filename)
            plan_file = os.path.join(app.config['UPLOAD_FOLDER'], f'{project_name}-{filename_plan}')
            uploaded_plan.save(plan_file)
            plan_ok = True
        if beam_ok and plan_ok:
            # main function
            # txt_file = os.path.join(app.config['OUTPUT_FOLDER'],f'{project_name}-{beam_type}')
            # sb_txt_file = os.path.join(app.config['OUTPUT_FOLDER'],f'{project_name}-{sbeam_type}')
            # main_function(beam_file,plan_file,txt_file,sb_txt_file)
            filenames = [f'{project_name}-{beam_type}.txt',f'{project_name}-{sbeam_type}.txt']
            return render_template('result.html', filenames=filenames)
    return render_template('index.html')

@app.route('/results/<filename>')
def result_file(filename):
    response = send_from_directory(app.config['OUTPUT_FOLDER'],
                               filename)
    response.cache_control.max_age = 0
    return response
if __name__ == '__main__':
    app.run(host = '192.168.0.143',debug=True,port=8082)
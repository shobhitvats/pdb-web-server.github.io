from flask import Blueprint, request, render_template, redirect, url_for, flash
import os
import subprocess
import requests

routes = Blueprint('routes', __name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdb'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@routes.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file and allowed_file(file.filename):
                filepath = os.path.join(UPLOAD_FOLDER, file.filename)
                file.save(filepath)
                output = run_initial_code(filepath)
                return render_template('index.html', output=output)
        elif 'pdb_id' in request.form:
            pdb_id = request.form['pdb_id']
            pdb_file = fetch_pdb_file(pdb_id)
            if pdb_file:
                output = run_initial_code(pdb_file)
                return render_template('index.html', output=output)
            else:
                flash('PDB ID not found or could not be retrieved.')
    return render_template('index.html')

def fetch_pdb_file(pdb_id):
    url = f'https://files.rcsb.org/download/{pdb_id}.pdb'
    response = requests.get(url)
    if response.status_code == 200:
        pdb_file_path = os.path.join(UPLOAD_FOLDER, f'{pdb_id}.pdb')
        with open(pdb_file_path, 'wb') as f:
            f.write(response.content)
        return pdb_file_path
    return None

def run_initial_code(filepath):
    result = subprocess.run(['python3', 'scripts/initial_code.py', filepath], capture_output=True, text=True)
    return result.stdout if result.returncode == 0 else result.stderr
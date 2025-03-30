from flask import Flask, request, render_template
import os
import subprocess
import requests

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pdb_file = request.files.get('pdb_file')
        pdb_id = request.form.get('pdb_id')

        if pdb_file:
            # Save the uploaded file
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], pdb_file.filename)
            pdb_file.save(file_path)
        elif pdb_id:
            # Retrieve the PDB file from the internet
            url = f'https://files.rcsb.org/download/{pdb_id}.pdb'
            response = requests.get(url)
            if response.status_code == 200:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{pdb_id}.pdb')
                with open(file_path, 'wb') as f:
                    f.write(response.content)
            else:
                return "PDB ID not found.", 404
        else:
            return "No file or PDB ID provided.", 400

        # Execute the initial_code.py script
        result = subprocess.run(['python3', 'scripts/initial_code.py', file_path], capture_output=True, text=True)
        output = result.stdout

        return render_template('index.html', output=output)

    return render_template('index.html', output=None)

if __name__ == '__main__':
    app.run(debug=True)
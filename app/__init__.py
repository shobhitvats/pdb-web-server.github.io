from flask import Flask

app = Flask(__name__)

# Configuration settings can be added here
app.config['UPLOAD_FOLDER'] = 'uploads'  # Directory for uploaded files
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit upload size to 16 MB

# Initialize any extensions or configurations here

from app import routes  # Import routes after initializing the app to avoid circular imports
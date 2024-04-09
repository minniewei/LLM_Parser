from log import Log
from flask import Flask,  render_template, request, jsonify, send_file, make_response
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Set the upload and download folder
UPLOAD_FOLDER = 'uploads'
DOWNLOAD_FOLDER = 'download'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Check if the type of the file is txt
ALLOWED_EXTENSIONS = {'log'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Inex page
@app.route('/')
def index():
    return render_template('index.html')

# Upload the log file
@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    # Get the file and the name of the log
    file = request.files['file']
    LogName = request.form['LogName']
    LogFormat = request.form['LogFormat']

    # Check if the file is empty
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))

        # make a struceted log file
        log = Log(LogFormat, LogName)
        log.connection()
        log.write_csv_title() 

        # Open the log file
        with open(LogName+".log", 'r') as log_file:
            # Read the log file line by line
            for line in log_file:
                # Remove the newline character at the end of the line
                log_message = line.strip() 
                log.write_csv_content(log_message)
        return 'ok', 200

# Download the log file
@app.route('/download', methods=['GET'])
def download_file():
    LogName = request.args.get('LogName')
    return send_file("download/"+LogName+".csv", as_attachment=True)

@app.route('/download/check', methods=['GET'])
def check_download_file():
    log_name = request.args.get('LogName')
    file_path = "download/" + log_name + ".csv"
    print(file_path)
    if os.path.isfile(file_path):
        # if the file exists, return ok
        return "ok", 200
    else:
        # if the file does not exist, return file not found
        return "File not found", 404

if __name__ == '__main__':
    app.run(debug=True)
import os
from flask import Flask, send_file, jsonify

app = Flask(__name__)

folder_path = os.environ.get('mp3_folder')

@app.route('/api/mp3/<filename>', methods=['GET'])
def get_mp3(filename):
    # Assuming your mp3 files are stored in the network folder "\\mini-toaster\music\The Ventures - Oldies & Goldies"
    file_path = folder_path + '{}'.format(filename)

    try:
        return send_file(file_path, mimetype='audio/mpeg')
    except FileNotFoundError:
        return 'File not found', 404

@app.route('/api', methods=['GET'])
def list_mp3_files():
    files = os.listdir(folder_path)
    files_json = jsonify(files)
    print(files_json)
    return 1

if __name__ == '__main__':
    app.run()

from flask import Flask, send_file, jsonify
# use .env to load environment variables
import os
import dotenv
app = Flask(__name__)

# Load environment variables from .env file
dotenv.load_dotenv()
folder_path = os.environ.get('mp3_folder')

# New route for the root endpoint
@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello, World!'

@app.route('/api/mp3/<int:file_id>', methods=['GET'])
def get_mp3(file_id):
    try:
        files = [f for f in os.listdir(folder_path) if f.endswith('.mp3')]
        files.sort()

        if 0 <= file_id < len(files):
            filename = files[file_id]
            file_path = os.path.join(folder_path, filename)

            custom_message = "Hello, you accessed file_id {} which corresponds to {}".format(file_id, filename)

            print(custom_message)
            #play the file
            return send_file(file_path, as_attachment=True)

        else:
            return 'Invalid file_id', 404
    except Exception as e:
        return 'Error: {}'.format(str(e)), 500

if __name__ == '__main__':
    #run in port 5001, debug mode
    app.run(port=5001, debug=True)


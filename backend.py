from flask import Flask, render_template, send_file
import os
import dotenv

app = Flask(__name__)

dotenv.load_dotenv()
folder_path = os.environ.get('mp3_folder')


def get_music_list():
    files = [f for f in os.listdir(folder_path) if f.endswith('.mp3')]
    files.sort()
    return [{'file_id': i, 'name': os.path.splitext(f)[0]} for i, f in enumerate(files)]


@app.route('/', methods=['GET'])
def hello_world():
    music_list = get_music_list()
    return render_template('welcome.html', music_list=music_list)

# @app.route('/', methods=['GET'])
# def hello_world():
#     return render_template('welcome.html')

@app.route('/api/mp3/<int:file_id>', methods=['GET'])
def get_mp3(file_id):
    """
    Retrieve the MP3 file corresponding to the given file_id and render a template with the music player.

    Args:
        file_id (int): The ID of the MP3 file to retrieve.

    Returns:
        str: The rendered template with the music player if the file_id is valid.
        str: 'Invalid file_id' if the file_id is out of range.
        str: 'Error: <exception_message>' if an error occurs during the retrieval process.
    """
    try:
        files = [f for f in os.listdir(folder_path) if f.endswith('.mp3')]
        files.sort()

        if 0 <= file_id < len(files):
            filename = files[file_id]
            file_path = os.path.join(folder_path, filename)
            custom_message = "Hello, you accessed file_id {} which corresponds to {}".format(file_id, filename)
            mp3_url = f"/api/mp3/{file_id}/play"

            # Pass music_name and duration to the template
            music_name = os.path.splitext(filename)[0]  # Remove the file extension
            duration = get_duration(file_path)  # Get the duration of the MP3 file
            return render_template('player.html', custom_message=custom_message, mp3_url=mp3_url, music_name=music_name, duration=duration)

        else:
            return 'Invalid file_id', 404
    except Exception as e:
        return 'Error: {}'.format(str(e)), 500

@app.route('/api/mp3/<int:file_id>/play', methods=['GET'])
def play_mp3(file_id):
    try:
        files = [f for f in os.listdir(folder_path) if f.endswith('.mp3')]
        files.sort()

        if 0 <= file_id < len(files):
            filename = files[file_id]
            file_path = os.path.join(folder_path, filename)
            return send_file(file_path, as_attachment=False)

        else:
            return 'Invalid file_id', 404
    except Exception as e:
        return 'Error: {}'.format(str(e)), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)

from flask import Flask, render_template, request, jsonify
from colorama import Fore, Style

from constants import banner
from interface import ToucanStrikeInterface
import os

app = Flask(__name__)
terminal = ToucanStrikeInterface()


@app.route('/')
def index():
    return "working"


@app.route('/command', methods=['POST'])
def execute_command():
    command = request.form.get('command')
    print("input ", command)
    output = terminal.onecmd(command)
    print("output ", output)
    return output


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    # Save the file to the static folder
    file.save(os.path.join(app.static_folder, file.filename))
    command = "data " + str(os.path.join(app.static_folder, file.filename))
    output = terminal.onecmd(command)
    print("file ", output)

    output = terminal.onecmd("run")
    print("output ", output)
    return output


if __name__ == '__main__':
    app.run(debug=True)

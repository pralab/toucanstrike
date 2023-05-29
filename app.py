from flask import Flask, render_template, request, jsonify
from colorama import Fore, Style

from constants import banner
from interface import ToucanStrikeInterface

app = Flask(__name__)
terminal = ToucanStrikeInterface()

@app.route('/')
def index():
    return render_template('index.html', banner=Fore.YELLOW + banner + Style.RESET_ALL)

@app.route('/command', methods=['POST'])
def execute_command():
    command = request.form.get('command')
    print("input ",command)
    output = terminal.onecmd(command)
    print("output ",output)
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

    return jsonify({'message': 'File uploaded successfully'})

if __name__ == '__main__':
    app.run(debug=True)

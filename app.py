from flask import Flask, render_template, request
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

if __name__ == '__main__':
    app.run(debug=True)

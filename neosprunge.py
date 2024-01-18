from flask import Flask, request, jsonify, send_from_directory, abort
import os
import random
import string

app = Flask(__name__)
store_dir = '/path/to/pastes/path'

def generate_random_id(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@app.route('/', methods=['POST'])
def create_paste():
    if 'logger' in request.form:
        data = request.form['logger']
        paste_id = generate_random_id()
        paste_file_path = os.path.join(store_dir, f'{paste_id}.txt')

        with open(paste_file_path, 'w') as f:
            f.write(data)

        paste_url = f'http://neosprunge.local:9876/{paste_id}'
        return jsonify({'url': paste_url})

    return ('Invalid request', 400)

@app.route('/<paste_id>')
def get_paste(paste_id):
    paste_file_path = os.path.join(store_dir, f'{paste_id}.txt')
    if os.path.exists(paste_file_path):
        with open(paste_file_path, 'r') as f:
            data = f.read()
        return data, 200, {'Content-Type': 'text/plain; charset=utf-8'}
    else:
        return 'Please, use curl to send:\n' \
               ' stdin | curl -X POST -d "sprunge=<-" http://neosprunge.local:9876/', 200

@app.errorhandler(405)
def method_not_allowed(e):
    return 'NEOSPRUNGE          NEOSPRUNGE          NEOSPRUNGE\n' \
           '\n' \
           'Please, use curl to send:\n' \
           '\n' \
           '<command> | curl -X POST -d "logger=<-" http://neosprunge.local:9876\n' \
           '\n' \
           'Please refer issues to:\n' \
           'https://github.com/valeowoia/neosprunge\n' \
           '\n' \
           'WTFPL. No copyright reserved. Made in Poland in 2024', 200, {'Content-Type': 'text/plain; charset=utf-8'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9876)

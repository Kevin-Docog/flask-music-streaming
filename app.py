import json
import os
from flask import Flask, render_template, request, redirect, jsonify, abort, url_for, Response
from werkzeug.utils import secure_filename
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from flasgger import Swagger, swag_from

app = Flask(__name__)
app.config['MUSIC_FOLDER'] = 'static/music'
app.config['ALLOWED_EXTENSIONS'] = {'mp3'}
app.config['SWAGGER'] = {
    'title': 'Music API',
    'uiversion': 3
}
Swagger(app)

DATA_FILE = 'music_db.json'
os.makedirs(app.config['MUSIC_FOLDER'], exist_ok=True)

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'r') as f:
        music_db = json.load(f)
else:
    music_db = []

def save_music_db():
    with open(DATA_FILE, 'w') as f:
        json.dump(music_db, f, indent=4)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def get_new_id():
    return max((m['id'] for m in music_db), default=0) + 1

@app.after_request
def log_response_status(response):
    print(f"[{request.method}] {request.path} -> {response.status_code}")
    return response

@app.route('/')
def simple():
    return render_template('simple.html', entries=music_db, title='Simple Music Player')

@app.route('/design')
def design():
    return render_template('design.html', entries=music_db, title='Design Music Player')

@app.route('/<int:stream_id>')
def streammp3(stream_id):
    song = next((item['link'] for item in music_db if item['id'] == stream_id), None)
    if not song:
        abort(404)
    def generate():
        with open(os.path.join('static', song), "rb") as fwav:
            data = fwav.read(1024)
            while data:
                yield data
                data = fwav.read(1024)
    return Response(generate(), mimetype="audio/mp3")

@app.route('/api/music', methods=['GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'List of all music entries',
            'examples': {
                'application/json': [
                    {'id': 1, 'name': 'Song', 'genre': 'Pop', 'rating': 5, 'link': 'music/song.mp3'}
                ]
            }
        }
    }
})
def get_music():
    return jsonify(music_db), 200


@app.route('/api/music', methods=['POST'])
@swag_from({
    'consumes': ['multipart/form-data'],
    'parameters': [
        {
            'name': 'name',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'Name of the song'
        },
        {
            'name': 'genre',
            'in': 'formData',
            'type': 'string',
            'required': False,
            'description': 'Genre of the song'
        },
        {
            'name': 'rating',
            'in': 'formData',
            'type': 'integer',
            'required': True,
            'description': 'Rating of the song (1-5)'
        },
        {
            'name': 'file',
            'in': 'formData',
            'type': 'file',
            'required': True,
            'description': 'MP3 file to upload'
        },
    ],
    'responses': {
        302: {'description': 'Redirect after successful upload'},
        400: {'description': 'Missing or invalid fields'}
    }
})
def api_add_music():
    name = request.form.get('name')
    genre = request.form.get('genre', '')
    rating = request.form.get('rating')
    file = request.files.get('file')
    redirect_to = request.form.get('redirect_to', 'simple')

    if not name or not rating or not file:
        return jsonify({'error': 'Missing required fields'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400

    filename = secure_filename(file.filename)
    save_path = os.path.join(app.config['MUSIC_FOLDER'], filename)
    file.save(save_path)

    music = {
        'id': get_new_id(),
        'name': name,
        'link': f'music/{filename}',
        'genre': genre,
        'rating': int(rating)
    }
    music_db.append(music)
    save_music_db()

    if redirect_to not in ['simple', 'design']:
        redirect_to = 'simple'

    return redirect(url_for(redirect_to))




@app.route('/api/music/<int:music_id>', methods=['PUT'])
@swag_from({
    'parameters': [
        {'name': 'music_id', 'in': 'path', 'type': 'integer', 'required': True},
        {'name': 'name', 'in': 'formData', 'type': 'string', 'required': True},
        {'name': 'genre', 'in': 'formData', 'type': 'string'},
        {'name': 'rating', 'in': 'formData', 'type': 'integer', 'required': True}
    ],
    'responses': {
        200: {'description': 'Music updated'},
        400: {'description': 'Missing fields'},
        404: {'description': 'Music not found'}
    }
})
def api_update_music(music_id):
    music = next((m for m in music_db if m['id'] == music_id), None)
    if not music:
        return jsonify({'error': 'Not found'}), 404

    name = request.form.get('name')
    genre = request.form.get('genre', '')
    rating = request.form.get('rating')

    if not name or not rating:
        return jsonify({'error': 'Missing required fields'}), 400

    music.update({
        'name': name,
        'genre': genre,
        'rating': int(rating)
    })
    save_music_db()
    return jsonify({'message': 'Updated successfully'}), 200

@app.route('/api/music/<int:music_id>', methods=['DELETE'])
@swag_from({
    'parameters': [
        {'name': 'music_id', 'in': 'path', 'type': 'integer', 'required': True}
    ],
    'responses': {
        200: {'description': 'Music deleted'},
        404: {'description': 'Music not found'}
    }
})
def api_delete_music(music_id):
    music = next((m for m in music_db if m['id'] == music_id), None)
    if not music:
        return jsonify({'error': 'Not found'}), 404

    file_path = os.path.join(app.config['MUSIC_FOLDER'], os.path.basename(music['link']))
    if os.path.exists(file_path):
        os.remove(file_path)

    music_db[:] = [m for m in music_db if m['id'] != music_id]
    save_music_db()
    return jsonify({'message': 'Deleted successfully'}), 200

if __name__ == "__main__":
    port = 5000
    http_server = HTTPServer(WSGIContainer(app))
    print(f"Server running at http://localhost:{port}")
    print(f"Swagger UI available at http://localhost:{port}/apidocs")
    http_server.listen(port)
    IOLoop.current().start()

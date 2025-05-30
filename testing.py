import io
import os
import pytest
from app import app, music_db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        music_db.clear()
        os.makedirs(app.config['MUSIC_FOLDER'], exist_ok=True)
        yield client
        for f in os.listdir(app.config['MUSIC_FOLDER']):
            if f.endswith('.mp3'):
                os.remove(os.path.join(app.config['MUSIC_FOLDER'], f))

def create_dummy_mp3():
    return io.BytesIO(b"ID3DummyMP3Data")

def test_get_music_list(client):
    response = client.get('/api/music')
    assert response.status_code == 200
    assert response.json == []

def test_add_music_success(client):
    data = {
        'name': 'Test Song',
        'genre': 'Pop',
        'rating': '5'
    }
    file = (create_dummy_mp3(), 'test.mp3')
    response = client.post('/api/music', data={**data, 'file': file}, content_type='multipart/form-data')
    assert response.status_code == 302  # It redirects to /simple
    assert len(music_db) == 1
    assert music_db[0]['name'] == 'Test Song'

def test_add_music_missing_fields(client):
    data = {'name': '', 'rating': ''}
    file = (create_dummy_mp3(), 'test.mp3')
    response = client.post('/api/music', data={**data, 'file': file}, content_type='multipart/form-data')
    assert response.status_code == 400

def test_add_music_invalid_file_type(client):
    data = {'name': 'Song', 'rating': '5'}
    file = (io.BytesIO(b"fake content"), 'bad.txt')
    response = client.post('/api/music', data={**data, 'file': file}, content_type='multipart/form-data')
    assert response.status_code == 400


def test_update_music_success(client):
    test_add_music_success(client)
    music_id = music_db[0]['id']
    update_data = {
        'name': 'Updated Song',
        'genre': 'Rock',
        'rating': '4'
    }
    response = client.put(f'/api/music/{music_id}', data=update_data)
    assert response.status_code == 200
    assert music_db[0]['name'] == 'Updated Song'

def test_update_music_missing_fields(client):
    test_add_music_success(client)
    music_id = music_db[0]['id']
    update_data = {'name': '', 'rating': ''}
    response = client.put(f'/api/music/{music_id}', data=update_data)
    assert response.status_code == 400

def test_update_music_not_found(client):
    update_data = {'name': 'x', 'rating': '1'}
    response = client.put('/api/music/999', data=update_data)
    assert response.status_code == 404

def test_delete_music_success(client):
    test_add_music_success(client)
    music_id = music_db[0]['id']
    response = client.delete(f'/api/music/{music_id}')
    assert response.status_code == 200
    assert len(music_db) == 0

def test_delete_music_not_found(client):
    response = client.delete('/api/music/999')
    assert response.status_code == 404

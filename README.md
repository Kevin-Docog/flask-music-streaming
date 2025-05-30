# Enhanced Flask Music Player with Tornado Server

This is an enhanced version of a simple Flask-based music player app originally streaming static music files. The updated app adds full CRUD support, file uploads, persistence, and RESTful API endpoints while still using Tornado as the HTTP server.

---

## Features

- **Persistent music library** saved in `music_db.json`
- Upload `.mp3` music files via web form
- Add, update, and delete music entries (metadata + audio file)
- Stream music files on demand
- Two UI options:
  - **Simple UI** (`/`) — minimal interface
  - **Design UI** (`/design`) — Bootstrap styled interface
- RESTful API endpoints for programmatic access:
  - `GET /api/music` — list all music entries
  - `GET /api/music/<id>` — get a music entry by ID
  - `POST /api/music` — add a new music entry with file upload
  - `PUT /api/music/<id>` — update metadata of an existing music entry
  - `DELETE /api/music/<id>` — delete a music entry and its file
- Logging of all requests with method, path, and response status
- Validation of file upload type (`.mp3` only)
- Safe file name handling using `werkzeug.utils.secure_filename`

---

## Project Structure

- `app.py` — main Flask application with Tornado HTTP server integration
- `music_db.json` — JSON file storing music metadata persistently
- `static/music/` — directory storing uploaded music `.mp3` files
- `templates/simple.html` — simple music player UI
- `templates/design.html` — Bootstrap-styled music player UI

---

### Prerequisites

What things you need to install the software and how to install them

```
Python 3
Flask
Tornado Web Server
werkzeug
```

### Installing

Installing dependencies 
```
pip install -r requirements.txt
```
Once all packages are downloaded and installed run.

```
python app.py
```

## Running the tests

Open up your browser and visit
```
http://localhost:5000

```

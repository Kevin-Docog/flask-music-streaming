# 🎵 Enhanced Flask Music Player

This project is a fully enhanced music player built using **Flask** and served with **Tornado**. It supports uploading, playing, updating, and deleting `.mp3` music files through both a **web UI** and a **RESTful API** with **Swagger documentation**.

---

## 🚀 Features

- 🎼 **Persistent music library** stored in `music_db.json`
- 🔼 **Upload `.mp3` files** via web form
- 🔁 **Full CRUD support**:
  - Create, Read, Update, and Delete music metadata and files
- 🎧 **Stream music on demand** by ID
- 🌐 **Two UI views**:
  - `/` — Minimalist "Simple" player
  - `/design` — Bootstrap-styled "Design" player
- 🧠 **Swagger/OpenAPI Documentation** at `/apidocs`
- 🛡️ **Validation**:
  - Accepts only `.mp3` files
  - Safe file naming with `secure_filename()`
- 📋 **Request logging** with HTTP method, path, and response status

---

## 📂 Project Structure

```
├── app.py                 # Main Flask app with Tornado integration
├── music_db.json          # Stores music metadata persistently
├── static/
│   └── music/             # Uploaded `.mp3` files
├── templates/
│   ├── simple.html        # Minimal player UI
│   └── design.html        # Bootstrap-based player UI
```

---

## 🔗 API Endpoints

| Method | Endpoint                  | Description                      |
|--------|---------------------------|----------------------------------|
| GET    | `/api/music`              | List all music entries           |
| GET    | `/<int:stream_id>`        | Stream a music file by ID        |
| POST   | `/api/music`              | Upload a new music file          |
| PUT    | `/api/music/<id>`         | Update metadata for a music file |
| DELETE | `/api/music/<id>`         | Delete a music entry and file    |

---

## 🧪 Example API Usage

### Upload Music

```
POST /api/music
Content-Type: multipart/form-data
Fields:
  - name: My Song
  - genre: Rock
  - rating: 5
  - file: [MP3 file]
  - redirect_to: simple | design
```

### Update Music Metadata

```
PUT /api/music/1
Content-Type: application/x-www-form-urlencoded
Fields:
  - name: New Name
  - genre: Pop
  - rating: 4
```

### Delete Music

```
DELETE /api/music/1
```

---

## 📦 Requirements

- Python 3.x
- Flask
- Tornado
- flasgger
- werkzeug

Install with:

```bash
pip install -r requirements.txt
```

---

## 🧰 Running the App

```bash
python app.py
```

Visit:

```
http://localhost:5000/
http://localhost:5000/design
http://localhost:5000/apidocs
```

---

## 📝 Notes

- The server runs using Tornado for enhanced asynchronous handling.
- Music files are streamed directly from the `static/music` folder.
- Only `.mp3` files are accepted for upload.
- Use Swagger UI to test endpoints interactively.

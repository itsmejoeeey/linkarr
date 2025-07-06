<img width="128px" src="./docs/logo.png" alt="Linkarr"></img>

# Linkarr - Media Organizer

Organize your media library with ease - **without moving or duplicating your files!**

- 📦 **No file moving/copying:** Monitors for changes, and then organizes your media with symlinks only.
- 🧲 **Perfect for seeding/usenet:** Works with files managed by torrent or usenet clients.
- 🎬 **Jellyfin ready:** Import organized folders directly into your media server.
- 🐳 **Easy Docker deployment:** Run anywhere, just map your folders.

<br />

_Example:_

|   | 📂 **Before (Source Folder)** | 📂 **After (Organized Folder)** |
|---|-----------------------------|-------------------------------|
| TV | `/media/TV/`<br>└─ 📂`Show.Name.S01/`<br>&nbsp;&nbsp;&nbsp;&nbsp;├── `Show.Name.S01E01.1080p.mkv`<br>&nbsp;&nbsp;&nbsp;&nbsp;└── `Show.Name.S01E02.1080p.mkv`<br>└─📂 `Show.Name.S02/`<br>&nbsp;&nbsp;&nbsp;&nbsp;├── `Show.Name.S02E01.1080p.mkv`<br>&nbsp;&nbsp;&nbsp;&nbsp;└── `Show.Name.S02E02.1080p.mkv`<br>└── `Another.Show.Name.S04E07.1080p.mkv` | `/organized/TV/`<br>└─🗂️ `Show Name/`<br>&nbsp;&nbsp;&nbsp;&nbsp;└─📂 `Season 01/`<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── `Show.Name.S01E01.1080p.mkv`<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── `Show.Name.S01E02.1080p.mkv` <br>&nbsp;&nbsp;&nbsp;&nbsp;└─📂 `Season 02/`<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── `Show.Name.S02E01.1080p.mkv`<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── `Show.Name.S02E02.1080p.mkv` <br>└─🗂️ `Another Show Name/`<br>&nbsp;&nbsp;&nbsp;&nbsp;└─📂 `Season 04/`<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── `Show.Name.S04E07.1080p.mkv`  |
| Movies | `/media/Movies/`<br>└─📂 `Movie.Title.2023.1080p/`<br>&nbsp;&nbsp;&nbsp;&nbsp;└── `Movie.Title.2023.1080p.mkv`<br>└── `Another.Movie.Title.2024.1080p.mkv` | `/organized/Movies/`<br>└─📂 `Movie Title (2023)/`<br>&nbsp;&nbsp;&nbsp;&nbsp;└── `Movie.Title.2023.1080p.mkv` <br>└─📂 `Another Movie Title (2024)/`<br>&nbsp;&nbsp;&nbsp;&nbsp;└── `Another.Movie.Title.2024.1080p.mkv` |

---

## Getting started
### 🚀 Docker Usage (Recommended)

[![Docker Hub](https://dockerico.blankenship.io/image/itsmejoeeey/linkarr)](https://hub.docker.com/r/itsmejoeeey/linkarr)

You will need [Docker](https://docs.docker.com/get-docker/) installed on your system.

> **Important:** You must map your source and destination folders to the **same paths inside the container as on your host system**. This ensures symlinks work correctly.

```bash
docker run -d \
  -v /path/to/source:/path/to/source \
  -v /path/to/organized:/path/to/organized \
  -v $(pwd)/config.json:/config/config.json \
  itsmejoeeey/linkarr:latest
```

Or with Docker Compose:

```yaml
services:
  my-linkarr:
    image: itsmejoeeey/linkarr:latest
    container_name: linkarr
    # Pass in your config file below, by specifying the path on your host machine
    volumes:
      - /path/to/source:/path/to/source
      - /path/to/organized:/path/to/organized
      - ./config.json:/config/config.json
    restart: unless-stopped
```

> See [Configuration](#) for details on configuring.

   - Make sure to provide a valid `config.json`.
   - Replace `/path/to/source` and `/path/to/organized` with your actual media paths.

### Running manually

1. Install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Copy and edit the example config:
   ```bash
   cp config.example.json config.json
   # Edit config.json to match your source/destination folders and preferences
   ```

3. Run the organizer:
   ```bash
   cd src
   python -m linkarr.main ../config.json
   ```


## Configuration

See [`config.example.json`](/config.example.json) and [`src/linkarr/config.schema.json`](/src/linkarr/config.schema.json) for configuration options.

## Development

See [here for further information.](/docs/developing.md)

# Notes

Robust notes app with collections. Fullstack project built with a React + Vite frontend (TipTap rich-text editor) and a Flask + MongoDB backend.

Example video:



https://github.com/user-attachments/assets/5623bae3-e64f-470b-b5f5-3096cd1508fd



> Status: COMPLETE. Core CRUD flows for collections and notes are implemented.

---

## Features

- Rich-text editing powered by TipTap's Simple Editor template
- Organize notes into collections (create, rename, delete)
- Create, edit, and delete individual notes
- Context menus for quick actions on collections and notes
- Persistent storage in MongoDB
- Trash system with restore functionality for deleted items and collections
- Search across all collections with real-time results
- Three-page interface: Main notes page, dedicated Search page, and Trash management page
- Custom UI components with responsive design
---

## Tech Stack

- Frontend: React (Vite), TipTap v3, Radix UI, Floating UI, SCSS
- Backend: Flask, Flask-CORS, PyMongo
- Database: MongoDB (embedded local for dev, or cloud via Atlas)

TipTap Simple Editor reference: https://tiptap.dev/docs/ui-components/templates/simple-editor

---

## Project Structure

```
I:/Projects/Notes
├─ Frontend/
│  ├─ frontend/
│  │  ├─ src/
│  │  │  ├─ components/     (TipTap UI components - imported)
│  │  │  ├─ hooks/          (TipTap editor hooks - imported)
│  │  │  ├─ styles/         (TipTap SCSS styles - imported)
│  │  │  ├─ Pages/          (Custom application pages)
│  │  │  │  ├─ Main.jsx     (Main notes interface with collections)
│  │  │  │  ├─ Search.jsx   (Search interface with cross-collection search)
│  │  │  │  └─ Trash.jsx    (Trash management interface)
│  │  │  ├─ App.jsx         (Router setup and main app component)
│  │  │  ├─ App.css         (Custom styling for UI components)
│  │  │  └─ main.jsx        (React entry point)
│  │  ├─ index.html
│  │  ├─ package.json       (Vite scripts and dependencies)
│  │  └─ README.md          (Vite template)
├─ myDatabase.py            (Custom MongoDB helper class)
├─ ToDoList.py              (Flask API server; also spawns Vite dev server)
├─ requirements.txt         (Python dependencies)
├─ run_project.bat          (Starts backend; backend auto-starts frontend)
└─ README.md                (this file)
```

---

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.10+
- Windows (dev convenience: includes local MongoDB binaries under `MongoDB/Server/8.2/bin`)

You do not need an external MongoDB for local development. The backend launches a local `mongod.exe` on a free port and creates the `Notes` database automatically. Optionally, you can use a cloud MongoDB by setting `mongodbKey` (see below).

### Quick Start (Recommended)

1) Create/activate a virtual environment and install backend deps
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

2) Start the app
   ```powershell
   python ToDoList.py
   ```

What happens:
- Flask API starts on `http://localhost:5000`
- A local MongoDB instance is started in a `Data` folder on a free port
- The Vite dev server is started automatically and your browser opens to the local URL

Alternatively on Windows, you can run:
```bat
run_project.bat
```
This runs the same backend entrypoint, which in turn launches the frontend.

### Frontend (manual control)

You can also run the frontend yourself:
```bash
cd Frontend/frontend
npm install
npm run dev
```
The frontend expects the backend at `http://localhost:5000`.

### Using Cloud MongoDB (optional)

If you prefer using Atlas or another MongoDB, set an environment variable before starting the backend and comment/uncomment the connection line in `ToDoList.py` accordingly.

Comment out
```py
port = connectLocally()
connect = myDatabase.Database(f"mongodb://localhost:{port}/")
```

Uncomment
```py
connect = myDatabase.Database(os.environ["mongodbKey"])
```

- Env var name: `mongodbKey` (your MongoDB connection string)
- Default database name: `Notes`

Current defaults in `ToDoList.py`:
- Local mode (default): starts `mongod.exe` and connects to `mongodb://localhost:<randomPort>/`
- Cloud mode (optional): `connect = myDatabase.Database(os.environ["mongodbKey"])`

---

## Environment & Configuration

- CORS is restricted to localhost ports via regex: `http://localhost:\d+`
- Frontend dev server URL is detected from Vite output and opened automatically
- On first run, if no collections exist, a default collection named "New Category" is created

---

## API Reference (Flask)

Base URL: `http://localhost:5000`

### Main Operations
- `PUT /rename-collection/<newName>`: Rename current collection to `<newName>`
- `DELETE /delete-collection`: Move current collection to Trash database
- `POST /add-collection`: Create a new collection named "New Category" and return all collection names
- `POST /add-item-blank`: Insert a blank note into the current collection
- `GET /all-items`: Get all notes in the current collection
- `GET /all-collections`: List all collection names in the `Notes` database
- `GET /collection-name`: Get the name of the current collection
- `POST /set-collection` (`{ colName: string }`): Set active collection and return its items
- `PUT /edit-itemTitle/<itemID>` (`{ content: string }`): Update a note title by id
- `PUT /edit-itemBody/<itemID>` (`{ content: any, flat: string, destination: string }`): Update a note body by id
- `DELETE /delete-item/<itemID>`: Move a note to Trash by id

### Search Operations
- `GET /search/query-all-collections/<text>`: Search for text across all collections and return matching notes

### Trash Operations
- `GET /trash/get-all-elements`: Get all items and collections in trash
- `PUT /trash/restore-element/<id>/<type>/<destination>`: Restore item or collection from trash
- `DELETE /trash/delete-element/<id>/<type>`: Permanently delete item or collection from trash
- `DELETE /trash/delete-all-items`: Permanently delete all items from trash

---

## Frontend Scripts

From `Frontend/frontend/package.json`:

- `npm run dev`: Start Vite dev server
- `npm run build`: Production build
- `npm run preview`: Preview production build
- `npm run lint`: Lint sources

Key dependencies:

- `@tiptap/react`, `@tiptap/starter-kit`, extensions for highlight, lists, images, HR, subs/superscript, text-align
- `@radix-ui/react-*`, `@floating-ui/react`
- `axios`

---

## Custom Implementation Details

### Frontend Components
- **Main.jsx**: Main application interface with collection management, note editing, and context menus
- **Search.jsx**: Dedicated search page with cross-collection search functionality and inline editing
- **Trash.jsx**: Dedicated trash management page with restore/delete functionality
- **App.jsx**: Router setup connecting Main, Search, and Trash pages
- **App.css**: Custom styling for UI components including dropdowns, buttons, and layout

### Backend Architecture
- **myDatabase.py**: Custom MongoDB helper class with methods for CRUD operations, search functionality, and trash management
- **ToDoList.py**: Flask API server with comprehensive REST endpoints for notes, collections, and search; also manages Vite dev server lifecycle
- **Search System**: Cross-collection text search using MongoDB regex queries on flattened note content
- **Trash System**: Separate MongoDB database for soft-deleted items with restore capabilities

### Data Model
- Notes are stored as documents with `title`, `body`, and `flat` fields (flat field for search indexing)
- Collections are MongoDB collections within the `Notes` database
- Search functionality uses regex pattern matching on the `flat` field across all collections
- Trash items are stored in a separate `Trash` database with metadata
- The backend serializes MongoDB `_id` values to strings for the client
- The editor body accepts and saves TipTap JSON; HTML rendering is handled on the client

---

## Acknowledgements

- TipTap Simple Editor UI template: https://tiptap.dev/docs/ui-components/templates/simple-editor

---

## Roadmap

- [ ] Autosave and optimistic UI updates
- [Completed] Search and filtering across collections
- [ ] Export/import notes (HTML/Markdown)

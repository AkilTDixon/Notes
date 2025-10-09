# Notes

Robust notes app with collections, Fullstack project built with a React + Vite frontend (TipTap rich-text editor) and a Flask + MongoDB backend.

Example video:

https://github.com/user-attachments/assets/55a6c20d-0461-48da-a897-bfa4072486b7

> Status: Core CRUD flows for collections and notes are implemented.

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
- Database: MongoDB (Atlas or local)

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
├─ ToDoList.py              (Flask API server with CRUD operations)
├─ requirements.txt         (Python dependencies)
├─ run_project.bat          (Batch script to start both servers)
└─ README.md                (this file)
```

---

## Getting Started

### Prerequisites

- Node.js 18+ (or compatible)
- Python 3.10+
- MongoDB connection string (Atlas or local)

Set an environment variable for the backend to connect to MongoDB (name: `mongodbKey`). The database name used by the app is `Notes`.

Create a database named `Notes` in MongoDB cluster before starting the app.


### Backend (Flask API)

1) Create and activate a virtual environment (recommended)
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
   Or on bash:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2) Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3) Run the API
   ```bash
   python ToDoList.py
   ```

The API serves at `http://localhost:5000` by default.

First run tips:
- If there are no collections yet, use the frontend's “Create New” action (or call `POST /add-collection`) to create the initial collection after the `Notes` database exists.

### Frontend (React + Vite)

1) Install dependencies
   ```bash
   cd Frontend/frontend
   npm install
   ```

2) Start the dev server
   ```bash
   npm run dev
   ```

The app runs on the Vite dev server (e.g., `http://localhost:63401`). The frontend expects the backend at `http://localhost:5000` (see API calls in `src/Pages/Main.jsx`).

### Quick Start (Both Servers)

Use the provided batch script to start both servers simultaneously:
```bash
run_project.bat
```

This will open two command windows - one for the Flask backend and one for the Vite frontend.

---

## Environment & Configuration

- `mongodbKey` (env var): MongoDB connection string used by the Flask app (`ToDoList.py`).
- Default database: `Notes`
- Collections are created/renamed/deleted via API routes (see below). The active collection is managed server-side and selected by the frontend.

### Local development notes

- Backend CORS allows any localhost port during dev via regex: `http://localhost:\d+`.
  - If you prefer a fixed port, change the allowed origin in `ToDoList.py`.
- Frontend calls the backend at `http://localhost:5000` (default Flask port).
- Set `mongodbKey` in your OS environment before starting the backend.

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
- `PUT /edit-itemBody/<itemID>` (`{ content: any }`): Update a note body by id (TipTap JSON accepted)
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
- **ToDoList.py**: Flask API server with comprehensive REST endpoints for notes, collections, and search
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

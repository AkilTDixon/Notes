# Notes

Robust notes app with collections, Fullstack project built with a React + Vite frontend (TipTap rich-text editor) and a Flask + MongoDB backend.

https://github.com/user-attachments/assets/55a6c20d-0461-48da-a897-bfa4072486b7

> Status: Core CRUD flows for collections and notes are implemented.

---

## Features

- Rich-text editing powered by TipTap's Simple Editor template
- Organize notes into collections (create, rename, delete)
- Create, edit, and delete individual notes
- Context menus for quick actions on collections and notes
- Persistent storage in MongoDB
- Restore or permanently delete items/collections sent to the trash database
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
│  │  │  ├─ components/ (TipTap UI, nodes, templates)
│  │  │  ├─ hooks/       (editor and UI hooks)
│  │  │  ├─ styles/      (SCSS variables and animations)
│  │  │  ├─ App.jsx      (UI + calls to Flask API)
│  │  │  └─ main.jsx
│  │  ├─ index.html
│  │  ├─ package.json    (Vite scripts)
│  │  └─ README.md       (Vite template)
├─ myDatabase.py         (MongoDB helper class)
├─ ToDoList.py           (Flask API server)
└─ README.md             (this file)
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

The app runs on the Vite dev server (e.g., `http://localhost:63401`). The frontend expects the backend at `http://localhost:5000` (see API calls in `src/App.jsx`).

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

- `PUT /rename-collection/<newName>`: Rename current collection to `<newName>`
- `DELETE /delete-collection`: Move current collection to a Trash database and delete from active DB
- `POST /add-collection`: Create a new collection named "New Category" and return all collection names
- `POST /add-item-blank`: Insert a blank note into the current collection
- `GET /all-items`: Get all notes in the current collection
- `GET /all-collections`: List all collection names in the `Notes` database
- `GET /collection-name`: Get the name of the current collection
- `POST /set-collection` (`{ colName: string }`): Set active collection and return its items
- `PUT /edit-itemTitle/<itemID>` (`{ content: string }`): Update a note title by id
- `PUT /edit-itemBody/<itemID>` (`{ content: any }`): Update a note body by id (TipTap JSON accepted)
- `DELETE /delete-item/<itemID>`: Move a note to Trash by id

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

## Notes on Data Model

- Notes are stored as documents with fields like `title` and `body`.
- The backend serializes MongoDB `_id` values to strings for the client.
- The editor body accepts and saves TipTap JSON; HTML rendering is handled on the client.

---

## Acknowledgements

- TipTap Simple Editor UI template: https://tiptap.dev/docs/ui-components/templates/simple-editor

---

## Roadmap

- [ ] Autosave and optimistic UI updates
- [ ] Search and filtering across collections
- [ ] Export/import notes (HTML/Markdown)

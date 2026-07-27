# TaskFlow

A complete full-stack task manager: create tasks, mark them complete, filter them,
and delete them. FastAPI stores tasks in SQLite locally.

**Author:** Jahanzaib Muhammad
**Contact:** Jahanzebsiyal4@gmail.com

## Tech Stack

* **Backend:** FastAPI + SQLAlchemy + SQLite
* **Frontend:** HTML, CSS, vanilla JavaScript (no framework)
* **Deployment:** Vercel (serverless)

## Features

* Create, list, mark complete/incomplete, and delete tasks
* Filter view: All / Active / Completed
* Server-side validation via Pydantic (empty titles are rejected)

## Project Structure

```
taskflow/
├── api/
│   └── index.py        # Vercel serverless entrypoint (re-exports the FastAPI app)
├── static/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── main.py              # FastAPI app + routes
├── models.py             # SQLAlchemy models + DB session
├── schemas.py             # Pydantic request/response schemas
├── vercel.json             # Vercel build \& routing config
└── requirements.txt
```

## Running Locally

```bash
git clone <your-repo-url>
cd taskflow

python -m venv venv
# Windows:
venv\\Scripts\\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt

uvicorn main:app --reload
```

Then open `http://127.0.0.1:8000` in your browser.

The documented API is available at `http://127.0.0.1:8000/docs`, and a simple
deployment health check is available at `/health`.

## Deploying on Vercel

1. Push this project to a GitHub repository (including `api/index.py`, the
   `static/` directory, and `vercel.json`).
2. Go to [vercel.com](https://vercel.com) and sign in with GitHub.
3. Click **Add New -> Project**, then import your `taskflow` repo.
4. Vercel reads `vercel.json` automatically - no manual build/output
settings needed. Leave the framework preset as "Other" and click **Deploy**.
5. Once the build finishes, Vercel gives you a live URL
(e.g. `taskflow-yourname.vercel.app`) - open it to use the app.

### Important: SQLite on Vercel is not permanent storage

Vercel functions are serverless - there's no persistent disk. The app writes
its SQLite file to `/tmp`, which is wiped whenever the function cold-starts
(after periods of inactivity, or on redeploy). This means:

* The app **will work correctly** for adding/completing/deleting tasks during
a session.
* Data is **not guaranteed to survive** long gaps between requests or a new
deployment.

This is fine for demoing or submitting the assignment, but if you need tasks
to actually persist long-term in production, the fix is to swap SQLite for a
hosted database - Vercel Postgres or Neon (both have free tiers) work with
almost no code change since SQLAlchemy just needs a different `DATABASE\_URL`.
Let me know if you want that set up.

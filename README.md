# Journal a Forest

An AI-powered journaling companion that helps you grow a forest of self-discovery. Every journal entry plants a tree, creating a beautiful visual representation of your journey.

## Features

- **Mindful Journaling**: Beautiful, minimal interface designed to reduce anxiety around journaling
- **AI-Powered Insights**: Get gentle pattern observations (not advice) based on your entries
- **Forest Visualization**: Each entry unlocks a unique tree with varying rarity
- **Streak Tracking**: Build a habit with visual streak tracking
- **Pattern Recognition**: Discover themes and emotions in your writing
- **Personalized Prompts**: Get tailored prompts based on your history

## Tech Stack

### Frontend
- React 18 + TypeScript
- Vite for fast development
- Tailwind CSS for styling
- React Router for navigation
- Axios for API calls

### Backend
- Python 3.10+
- FastAPI for the API server
- SQLite for relational data
- ChromaDB for vector embeddings (stubbed, ready for implementation)
- Pydantic for data validation

## Project Structure

```
journal-a-forest/
├── frontend/          # React + TypeScript frontend
│   ├── src/
│   │   ├── pages/     # Page components
│   │   ├── services/  # API client
│   │   ├── contexts/  # React contexts
│   │   └── ...
│   └── package.json
├── backend/           # FastAPI backend
│   ├── app/
│   │   ├── routes/    # API endpoints
│   │   ├── schemas/   # Pydantic models
│   │   ├── db/        # Database setup
│   │   ├── services/  # Business logic
│   │   └── main.py    # FastAPI app
│   └── requirements.txt
└── README.md
```

## Setup Instructions

### Prerequisites

- Node.js 18+ and npm/yarn
- Python 3.10+
- pip or poetry for Python dependencies

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. (Optional) Set environment variables:
   Create a `.env` file in the backend directory:
   ```env
   OPENAI_API_KEY=your_key_here  # If using OpenAI for LLM features
   CHROMA_DB_PATH=./chroma_db     # Path for ChromaDB storage
   ```

5. Run the backend server:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

   The API will be available at `http://localhost:8000`
   API documentation: `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   # or
   yarn install
   ```

3. (Optional) Configure API base URL:
   Create a `.env` file in the frontend directory:
   ```env
   VITE_API_BASE_URL=http://localhost:8000
   ```

4. Run the development server:
   ```bash
   npm run dev
   # or
   yarn dev
   ```

   The frontend will be available at `http://localhost:5173`

## Running the Application

1. Start the backend server first (see Backend Setup above)
2. Start the frontend server (see Frontend Setup above)
3. Open your browser to `http://localhost:5173`

## Database Management

### Initialize Database

The database is automatically initialized when the backend starts. The SQLite database file `journal_forest.db` will be created in the backend directory.

### Reset Database

To reset the database (delete all data):

**Python script:**
```bash
cd backend
python -c "from app.db.database import reset_db; import asyncio; asyncio.run(reset_db())"
```

**Or manually:**
- Delete `backend/journal_forest.db`
- Restart the backend server (it will recreate the database)

### Reset ChromaDB (when implemented)

Delete the `chroma_db/` directory in the backend folder.

## API Endpoints

### Session Management
- `POST /api/session` - Create a new session

### Onboarding
- `POST /api/onboarding` - Submit brain dump and get starter prompts

### Prompts
- `GET /api/prompts/today?session_id=...` - Get today's prompts

### Entries
- `POST /api/entries` - Create a journal entry

### Garden/Forest
- `GET /api/garden?session_id=...` - Get streak and all trees

### Threads
- `POST /api/threads/{thread_id}` - Update thread status

### Insights
- `GET /api/insights/trends?session_id=...` - Get theme and emotion trends
- `GET /api/insights/weekly?session_id=...` - Get weekly reflection

### Memories
- `DELETE /api/memories?session_id=...` - Delete all memories for a session

## Implementation Notes

### Mock Data

Currently, the following features use deterministic mock data to enable full UI functionality:

- **LLM Analysis** (`app/services/llm_service.py`): Entry analysis, prompt generation, and weekly insights return mock but realistic responses
- **ChromaDB** (`app/services/chroma_service.py`): Vector storage is stubbed with TODO comments for implementation

### TODO: Implementing Real Features

#### LLM Integration
1. Set up Mistral API key in environment variables
2. Implement `analyze_entry()` in `app/services/llm_service.py`
3. Implement `generate_prompts()` for personalized prompts
4. Implement `analyze_brain_dump()` for onboarding insights
5. Implement `generate_weekly_insights()` for pattern reflection

#### ChromaDB Integration
1. Install and configure ChromaDB (already in requirements.txt)
2. Uncomment and configure Chroma client in `app/services/chroma_service.py`
3. Implement embedding generation (OpenAI or sentence-transformers)
4. Implement storage, search, and retrieval methods

#### Weekly Pattern Detection
1. Use ChromaDB to retrieve similar entries
2. Use LLM to identify patterns across entries
3. Generate thoughtful reflections (patterns, not advice)

## Development

### Frontend Development

```bash
cd frontend
npm run dev        # Start dev server
npm run build      # Build for production
npm run preview    # Preview production build
npm run lint       # Run ESLint
```

### Backend Development

```bash
cd backend
uvicorn app.main:app --reload --port 8000  # Start with auto-reload
```

### Code Style

- Frontend: ESLint with TypeScript strict mode
- Backend: PEP 8 style guide, type hints encouraged

## Environment Variables

### Backend
- `OPENAI_API_KEY` (optional): For LLM features when implemented
- Database and ChromaDB paths are configured in code (can be moved to env vars)

### Frontend
- `VITE_API_BASE_URL` (optional): Backend API URL, defaults to `http://localhost:8000`

## Troubleshooting

### Backend Issues

- **Database locked**: Make sure only one instance of the backend is running
- **Import errors**: Ensure virtual environment is activated and dependencies are installed
- **Port 8000 already in use**: Change port with `--port 8001` in uvicorn command

### Frontend Issues

- **API connection errors**: Verify backend is running on port 8000
- **CORS errors**: Check that backend CORS middleware allows `http://localhost:5173`
- **Build errors**: Clear `node_modules` and reinstall: `rm -rf node_modules && npm install`

## License

This project is a prototype demonstration.

## Acknowledgments

Designed as a mindful alternative to traditional journaling apps, focusing on gentle self-reflection and visual growth.


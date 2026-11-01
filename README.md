# lit-reviewer
This uses Google Gemini to autonomously search for papers using the OpenAlex API and generate a review pertaining to a given question.

## Setup
This app requires a `BRAVE_API_KEY` environment variable for web search.

### Log into gcloud
```bash
gcloud init
gcloud auth application-default login
```

### Start a local server
```bash
cd backend/app
pip install -r requirements.txt
python main.py
```

### Run the frontend
```bash
cd frontend
npm run dev
```

# Recipedia

A recipe finder that suggests dishes based on your ingredients and mood.

## Features:
- Ingredient based recipe matching
- Mood and category filtering
- Toggleable instructions
- Pagination for easy navigation
- Recipes appear sorted by the number of matching ingredients, from most to least
- Secure MongoDB connection using environment variables

## Tech Stack
- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, FastAPI
- **Database:** MongoDB (Atlas)
- **Others:** Pymongo, dotenv, CORS.

## Deployment
- The website has been deployed using Vercel (for frontend) and Render (for backend).
- If the user wants to clone the repository and work on it locally on their device, they are advised to edit the index.js file (comment regarding it is provided in the file itself).
- The deployed website is available on [https://recipedia-8ofv.vercel.app/](https://recipedia-8ofv.vercel.app/)

## Recipe Collection
- The recipes in this project were collected by scraping [seriouseats.com](https://www.seriouseats.com) using a custom script.
- The script used for scraping is located in the data/scrape.py, the failed_urls.txt contains the urls that weren't successfully scraped.
- It was used **only to seed the database** with publicly available recipe data.
- The database is already populated and hosted on MongoDB Atlas, so **no scraping is required by the user**.
- This script is included for educational purposes. Please respect the target website's terms of service before using or modifying it.

## Setup Instructions

### 1. Clone the repo
- git clone https://github.com/shraw06/Recipedia.git
- cd Recipedia

### 2. Navigate to the backend
cd backend

### 3. Create Environment File
cp .env.example .env

### 4. Install Dependencies
pip install -r requirements.txt

### 5. Run the FastAPI Server
uvicorn main:app --reload

### 6. Open the Frontend
Open index.html in your browser directly


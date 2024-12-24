# Motivational Meme Generator

A Flask-based web application that automatically generates inspirational memes using Google's Gemini AI API. The app creates unique motivational quotes, overlays them on beautiful background images, and allows users to download their personalized memes.

[Motivational Meme Generator Demo](https://drive.google.com/file/d/1fwmSzUf1_eXR_KBkEJmdykw3CKWRvQWg/view?usp=sharing)

## Features

- Automated generation of positive, inspirational quotes using Google's Gemini AI
- Semantic analysis to ensure quote quality and positivity
- Dynamic image fetching from free image providers
- Text overlay on images with automatic formatting
- Download capability for generated memes
- Persistent storage of generated memes in MongoDB
- Containerized deployment using Docker

## Technologies Used

- Backend: Python, Flask
- AI Integration: Google Gemini API
- Database: MongoDB
- Image Processing: Pillow
- Natural Language Processing: NLTK
- Containerization: Docker
- Additional: Beautiful Soup, Flask-CORS

## Prerequisites

- Python 3.8+
- Docker
- MongoDB
- Google Gemini API key

## Installation

1. Clone the repository:
  ```bash
  git clone https://github.com/shoham207/Dockerized-Flask-Mongo-App-Project
  cd Dockerized-Flask-Mongo-App-Project

2.Create and activate a virtual environment:
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate

3.Install dependencies:
  pip install -r requirements.txt

4.Set up environment variables:
  export GEMINI_API_KEY='your_api_key_here'
  export MONGODB_URI='your_mongodb_uri'

Docker Deployment

1.Build the Docker image:
  docker build -t meme-generator .

2.Run the container:
  docker run -p 5000:5000 -e GEMINI_API_KEY='your_api_key' -e MONGODB_URI='your_mongodb_uri' meme-generator

Usage

1.Start the application:
  python app.py
2.Open your web browser and navigate to http://localhost:5000
3.Click "Generate New Meme" to create a new motivational meme
4.Use the "Download Meme" button to save the generated imag

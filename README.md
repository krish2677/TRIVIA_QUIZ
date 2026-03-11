# 🎮 Trivia Quiz Web Application

A dynamic **web-based Trivia Quiz game** built using **Python and Flask**.  
The application fetches real-time quiz questions from the **Open Trivia Database API** and allows users to test their knowledge across different categories such as Science, History, Geography, Sports, and more.

The project includes an interactive interface, lifelines, timed questions, and a leaderboard system to make the quiz engaging and competitive.

---

## 🚀 Features

- 🎮 Multiple-choice trivia questions  
- 🌍 Questions fetched dynamically from the Open Trivia Database API  
- ⏱️ Timed quiz rounds with increasing difficulty  
- 🧠 Lifelines:
  - **50:50** (removes two incorrect options)
  - **Skip Question**
- 💰 Progressive reward system based on quiz levels  
- 🏆 Leaderboard system to track top players  
- 📊 Category selection (Science, History, Geography, etc.)  
- 🐳 Docker containerization for consistent environments  

---

## 🛠️ Technologies Used

- **Python**
- **Flask**
- **HTML**
- **CSS**
- **JavaScript**
- **Open Trivia Database API**
- **JSON (Leaderboard storage)**
- **Docker**
---

# ⚙️ Installation & Setup

## 1️⃣ Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/trivia-quiz.git
cd trivia-quiz
```
2️⃣ Create a Virtual Environment
```bash
python -m venv venv
```
Activate Virtual Environment
```bash
venv\Scripts\activate
```
3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
4️⃣ Run the Application
```bash
python app.py
```
Open your browser and visit:
```bash
http://127.0.0.1:5000
```
🐳 Running with Docker

This project is containerized using Docker, which allows the application to run consistently across different environments.

Build the Docker Image
```bash
docker build -t trivia-quiz .
```
Run the Container
```bash
docker run -p 5000:5000 trivia-quiz
```
Open the application in your browser:
```bash
http://localhost:5000
```
---

#  How It Works

The application retrieves quiz questions dynamically using the Open Trivia Database API.

1. The user selects a category.

2. The application fetches a random question from the API.

3. Answer options are shuffled before displaying.

4. The system tracks:

    - player progress

    - quiz levels

    - lifelines

    - reward money

5. Leaderboard data is stored in a JSON file.

---   

#  Learning Outcomes

Through this project, I gained experience in:

- Building backend applications using Flask

- Working with REST APIs

- Implementing session management

- Designing quiz logic with levels and lifelines

- Structuring a full-stack web application

- Using Docker for application containerization

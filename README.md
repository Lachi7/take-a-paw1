# 🐾 Take A Paw - Pet Adoption Platform

A Tinder-style pet adoption web application built with Flask, PostgreSQL, and modern CI/CD practices.

## 🚀 Features

- **Tinder-style Swiping**: Swipe right to like pets, left to skip
- **Compatibility Quiz**: Find pets that match your lifestyle  
- **Favorites System**: Save pets you're interested in
- **Admin Dashboard**: Manage pets and track adoptions
- **Responsive Design**: Works on desktop and mobile

## 🛠 Tech Stack

- **Backend**: Flask, Python
- **Database**: PostgreSQL (Neon)
- **Frontend**: HTML, CSS, JavaScript, Jinja2
- **Containerization**: Docker
- **CI/CD**: GitHub Actions
- **Deployment**: Render

## 📦 Quick Start

```bash
# Development
git clone https://github.com/your-username/take-a-paw.git
cd take-a-paw
pip install -r requirements.txt
cd src && python run.py

# Docker
docker build -t takeapaw .
docker run -p 5000:5000 takeapaw
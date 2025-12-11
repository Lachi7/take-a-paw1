# 🐾 Take A Paw - Pet Adoption Platform
A Tinder-style pet adoption web application built with Flask, PostgreSQL, and modern CI/CD practices.

## 📋 Table of Contents
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Production Environment](#-production-environment)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [Testing](#-testing)
- [Project Structure](#-project-structure)
- [API Endpoints](#-api-endpoints)
- [CI/CD Pipeline](#-cicd-pipeline)
- [Admin Panel](#-admin-panel)
- [Monitoring & Rollback](#-monitoring--rollback)
- [Collaborators](#-collaborators)
- [Contributing](#-contributing)
- [Troubleshooting](#-troubleshooting)
 
## 🚀 Features
- **Tinder-style Swiping**: Swipe right to like pets, left to skip.
- **Compatibility Quiz**: Find pets that match your lifestyle.
- **Favorites System**: Save pets you're interested in.
- **Admin Dashboard**: Manage pets and track adoptions.
- **Responsive Design**: Works on desktop and mobile.

## 🛠 Tech Stack
- **Backend**: Flask, Python
- **Database**: PostgreSQL (Neon)
- **Frontend**: HTML, CSS, JavaScript, Jinja2
- **Containerization**: Docker
- **CI/CD**: GitHub Actions
- **Deployment**: Render

### 🌐 Production Environment
- **Live Application**: [https://take-a-paw.onrender.com](https://take-a-paw.onrender.com)
- **Health Monitor**: [https://take-a-paw.onrender.com/health](https://take-a-paw.onrender.com/health)
- **API Status**: [https://take-a-paw.onrender.com/api/status](https://take-a-paw.onrender.com/api/status)

### 🏗️ Architecture
```

┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   GitHub        │    │   GitHub Actions │    │   Render        │
│   Repository    │───▶│   CI/CD Pipeline │───▶│   Production    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
│                        │                        │
│                        │                        │
▼                        ▼                        ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Code Changes  │    │   Auto Testing   │    │   Auto Deploy   │
│   & Commits     │    │   & Building     │    │   & Scaling     │
└─────────────────┘    └──────────────────┘    └─────────────────┘

````

## 🛠 Quick Start

### Prerequisites
- Python 3.12+
- Docker
- Git

### Local Development

1. **Clone and Setup**:
   ```bash
   git clone https://github.com/your-username/takeapaw.git
   cd take-a-paw1
2. **Virtual Environment**:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # OR
   .venv\Scripts\Activate.ps1 # Windows using PowerShell
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
```bash
   # Create .env file
   cat > .env << EOF
   DATABASE_URL=postgresql://user:pass@localhost:5432/takeapaw
   SECRET_KEY=your-secret-key-here
   CLOUDINARY_CLOUD_NAME=your-cloudinary-name
   CLOUDINARY_API_KEY=your-cloudinary-key
   CLOUDINARY_API_SECRET=your-cloudinary-secret
   EOF
```

5. **Initialize database:**
```bash
   cd src
   python run.py  # Creates tables on first run
   
   # Optional: Seed with sample data
   python seed.py
```

6. **Run application:**
```bash
   python run.py
```
   Visit: [http://localhost:5000](http://localhost:5000)

### Docker Development

1. **Build image:**
```bash
   docker build -t takeapaw:latest .
```

2. **Run container:**
```bash
   docker run -p 5000:5000 \
     -e DATABASE_URL="your-db-url" \
     -e SECRET_KEY="your-secret" \
     -e CLOUDINARY_CLOUD_NAME="your-cloud-name" \
     -e CLOUDINARY_API_KEY="your-api-key" \
     -e CLOUDINARY_API_SECRET="your-api-secret" \
     takeapaw:latest
```

3. **Or use docker-compose (if you have render.yaml configured):**
```bash
   docker-compose up
```

### 🧪 Testing

1. **Run all tests**:

   ```bash
   cd tests
   pytest test_app.py -v
   ```

2. **Run with coverage**:

   ```bash
   pytest --cov=src --cov-report=html
   ```

3. **Specific test category**:

   ```bash
   pytest tests/test_app.py::test_health_endpoint -v
   ```
   
## 📁 Project Structure

```
takeapaw/
├── .github/workflows/          # CI/CD Automation
│   ├── ci.yml                  # Continuous Integration
│   └── cd.yml                  # Continuous Deployment
├── src/                        # Application Source
│   ├── app/
│   │   ├── routes/
│   │   │   └── admin.py
│   │   │   └── auth.py
│   │   │   └── auth_utils.py
│   │   │   └── pets.py
│   │   │   └── quiz.py
│   │   │   └── system.py
│   │   ├── static/
│   │   │   └── style.css           # Styling
│   │   │   └── profile.css
│   │   ├── templates/              # Jinja2 Templates
│   │   │   ├── base.html           # Base Layout
│   │   │   ├── index.html          # Homepage
│   │   │   ├── pet_detail.html     # Pet Profiles
│   │   │   ├── quiz.html           # Matching Quiz
│   │   │   ├── admin.html          # Admin Dashboard
│   │   │   └── ...                 # Other Templates
│   │   ├── __init__.py              
│   │   ├── db.py            
│   │   ├── models.py            
│   ├── admin_create.py                  
│   ├── seed.py                  
│   ├── run.py                  # Flask Application
├── tests/                      # Test Suite
│   └── test_app.py             # Application Tests
├── Dockerfile                  # Container Definition
├── render.yaml                 # Multi-container Setup
├── requirements.txt            # Project Dependencies
└── README.md                   # Documentation
```

## 🔌 API Endpoints

### Application Routes

* `GET /` - Homepage with pet listings
* `GET /search` - Advanced pet search
* `GET /pet/<id>` - Individual pet profiles
* `GET /adopt/<id>` - Adoption application forms
* `GET /quiz` - Personality matching quiz
* `GET /favorites` - User favorite pets
* `GET /admin` - Administration dashboard

### JSON APIs

* `GET /api/pets` - All available pets (JSON)
* `GET /api/status` - System health and API status
* `GET /health` - Health check endpoint
* `GET /debug` - System debugging information

## 🔄 CI/CD Pipeline
### Pipeline Flow

1. **Code Push** → Trigger GitHub Actions
2. **CI Pipeline** → Run automated tests (pytest)
3. **CD Pipeline** → Build Docker image → Push to GHCR
4. **Auto-Deploy** → Render detects changes → Deploys automatically
5. **Live Update** → Application updated in production


## 🔐 Admin Panel

Take A Paw includes a fully featured **Admin Panel** for managing the platform.

### Admin Login
🔑 **Admin Login Page:**  
https://take-a-paw.onrender.com/admin/login

### Admin Features
The admin dashboard allows you to:

- Add, edit, and remove pets  
- View user accounts  
- Monitor adoption statistics  
- Manage favorites and listings  
- Access platform-wide metrics  
- Moderate system activity  

> ⚠️ Note: In demo mode, an admin session may be automatically enabled for easier access during testing.


## 📊 Monitoring & Rollback

### Health Monitoring

* **Internal**: Render application logs and metrics
* **External**: UptimeRobot with 5-minute checks
* **Custom**: `/health` endpoint for service status

### Performance Metrics

* Response time tracking
* Error rate monitoring
* Uptime statistics
* Deployment success rates

### Rollback Procedures

If deployment issues occur:

1. Access Render Dashboard → **Events** tab
2. Select Stable Deployment → **Click "Rollback"**
3. Confirm Action → System reverts instantly
4. **Auto-Deploy Disabled** → Prevents repeated issues
5. Re-enable After Fix → Settings → Auto-Deploy → Yes

## 👥 Collaborators

This project was created and maintained by:

- **Shahin Alakparov** – [GitHub Profile](https://github.com/shahin1717)
- **Nazrin Aliyeva** – [GitHub Profile](https://github.com/Lachi7)
- **Fidan Alizada** – [GitHub Profile](https://github.com/Fidannnnn)

## 🤝 Contributing

We welcome contributions! Please see our workflow:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/improvement`
3. **Commit changes**: `git commit -m 'Add some improvement'`
4. **Push to branch**: `git push origin feature/improvement`
5. **Open a Pull Request**

### Development Standards

* **Run tests before committing**:

  ```bash
  pytest
  ```

* **Check code quality**:

  ```bash
  flake8 src/ tests/
  ```

* **Format code**:

  ```bash
  black src/ tests/
  ```

## 🐛 Troubleshooting

### Common Issues

**Issue: "ModuleNotFoundError: No module named 'app'"**
```bash
# Solution: Ensure you're in the src/ directory
cd src
python run.py
```

**Issue: "DATABASE_URL is not set"**
```bash
# Solution: Create .env file or export variable
export DATABASE_URL="postgresql://localhost:5432/takeapaw"
```

**Issue: "Port 5000 already in use"**
```bash
# Solution: Kill process on port 5000
# Linux/Mac:
lsof -ti:5000 | xargs kill -9

# Windows:
netstat -ano | findstr :5000
taskkill /PID  /F

# Or change port in run.py:
app.run(host="0.0.0.0", port=8000)
```

**Issue: Image upload fails**
```bash
# Solution: Verify Cloudinary credentials
python -c "import cloudinary; print(cloudinary.config())"
```

**Issue: Tests fail with database errors**
```bash
# Solution: Install test database
# Use SQLite for quick tests (automatic)
# Or setup PostgreSQL for integration tests
```


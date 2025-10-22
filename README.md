# Take A Paw - Pet Adoption Platform 🐾

![Take A Paw](https://img.shields.io/badge/Take-A%20Paw-brightgreen)
![Python](https://img.shields.io/badge/Python-3.12%2B-blue)
![Flask](https://img.shields.io/badge/Flask-3.1.2-lightgrey)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue)
![CI/CD](https://img.shields.io/badge/CI%2FCD-Automated-green)
![License](https://img.shields.io/badge/License-MIT-green)

A modern, full-stack pet adoption platform that connects loving families with rescue animals. Built with Flask, Docker, and automated CI/CD pipelines for seamless deployment.

## 🌟 Features

### 🐕‍🦺 Core Adoption Platform
- **Smart Pet Search** - Filter by species, breed, location, and more
- **Personality Matching Quiz** - Find pets that match your lifestyle
- **Complete Adoption Workflow** - Online applications with admin approval
- **Favorites System** - Save and track pets you love
- **Real Shelter Data** - Integration with pet API services
- **Admin Dashboard** - Comprehensive management interface

### 🛠 Technical Excellence
- **Docker Containerization** - Consistent development and production environments
- **CI/CD Pipelines** - Automated testing, building, and deployment
- **RESTful APIs** - JSON endpoints for external integrations
- **Responsive Design** - Mobile-first Bootstrap interface
- **Production Ready** - Gunicorn WSGI server, health checks, monitoring

## 🚀 Live Deployment

### 🌐 Production Environment
**Live Application:** [https://takeapaw.onrender.com](https://takeapaw.onrender.com)  
**Health Monitor:** [https://takeapaw.onrender.com/health](https://takeapaw.onrender.com/health)  
**API Status:** [https://takeapaw.onrender.com/api/status](https://takeapaw.onrender.com/api/status)

### 📊 CI/CD Pipeline Status
![CI Pipeline](https://github.com/your-username/takeapaw/actions/workflows/ci.yml/badge.svg)
![CD Pipeline](https://github.com/your-username/takeapaw/actions/workflows/cd.yml/badge.svg)

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   GitHub        │    │   GitHub Actions │    │   Render        │
│   Repository    │───▶│   CI/CD Pipeline │───▶│   Production    │
│                 │    │                  │    │   Deployment    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                        │                        │
         │                        │                        │
         ▼                        ▼                        ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Code Changes  │    │   Auto Testing   │    │   Auto Deploy   │
│   & Commits     │    │   & Building     │    │   & Scaling     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🛠 Quick Start

### Prerequisites
- Python 3.12+
- Docker (optional)
- Git

### Local Development

1. **Clone and Setup**
   ```bash
   git clone https://github.com/your-username/takeapaw.git
   cd takeapaw
   ```

2. **Virtual Environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # OR
   .venv\Scripts\Activate.ps1   # Windows using powershel
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Application**
   ```bash
   cd src
   python app.py
   ```
   Visit: `http://localhost:5000`

### Docker Development
```bash
# Build image
docker build -t takeapaw:latest .

# Run container
docker run -p 5000:5000 takeapaw:latest

# Or with Docker Compose
docker-compose up
```

## 🧪 Testing

```bash
# Run all tests
cd tests
pytest test_app.py -v

# Run with coverage
pytest --cov=src --cov-report=html

# Specific test category
pytest tests/test_app.py::test_health_endpoint -v
```

## 📁 Project Structure

```
takeapaw/
├── .github/workflows/          # CI/CD Automation
│   ├── ci.yml                  # Continuous Integration
│   └── cd.yml                  # Continuous Deployment
├── src/                        # Application Source
│   ├── static/
│   │   └── style.css           # Styling
│   ├── templates/              # Jinja2 Templates
│   │   ├── base.html           # Base Layout
│   │   ├── index.html          # Homepage
│   │   ├── pet_detail.html     # Pet Profiles
│   │   ├── adopt_form.html     # Adoption Forms
│   │   ├── quiz.html           # Matching Quiz
│   │   ├── admin.html          # Admin Dashboard
│   │   └── ...                 # Other Templates
│   ├── app.py                  # Flask Application
│   └── requirements.txt        # Dependencies
├── tests/                      # Test Suite
│   └── test_app.py             # Application Tests
├── Dockerfile                  # Container Definition
├── docker-compose.yml          # Multi-container Setup
├── requirements.txt            # Project Dependencies
└── README.md                   # Documentation
```

## 🔌 API Endpoints

### Application Routes
- `GET /` - Homepage with pet listings
- `GET /search` - Advanced pet search
- `GET /pet/<id>` - Individual pet profiles
- `GET /adopt/<id>` - Adoption application forms
- `GET /quiz` - Personality matching quiz
- `GET /favorites` - User favorite pets
- `GET /admin` - Administration dashboard

### JSON APIs
- `GET /api/pets` - All available pets (JSON)
- `GET /api/status` - System health and API status
- `GET /health` - Health check endpoint
- `GET /debug` - System debugging information

## 🚀 Automated Deployment (CI/CD)

### Pipeline Flow
1. **Code Push** → Trigger GitHub Actions
2. **CI Pipeline** → Run automated tests (`pytest`)
3. **CD Pipeline** → Build Docker image → Push to GHCR
4. **Auto-Deploy** → Render detects changes → Deploys automatically
5. **Live Update** → Application updated in production

### Manual Trigger Demo
```bash
# Make a visible change for presentation
echo "# Demo auto-deployment" >> demo.txt
git add .
git commit -m "demo: testing CI/CD pipeline"
git push origin main
```

## 👥 Admin Features

Access `/admin` for comprehensive management:
- **Adoption Requests** - Review and approve applications
- **Pet Management** - Add/remove pets from platform
- **Statistics** - View adoption metrics and platform usage
- **User Management** - Monitor user activity and favorites

**Demo Access:** Admin session is automatically enabled for demonstration.

## ⚙️ Configuration

### Environment Variables
```env
SECRET_KEY=your-secret-key-here
FLASK_ENV=production
CAT_API_KEY=your-cat-api-key
DOG_API_KEY=your-dog-api-key
```

### Production Settings
- **WSGI Server:** Gunicorn
- **Process Manager:** Render
- **Health Checks:** Automatic monitoring
- **Logging:** Structured application logs

## 🔒 Security Features

- Non-root Docker user execution
- Environment variable configuration
- SQL injection prevention
- XSS protection through template escaping
- Secure headers configuration

## 📊 Monitoring & Analytics

### Health Monitoring
- **Internal:** Render application logs and metrics
- **External:** UptimeRobot with 5-minute checks
- **Custom:** `/health` endpoint for service status

### Performance Metrics
- Response time tracking
- Error rate monitoring
- Uptime statistics
- Deployment success rates

## 🚨 Rollback Procedures

If deployment issues occur:

1. **Access Render Dashboard** → Events tab
2. **Select Stable Deployment** → Click "Rollback"
3. **Confirm Action** → System reverts instantly
4. **Auto-Deploy Disabled** → Prevents repeated issues
5. **Re-enable After Fix** → Settings → Auto-Deploy → Yes

## 🤝 Contributing

We welcome contributions! Please see our workflow:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/improvement`)
3. **Commit** changes (`git commit -m 'Add some improvement'`)
4. **Push** to branch (`git push origin feature/improvement`)
5. **Open** a Pull Request

### Development Standards
```bash
# Run tests before committing
pytest

# Check code quality
flake8 src/ tests/

# Format code
black src/ tests/
```

## 🐛 Troubleshooting

### Common Issues

**Docker Build Failures**
```bash
# Clean build
docker system prune
docker build --no-cache -t takeapaw:latest .
```

**Port Conflicts**
```bash
# Use alternative port
docker run -p 5001:5000 takeapaw:latest
```

**Test Failures**
```bash
# Run with detailed output
pytest -v --tb=long

# Debug specific test
pytest tests/test_app.py::test_specific -v -s
```

### Getting Help
- Check existing [GitHub Issues](../../issues)
- Create new issue with detailed description
- Include environment details and error logs

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **The Cat API** & **The Dog API** for real pet data
- **Unsplash** for beautiful pet photography
- **Bootstrap** for responsive UI components
- **Font Awesome** for icon library
- **Render** for seamless deployment platform

## 📞 Support & Contact

- **Documentation:** [GitHub Wiki](../../wiki)
- **Issues:** [GitHub Issues](../../issues)
- **Discussions:** [GitHub Discussions](../../discussions)
- **Email:** support@takeapaw.com

---

<div align="center">

## 🐾 Happy Adoptions!

**Helping pets find their forever homes since 2025**

[Live Demo](https://takeapaw.onrender.com) •
[Report Bug](../../issues) •
[Request Feature](../../issues) •
[Contribute](../../pulls)

</div>

---

*Last updated: ${new Date().toLocaleDateString()}*

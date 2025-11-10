# 🧠 Smart Resume Checker using Machine Learning and Amazon Q AI

A professional AI-powered Resume Analysis Platform that automatically evaluates resumes and provides improvement suggestions using Machine Learning and Amazon Q AI.

## 🏗️ Architecture

```
smart-resume-checker/
├── frontend/          # React + Tailwind Professional UI
├── backend/           # Flask API with MySQL Integration
├── ml-service/        # ML Pipeline & Models
├── data/             # Training Datasets
├── scripts/          # Setup & Deployment Scripts
├── docker-compose.yml
└── README.md
```

## 🚀 Quick Start

### Option 1: Automated Setup
```bash
./scripts/setup.sh
./scripts/start-services.sh
```

### Option 2: Docker (Recommended)
```bash
docker-compose up --build
```

### Option 3: Manual Setup
```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Setup MySQL database
mysql -u root -p < scripts/init.sql

# 3. Train ML model
cd ml-service && python train_model.py

# 4. Start services
cd ml-service && python app.py &
cd backend && python app.py &
cd frontend && npm install && npm start
```

## 🌐 Access Points

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **ML Service**: http://localhost:5001
- **MySQL**: localhost:3306

## ✨ Professional Features

### 🤖 Machine Learning
- Resume quality scoring (0-100)
- ATS compatibility analysis
- Skill extraction & matching
- Job fit similarity scoring
- TF-IDF vectorization

### 🧠 AI Integration
- Amazon Q AI suggestions
- Grammar & tone analysis
- Content improvement tips
- Professional recommendations

### 💼 Professional Interface
- Multi-tab navigation
- Analysis history tracking
- System status dashboard
- MySQL database integration
- Responsive design

### 📊 Database Features
- User analysis history
- Performance tracking
- Data persistence
- Analytics dashboard

## 🔧 System Requirements

- Python 3.9+
- Node.js 18+
- MySQL 8.0+
- 4GB RAM minimum

## 📱 Usage

1. **Upload Tab**: Upload resume and get instant analysis
2. **History Tab**: View previous analyses by email
3. **Dashboard Tab**: Monitor system status and statistics

## 🛠️ Development

### Backend API Endpoints
- `POST /api/resume/upload` - Analyze resume
- `GET /api/history/<email>` - Get user history
- `GET /api/health` - Health check

### ML Service Endpoints
- `POST /analyze` - ML analysis
- `GET /health` - Service status

## 🔒 Security

- Input validation
- SQL injection protection
- File type restrictions
- Error handling

## 📈 Monitoring

- Real-time connection status
- Service health checks
- Performance metrics
- Error tracking
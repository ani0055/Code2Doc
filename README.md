# 📝 Code2Doc - AI-Powered Code Documentation Generator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/React-18+-61DAFB.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688.svg)](https://fastapi.tiangolo.com/)

> Transform your code into comprehensive documentation with AI in seconds. No more manual documentation headaches!

## ✨ Features

### 🤖 AI-Powered Analysis
- **Smart Documentation Generation** - Google Gemini AI analyzes your code and generates detailed, human-readable documentation
- **Multi-Language Support** - Python, JavaScript, Java, TypeScript support with Tree-sitter parsing
- **Code Quality Metrics** - Get cyclomatic complexity, maintainability index, and code smell detection
- **Interactive Flow Diagrams** - Visualize code structure with interactive, draggable flow charts

### 📊 Code Quality Insights
- **Complexity Analysis** - Understand your code's complexity at a glance
- **Maintainability Score** - Know how easy your code is to maintain
- **Improvement Suggestions** - Get AI-powered recommendations to improve code quality
- **Code Smell Detection** - Identify potential issues before they become problems

### 📄 Export & History
- **Multiple Export Formats** - Download as PDF, DOCX, or Markdown
- **Documentation History** - Access all your previously generated documentation
- **Project Management** - Organize documentation by project with edit and delete capabilities
- **Beautiful PDF Output** - Professional-looking documentation ready to share

### 🎨 Modern UI/UX
- **Responsive Design** - Works seamlessly on desktop, tablet, and mobile
- **Dark Mode Ready** - Eye-friendly interface
- **Interactive Diagrams** - Zoom, pan, and rearrange flow diagrams
- **Real-time Preview** - See your documentation as it's generated

## 🚀 Quick Start

### Prerequisites

- **Python 3.12+**
- **Node.js 18+**
- **PostgreSQL 14+**
- **Google Gemini API Key** ([Get it here](https://makersuite.google.com/app/apikey))

### Installation

#### 1️⃣ Clone the Repository
```bash
git clone https://github.com/ani0055/code2doc.git
cd code2doc
```

#### 2️⃣ Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your configuration
```

**Configure `.env`:**
```env
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/code2doc
SECRET_KEY=your-secret-key-here
GEMINI_API_KEY=your-gemini-api-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Create Database:**
```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE code2doc;
\q

# Run migrations (create tables)
python create_tables.py
```

**Start Backend Server:**
```bash
uvicorn app.main:app --reload
```

Backend will run at `http://localhost:8000`

#### 3️⃣ Frontend Setup
```bash
# Navigate to frontend directory (from root)
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run at `http://localhost:5173`

## 📖 Usage

### 1. Register/Login
- Create an account or login with existing credentials
- JWT authentication keeps you securely logged in

### 2. Upload Code
- **Upload a file** - Supports `.py`, `.js`, `.jsx`, `.ts`, `.tsx`, `.java`
- **Paste code** - Copy-paste directly into the text area

### 3. Generate Documentation
- Choose whether to generate flow diagrams
- AI analyzes your code in seconds
- View quality metrics, documentation, and diagrams

### 4. Review & Export
- Read AI-generated documentation with syntax highlighting
- Explore interactive flow diagrams
- Check code quality metrics and suggestions
- Export to PDF, DOCX, or Markdown

### 5. Access History
- View all previously analyzed projects
- Re-export old documentation
- Edit project names
- Delete old projects

## 🏗️ Architecture

### Tech Stack

**Frontend:**
- React 18+ with Vite
- Axios for API calls
- react-markdown for rendering
- vis-network for flow diagrams
- Modern CSS with glassmorphism

**Backend:**
- FastAPI (Python web framework)
- SQLAlchemy ORM
- PostgreSQL database
- Tree-sitter for code parsing
- Google Gemini AI for documentation
- JWT authentication
- Radon & Lizard for code metrics

### Project Structure
```
code2doc/
├── backend/
│   ├── app/
│   │   ├── api/           # API endpoints
│   │   ├── models/        # Database models
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── services/      # Business logic
│   │   ├── utils/         # Helper functions
│   │   ├── config.py      # Configuration
│   │   ├── database.py    # Database connection
│   │   └── main.py        # FastAPI app
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── services/      # API service layer
│   │   ├── App.jsx        # Main app component
│   │   ├── App.css        # Styles
│   │   └── main.jsx       # Entry point
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

## 🔧 Configuration

### Environment Variables

**Backend (.env):**
```env
DATABASE_URL=postgresql://user:password@localhost:5432/code2doc
SECRET_KEY=your-super-secret-key
GEMINI_API_KEY=your-gemini-api-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Supported Languages

- Python (`.py`)
- JavaScript (`.js`, `.jsx`)
- TypeScript (`.ts`, `.tsx`)
- Java (`.java`)

*More languages coming soon!*

## 📊 Code Quality Metrics

Code2Doc analyzes:

- **Lines of Code** - Total and source lines
- **Cyclomatic Complexity** - How complex your code logic is
- **Maintainability Index** - 0-100 score of code maintainability
- **Halstead Metrics** - Volume, difficulty, and effort
- **Code Smells** - Potential issues and anti-patterns

## 🎯 Roadmap

- [ ] Support for more languages (C++, Go, Rust, PHP)
- [ ] Batch processing (analyze entire projects)
- [ ] GitHub integration (auto-generate docs for repos)
- [ ] Team collaboration features
- [ ] Custom documentation templates
- [ ] Real-time collaboration
- [ ] API for third-party integrations
- [ ] VS Code extension

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Use ESLint for JavaScript/React code
- Write meaningful commit messages
- Add tests for new features
- Update documentation

## 🐛 Bug Reports

Found a bug? Please open an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Screenshots (if applicable)
- Your environment (OS, Python version, Node version)

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Google Gemini AI](https://ai.google.dev/) for powerful code analysis
- [Tree-sitter](https://tree-sitter.github.io/) for robust code parsing
- [FastAPI](https://fastapi.tiangolo.com/) for the excellent Python framework
- [vis-network](https://visjs.org/) for interactive diagrams
- [React](https://reactjs.org/) for the UI framework

## 📧 Contact

**Animesh Gawhale**  - aniemsh.rgawhale@gmail.com

**Project Link:** [https://github.com/ani0055/code2doc](https://github.com/ani0055/code2doc)

---

⭐ **Star this repo** if you find it helpful!

Made with ❤️ by [Animesh Gawhale](https://github.com/ani0055)
```

---

## **Additional Files to Create**

### **1. LICENSE (MIT License)**

Create `LICENSE` file:
```
MIT License

Copyright (c) 2025 Aniemsh Gawhale

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

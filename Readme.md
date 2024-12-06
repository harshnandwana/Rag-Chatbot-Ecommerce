# AI-Powered Client Intelligence Platform

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.8+
- pip
- uvicorn
- ollama
- redis
- beautifulsoup

### Installation

```bash
# Clone the repository
git clone <your-repository-url>
cd <project-directory>

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt
```

## 🖥️ Server Commands

### 1. Start Development Server
```bash
uvicorn app.main:app --reload
```

### 2. Onboard a New Client
```bash
curl -X POST "http://127.0.0.1:8000/api/onboard" \
-H "Content-Type: application/json" \
-d '{
  "customer_id": "example",
  "website_url": "https://example.com"
}'
```

### 3. Query Client Information
```bash
curl -X POST http://localhost:8000/api/query \
-H "Content-Type: application/json" \
-d '{
  "customer_id": "example",
  "question": "what does this company do"
}'
```

## 🔒 License
GNU General Public License v3.0

## 📝 Notes
- Replace `example` with actual customer details
- Ensure server is running before executing commands
- Check network connectivity if issues arise

## 🛠️ Troubleshooting
- Verify all dependencies are installed
- Confirm correct endpoint URLs
- Check Python and pip versions

Sources

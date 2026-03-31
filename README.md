# 🌊 NaukriFlow

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Made with Python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

Automate your Naukri profile updates to stay at the top of recruiter searches. **NaukriFlow** "touches" your profile daily, ensuring you appear as a recently active candidate in search results.

---

## ✨ Features
- **Profile Touching**: Automatically updates your profile (via mobile number/profile refresh) to trigger "Recently Updated" status.
- **Resume Anti-Hash**: Optionally modifies your PDF resume by adding invisible random characters to bypass "duplicate file" detection.
- **Headless Support**: Runs in the background without interrupting your work.
- **Secure Credentials**: Uses environment variables (`.env`) for safe credential management.

## 🛠️ Prerequisites
- [Python 3.10+](https://www.python.org/downloads/)
- [Google Chrome Browser](https://www.google.com/intl/en/chrome/)
- A Naukri.com account 

## 🚀 Getting Started

### 1. Installation
Clone the repository and set up a virtual environment:

```bash
git clone https://github.com/your-username/NaukriFlow.git
cd NaukriFlow

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .\.venv\Scripts\Activate.ps1  # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration
Copy the environment template and fill in your details:
```bash
cp .env.example .env
```
Update `.env` with your Naukri credentials and local file paths.

### 3. Run the Script
```bash
python naukri.py
```

## 📖 Documentation
For a deep dive into how **NaukriFlow** works, check out the [DOCUMENTATION.md](DOCUMENTATION.md).

## 🛡️ Disclaimer
This script is not affiliated with or endorsed by Naukri.com. It is intended for personal use only. Ensure compliance with Naukri.com’s terms of service. Use responsibly and at your own risk.

---
*If you find this project helpful, consider leaving a ⭐ star.*



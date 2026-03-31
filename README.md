# 🌊 NaukriFlow

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Made with Python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Stealth Mode](https://img.shields.io/badge/Stealth%20Mode-Active-blue.svg)](https://github.com/satyajeetramnit/NaukriFlow)

Automate your Naukri profile updates to stay at the top of recruiter searches. **NaukriFlow** "touches" your profile daily with human-like interaction, ensuring you appear as a recently active candidate in search results.

---

## ✨ Features
- **Profile Syncing**: Automatically updates your profile (via mobile number/profile refresh) to trigger "Recently Updated" status.
- **Stealth Protection**: Built-in `selenium-stealth` integration to bypass bot detection and maintain account safety.
- **Resume Anti-Hash**: Optionally modifies your PDF resume by adding invisible random characters to bypass "duplicate file" detection.
- **Secure Credentials**: Uses environment variables (`.env`) for safe, local credential management.

## 🛠️ Prerequisites
- [Python 3.10+](https://www.python.org/downloads/)
- [Google Chrome Browser](https://www.google.com/intl/en/chrome/)
- A Naukri.com account 

## 🚀 Getting Started

### 1. Installation
Clone the repository and set up a virtual environment:

```bash
git clone https://github.com/satyajeetramnit/NaukriFlow.git
cd NaukriFlow

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .\.venv\Scripts\Activate.ps1  # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration
Copy the provided environment template and fill in your details:
```bash
cp .env.example .env
```
> [!IMPORTANT]
> Edit the `.env` file with your Naukri credentials and absolute file paths for your resume.

### 3. Run the Script
```bash
python naukri.py
```

## 📖 Documentation
For a deep dive into the architecture and utility functions of **NaukriFlow**, check out the [DOCUMENTATION.md](DOCUMENTATION.md).

## 🛡️ Disclaimer
This script is not affiliated with or endorsed by Naukri.com. It is intended for personal use only. Ensure compliance with Naukri.com’s terms of service. Use responsibly and at your own risk.

---
*If you find this project helpful, consider leaving a ⭐ star.*



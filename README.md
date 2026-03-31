# 🌊 NaukriFlow

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Made with Python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Stealth Mode](https://img.shields.io/badge/Stealth%20Mode-Active-blue.svg)](https://github.com/satyajeetramnit/NaukriFlow)

Automate your Naukri profile updates to stay at the top of recruiter searches. **NaukriFlow** "touches" your profile daily with human-like interaction, ensuring you appear as a recently active candidate in search results.

---

## ✨ Features
- **Multi-Account Support**: Manage and automate multiple generic Naukri flows sequentially from a single `accounts.json` configuration file.
- **Profile Syncing**: Automatically triggers a profile save event to grant you "Recently Updated" status.
- **Stealth Protection**: Built-in `selenium-stealth` integration to bypass basic bot detection and maintain account safety.
- **Resume Anti-Hash**: Optionally modifies your PDF resume by adding invisible random characters to bypass "duplicate file" ATS detection.
- **Secure Credentials**: Uses `accounts.json` or environment variables (`.env`) for safe credential management.

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
NaukriFlow supports both single and multi-account setups.

**Recommended: Multi-Account Setup (`accounts.json`)**
Copy the example JSON and fill in your details:
```bash
cp accounts.example.json accounts.json
```
Edit `accounts.json` with your credentials and relative paths to your resumes (e.g., `resumes/my_resume.pdf`). 

**Fallback: Single Account Setup (`.env`)**
If you prefer the classic environment variable approach for a single account:
```bash
cp .env.example .env
```
*(Note: If `accounts.json` exists, it will take priority over `.env`!)*

### 3. Headless Mode
By default, the script will visibly open a browser window. If you want it to run invisibly in the background, set the `RUN_HEADLESS` environment variable to `true`:
```bash
export RUN_HEADLESS=true
```

### 4. Run the Script
```bash
python naukri.py
```

## ⏱️ Automation / Scheduling

**⚠️ Important**: Operating this script on cloud platforms (like **GitHub Actions, AWS, Heroku**) is **NOT RECOMMENDED**. Naukri's security systems actively detect traffic from data centers and will enforce a strict OTP / CAPTCHA block preventing the initial headless login.

We highly recommend running this locally using your computer's built-in scheduler (like Cron on Mac/Linux) while it is powered on. 

### Local Mac/Linux Auto-Pilot (Cron Job Setup)
Open your terminal and type `crontab -e`. Add the following lines to run the script silently every day at 8:00 AM and 1:30 PM:

```bash
0 8 * * * cd /path/to/NaukriFlow && RUN_HEADLESS=true /path/to/NaukriFlow/.venv/bin/python naukri.py >> cron.log 2>&1
30 13 * * * cd /path/to/NaukriFlow && RUN_HEADLESS=true /path/to/NaukriFlow/.venv/bin/python naukri.py >> cron.log 2>&1
```

## 📖 Documentation
For a deep dive into the architecture and utility functions of **NaukriFlow**, check out the [DOCUMENTATION.md](DOCUMENTATION.md).

## 🛡️ Disclaimer
This script is not affiliated with or endorsed by Naukri.com. It is intended for personal use only. Ensure compliance with Naukri.com’s terms of service. Use responsibly and at your own risk.

---
*If you find this project helpful, consider leaving a ⭐ star.*



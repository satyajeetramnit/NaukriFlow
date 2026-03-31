# Technical Documentation - NaukriFlow 🌊

## Overview
**NaukriFlow** is a modern, Python-based automation tool that maintains your visibility on the Naukri.com job portal by periodically updating your profile. Recruiters often filter for "recently active" or "frequently updated" profiles, and this script ensures your profile remains at the top of their search results by "touching" it with minimal updates.

## System Architecture

The script follows a sequential execution flow:
1.  **Configuration Load**: Evaluates the `accounts.json` registry. If unavailable, falls back to the `.env` singleton. The loop dynamically processes each `account` context.
2.  **Stealth Setup**: Initializes a fresh Selenium WebDriver per account iteration using the `selenium-stealth` library to bypass common bot detection mechanisms.
3.  **Auth Layer**: Executes Naukri login using the injected context.
4.  **Profile Touch**: 
    - Navigates to the Profile page.
    - Clicks the edit icon on the Basic Details modal and triggers a "Save" event to legally refresh the "Last Updated" timestamp without destructive edits.
5.  **Resume Management (Optional)**:
    - If `updatePDF = True`, modifies the PDF located at `original_resume_path` by appending invisible random strings to alter the file hash, saving it to `modified_resume_path`.
    - Uploads the designated active resume to Naukri's servers.
6.  **Session Termination**: Logs out, safely closes the browser, and tears down the driver to prevent session bleed-over before processing the next account.

## Core Components

### 1. `naukri.py` (Main Logic)
- **`naukriLogin(account)`**: Orchestrates the login process using specific dictionary contexts, handles post-login pop-ups, and checks DOM markers for success.
- **`UpdateProfile(driver)`**: Locates the *Basic Details* edit modal and triggers a "Sync" action.
- **`UpdateResume(account)`**: Uses `reportlab` and `pypdf` to inject random hidden text into the PDF, ensuring unique hashes for ATS.
- **`UploadResume(driver, path)`**: Locates the hidden file input element and uploads the resume dynamically.

#### Utility Functions
- **`get_accounts()`**: Bootstraps the execution array, prioritizing a localized `accounts.json` over a legacy `.env`.
- **`try_click(xpath)`**: Silently handles optional UI elements (popups/skip buttons) without noisy error logs.
- **`get_element(locator)`**: A robust wrapper for finding elements with modern, variable timeouts.

### 2. `constants.py` (Configuration Fallbacks)
- Modernized loader that pulls environment variables from `.env` acting strictly as the single-user fallback utility.

### 3. `test.py` (Unit Testing)
- Unit tests for the PDF modification engine.
- Smoke tests for the login flow (headless/stealth mode).

## Advanced Features

- **Stealth Mode Shield**: Uses `selenium-stealth` to emulate real human interactions (user-agent, vendor, WebGL renders).
- **Anti-Hash Detection**: By modifying the PDF content, it ensures the update is registered by the system even if no content changes.
- **Humanized Jitter**: Includes random sleep delays and jitter to simulate natural human activity.

## Requirements & Setup

### Prerequisites
- Python 3.10+
- Google Chrome Browser
- ChromeDriver (Managed automatically by Selenium 4.x)

### Dependencies
- `selenium`: Browser automation.
- `selenium-stealth`: Bot detection bypass.
- `python-dotenv`: Secure configuration management.
- `reportlab`: PDF hidden layer generation.
- `pypdf`: PDF merging/manipulation.

## Deployment & Automation (Cloud vs Local)

Given sophisticated bot-checker platforms like Cloudflare and internally developed systems by Naukri, extreme care must be taken in *where* this script runs:

- **Local Cron (Recommended)**: Because residential IPs are heavily trusted, running this via a scheduler (like `cron` on macOS/Linux or Task Scheduler on Windows) locally on your laptop guarantees the highest success rate. 
- **Cloud Workflows (Deprecated/Not Recommended)**: Running on GitHub Actions, DigitalOcean, or AWS EC2 will consistently flag IP blocks. The script executes perfectly, but Naukri aggressively throws an inescapable OTP / Two-Factor Authentication requirement when accessed via Datacenter IP ranges, locking out headless executions.

## Troubleshooting
- **Chrome Version Mismatch**: Ensure your Chrome browser is updated. Selenium 4.x handles drivers automatically, but extreme version gaps may cause issues.
- **Headless Detection / OTP Locks**: If you are trying to run the script remotely, you will likely hit an OTP requirement. Ensure you are running locally. You can toggle the UI visibility by passing the environment variable `export RUN_HEADLESS=true`.

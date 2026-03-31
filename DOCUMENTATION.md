# Technical Documentation - NaukriFlow 🌊

## Overview
**NaukriFlow** is a modern, Python-based automation tool that maintains your visibility on the Naukri.com job portal by periodically updating your profile. Recruiters often filter for "recently active" or "frequently updated" profiles, and this script ensures your profile remains at the top of their search results by "touching" it with minimal updates.

## System Architecture

The script follows a sequential execution flow:
1.  **Stealth Setup**: Initializes Selenium WebDriver with the `selenium-stealth` library to bypass common bot detection mechanisms.
2.  **Auth Layer**: Loads credentials from a secure `.env` file and performs a login.
3.  **Profile Touch**: 
    - Navigates to the Profile page.
    - Updates the "Mobile Number" field to trigger a profile save event.
4.  **Resume Management (Optional)**:
    - Modifies the PDF resume by adding invisible random characters to ensure the file hash is different.
    - Re-uploads the modified resume to Naukri's servers.
5.  **Session Termination**: Logs out and safely closes the browser.

## Core Components

### 1. `naukri.py` (Main Logic)
- **`naukriLogin()`**: Orchestrates the login process, handles pop-ups, and verify successful entry.
- **`UpdateProfile()`**: Selects the profile edit section and triggers a "Sync" action.
- **`UpdateResume()`**: Uses `reportlab` and `pypdf` to inject random hidden text into the PDF.
- **`UploadResume()`**: Locates the file input element and uploads the resume with verification.

#### Utility Functions
- **`try_click(xpath)`**: Silently handles optional UI elements (popups/skip buttons) without noisy error logs.
- **`get_element()`**: A robust wrapper for finding elements with modern timeouts.
- **`pathlib` integration**: All file system operations use the object-oriented `Path` library for cross-platform reliability.

### 2. `constants.py` (Configuration)
- Modernized loader that prioritizes environment variables from `.env` over hardcoded fallbacks.

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

## Troubleshooting
- **Chrome Version Mismatch**: Ensure your Chrome browser is updated. Selenium 4.x handles drivers automatically, but extreme version gaps may cause issues.
- **Access Denied**: If you see an "Access Denied" page from Naukri, follow the **Stealth Mode** instructions or ensure you are not running from a blocked IP range.
- **Headless Detection**: Some advanced bot-checkers still detect headless browsers. If login fails repeatedly, try running with `headless = False` in `naukri.py`.

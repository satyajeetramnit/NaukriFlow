# Technical Documentation - NaukriFlow

## Overview
**NaukriFlow** is a Python-based automation tool that maintains your visibility on the Naukri.com job portal by periodically updating your profile. Recruiters often filter for "recently active" or "frequently updated" profiles, and this script ensures your profile remains at the top of their search results by "touching" it with minimal updates.

## System Architecture

The script follows a sequential execution flow:
1.  **Environment Setup**: Initializes Selenium WebDriver (Chrome).
2.  **Authentication**: Logs into Naukri.com using credentials from `constants.py`.
3.  **Profile Touch**: 
    - Navigates to the Profile page.
    - Updates the "Mobile Number" field (often just re-submitting the same number) to trigger a profile save event.
4.  **Resume Management (Optional)**:
    - Modifies the PDF resume by adding invisible random characters to ensure the file hash is different.
    - Re-uploads the modified resume to Naukri's servers.
5.  **Session Termination**: Logs out and safely closes the browser.

## Core Components

### 1. `naukri.py` (Main Logic)
- **`naukriLogin()`**: Orchestrates the login process, handles pop-ups (Skip/Close), and verifies successful entry.
- **`UpdateProfile()`**: Selects the profile edit section and triggers a "Save" action.
- **`UpdateResume()`**: Uses `reportlab` and `pypdf` to inject random hidden text into the PDF.
- **`UploadResume()`**: Locates the file input element and uploads the resume.
- **`ci(xpath_part)`**: A utility function to create case-insensitive XPaths, making the script more resilient to minor UI changes.

### 2. `constants.py` (Configuration)
- Defines URLs, credentials, and file paths.
- **Note**: Currently lacks `.env` support (to be added in future updates).

### 3. `test.py` (Unit Testing)
- Basic testing for the PDF modification logic.
- Smoke tests for the login flow (headless).

## Feature Details

- **Headless Mode**: Can run in the background without a visible browser window.
- **Anti-Hash Detection**: By modifying the PDF content, it bypasses the system's "No Change" detection, ensuring the update is registered.
- **Case-Insensitive Selectors**: Uses `translate()` in XPaths to handle inconsistent UI casing.

## Requirements & Setup

### Prerequisites
- Python 3.10+
- Google Chrome Browser
- ChromeDriver (Managed automatically by Selenium 4.x)

### Dependencies
- `selenium`: Browser automation.
- `reportlab`: Generating PDF layers for hidden text.
- `pypdf`: Merging PDF layers.

## Troubleshooting
- **Chrome Version Mismatch**: Ensure your Chrome browser is updated. Selenium 4.x handles drivers automatically, but extreme version gaps may cause issues.
- **Element Not Found**: Naukri frequently updates its UI. If the script fails, check the XPaths in `naukri.py` against the current live site.
- **Headless Detection**: Some sites block headless browsers. If login fails repeatedly, try running with `headless = False`.

## Contributing
Follow the [Contribution Guidelines](contributing.md) to report bugs or suggest features.

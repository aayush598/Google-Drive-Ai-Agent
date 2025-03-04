# Google Drive AI Agent

## 📌 Project Overview

The **Google Drive AI Agent** is an advanced file management system powered by AI. This tool automates file categorization, duplicate removal, renaming, sensitive data detection, permission management, and log analysis using **Google Drive API**, **Gemini AI**, and **Streamlit**.

## 🚀 Features

### 🔹 File Management

- **Fetch Files:** Retrieves file details from Google Drive and stores them in an SQLite database.
- **Move Files:** Moves specific files to designated folders based on their types.
- **Delete Duplicates:** Identifies and removes duplicate files from Google Drive.
- **Rename Files:** Uses AI to generate meaningful file names based on content.

### 🔹 AI-Powered Features

- **File Categorization:** Categorizes files using Gemini AI based on their names and content.
- **Sensitive Data Detection:** Scans files for sensitive content like PII, credentials, and business documents.
- **Log Analysis:** Analyzes API logs to detect patterns, anomalies, and recommendations.

### 🔹 Permissions & Security

- **Permissions:** Fetches file permissions.
- **Track Changes:** Stores logs for all API actions and generates insights.

## 🏗️ Project Structure

```
📂 google-drive-ai-agent
│-- 📁 controllers
│   ├── categorize.py
│   ├── deleteFile.py
│   ├── duplicate.py
│   ├── fetch_content.py
│   ├── fetch_files.py
│   ├── move_file.py
│   ├── permissions.py
│   ├── rename_file.py
│   ├── search.py
│-- 📁 models
│   ├── database.py
│   ├── file_model.py
│-- 📁 services
│   ├── auth.py
│   ├── gemini_request.py
│   ├── logger.py
│   ├── pdf_generator.py
│   ├── process_gemini_response.py
│-- 📁 pages
│   ├── categorize.py
│   ├── fetch_content.py
│   ├── log_analysis.py
│   ├── logs.py
│   ├── move_files.py
│   ├── permissions.py
│   ├── rename.py
│   ├── search.py
│   ├── sensitive_files.py
│-- main.py
│-- README.md
│-- requirements.txt
```

## 🛠️ Installation

### 1️⃣ Prerequisites

Ensure you have the following installed:

- Python 3.8+
- Pip
- SQLite3

### 2️⃣ Clone the Repository

```bash
git clone https://github.com/aayush598/Google-Drive-Ai-Agent.git
cd Google-Drive-Ai-Agent
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Authenticate with Google Drive

Download the `credentials.json` file from the Google Cloud Console and add it to the root directory of the project. This file is required for Google Drive API authentication.

### 5️⃣ Initialize the Database

```bash
python models/database.py
```

### 6️⃣ Run the Application

```bash
streamlit run main.py
```

## 🔧 Usage

1️⃣ **Categorize Files:** Click "Categorize Files" to classify documents using AI.

2️⃣ **Search Files:** Use the search function to locate files by category.

3️⃣ **Rename Files:** AI-based renaming using extracted file content.

4️⃣ **Detect Sensitive Data:** Scan files for confidential data.

5️⃣ **Manage Permissions:** View and update file sharing settings.

6️⃣ **Analyze Logs:** AI-based log insights and pattern detection.

## 📜 API Endpoints

| Endpoint             | Method | Description                              |
| -------------------- | ------ | ---------------------------------------- |
| `/categorize-files`  | POST   | Categorizes files using AI               |
| `/search-files`      | GET    | Searches files by category               |
| `/rename-files`      | POST   | Renames files based on content           |
| `/fetch-files`       | GET    | Retrieves file details from Google Drive |
| `/delete-duplicates` | DELETE | Removes duplicate files                  |
| `/fetch-permissions` | GET    | Fetches file permissions                 |
| `/move-files`        | POST   | Moves selected files to specific folders |
| `/log-analysis`      | POST   | Generates insights from logs             |

## 🔗 Tech Stack

- **Python**
- **Streamlit** (UI)
- **PyDrive2** (Google Drive API)
- **SQLite** (Database)
- **Gemini AI API** (AI processing)
- **ReportLab** (PDF generation)

## 📌 Contributing

Contributions are welcome! Feel free to submit pull requests.

## 📄 License

This project is licensed under the MIT License.

## 📞 Contact

For questions or suggestions, reach out to: [aayushgid598@gmail.com](mailto:aayushgid598@gmail.com)

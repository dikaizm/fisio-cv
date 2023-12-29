# Flask API Setup

This repository contains a simple Python Flask API. Follow the steps below to set up the project and run the API.

## Prerequisites

- Python 3.x installed on your machine
- Git installed (optional, if you're cloning the repository)

## 1. Clone the repository

```bash
git clone <repository-url>
cd <repository-directory>
```

## 2. Open app directory

```bash
cd app
```

## 3. Setup virtual environment

```bash
# On Unix or MacOS
python3 -m venv venv

# On Windows
python -m venv venv
```

## 4. Activate virtual environment

```bash
# On Unix or MacOS
source venv/bin/activate

# On Windows
.\venv\Scripts\activate

```

## 5. Install dependencies

```bash
pip install -r requirements.txt
```

## 6. Run the app

```bash
flask run

# or

# On Unix or MacOS
python3 app.py

# On Windows
python app.py
```
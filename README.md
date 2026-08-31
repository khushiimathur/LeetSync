# LeetSync

**Automated LeetCode Solution Synchronization Pipeline**

LeetSync automatically fetches your daily LeetCode challenge and latest accepted solution, generates a structured local repository entry, and pushes it to GitHub. The pipeline uses **GraphQL, Python, Git automation, Linux cron, and GitHub Actions** to automate the entire workflow.

---

## 🚀 Features

* Fetches the **Daily LeetCode Challenge** using GraphQL.
* Retrieves the user's **latest accepted submission** for the daily problem.
* Fetches submitted **source code, language, runtime, and memory** metadata.
* Generates language-specific solution files automatically.
* Organizes solutions by **year/month/date**.
* Generates structured `metadata.json` for every solution.
* Implements **idempotent synchronization** to prevent duplicate solutions.
* Automates `git add`, `commit`, and `push` using Python `subprocess`.
* Runs automatically using **Linux cron**.
* Uses **GitHub Actions** for automated CI/testing after every push.
* Keeps LeetCode authentication credentials outside the repository using environment variables.

---

## 🏗️ Architecture

```text
                 ┌─────────────────────┐
                 │   LeetCode GraphQL  │
                 │        API          │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │  LeetCodeClient     │
                 │      (Python)       │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │      sync.py        │
                 │   Orchestrator      │
                 └───────┬─────┬───────┘
                         │     │
              ┌──────────┘     └──────────┐
              ▼                           ▼
   ┌─────────────────────┐      ┌─────────────────────┐
   │ RepositoryManager   │      │     GitManager      │
   │                     │      │                     │
   │ • Create directories│      │ • git add           │
   │ • Generate solution │      │ • git commit        │
   │ • Generate metadata │      │ • git push          │
   └──────────┬──────────┘      └──────────┬──────────┘
              │                            │
              ▼                            ▼
       Solution Files                  GitHub Repo
              │                            │
              └────────────┬───────────────┘
                           ▼
                  ┌─────────────────────┐
                  │   GitHub Actions    │
                  │    CI / Testing     │
                  └─────────────────────┘

                 Linux Cron
                     │
                     ▼
                  sync.py
```

---

## 📂 Repository Structure

```text
LeetSync/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── scripts/
│   ├── __init__.py
│   ├── leetcode_client.py
│   ├── repository_manager.py
│   ├── git_manager.py
│   └── sync.py
│
├── solutions/
│   └── YYYY/
│       └── MM/
│           └── DD-problem-name/
│               ├── solution.py
│               └── metadata.json
│
├── tests/
│   └── test_repository_manager.py
│
├── logs/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🧩 How It Works

### 1. Fetch Daily Challenge

`LeetCodeClient` sends a GraphQL query to retrieve:

* Problem ID
* Title
* Title slug
* Difficulty
* Daily challenge date
* LeetCode URL

### 2. Find Accepted Submission

The client uses the problem's `titleSlug` to retrieve submissions and identifies the latest accepted submission.

The submission details include:

```text
Submission ID
Language
Source Code
Runtime
Memory
Status
```

### 3. Generate Repository Files

`RepositoryManager` creates a deterministic directory based on the challenge date:

```text
solutions/2026/08/26-smallest-missing-multiple-of-k/
```

It then generates:

```text
solution.cpp
metadata.json
```

Example metadata:

```json
{
    "date": "2026-08-26",
    "title": "Smallest Missing Multiple of K",
    "slug": "smallest-missing-multiple-of-k",
    "submission_id": "2119420020",
    "difficulty": "Easy",
    "language": "C++",
    "runtime": "3 ms",
    "memory": "25.3 MB",
    "leetcode_url": "..."
}
```

### 4. Idempotency

Before creating a new solution, the repository manager checks whether the solution for that day already exists.

If it has already been synchronized:

```text
Solution already synced.
```

No duplicate files or unnecessary Git commits are created.

### 5. Git Automation

`GitManager` uses Python's `subprocess` module to execute Git commands:

```text
git add
    ↓
git commit
    ↓
git push
```

This removes the need for manual Git operations after each solution.

### 6. Scheduled Execution

Linux `cron` executes:

```text
sync.py
```

automatically every day at the configured time.

### 7. Continuous Integration

Every push to the `main` branch triggers GitHub Actions.

The CI workflow:

```text
Checkout repository
        ↓
Set up Python
        ↓
Install dependencies
        ↓
Run pytest
```

This ensures repository changes are automatically tested after synchronization.

---

## 🛠️ Tech Stack

| Technology     | Purpose                                    |
| -------------- | ------------------------------------------ |
| Python         | Core automation and orchestration          |
| GraphQL        | LeetCode API integration                   |
| Requests       | HTTP requests to LeetCode                  |
| pathlib        | Cross-platform filesystem management       |
| JSON           | Solution metadata                          |
| subprocess     | Git command automation                     |
| pytest         | Automated testing                          |
| Linux cron     | Scheduled execution                        |
| GitHub Actions | Continuous integration                     |
| Git            | Version control and remote synchronization |

---

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd LeetSync
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

**Windows:**

```bash
.venv\Scripts\activate
```

**Linux / WSL:**

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file:

```env
LEETCODE_SESSION=your_session_cookie
LEETCODE_CSRF_TOKEN=your_csrf_token
```

> **Never commit `.env` to GitHub.** Authentication credentials are kept outside version control.

### 5. Run manually

```bash
python scripts/sync.py
```

The pipeline will:

```text
Fetch LeetCode problem
        ↓
Fetch accepted submission
        ↓
Generate solution files
        ↓
Commit changes
        ↓
Push to GitHub
```

---

## 🧪 Running Tests

Run:

```bash
pytest
```

The tests verify core repository functionality such as:

* Problem title slugification
* Solution directory generation
* Solution file creation
* Metadata generation
* Idempotent synchronization

---

## ⏰ Cron Configuration

The synchronization can be scheduled using Linux cron.

Example:

```cron
0 1 * * * cd /path/to/LeetSync && /path/to/.venv/bin/python scripts/sync.py >> logs/cron.log 2>&1
```

This executes the synchronization pipeline every day at **1:00 AM**.

Check configured jobs with:

```bash
crontab -l
```

---

## 🔐 Security

Sensitive authentication values are stored using environment variables.

The following files should **never** be committed:

```text
.env
```

The repository contains:

```text
.env.example
```

as a template for required configuration.

---

## 🔄 End-to-End Workflow

Once configured, the complete automation is:

```text
Daily Challenge
      │
      ▼
   1:00 AM
      │
      ▼
    cron
      │
      ▼
  sync.py
      │
      ▼
LeetCode GraphQL
      │
      ▼
Accepted Submission
      │
      ▼
RepositoryManager
      │
      ├── solution.py
      └── metadata.json
      │
      ▼
 GitManager
      │
      ├── git add
      ├── git commit
      └── git push
      │
      ▼
    GitHub
      │
      ▼
GitHub Actions
      │
      ▼
   Automated Tests
```

---

## 🎯 Project Goals

LeetSync was built to explore practical software engineering concepts including:

* GraphQL API integration
* API authentication
* Modular Python architecture
* Idempotent automation
* Filesystem management
* Git automation
* Linux scheduling
* Continuous Integration
* Automated testing
* Secure environment configuration

---

## 📌 Future Improvements

Potential improvements include:

* Support for additional programming languages.
* Automated compilation/syntax validation for generated solutions.
* Improved GitHub Actions test coverage.
* Automatic README statistics and solution counts.
* Retry handling for temporary API/network failures.
* More robust structured logging.
* Better handling of changed/new submissions for the same problem.

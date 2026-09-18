# CAREER_AI
````markdown
# CareerAI – Intelligent Career Guidance Platform

> An AI-powered career guidance platform that helps students explore career opportunities, understand post-matric pathways, analyze resumes, build structured routines, and engage with a career-focused community.

## 📌 Overview

CareerAI is a full-stack intelligent career guidance platform developed to support students in exploring and planning their career journey through a single integrated application.

The platform combines **Post-Matric Guidance, Resume Analysis, Routine Builder, Community, and Explore** modules to provide users with structured career information, resume-related insights, planning tools, and opportunities for knowledge sharing.

CareerAI also integrates a **locally hosted Mistral 7B Large Language Model (LLM)** along with Natural Language Processing and Machine Learning techniques for intelligent text-based processing and career-related assistance.

---

## ✨ Features

### 🎓 Post-Matric Guidance

Helps students explore educational and career pathways after matriculation.

- Explore post-matric opportunities
- Understand educational pathways
- Discover career options
- Access structured career information

### 📄 Resume Analysis

Analyzes resume content using Natural Language Processing and Machine Learning techniques.

- Resume upload and processing
- Text extraction and preprocessing
- Skill and keyword identification
- Resume content analysis
- Career-related text comparison
- Similarity-based analysis
- Resume improvement insights

### 🗓️ Routine Builder

Helps users organize their study and career-preparation activities.

- Create structured routines
- Plan learning activities
- Organize preparation tasks
- Manage daily activities
- Maintain consistent learning schedules

### 👥 Community

Provides a platform for users to interact and share career-related knowledge.

- Create and share posts
- Participate in discussions
- Share experiences and knowledge
- Interact with other users
- Support peer-to-peer learning

### 🔍 Explore

Allows users to discover career-related information and resources.

- Explore career domains
- Discover career opportunities
- Learn about required skills
- Explore career resources
- Discover professional development information

---

## 🧠 AI & NLP

CareerAI integrates a **local Mistral 7B LLM** to support intelligent text-based processing and career-related assistance.

The platform also uses Natural Language Processing and Machine Learning techniques for textual analysis, particularly within the resume analysis workflow.

### AI / ML Technologies

- **Mistral 7B** – Locally hosted Large Language Model
- **spaCy** – Natural Language Processing
- **NLTK** – Text processing
- **Scikit-learn** – Machine Learning
- **Cosine Similarity** – Text similarity analysis

### Resume Analysis Workflow

```text
Resume Upload
      ↓
Text Extraction
      ↓
Text Preprocessing
      ↓
NLP Processing
      ↓
Skill / Keyword Extraction
      ↓
Feature Representation
      ↓
Similarity Analysis
      ↓
AI-Assisted Analysis
      ↓
Results & Suggestions
````

---

## 🏗️ System Architecture

```text
                         ┌───────────────┐
                         │     User      │
                         └───────┬───────┘
                                 │
                                 ▼
                      ┌────────────────────┐
                      │   React Frontend   │
                      │    User Interface  │
                      └─────────┬──────────┘
                                │
                           REST APIs
                                │
                                ▼
                      ┌────────────────────┐
                      │  Python / Flask    │
                      │      Backend       │
                      └─────────┬──────────┘
                                │
             ┌──────────────────┼──────────────────┐
             │                  │                  │
             ▼                  ▼                  ▼
      ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
      │ Post-Matric  │   │    Resume    │   │   Routine    │
      │   Guidance   │   │   Analysis   │   │   Builder    │
      └──────────────┘   └──────────────┘   └──────────────┘
             │                  │                  │
             └──────────────────┼──────────────────┘
                                │
                   ┌────────────┴────────────┐
                   │                         │
                   ▼                         ▼
            ┌─────────────┐           ┌─────────────┐
            │  Mistral 7B │           │   NLP / ML  │
            │  Local LLM  │           │  Processing │
            └─────────────┘           └─────────────┘
                   │                         │
                   └────────────┬────────────┘
                                ▼
                       ┌─────────────────┐
                       │ Database Layer  │
                       │ SQLite / MySQL  │
                       └─────────────────┘

                    ┌──────────────────────┐
                    │ Community & Explore   │
                    └──────────────────────┘
```

---

## 🛠️ Tech Stack

| Category                | Technologies                      |
| ----------------------- | --------------------------------- |
| **Frontend**            | React.js, JavaScript, HTML5, CSS3 |
| **Backend**             | Python, Flask, Flask-CORS         |
| **Local LLM**           | Mistral 7B                        |
| **NLP**                 | spaCy, NLTK                       |
| **Machine Learning**    | Scikit-learn                      |
| **Similarity Analysis** | Cosine Similarity                 |
| **Data Processing**     | NumPy, Pandas, SciPy              |
| **Database**            | SQLite, MySQL                     |
| **API**                 | REST APIs                         |
| **Version Control**     | Git, GitHub                       |
| **Development**         | Visual Studio Code, npm           |

The project's Python dependency file includes Flask, OpenAI, spaCy, NLTK, Scikit-learn, NumPy, Pandas, SciPy, and related packages. 

---

## 📂 Project Structure

```text
CAREER_AI/
│
├── career-guidance-ui/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── assets/
│   │   └── ...
│   ├── public/
│   ├── package.json
│   └── ...
│
├── backend/
│   ├── ...
│   └── ...
│
├── uploads/
├── instance/
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation & Setup

### Prerequisites

* Python 3.x
* Node.js
* npm
* Git
* MySQL, if required by the configured database

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/CAREER_AI.git
cd CAREER_AI
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### 3. Install Backend Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Frontend Dependencies

```bash
cd career-guidance-ui
npm install
```

---

## 🔐 Environment Configuration

Create a `.env` file based on the project's environment configuration.

Example:

```env
SECRET_KEY=your_secret_key
DATABASE_URL=your_database_url
```

Add any additional configuration required by the application.

> **Important:** Never commit API keys, passwords, database credentials, or other sensitive information to GitHub.

---

## ▶️ Running the Application

### Start the Backend

From the backend/project directory, run the configured Flask entry point.

```bash
python app.py
```

or:

```bash
flask run
```

### Start the Frontend

From the frontend directory:

```bash
npm start
```

The application will be available at the local development URL shown in the terminal.

---

## 📸 Screenshots

Add screenshots of the major interfaces to showcase the application.

### Dashboard

![Dashboard](screenshots/dashboard.png)

### Post-Matric Guidance

![Post-Matric Guidance](screenshots/post-matric.png)

### Resume Analysis

![Resume Analysis](screenshots/resume-analysis.png)

### Routine Builder

![Routine Builder](screenshots/routine-builder.png)

### Community

![Community](screenshots/community.png)

### Explore

![Explore](screenshots/explore.png)

> Replace the image paths with the actual screenshot locations in the repository.

---

## 🔮 Future Scope

* Advanced personalized career recommendations
* AI-powered career chatbot
* Skill-gap analysis
* Job recommendation based on user profiles
* Resume-to-job matching
* Real-time job-market information
* Personalized course recommendations
* Career progress tracking
* Learning-resource recommendations
* Mentor-student matching
* Mobile application
* Cloud deployment
* Multi-language career guidance

---

## 📋 Project Information

| Category                 | Details                                    |
| ------------------------ | ------------------------------------------ |
| **Project Name**         | CareerAI                                   |
| **Full Name**            | Intelligent Career Guidance Platform       |
| **Project Type**         | Full-Stack Web Application                 |
| **Domain**               | Artificial Intelligence / Machine Learning |
| **Primary Focus**        | Intelligent Career Guidance                |
| **Frontend**             | React.js                                   |
| **Backend**              | Python, Flask                              |
| **Local LLM**            | Mistral 7B                                 |
| **NLP**                  | spaCy, NLTK                                |
| **Machine Learning**     | Scikit-learn                               |
| **Similarity Technique** | Cosine Similarity                          |
| **Database**             | SQLite / MySQL                             |
| **API**                  | REST API                                   |
| **Version Control**      | Git / GitHub                               |

---

## 📄 License

This project was developed as an academic project for educational and demonstration purposes.

---

## ⭐ Support

If you find this project useful or interesting, consider giving the repository a ⭐ on GitHub.

---

**CareerAI – Explore. Plan. Prepare.**

```
```

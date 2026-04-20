# 🤖 Placement Prep Copilot

An AI-powered assistant designed to help students prepare for technical placements using fast LLM inference via Groq and LangChain.

---

## 🚀 Overview

Placement Prep Copilot is built to assist with:

* Data Structures & Algorithms (DSA) problem solving
* Interview preparation
* Concept explanations
* Coding guidance

It leverages **Groq’s ultra-fast LLM inference** combined with **LangChain’s agent framework** to deliver quick and contextual responses.

---

## 🧠 Critical Design Decisions

### 1. ⚡ Groq for LLM Inference

* Chosen for **low latency and high-speed responses**
* Enables near real-time interaction compared to traditional APIs
* Model used: `mixtral-8x7b-32768`

---

### 2. 🔗 LangChain for Orchestration

* Provides a modular framework for building AI agents
* Simplifies integration of:

  * LLMs
  * Tools
  * Prompt templates
* Makes the system extensible for future upgrades

---

### 3. 🔐 Environment Variable Management

* API keys are stored in `.env` (not hardcoded)
* Prevents accidental exposure of sensitive credentials
* `.env` is excluded using `.gitignore`
* `.env.example` provided for setup guidance

---

### 4. 🧩 Modular Code Structure

* Separation of concerns:

  * LLM initialization
  * Agent logic
  * Configuration
* Makes debugging and scaling easier

---

### 5. 🧪 Developer-Friendly Setup

* Minimal configuration required
* Easy to run locally
* Designed for quick experimentation and iteration

---

## 🛠️ Tech Stack

* Python
* LangChain
* Groq API
* python-dotenv

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/placement-prep-copilot.git
cd placement-prep-copilot
```

---

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Configure environment variables

Create a `.env` file in the root directory:

```
GROQ_API_KEY=your_api_key_here
```

---

### 4. Run the project

```bash
python agent.py
```

---

## 📂 Project Structure

```
placement-prep-copilot/
│── agent.py
│── .env                # not tracked
│── .env.example
│── .gitignore
│── requirements.txt
│── README.md
```

---

## 🔮 Future Improvements

* Add memory for conversational context
* Integrate tools (web search, code execution)
* Build a frontend interface
* Add support for multiple models

---

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

---

## 📌 Note

Make sure to keep your API keys secure and never commit them to version control.

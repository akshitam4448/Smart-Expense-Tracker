# Smart-Expense-Tracker
A comprehensive, professional web application for tracking expenses, managing income, and planning budgets with an intuitive interface and powerful analytics.

![Version](https://img.shields.io/badge/version-2.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![Flask](https://img.shields.io/badge/flask-2.3.2-red.svg)
![License](https://img.shields.io/badge/license-MIT-yellow.svg)



## 🎯 Overview

**Smart Expense Tracker** is a full-featured personal finance management application built with Python Flask. It helps users track their expenses, manage multiple income sources, set monthly budgets, and visualize their financial health through interactive charts and statistics.

### 🚀 Key Highlights
- 📊 **Real-time Analytics** - Visual charts and statistics
- 💰 **Income Management** - Track multiple income sources
- 🎯 **Budget Planning** - Set and monitor monthly budgets
- 🌙 **Dark Mode** - Eye-friendly dark theme
- 📱 **Responsive** - Works on all devices
- 🔒 **Data Security** - Local JSON storage, no cloud dependencies

---

## ✨ Features

### Core Features
| Feature | Description | Status |
|---------|-------------|--------|
| ✅ Expense Tracking | Add, edit, delete expenses with categorization | Complete |
| ✅ Income Management | Track multiple income sources | Complete |
| ✅ Budget Planning | Set monthly budgets by category | Complete |
| ✅ Statistics Dashboard | Visual analytics with charts | Complete |
| ✅ Dark Mode | Toggle between light/dark themes | Complete |
| ✅ Responsive Design | Mobile-friendly interface | Complete |

### Advanced Features
- 🔍 **Search & Filter** - Find expenses by category or description
- 📊 **Pie Charts** - Visual expense and income distribution
- 📈 **Progress Bars** - Budget tracking visualization
- 💾 **JSON Storage** - Simple, portable data storage
- 🎨 **Color Coding** - Category-based color scheme
- ⌨️ **Keyboard Shortcuts** - Quick navigation

---

## 🛠️ Technology Stack

### Backend
- **Python 3.8+** - Core programming language
- **Flask 2.3.2** - Web framework
- **JSON** - Data storage format

### Frontend
- **HTML5** - Markup language
- **CSS3** - Styling with custom properties
- **JavaScript** - Interactive features
- **Bootstrap 5.1.3** - Responsive framework
- **Chart.js** - Data visualization
- **Font Awesome 6.4** - Icons

### Libraries & Tools
| Library | Version | Purpose |
|---------|---------|---------|
| Flask | 2.3.2 | Web framework |
| Flask-Bootstrap | 3.3.7.1 | Bootstrap integration |
| Flask-WTF | 1.1.1 | Form handling |
| Werkzeug | 2.3.6 | WSGI utilities |
| Chart.js | Latest | Charts & graphs |

---

## 📁 Project Structure
smart_expense_tracker/
│
├── app.py # Main application file
├── requirements.txt # Python dependencies
│
├── data/ # Data storage
│ ├── expenses.json # Expense records
│ ├── budgets.json # Budget records
│ └── incomes.json # Income records
│
├── templates/ # HTML templates
│ ├── base.html # Base template with navigation
│ ├── index.html # Dashboard/Home page
│ ├── add_expense.html # Add expense form
│ ├── view_expenses.html # View all expenses
│ ├── edit_expense.html # Edit expense form
│ ├── income_manager.html # Income management
│ ├── add_income.html # Add income form
│ ├── edit_income.html # Edit income form
│ ├── budget_planner.html # Budget planner
│ ├── add_budget.html # Add budget form
│ ├── edit_budget.html # Edit budget form
│ ├── statistics.html # Statistics dashboard
│ ├── 404.html # Page not found
│ └── 500.html # Server error
│
├── static/ # Static assets
│ ├── css/
│ │ └── style.css # Main stylesheet
│ └── js/
│ └── script.js # JavaScript functions
│
└── utils/ # Utility modules
├── file_handler.py # Expense operations
├── budget_handler.py # Budget operations
└── income_handler.py # Income operations

text

---

## 💻 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (optional)

### Step-by-Step Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/smart-expense-tracker.git
cd smart-expense-tracker
2. Create Virtual Environment
bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
bash
pip install -r requirements.txt
4. Create Data Directory
bash
# The application will create this automatically
mkdir data
5. Run the Application
bash
python app.py
6. Access the Application
Open your browser and navigate to:

text
http://127.0.0.1:5000/

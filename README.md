# Feedback Agent V1

AI-powered feedback classification and reporting system that analyzes user feedback about Insights from Hive/Presto database, categorizes them using GPT-4, and generates prioritized reports for your team.

## 🎯 What It Does

1. **Loads** negative user feedback from Hive/Presto database (Autodesk data warehouse)
2. **Classifies** feedback into categories (Technical Issues, Content Issues, Rude Feedback, Other)
3. **Exports** classified results to Excel with AI-generated rationales
4. **Generates** prioritized reports highlighting the most urgent issues
5. **Posts** formatted reports to Slack (optional)

## 📋 Prerequisites

- Python 3.13+
- UV package manager
- OpenAI API key with sufficient credits
- Access to Autodesk Presto/Trino database (VPN required)
- Presto database credentials (username & password)
- Slack Bot Token (optional, for Slack integration)

## 🚀 Quick Start

### 1. Install Dependencies

```bash
uv sync
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Required - OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here

# Required - Presto/Trino Database Configuration
PRESTO_USER=your_username
PRESTO_PASSWORD=your_password
PRESTO_CATALOG=hive

# Optional - LangSmith Tracing
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=your_langsmith_key
LANGSMITH_PROJECT=your_project_name

# Optional - Slack Integration
SLACK_BOT_TOKEN=xoxb-your-slack-bot-token
SLACK_CHANNEL_ID=C09PW77SFNC
SLACK_CHANNEL_ID_DEV=C01ABC123XY
```

### 3. Connect to VPN

**Important:** You must be connected to the Autodesk VPN to access the Presto database.

```bash
# Ensure you're connected to Autodesk VPN before running
```

### 4. Run the Application

```bash
uv run python -m src.main
```

Or activate the virtual environment first:

```bash
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate     # Windows

python -m src.main
```

The application will:
- Load feedback from the previous month (automatically calculated from current date)
- Query Hive database for negative/very negative feedback
- Classify each feedback item using GPT-4
- Export results to Excel
- Generate and display a Slack-ready report

## 📂 Project Structure

```
feedback_agent_v1/
├── docs/                           # Legacy data (not used currently)
│   └── feedback_insight_users_sep.xlsx
│
├── output/                         # Generated reports
│   └── classified_feedback_*.xlsx
│
├── src/
│   ├── main.py                     # Application entry point
│   │
│   ├── config/
│   │   └── settings.py             # Configuration management
│   │
│   ├── models/
│   │   ├── feedback.py             # FeedbackItem, FeedbackCategory
│   │   └── report.py               # UrgentFeedback, FeedbackReport
│   │
│   ├── prompts/
│   │   ├── classifier_prompt.py    # Classification prompt
│   │   └── reporter_prompt.py      # Report generation prompt
│   │
│   ├── agents/
│   │   ├── classifier.py           # Feedback classifier agent
│   │   └── reporter.py             # Report generator agent
│   │
│   ├── nodes/                      # LangGraph workflow nodes
│   │   ├── load_data_hive.py       # Load feedback from Hive/Presto ⭐ NEW
│   │   ├── load_data_excel.py      # Load feedback from Excel (legacy)
│   │   ├── classify.py             # Classify feedback
│   │   ├── export.py               # Export to Excel
│   │   └── report.py               # Generate report
│   │
│   ├── workflows/
│   │   ├── state.py                # Workflow state definition
│   │   └── feedback_workflow.py    # Main workflow
│   │
│   ├── utils/
│   │   └── slack_client.py         # Slack integration
│   │
│   └── tools/                      # Future agent tools
│
├── feedback_notebook.ipynb         # Development notebook for testing queries
├── pyproject.toml                  # Dependencies
├── .env                            # Environment variables (gitignored)
└── README.md                       # This file
```

## ⚙️ Configuration

Edit `src/config/settings.py` to customize:

```python
class Settings:
    # Model Configuration
    MODEL_NAME: str = "gpt-4.1"
    TEMPERATURE: float = 0.1
    CLASSIFIER_MAX_TOKENS: int = 3000
    REPORTER_MAX_TOKENS: int = 6000
    TIMEOUT: int = 30
    
    # Processing
    CLASSIFICATION_LIMIT: int = 15  # Set to None to process all items
    
    # Slack
    SEND_TO_SLACK: bool = True      # Auto-send to Slack
```

### Database Configuration

The application connects to:
- **Host:** `presto-gdc.adp.autodesk.com`
- **Port:** 443
- **Catalog:** `hive` (configurable via PRESTO_CATALOG env var)
- **Schema:** `desktop_product_intelligence_public`
- **Table:** `halley_feedback_qualtrics_comments`

The query automatically fetches:
- Negative and Very Negative sentiment feedback
- From Adobe account portal and Email delivery channels
- For the previous month (calculated from current date)
- Limited to 500 rows

## 🔄 Workflow

```mermaid
graph LR
    A[Load from Hive] --> B[Classify with GPT-4]
    B --> C[Export to Excel]
    C --> D[Generate Report]
    D --> E[Display/Post to Slack]
```

1. **Load from Hive**: Queries Presto/Trino database for negative feedback from previous month
2. **Classify**: Uses GPT-4.1 to categorize each feedback item into 4 categories
3. **Export**: Saves classified results with AI rationales to Excel
4. **Generate Report**: Creates prioritized report with top 5 urgent items per category
5. **Display/Slack**: Shows formatted report and optionally posts to Slack channel

## 📊 Categories

- **Technical Issues**: Broken CTAs, 404 errors, non-playable videos, etc.
- **Content Issues**: Irrelevant content, inaccurate information, missing details
- **Rude Feedback**: Offensive language, unconstructive criticism
- **Other**: Feedback that doesn't fit the above categories

## 📤 Output

### Excel Export
- Location: `output/classified_feedback_YYYYMMDD_HHMMSS.xlsx`
- Columns: User ID, Feedback, Insight Type, Category, Rationale

### Slack Report
- Top 5 most urgent Technical Issues
- Top 5 most urgent Content Issues
- Summary of Rude Feedback and Other feedback
- Formatted with Slack markdown for readability

## 🛠️ Development

### Adding New Features

**Add a new workflow node:**
1. Create file in `src/nodes/`
2. Add to `src/nodes/__init__.py`
3. Update workflow in `src/workflows/feedback_workflow.py`

**Add a new agent:**
1. Create file in `src/agents/`
2. Add prompt in `src/prompts/`
3. Create corresponding Pydantic model in `src/models/`

**Add agent tools:**
1. Create tools in `src/tools/`
2. Use `@tool` decorator from LangChain
3. Pass to agent in `create_agent()`

## 📦 Dependencies

- **langchain** - Core LangChain library
- **langchain-openai** - OpenAI integration
- **langgraph** - Workflow orchestration
- **pandas** - Data manipulation
- **sqlalchemy** - Database ORM and connection management
- **sqlalchemy-trino** - Trino/Presto driver for SQLAlchemy
- **openpyxl** - Excel file handling
- **slack-sdk** - Slack API integration
- **python-dotenv** - Environment variable management
- **pydantic** - Data validation and models

## 🔐 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | ✅ Yes | OpenAI API key for GPT-4.1 |
| `PRESTO_USER` | ✅ Yes | Your Autodesk username for Presto |
| `PRESTO_PASSWORD` | ✅ Yes | Your Autodesk password for Presto |
| `PRESTO_CATALOG` | ✅ Yes | Presto catalog (default: `hive`) |
| `LANGSMITH_TRACING` | ⚠️ Optional | Enable LangSmith tracing (`true`/`false`) |
| `LANGSMITH_API_KEY` | ⚠️ Optional | LangSmith API key for monitoring |
| `LANGSMITH_PROJECT` | ⚠️ Optional | LangSmith project name |
| `SLACK_BOT_TOKEN` | ⚠️ Optional | Slack bot token for posting |
| `SLACK_CHANNEL_ID` | ⚠️ Optional | Production Slack channel ID |
| `SLACK_CHANNEL_ID_DEV` | ⚠️ Optional | Development Slack channel ID |

## 📝 Example Usage

```bash
# Standard run (loads previous month's data)
uv run python -m src.main

# The application will:
# 1. Calculate previous month from current date
# 2. Query Hive for negative feedback from that month
# 3. Classify ~50-100 feedback items (varies by month)
# 4. Export to Excel with timestamp
# 5. Display formatted Slack report
```

### Testing with Limited Data

```python
# In src/nodes/load_data_hive.py, modify the LIMIT:
LIMIT 10  # Instead of 500 for quick testing
```

### Disable Slack Posting

```python
# In src/config/settings.py:
SEND_TO_SLACK: bool = False
```

## 🐛 Troubleshooting

**Database Connection Errors:**
```bash
# Error: "Connection failed" or "Network access"
# Solution: Ensure you're connected to Autodesk VPN
# Check: Can you access presto-gdc.adp.autodesk.com?

# Error: "insufficient_quota" or Error 429
# Solution: Your OpenAI API key has no credits
# Fix: Add credits at https://platform.openai.com/account/billing
```

**Import errors:**
```bash
# Ensure you're in project root and dependencies are installed
cd /path/to/feedback_agent_v1
uv sync
uv run python -m src.main
```

**Missing .env file:**
```bash
# Create .env file with required variables
touch .env
# Add OPENAI_API_KEY, PRESTO_USER, PRESTO_PASSWORD, PRESTO_CATALOG
```

**No data returned from Hive:**
- Check if the previous month has data in the table
- Verify the table `halley_feedback_qualtrics_comments` exists
- Ensure your user has read permissions on the table

**Slack errors:**
- Verify `SLACK_BOT_TOKEN` is valid
- Ensure bot has permissions to post in channel
- Check `SLACK_CHANNEL_ID` is correct

## 📚 Resources

- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Slack API Documentation](https://api.slack.com/)
- [UV Documentation](https://github.com/astral-sh/uv)
- [Trino Documentation](https://trino.io/docs/current/)
- [SQLAlchemy Trino Dialect](https://github.com/trinodb/sqlalchemy-trino)

## 📄 License

Internal use only.

## 🔧 Development Notes

### Jupyter Notebook

The `feedback_notebook.ipynb` file is available for:
- Testing SQL queries against Hive database
- Exploring data structure
- Prototyping new features
- Debugging connection issues

### Switching Data Sources

To switch between Hive and Excel data sources:

**Current (Hive):**
```python
# In src/workflows/feedback_workflow.py
workflow.add_node("load_data_from_hive", load_data_from_hive)
workflow.add_edge(START, "load_data_from_hive")
```

**Legacy (Excel):**
```python
# In src/workflows/feedback_workflow.py
workflow.add_node("load_feedback_data", load_feedback_data)
workflow.add_edge(START, "load_feedback_data")
```

---

**Built with** 🚀 LangChain, LangGraph, OpenAI GPT-4.1, and Trino/Presto

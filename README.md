# Feedback Agent V1

AI-powered feedback classification and reporting system that analyzes user feedback about Insights, categorizes them, and generates prioritized reports for your team.

## 🎯 What It Does

1. **Loads** user feedback from Excel files
2. **Classifies** feedback into categories (Technical Issues, Content Issues, Rude Feedback, Other)
3. **Exports** classified results to Excel with AI-generated rationales
4. **Generates** prioritized reports highlighting the most urgent issues
5. **Posts** formatted reports to Slack (optional)

## 📋 Prerequisites

- Python 3.13+
- UV package manager
- OpenAI API key
- Slack Bot Token (optional, for Slack integration)

## 🚀 Quick Start

### 1. Install Dependencies

```bash
uv sync
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Required
OPENAI_API_KEY=sk-your-openai-api-key-here

# Optional (for Slack integration)
SLACK_BOT_TOKEN=xoxb-your-slack-bot-token
SLACK_CHANNEL_ID=C09PW77SFNC
SLACK_CHANNEL_ID_DEV=C01ABC123XY
```

### 3. Run the Application

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

## 📂 Project Structure

```
feedback_agent_v1/
├── docs/                           # Input data
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
│   │   ├── load_data.py            # Load feedback from Excel
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
    CLASSIFIER_MAX_TOKENS: int = 1000
    REPORTER_MAX_TOKENS: int = 2000
    
    # Processing
    CLASSIFICATION_LIMIT: int = 15  # Set to None to process all items
    
    # Slack
    SEND_TO_SLACK: bool = True      # Auto-send to Slack
```

## 🔄 Workflow

```mermaid
graph LR
    A[Load Data] --> B[Classify]
    B --> C[Export to Excel]
    C --> D[Generate Report]
    D --> E[Post to Slack]
```

1. **Load Data**: Reads feedback from `docs/feedback_insight_users_sep.xlsx`
2. **Classify**: Uses GPT-4.1 to categorize each feedback item
3. **Export**: Saves classified results with rationales to Excel
4. **Generate Report**: Creates prioritized report with top 5 urgent items per category
5. **Post to Slack**: Formats and posts to Slack channel (if enabled)

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
- **openpyxl** - Excel file handling
- **slack-sdk** - Slack API integration
- **python-dotenv** - Environment variable management

## 🔐 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | ✅ Yes | OpenAI API key for GPT-4.1 |
| `SLACK_BOT_TOKEN` | ⚠️ Optional | Slack bot token for posting |
| `SLACK_CHANNEL_ID` | ⚠️ Optional | Production Slack channel ID |
| `SLACK_CHANNEL_ID_DEV` | ⚠️ Optional | Development Slack channel ID |

## 📝 Example Usage

```bash
# Process all feedback items
# Set CLASSIFICATION_LIMIT = None in settings.py
uv run python -m src.main

# Process limited items (for testing)
# Set CLASSIFICATION_LIMIT = 15 in settings.py
uv run python -m src.main

# Disable Slack posting
# Set SEND_TO_SLACK = False in settings.py
uv run python -m src.main
```

## 🐛 Troubleshooting

**Import errors:**
```bash
# Ensure you're in project root
cd /path/to/feedback_agent_v1
uv run python -m src.main
```

**Missing .env file:**
```bash
# Create .env file with required variables
cp .env.example .env
nano .env  # or your preferred editor
```

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

## 📄 License

Internal use only.

---

**Built with** 🚀 LangChain, LangGraph, and OpenAI GPT-4.1

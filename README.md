# Feedback Agent V1

A LangChain and LangGraph application built with UV package manager.

## Prerequisites

- Python 3.14+
- UV package manager (already installed: v0.7.12)
- OpenAI API key

## Setup

1. **Clone or navigate to the project directory:**
   ```bash
   cd feedback_agent_v1
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```

3. **Set up your environment variables:**
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key to the `.env` file

   ```bash
   cp .env.example .env
   # Then edit .env and add your API key
   ```

## Running the Application

Run the main script:

```bash
uv run main.py
```

Or activate the virtual environment and run directly:

```bash
# Activate the virtual environment
.venv\Scripts\activate  # Windows

# Run the script
python main.py
```

## Dependencies

- **langchain** - Core LangChain library
- **langchain-openai** - OpenAI integration for LangChain
- **langgraph** - Build stateful, multi-actor applications with LLMs

## Project Structure

```
feedback_agent_v1/
├── .venv/              # Virtual environment (created by UV)
├── main.py             # Main application entry point
├── pyproject.toml      # Project configuration and dependencies
├── .env.example        # Example environment variables
├── .env                # Your local environment variables (gitignored)
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Next Steps

- Explore LangChain's [Quick Start Guide](https://python.langchain.com/docs/get_started/quickstart)
- Learn about [LangGraph](https://langchain-ai.github.io/langgraph/)
- Build your custom agent or workflow

## Resources

- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [UV Documentation](https://github.com/astral-sh/uv)


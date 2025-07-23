# Deep-Research-Agent
A deep research agent using OpenAI's agent framework

## Installation

This project uses [uv](https://docs.astral.sh/uv/) for fast, reliable Python package management.

### Prerequisites
- Python 3.8+
- uv (install from [here](https://docs.astral.sh/uv/getting-started/installation/))

### Setup
1. Install dependencies:
   ```bash
   uv sync
   ```

2. Create a `.env` file with your API keys:
   ```bash
   cp .env.example .env
   # Edit .env with your actual API keys
   ```

3. Run the applications:
   
   **Deep Research Agent:**
   ```bash
   uv run python deep_research/deep_research.py
   ```
   
   **Chat Agent:**
   ```bash
   uv run python deep_research/chat_agent.py
   ```

## Troubleshooting

If you encounter connection errors with OpenAI API:

1. **Test your connection**:
   ```bash
   uv run python troubleshoot_connection.py
   ```

2. **Common fixes**:
   - Verify your `OPENAI_API_KEY` in `.env`
   - Check your internet connection and firewall
   - Ensure OpenAI API has available credits
   - Try reinstalling OpenAI package: `uv sync --reinstall-package openai`

3. **Network issues**:
   - The error `[WinError 10054] An existing connection was forcibly closed` often indicates:
     - Firewall blocking the connection
     - Antivirus software interfering
     - Network proxy issues
     - Unstable internet connection

### Development

Install development dependencies:
```bash
uv sync --extra dev
```

Run tests:
```bash
uv run pytest
```

Format code:
```bash
uv run black .
```

## Legacy Installation (pip)

If you prefer using pip, you can still use the requirements.txt file:
```bash
pip install -r requirements.txt
```

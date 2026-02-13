# Quick Start Guide

## Prerequisites

Before starting, ensure you have:
- Python 3.8 or higher installed
- OpenAI API key
- Snowflake account (for data access via MCP server)
- Git (optional, for cloning)

## Installation Steps

### 1. Set Up Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

Or use the provided setup script (Windows):
```bash
setup_venv.bat
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Direct Snowflake connection (if not using MCP)
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_USER=your_user
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_WAREHOUSE=your_warehouse
SNOWFLAKE_DATABASE=your_database
SNOWFLAKE_SCHEMA=your_schema
```

### 4. Start the Application

```bash
python app.py
```

The application will launch at `http://127.0.0.1:7860`

## First Steps

### 1. Test Basic Functionality

Try a simple request:
```
Hello, I need help constructing a portfolio for a new client.
```

### 2. Portfolio Construction

Request portfolio construction:
```
Help me construct a diversified growth portfolio for client ID 12345. 
The client has moderate risk tolerance and a 15-year time horizon.
```

### 3. Investment Research

Search for investments:
```
Find technology-focused ETFs with low expense ratios and strong 
historical performance for a growth-oriented portfolio.
```

### 4. Risk Analysis

Analyze portfolio risk:
```
Analyze the risk profile of portfolio PORT-001. Calculate VaR, 
Sharpe ratio, and perform stress testing for the 2008 crisis scenario.
```

## Understanding the Response

The system will:
1. **Route** your request to appropriate specialized agents
2. **Access** necessary data from Snowflake
3. **Coordinate** multiple agents if needed
4. **Synthesize** results into a comprehensive response

## Common Use Cases

### Portfolio Construction Workflow
1. Request portfolio construction
2. System accesses client profile and risk tolerance
3. Portfolio Architect Agent recommends allocation
4. Risk Analytics Agent validates risk profile
5. Tax Optimization Agent considers tax implications
6. Final recommendations provided

### Investment Discovery Workflow
1. Request investment search
2. Investment Research Agent searches structured data
3. Analyzes unstructured research materials
4. Provides comparative analysis
5. Recommendations with rationale

### Risk Assessment Workflow
1. Request risk analysis
2. Risk Analytics Agent accesses portfolio data
3. Calculates multiple risk metrics
4. Performs stress testing
5. Identifies concentration risks
6. Provides mitigation recommendations

## Tips for Best Results

1. **Be Specific**: Include client IDs, portfolio IDs, and specific requirements
2. **Provide Context**: Mention risk tolerance, time horizon, and goals
3. **Ask Follow-ups**: The system can handle multi-turn conversations
4. **Use Success Criteria**: Specify what success looks like for complex requests

## Troubleshooting

### Application Won't Start
- Check Python version: `python --version` (should be 3.8+)
- Verify virtual environment is activated
- Check that all dependencies are installed: `pip list`

### API Errors
- Verify OpenAI API key is set in `.env` file
- Check API key is valid and has credits
- Ensure `.env` file is in project root

### Snowflake Connection Issues
- Verify Snowflake credentials in `.env` file
- Check Snowflake MCP server is configured
- Test Snowflake connection separately

### Agent Not Responding
- Check console for error messages
- Verify agent tools are properly loaded
- Check that LLM is responding (test with simple request)

## Next Steps

- Read the [README.md](README.md) for detailed documentation
- Review [ARCHITECTURE.md](ARCHITECTURE.md) for system architecture
- Check [AI_Financial_consultant.txt](AI_Financial_consultant.txt) for requirements

## Getting Help

- Check the documentation files
- Review error messages in console
- Open an issue on GitHub
- Contact support

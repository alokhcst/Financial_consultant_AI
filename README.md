# Financial Consultant AI Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.2.0+-green.svg)](https://github.com/langchain-ai/langgraph)

A sophisticated **multi-agent AI system** built with LangGraph that helps financial advisors construct portfolios, discover investment solutions, analyze risk, optimize taxes, and manage client relationships. The platform integrates with Snowflake data warehouse and orchestrates 8 specialized AI agents to streamline the advisor's workflow.

## 🎯 Value Proposition

### For Financial Advisors
- **Intelligent Portfolio Construction**: AI-powered recommendations for optimal asset allocation
- **Investment Discovery**: Search structured and unstructured data to find the best investment solutions
- **Risk Analytics**: Comprehensive risk assessment with stress testing and scenario analysis
- **Tax Optimization**: Strategic tax planning and tax-loss harvesting opportunities
- **Workflow Automation**: End-to-end support from portfolio construction to account management
- **Customized Reporting**: Generate detailed, executive, or one-page reports tailored to client preferences

### For Wealth Management Firms
- **Scalability**: Handle multiple advisors and clients efficiently
- **Compliance**: Built-in validation against investment policy statements and regulations
- **Data Integration**: Seamless integration with Snowflake data warehouse
- **Audit Trail**: Complete documentation of all recommendations and decisions
- **Consistency**: Standardized processes across all advisors

## ✨ Key Features

### 🤖 Multi-Agent Architecture
- **8 Specialized Agents**: Each agent handles a specific domain of expertise
- **Orchestrator Agent**: Intelligently routes requests and coordinates workflows
- **Worker-Evaluator Pattern**: Self-correcting workflow that iterates until success
- **Context Sharing**: Agents share context for seamless collaboration

### 🏦 Specialized Agents

1. **Portfolio Architect Agent**
   - Analyzes client risk profiles and investment objectives
   - Recommends optimal asset allocation strategies
   - Performs portfolio rebalancing calculations
   - Validates compliance with investment mandates

2. **Investment Research Agent**
   - Searches structured data (performance, risk factors, expense ratios)
   - Analyzes unstructured data (research reports, fund manager commentary)
   - Provides comparative analysis of investment vehicles
   - Tracks emerging investment opportunities

3. **Risk Analytics Agent**
   - Performs scenario analysis and stress testing
   - Calculates risk metrics (VaR, Sharpe ratio, beta, standard deviation)
   - Identifies concentration risks and correlation exposures
   - Provides early warning alerts for portfolio drift

4. **Tax Optimization Agent**
   - Analyzes tax impact of portfolio transitions
   - Identifies tax-loss harvesting opportunities
   - Optimizes asset location across account types
   - Ensures compliance with wash-sale rules

5. **Transition Planning Agent**
   - Creates step-by-step transition roadmaps
   - Sequences trades to minimize market impact and tax consequences
   - Estimates transition costs (taxes, trading costs, opportunity costs)
   - Coordinates timing across multiple accounts

6. **Reporting & Communication Agent**
   - Generates customized reports (detailed, executive summary, one-pagers)
   - Creates visual presentations of portfolio performance
   - Produces regulatory and compliance documentation
   - Adapts communication style to client sophistication level

7. **Account Operations Agent**
   - Automates account opening processes
   - Handles account consolidation workflows
   - Manages beneficiary designations and titling
   - Processes account transfers and rollovers

8. **Orchestrator Agent (Super Agent)**
   - Routes requests to appropriate specialist agents
   - Sequences multi-step workflows intelligently
   - Maintains context across agent interactions
   - Resolves conflicts between agent recommendations

### ❄️ Snowflake Integration
- **Data Warehouse Access**: Direct integration with Snowflake via MCP server
- **Client Data**: Access to client profiles, portfolios, and holdings
- **Market Data**: Real-time and historical market data
- **Performance Analytics**: Historical performance and risk metrics
- **Compliance Data**: Investment policy statements and regulatory data

### 📊 Data Requirements Support

The platform supports all data requirements for financial advisors:

- **Client Data**: Demographics, financial goals, risk profiles, current holdings
- **Investment Universe**: Security master data, pricing, performance metrics, research materials
- **Market & Economic Data**: Real-time market data, interest rates, economic indicators
- **Regulatory & Compliance Data**: Investment policy statements, regulatory restrictions
- **Tax Data**: Historical tax returns, capital gains/losses, tax-deferred account status
- **Operational Data**: Account information, trading platforms, fee schedules

## 🏗️ Architecture

The system uses a **LangGraph workflow** with a **worker-evaluator pattern**:

```
┌─────────────┐
│   START     │
└──────┬──────┘
       │
       ▼
┌─────────────┐     ┌─────────────┐
│   Worker    │────▶│    Tools    │
│   (LLM)     │◀────│  (Execute)  │
└──────┬──────┘     └─────────────┘
       │
       ▼
┌─────────────┐
│ Evaluator   │
│  (Validate) │
└──────┬──────┘
       │
       ├─ Success? ──▶ END
       │
       └─ Continue ──▶ Worker (loop)
```

### Components

1. **Worker Node**: Processes requests using LLM with access to tools and agent routing
2. **Tools Node**: Executes data access, calculations, and agent calls
3. **Evaluator Node**: Validates results against success criteria
4. **Agent Routing**: Intelligently routes to specialized agents as needed

## 📁 Project Structure

```
Financial_consultant_AI/
│
├── 📄 Core Application Files
│   ├── orchestrator.py          # Main LangGraph orchestrator
│   ├── agents.py                 # 8 specialized agent definitions
│   ├── agent_tools.py            # Tools for agent interactions
│   └── app.py                    # Gradio web interface
│
├── 📚 Documentation
│   ├── README.md                 # This file - project overview
│   └── AI_Financial_consultant.txt  # Requirements document
│
├── 🔧 Configuration & Setup
│   ├── requirements.txt          # Python dependencies
│   ├── .env.example              # Environment variables template
│   └── .gitignore                # Git ignore rules
│
└── 🐍 Virtual Environment
    └── venv/                     # Python virtual environment (gitignored)
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+**
- **OpenAI API Key** (for LLM functionality)
- **Snowflake Account** (for data access via MCP server)
- **Git** (for cloning the repository)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Financial_consultant_AI
   ```

2. **Create virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
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

### Running the Application

```bash
python app.py
```

This will launch the Gradio web interface at `http://127.0.0.1:7860`

## 💻 Usage

### Basic Usage

1. **Start the application** (see Quick Start above)

2. **Enter your request** in the message box:
   ```
   Help me construct a portfolio for client ID 12345 with moderate risk tolerance
   ```

3. **Optional**: Specify custom success criteria

4. **Click "Send Message"** or press Enter

5. **Review results**: The orchestrator will automatically:
   - Route to appropriate specialized agents
   - Access necessary data from Snowflake
   - Coordinate multiple agents if needed
   - Provide comprehensive recommendations

### Example Requests

**Portfolio Construction:**
```
Construct a diversified growth portfolio for client ID 12345. 
Client has moderate risk tolerance and a 15-year time horizon.
```

**Investment Research:**
```
Find technology-focused ETFs with low expense ratios and strong 
historical performance for a growth-oriented portfolio.
```

**Risk Analysis:**
```
Analyze the risk profile of portfolio PORT-001. Calculate VaR, 
Sharpe ratio, and perform stress testing for 2008 crisis scenario.
```

**Tax Optimization:**
```
Identify tax-loss harvesting opportunities for client ID 12345 
across all taxable accounts.
```

**Report Generation:**
```
Generate a detailed portfolio report for client ID 12345 including 
performance, allocation, and recommendations.
```

**Account Operations:**
```
Open a new IRA account for client ID 12345 with beneficiary 
designations and proper titling.
```

## 🎓 Key Concepts

### Agent Orchestration
The Orchestrator Agent intelligently routes requests to specialized agents:
- **Single Agent Tasks**: Simple requests routed to one agent
- **Multi-Agent Workflows**: Complex requests coordinated across multiple agents
- **Context Sharing**: Agents share context for seamless collaboration
- **Conflict Resolution**: Orchestrator resolves conflicts between agent recommendations

### Data Integration
All data access is integrated with Snowflake:
- **Client Data**: Profiles, goals, risk tolerance, holdings
- **Portfolio Data**: Positions, values, performance metrics
- **Market Data**: Real-time and historical market data
- **Research Data**: Structured and unstructured research materials

### Workflow Automation
The platform automates end-to-end workflows:
- **Portfolio Construction**: From risk assessment to allocation recommendations
- **Investment Discovery**: From search criteria to comparative analysis
- **Risk Analysis**: From portfolio data to comprehensive risk metrics
- **Report Generation**: From data collection to formatted reports

## 📊 Use Cases

### 1. Portfolio Construction
Advisor requests portfolio construction → Orchestrator routes to Portfolio Architect → Accesses client data → Generates allocation recommendations → Validates compliance

### 2. Investment Research
Advisor searches for investments → Orchestrator routes to Investment Research Agent → Searches structured and unstructured data → Provides comparative analysis

### 3. Risk Assessment
Advisor requests risk analysis → Orchestrator routes to Risk Analytics Agent → Calculates risk metrics → Performs stress testing → Provides recommendations

### 4. Tax Optimization
Advisor requests tax analysis → Orchestrator routes to Tax Optimization Agent → Analyzes tax impact → Identifies harvesting opportunities → Optimizes asset location

### 5. Client Reporting
Advisor requests report → Orchestrator coordinates Reporting Agent → Gathers data from multiple sources → Generates customized report

### 6. Account Management
Advisor requests account operation → Orchestrator routes to Account Operations Agent → Executes operation → Updates documentation

## 🔧 Configuration

### Environment Variables

Create a `.env` file with:
```env
OPENAI_API_KEY=your_api_key_here
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_USER=your_user
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_WAREHOUSE=your_warehouse
SNOWFLAKE_DATABASE=your_database
SNOWFLAKE_SCHEMA=your_schema
```

### Customization

- **Agent Behavior**: Modify agent system prompts in `agents.py`
- **Tool Functions**: Extend tools in `agent_tools.py`
- **Workflow Logic**: Customize orchestrator in `orchestrator.py`
- **UI Interface**: Customize Gradio interface in `app.py`

## 📖 Documentation

- **[AI_Financial_consultant.txt](AI_Financial_consultant.txt)**: Complete requirements document
- **[README.md](README.md)**: This file - project overview

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [LangGraph](https://github.com/langchain-ai/langgraph)
- Uses [LangChain](https://github.com/langchain-ai/langchain) for LLM integration
- [Gradio](https://gradio.app/) for the web interface
- Architecture inspired by [sqlfilesbank](https://github.com/alokhcst/sqlfilesbank) project

## 📧 Contact

For questions or support, please open an issue on GitHub.

## 🗺️ Roadmap

- [ ] Enhanced Snowflake MCP integration
- [ ] Real-time market data API integration
- [ ] Advanced portfolio optimization algorithms
- [ ] Multi-client batch processing
- [ ] Integration with CRM systems
- [ ] Mobile app interface
- [ ] Advanced reporting templates
- [ ] Machine learning model integration for predictions

---

**Made with ❤️ for financial advisors**

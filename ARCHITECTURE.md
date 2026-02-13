# Architecture Documentation

## Overview

The Financial Consultant AI Platform is built using a **LangGraph-based multi-agent architecture** that orchestrates 8 specialized AI agents to help financial advisors with portfolio construction, investment research, risk analysis, tax optimization, and client management.

## Architecture Pattern

The system follows the **worker-evaluator pattern** from the sqlfilesbank architecture:

1. **Worker Node**: Processes requests using LLM with access to tools
2. **Tools Node**: Executes operations (data access, calculations, agent calls)
3. **Evaluator Node**: Validates results against success criteria
4. **Loop**: Continues until success criteria met or user input needed

## Component Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Gradio Web Interface                      │
│                         (app.py)                             │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              Financial Consultant Orchestrator               │
│                      (orchestrator.py)                      │
│                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   Worker     │───▶│    Tools     │───▶│  Evaluator   │  │
│  │    Node      │◀───│     Node     │    │     Node     │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Specialized Agents                        │
│                       (agents.py)                           │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ 1. Portfolio Architect Agent                         │  │
│  │ 2. Investment Research Agent                          │  │
│  │ 3. Risk Analytics Agent                               │  │
│  │ 4. Tax Optimization Agent                             │  │
│  │ 5. Transition Planning Agent                          │  │
│  │ 6. Reporting & Communication Agent                    │  │
│  │ 7. Account Operations Agent                           │  │
│  │ 8. Orchestrator Agent (Super Agent)                   │  │
│  └──────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      Agent Tools                             │
│                    (agent_tools.py)                          │
│                                                              │
│  • get_client_profile()                                     │
│  • get_portfolio_data()                                     │
│  • search_investment_solutions()                            │
│  • calculate_risk_metrics()                                 │
│  • analyze_tax_impact()                                     │
│  • create_transition_plan()                                 │
│  • generate_portfolio_report()                              │
│  • execute_account_operation()                              │
│  • get_market_data()                                        │
│  • validate_compliance()                                    │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Data Sources                              │
│                                                              │
│  • Snowflake Data Warehouse (via MCP)                       │
│  • Market Data APIs                                         │
│  • Research Databases                                        │
│  • Compliance Systems                                        │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

### Request Processing Flow

1. **User Input**: Advisor enters request in Gradio interface
2. **Orchestrator**: Routes request to appropriate agent(s)
3. **Agent Processing**: Agent uses tools to access data and perform calculations
4. **Tool Execution**: Tools interact with Snowflake and external APIs
5. **Result Synthesis**: Agent synthesizes results
6. **Evaluation**: Evaluator checks if success criteria met
7. **Response**: Final response returned to advisor

### Multi-Agent Workflow Example

**Portfolio Construction Request:**
```
User Request
    ↓
Orchestrator Agent
    ├─→ Portfolio Architect Agent
    │   ├─→ get_client_profile()
    │   ├─→ get_portfolio_data()
    │   └─→ calculate_portfolio_allocation()
    ├─→ Risk Analytics Agent
    │   ├─→ calculate_risk_metrics()
    │   └─→ perform_stress_test()
    └─→ Tax Optimization Agent
        └─→ analyze_tax_impact()
    ↓
Synthesized Response
    ↓
Evaluator
    ↓
Final Response to User
```

## State Management

The LangGraph workflow maintains state through the `State` TypedDict:

```python
class State(TypedDict):
    messages: List[Any]              # Conversation history
    success_criteria: str            # Success criteria for current request
    feedback_on_work: Optional[str]  # Feedback from evaluator
    success_criteria_met: bool       # Whether criteria met
    user_input_needed: bool          # Whether user input needed
    agent_context: Dict[str, Any]    # Context shared between agents
```

## Agent Communication

### Direct Agent Calls
Agents can be called directly by the orchestrator:
```python
result = await orchestrator.route_to_agent("portfolio_architect", task, context)
```

### Tool-Based Communication
Agents use shared tools to access data and perform operations:
```python
tools = get_agent_tools()
llm_with_tools = llm.bind_tools(tools)
```

### Context Sharing
Agents share context through the `agent_context` in state:
```python
state["agent_context"] = {
    "client_id": "12345",
    "portfolio_id": "PORT-001",
    "previous_analysis": {...}
}
```

## Integration Points

### Snowflake Integration
- **MCP Server**: Primary integration method (recommended)
- **Direct Connection**: Fallback option via environment variables
- **Data Access**: Client profiles, portfolios, market data, compliance data

### Market Data APIs
- **Real-time Data**: Current prices, quotes
- **Historical Data**: Performance metrics, risk calculations
- **Fundamental Data**: Company information, financials

### Research Data
- **Structured Data**: Performance metrics, risk factors
- **Unstructured Data**: Research reports, fund manager commentary

## Error Handling

### Agent Errors
- Agents catch exceptions and return error messages
- Orchestrator handles agent failures gracefully
- Fallback to alternative agents when possible

### Tool Errors
- Tools validate inputs before execution
- Return descriptive error messages
- Log errors for debugging

### Workflow Errors
- Evaluator detects incomplete responses
- Workflow loops until success or user input needed
- User can provide clarification if stuck

## Performance Considerations

### Caching
- Client profile data cached for session
- Portfolio data cached for recent requests
- Market data cached with TTL

### Parallel Processing
- Multiple agents can process in parallel
- Tools execute independently
- Results synthesized after completion

### Resource Management
- LLM calls optimized for cost
- Database queries optimized for performance
- Memory checkpointing for state persistence

## Security

### Data Access
- All data access through authenticated connections
- Client data access restricted by advisor permissions
- Audit trail for all operations

### API Keys
- Environment variables for sensitive credentials
- Never exposed in code or logs
- Rotated regularly

### Compliance
- All recommendations validated against IPS
- Regulatory compliance checked
- Audit trail maintained

## Extensibility

### Adding New Agents
1. Create agent class inheriting from `BaseAgent`
2. Define agent-specific system prompt
3. Register agent in `OrchestratorAgent`
4. Update orchestrator routing logic

### Adding New Tools
1. Define tool function in `agent_tools.py`
2. Create input model if needed
3. Register tool in `get_agent_tools()`
4. Update agent prompts if needed

### Customizing Workflows
1. Modify orchestrator routing logic
2. Add custom evaluation criteria
3. Extend state management
4. Add new workflow nodes if needed

## Testing Strategy

### Unit Tests
- Test individual agent processing
- Test tool functions
- Test state management

### Integration Tests
- Test agent orchestration
- Test workflow execution
- Test data integration

### End-to-End Tests
- Test complete workflows
- Test user interactions
- Test error scenarios

## Deployment

### Development
- Local virtual environment
- Direct Gradio interface
- Local Snowflake connection

### Production
- Containerized deployment
- Load balancing for multiple users
- Production Snowflake warehouse
- Monitoring and logging

## Monitoring

### Metrics
- Request processing time
- Agent usage statistics
- Tool execution times
- Error rates

### Logging
- All agent interactions logged
- Tool executions logged
- Error details logged
- User interactions logged

## Future Enhancements

- **Real-time Updates**: WebSocket connections for live updates
- **Batch Processing**: Process multiple clients simultaneously
- **Advanced Analytics**: Machine learning for predictions
- **Mobile Interface**: Native mobile app
- **CRM Integration**: Connect with Salesforce, HubSpot, etc.
- **Document Management**: Automated document generation and storage

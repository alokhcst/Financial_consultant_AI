"""
Specialized Agents for Financial Consultant AI Platform

This module defines the 8 specialized agents that handle different aspects
of financial advisory work. Each agent has specific expertise and tools.
"""

from typing import Dict, Any, List, Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from agent_tools import get_agent_tools
from datetime import datetime
import json


class BaseAgent:
    """Base class for all specialized agents"""
    
    def __init__(self, name: str, role: str, description: str, model: str = "gpt-4o-mini"):
        self.name = name
        self.role = role
        self.description = description
        self.llm = ChatOpenAI(model=model)
        self.tools = get_agent_tools()
        self.llm_with_tools = self.llm.bind_tools(self.tools)
    
    def get_system_prompt(self) -> str:
        """Get the system prompt for this agent"""
        return f"""You are the {self.name}, specialized in {self.description}.

Your role: {self.role}

You have access to tools that allow you to:
- Access client and portfolio data from Snowflake
- Search investment solutions
- Perform calculations and analytics
- Generate reports and documentation

Always provide accurate, compliant, and actionable recommendations.
Current date and time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

    async def process(self, task: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Process a task and return the result"""
        messages = [
            SystemMessage(content=self.get_system_prompt()),
            HumanMessage(content=task)
        ]
        
        if context:
            context_msg = f"\n\nContext: {json.dumps(context, indent=2)}"
            messages.append(HumanMessage(content=context_msg))
        
        response = await self.llm_with_tools.ainvoke(messages)
        return response.content


class PortfolioArchitectAgent(BaseAgent):
    """Intelligent portfolio construction and optimization agent"""
    
    def __init__(self):
        super().__init__(
            name="Portfolio Architect Agent",
            role="Intelligent portfolio construction and optimization",
            description="Analyzing client risk profiles, recommending optimal asset allocation, performing rebalancing calculations, and validating compliance"
        )
    
    def get_system_prompt(self) -> str:
        base_prompt = super().get_system_prompt()
        return f"""{base_prompt}

Your specific capabilities:
1. Analyze client risk profiles and investment objectives
2. Recommend optimal asset allocation strategies based on Modern Portfolio Theory
3. Perform portfolio rebalancing calculations
4. Validate compliance with investment mandates and regulatory requirements
5. Generate multiple portfolio scenarios for comparison
6. Consider tax efficiency in allocation recommendations

When constructing portfolios:
- Always consider client risk tolerance and capacity
- Ensure diversification across asset classes, sectors, and geographies
- Validate against investment policy statements
- Consider tax implications
- Provide clear rationale for recommendations
"""


class InvestmentResearchAgent(BaseAgent):
    """Investment solution discovery and analysis agent"""
    
    def __init__(self):
        super().__init__(
            name="Investment Research Agent",
            role="Investment solution discovery and analysis",
            description="Searching structured and unstructured data to find and analyze investment solutions"
        )
    
    def get_system_prompt(self) -> str:
        base_prompt = super().get_system_prompt()
        return f"""{base_prompt}

Your specific capabilities:
1. Search structured data (performance metrics, risk factors, expense ratios)
2. Analyze unstructured data (research reports, fund manager commentary, market insights)
3. Provide comparative analysis of investment vehicles
4. Track and evaluate emerging investment opportunities
5. Deliver contextual recommendations based on client needs

When researching investments:
- Use both structured quantitative data and qualitative research
- Compare similar investment options
- Highlight key differentiators
- Consider expense ratios, tax efficiency, and liquidity
- Provide balanced analysis of pros and cons
"""


class RiskAnalyticsAgent(BaseAgent):
    """Portfolio risk assessment and stress testing agent"""
    
    def __init__(self):
        super().__init__(
            name="Risk Analytics Agent",
            role="Portfolio risk assessment and stress testing",
            description="Performing scenario analysis, calculating risk metrics, and identifying concentration risks"
        )
    
    def get_system_prompt(self) -> str:
        base_prompt = super().get_system_prompt()
        return f"""{base_prompt}

Your specific capabilities:
1. Perform scenario analysis and stress testing
2. Calculate risk metrics (VaR, Sharpe ratio, beta, standard deviation, max drawdown)
3. Identify concentration risks and correlation exposures
4. Model downside protection scenarios
5. Provide early warning alerts for portfolio drift

When analyzing risk:
- Use multiple risk metrics for comprehensive assessment
- Test portfolios under various stress scenarios
- Identify concentration risks (sector, geography, individual securities)
- Consider correlation between holdings
- Provide actionable recommendations to mitigate risks
"""


class TaxOptimizationAgent(BaseAgent):
    """Tax-efficient investment strategies agent"""
    
    def __init__(self):
        super().__init__(
            name="Tax Optimization Agent",
            role="Tax-efficient investment strategies",
            description="Analyzing tax impact, identifying tax-loss harvesting opportunities, and optimizing asset location"
        )
    
    def get_system_prompt(self) -> str:
        base_prompt = super().get_system_prompt()
        return f"""{base_prompt}

Your specific capabilities:
1. Analyze tax impact of portfolio transitions
2. Identify tax-loss harvesting opportunities
3. Optimize asset location across account types (taxable, IRA, 401k, trust)
4. Calculate capital gains/losses for rebalancing decisions
5. Ensure compliance with wash-sale rules

When optimizing taxes:
- Consider client's tax bracket and filing status
- Maximize tax-loss harvesting opportunities
- Optimize asset location (tax-inefficient assets in tax-deferred accounts)
- Minimize realized capital gains
- Ensure compliance with tax regulations
"""


class TransitionPlanningAgent(BaseAgent):
    """Portfolio transition execution strategy agent"""
    
    def __init__(self):
        super().__init__(
            name="Transition Planning Agent",
            role="Portfolio transition execution strategy",
            description="Creating step-by-step transition roadmaps and sequencing trades to minimize impact"
        )
    
    def get_system_prompt(self) -> str:
        base_prompt = super().get_system_prompt()
        return f"""{base_prompt}

Your specific capabilities:
1. Create step-by-step transition roadmaps
2. Sequence trades to minimize market impact and tax consequences
3. Identify transition risks and mitigation strategies
4. Estimate transition costs (taxes, trading costs, opportunity costs)
5. Coordinate timing across multiple accounts

When planning transitions:
- Minimize tax impact through strategic sequencing
- Consider market impact of large trades
- Optimize timing to reduce costs
- Coordinate across multiple accounts
- Provide clear execution roadmap
"""


class ReportingCommunicationAgent(BaseAgent):
    """Client-facing documentation and reports agent"""
    
    def __init__(self):
        super().__init__(
            name="Reporting & Communication Agent",
            role="Client-facing documentation and reports",
            description="Generating customized reports and adapting communication to client sophistication level"
        )
    
    def get_system_prompt(self) -> str:
        base_prompt = super().get_system_prompt()
        return f"""{base_prompt}

Your specific capabilities:
1. Generate customized reports (detailed, executive summary, one-pagers)
2. Create visual presentations of portfolio performance
3. Produce regulatory and compliance documentation
4. Adapt communication style to client sophistication level
5. Generate meeting preparation materials

When creating reports:
- Tailor format and detail level to client preferences
- Use clear, jargon-free language for less sophisticated clients
- Include visualizations where helpful
- Highlight key insights and recommendations
- Ensure compliance documentation is complete
"""


class AccountOperationsAgent(BaseAgent):
    """Account inception and administrative workflows agent"""
    
    def __init__(self):
        super().__init__(
            name="Account Operations Agent",
            role="Account inception and administrative workflows",
            description="Automating account opening, consolidation, and administrative processes"
        )
    
    def get_system_prompt(self) -> str:
        base_prompt = super().get_system_prompt()
        return f"""{base_prompt}

Your specific capabilities:
1. Automate account opening processes
2. Handle account consolidation workflows
3. Manage beneficiary designations and titling
4. Process account transfers and rollovers
5. Ensure documentation completeness

When handling account operations:
- Ensure all required documentation is collected
- Validate information for accuracy
- Follow firm procedures and compliance requirements
- Coordinate with custodians and other parties
- Track status and provide updates
"""


class OrchestratorAgent(BaseAgent):
    """Super agent that coordinates all other agents"""
    
    def __init__(self):
        super().__init__(model="gpt-4o")  # Use more powerful model for orchestration
        self.name = "Orchestrator Agent"
        self.role = "Coordination and workflow management"
        self.description = "Routing requests, sequencing workflows, and maintaining context across agent interactions"
        
        # Initialize all specialized agents
        self.portfolio_architect = PortfolioArchitectAgent()
        self.investment_research = InvestmentResearchAgent()
        self.risk_analytics = RiskAnalyticsAgent()
        self.tax_optimization = TaxOptimizationAgent()
        self.transition_planning = TransitionPlanningAgent()
        self.reporting_communication = ReportingCommunicationAgent()
        self.account_operations = AccountOperationsAgent()
        
        self.agents = {
            "portfolio_architect": self.portfolio_architect,
            "investment_research": self.investment_research,
            "risk_analytics": self.risk_analytics,
            "tax_optimization": self.tax_optimization,
            "transition_planning": self.transition_planning,
            "reporting_communication": self.reporting_communication,
            "account_operations": self.account_operations,
        }
    
    def get_system_prompt(self) -> str:
        return f"""You are the Orchestrator Agent (Super Agent) for the Financial Consultant AI Platform.

Your role: Coordinate and manage workflows across all specialized agents.

Available agents:
1. Portfolio Architect Agent - Portfolio construction and optimization
2. Investment Research Agent - Investment solution discovery
3. Risk Analytics Agent - Risk assessment and stress testing
4. Tax Optimization Agent - Tax-efficient strategies
5. Transition Planning Agent - Portfolio transition execution
6. Reporting & Communication Agent - Client reports and documentation
7. Account Operations Agent - Account management workflows

Your responsibilities:
- Route requests to appropriate specialist agents
- Sequence multi-step workflows intelligently
- Maintain context across agent interactions
- Resolve conflicts between agent recommendations
- Provide unified interface for advisor interactions
- Track task completion and dependencies

When orchestrating:
- Determine which agent(s) are needed for the task
- Sequence agent calls in logical order
- Pass context between agents
- Synthesize results from multiple agents
- Provide comprehensive final response

Current date and time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
    
    async def route_to_agent(self, agent_name: str, task: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Route a task to a specific agent"""
        if agent_name in self.agents:
            return await self.agents[agent_name].process(task, context)
        else:
            return f"Unknown agent: {agent_name}"



"""
Financial Consultant AI Orchestrator

Main LangGraph workflow orchestrator that coordinates all specialized agents
following the worker-evaluator pattern from sqlfilesbank architecture.
"""

from typing import Annotated, TypedDict, List, Any, Optional, Dict
from typing_extensions import TypedDict as TypedDictExt
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from datetime import datetime
import uuid
import json

from agents import (
    OrchestratorAgent,
    PortfolioArchitectAgent,
    InvestmentResearchAgent,
    RiskAnalyticsAgent,
    TaxOptimizationAgent,
    TransitionPlanningAgent,
    ReportingCommunicationAgent,
    AccountOperationsAgent
)
from agent_tools import get_agent_tools

load_dotenv(override=True)


class State(TypedDict):
    """
    State dictionary for the LangGraph workflow.
    
    Maintains conversation history, success criteria, feedback, and workflow control flags.
    """
    messages: Annotated[List[Any], add_messages]
    success_criteria: str
    feedback_on_work: Optional[str]
    success_criteria_met: bool
    user_input_needed: bool
    agent_context: Optional[Dict[str, Any]]  # Context shared between agents


class EvaluatorOutput(BaseModel):
    """
    Structured output model for the evaluator LLM.
    
    Provides structured feedback on whether the worker's response meets success criteria.
    """
    feedback: str = Field(description="Feedback on the assistant's response")
    success_criteria_met: bool = Field(description="Whether the success criteria have been met")
    user_input_needed: bool = Field(
        description="True if more input is needed from the user, clarifications, or if assistant is stuck"
    )
    next_agent: Optional[str] = Field(
        default=None,
        description="Suggested next agent to involve if workflow should continue"
    )


class FinancialConsultantOrchestrator:
    """
    Main orchestrator class implementing LangGraph workflow for Financial Consultant AI.
    
    This class orchestrates the 8 specialized agents using a worker-evaluator pattern:
    1. Worker node processes requests using LLM with tools and agent routing
    2. Tools execute (data access, calculations, agent calls)
    3. Evaluator node checks if success criteria is met
    4. Loop continues until criteria met or user input needed
    """
    
    def __init__(self):
        """Initialize orchestrator instance."""
        self.worker_llm_with_tools = None
        self.evaluator_llm_with_output = None
        self.tools = None
        self.graph = None
        self.orchestrator_id = str(uuid.uuid4())
        self.memory = MemorySaver()
        
        # Initialize all agents
        self.orchestrator_agent = OrchestratorAgent()
        self.portfolio_architect = PortfolioArchitectAgent()
        self.investment_research = InvestmentResearchAgent()
        self.risk_analytics = RiskAnalyticsAgent()
        self.tax_optimization = TaxOptimizationAgent()
        self.transition_planning = TransitionPlanningAgent()
        self.reporting_communication = ReportingCommunicationAgent()
        self.account_operations = AccountOperationsAgent()
        
        self.agents = {
            "orchestrator": self.orchestrator_agent,
            "portfolio_architect": self.portfolio_architect,
            "investment_research": self.investment_research,
            "risk_analytics": self.risk_analytics,
            "tax_optimization": self.tax_optimization,
            "transition_planning": self.transition_planning,
            "reporting_communication": self.reporting_communication,
            "account_operations": self.account_operations,
        }
    
    async def setup(self):
        """
        Initialize and configure the orchestrator.
        
        Sets up LLM instances, loads tools, and builds the LangGraph workflow.
        Must be called before using the orchestrator.
        """
        self.tools = get_agent_tools()
        worker_llm = ChatOpenAI(model="gpt-4o-mini")
        self.worker_llm_with_tools = worker_llm.bind_tools(self.tools)
        evaluator_llm = ChatOpenAI(model="gpt-4o-mini")
        self.evaluator_llm_with_output = evaluator_llm.with_structured_output(EvaluatorOutput)
        await self.build_graph()
    
    def worker(self, state: State) -> Dict[str, Any]:
        """
        Worker node that processes user requests using LLM and tools.
        
        This node:
        - Constructs system prompts with task instructions and success criteria
        - Invokes the LLM with access to tools and agent routing capabilities
        - Handles feedback from previous evaluation attempts
        - Returns LLM response for routing to tools or evaluator
        """
        system_message = f"""You are the Financial Consultant AI Orchestrator, coordinating multiple specialized agents to help financial advisors.

Available Specialized Agents:
1. Portfolio Architect Agent - Portfolio construction, asset allocation, rebalancing
2. Investment Research Agent - Investment solution discovery and analysis
3. Risk Analytics Agent - Risk assessment, stress testing, risk metrics
4. Tax Optimization Agent - Tax-efficient strategies, tax-loss harvesting
5. Transition Planning Agent - Portfolio transition execution and sequencing
6. Reporting & Communication Agent - Client reports and documentation
7. Account Operations Agent - Account opening, consolidation, transfers

Your capabilities:
- Route requests to appropriate specialist agents
- Coordinate multi-agent workflows
- Access client and portfolio data from Snowflake
- Perform calculations and analytics
- Generate reports and documentation
- Execute account operations

When processing requests:
1. Understand the advisor's request and identify which agent(s) are needed
2. Use tools to access necessary data
3. Route to appropriate agents or use tools directly
4. Coordinate multiple agents if needed for complex workflows
5. Synthesize results into comprehensive response
6. Ensure all recommendations are compliant and actionable

Current date and time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Success criteria:
{state["success_criteria"]}
"""
        
        if state.get("feedback_on_work"):
            system_message += f"""

Previously you thought you completed the assignment, but your reply was rejected because the success criteria was not met.
Here is the feedback on why this was rejected:
{state["feedback_on_work"]}
With this feedback, please continue the assignment, ensuring that you meet the success criteria or have a question for the user.
"""
        
        # Add system message if not present
        found_system_message = False
        messages = state["messages"]
        for message in messages:
            if isinstance(message, SystemMessage):
                found_system_message = True
                break
        
        if not found_system_message:
            messages = [SystemMessage(content=system_message)] + messages
        else:
            # Update existing system message
            updated_messages = []
            for message in messages:
                if isinstance(message, SystemMessage):
                    updated_messages.append(SystemMessage(content=system_message))
                else:
                    updated_messages.append(message)
            messages = updated_messages
        
        # Invoke LLM with tools
        response = self.worker_llm_with_tools.invoke(messages)
        
        return {"messages": [response]}
    
    def worker_router(self, state: State) -> str:
        """
        Route worker output to either tools or evaluator.
        
        Checks if the last message contains tool calls.
        Returns "tools" if tool calls present, "evaluator" otherwise.
        """
        messages = state["messages"]
        last_message = messages[-1]
        
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return "tools"
        else:
            return "evaluator"
    
    def format_conversation(self, messages: List[Any]) -> str:
        """
        Format conversation messages into readable text string.
        
        Converts list of message objects into formatted string showing conversation history.
        """
        formatted = []
        for msg in messages:
            if isinstance(msg, HumanMessage):
                formatted.append(f"User: {msg.content}")
            elif isinstance(msg, AIMessage):
                formatted.append(f"Assistant: {msg.content}")
            elif isinstance(msg, SystemMessage):
                formatted.append(f"System: {msg.content}")
        return "\n".join(formatted)
    
    def evaluator(self, state: State) -> State:
        """
        Evaluator node that checks if success criteria has been met.
        
        Reviews worker's response against success criteria and provides structured feedback.
        """
        messages = state["messages"]
        conversation = self.format_conversation(messages)
        success_criteria = state["success_criteria"]
        
        evaluator_prompt = f"""You are an evaluator for the Financial Consultant AI system.

Review the following conversation and determine if the success criteria have been met.

Success Criteria:
{success_criteria}

Conversation:
{conversation}

Evaluate whether:
1. The assistant's response fully addresses the user's request
2. All success criteria are met
3. The response is complete and actionable
4. Any specialized agents were appropriately used
5. The response provides value to the financial advisor

Provide structured feedback on the response quality and whether success criteria are met.
If the response is incomplete, suggest which agent or tool should be used next.
"""
        
        evaluation = self.evaluator_llm_with_output.invoke([HumanMessage(content=evaluator_prompt)])
        
        return {
            "feedback_on_work": evaluation.feedback,
            "success_criteria_met": evaluation.success_criteria_met,
            "user_input_needed": evaluation.user_input_needed,
            "agent_context": {
                **state.get("agent_context", {}),
                "suggested_next_agent": evaluation.next_agent
            }
        }
    
    def route_based_on_evaluation(self, state: State) -> str:
        """
        Route based on evaluation results.
        
        Returns "END" if success criteria met OR user input needed,
        otherwise "worker" to continue processing.
        """
        if state.get("success_criteria_met") or state.get("user_input_needed"):
            return "END"
        else:
            return "worker"
    
    async def build_graph(self):
        """
        Build and compile the LangGraph workflow.
        
        Graph Structure:
        - Nodes: worker, tools, evaluator
        - Flow: START → worker → (tools or evaluator)
        - Loops: tools → worker, evaluator → worker (if not complete)
        """
        workflow = StateGraph(State)
        
        # Add nodes
        workflow.add_node("worker", self.worker)
        workflow.add_node("tools", ToolNode(self.tools))
        workflow.add_node("evaluator", self.evaluator)
        
        # Set entry point
        workflow.set_entry_point("worker")
        
        # Add edges
        workflow.add_conditional_edges(
            "worker",
            self.worker_router,
            {
                "tools": "tools",
                "evaluator": "evaluator"
            }
        )
        
        workflow.add_edge("tools", "worker")
        
        workflow.add_conditional_edges(
            "evaluator",
            self.route_based_on_evaluation,
            {
                "END": END,
                "worker": "worker"
            }
        )
        
        # Compile with memory checkpointing
        self.graph = workflow.compile(checkpointer=self.memory)
    
    async def run_superstep(self, message: str, success_criteria: str = "", history: List[Dict] = None) -> List[Dict]:
        """
        Execute one processing step through the LangGraph workflow.
        
        Args:
            message: User's input message
            success_criteria: Optional success criteria for this request
            history: Previous conversation history
            
        Returns:
            Updated conversation history with user message, assistant reply, and evaluator feedback
        """
        if history is None:
            history = []
        
        # Default success criteria if not provided
        if not success_criteria:
            success_criteria = "The assistant should provide a complete, accurate, and actionable response to the advisor's request, using appropriate specialized agents and tools as needed."
        
        # Convert history to LangChain message format
        langchain_messages = []
        for msg in history:
            if isinstance(msg, dict):
                role = msg.get("role", "user")
                content = msg.get("content", "")
                if role == "user":
                    langchain_messages.append(HumanMessage(content=content))
                elif role == "assistant":
                    langchain_messages.append(AIMessage(content=content))
        
        # Add current user message
        langchain_messages.append(HumanMessage(content=message))
        
        # Initial state
        initial_state = {
            "messages": langchain_messages,
            "success_criteria": success_criteria,
            "feedback_on_work": None,
            "success_criteria_met": False,
            "user_input_needed": False,
            "agent_context": {}
        }
        
        # Run the graph
        config = {"configurable": {"thread_id": self.orchestrator_id}}
        final_state = None
        
        async for event in self.graph.astream(initial_state, config):
            # Process events (could add logging here)
            for node_name, node_state in event.items():
                if node_name == "evaluator":
                    final_state = node_state
        
        # If no final state from evaluator, get the last state
        if final_state is None:
            # Get the last state from the graph
            final_state = await self.graph.ainvoke(initial_state, config)
        
        # Format results for return
        results = []
        
        # Add original history
        for msg in history:
            if isinstance(msg, dict):
                results.append(msg)
        
        # Add user message
        results.append({"role": "user", "content": message})
        
        # Add assistant response
        messages = final_state.get("messages", [])
        assistant_messages = [msg for msg in messages if isinstance(msg, AIMessage)]
        if assistant_messages:
            last_assistant_msg = assistant_messages[-1]
            results.append({"role": "assistant", "content": last_assistant_msg.content})
        
        # Add evaluator feedback if available
        if final_state.get("feedback_on_work"):
            results.append({
                "role": "system",
                "content": f"Evaluator Feedback: {final_state['feedback_on_work']}"
            })
        
        return results
    
    def cleanup(self):
        """Cleanup resources when orchestrator is no longer needed."""
        # Placeholder for future resource cleanup
        pass

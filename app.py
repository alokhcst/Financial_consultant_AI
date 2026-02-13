"""
Financial Consultant AI - Gradio Web Interface

Interactive web interface for financial advisors to interact with the AI platform.
"""

import gradio as gr
from orchestrator import FinancialConsultantOrchestrator
from typing import List, Dict, Tuple


async def setup() -> FinancialConsultantOrchestrator:
    """
    Initialize Financial Consultant orchestrator for Gradio interface.
    
    Creates a new orchestrator instance and sets it up with LLMs and tools.
    Called when the Gradio interface loads.
    
    Returns:
        Initialized FinancialConsultantOrchestrator instance
    """
    orchestrator = FinancialConsultantOrchestrator()
    await orchestrator.setup()
    return orchestrator


async def process_message(
    orchestrator: FinancialConsultantOrchestrator,
    message: str,
    success_criteria: str,
    history: List[Tuple[str, str]]
) -> Tuple[List[Tuple[str, str]], FinancialConsultantOrchestrator]:
    """
    Process a user message through the Financial Consultant orchestrator workflow.
    
    This function:
    1. Normalizes conversation history format
    2. Runs the orchestrator workflow with user message
    3. Formats results for Gradio Chatbot component
    4. Returns updated conversation history
    
    Args:
        orchestrator: FinancialConsultantOrchestrator instance
        message: User's input message
        success_criteria: Optional success criteria
        history: Previous conversation history (list of tuples)
        
    Returns:
        Tuple of (formatted_results, orchestrator) where formatted_results is
        a list of tuples (user_msg, bot_msg) for Gradio
    """
    # Convert history to list of dicts if needed
    if history is None:
        history = []
    
    # Convert Gradio tuple format to dict format
    normalized_history = []
    for msg in history:
        if isinstance(msg, tuple) and len(msg) == 2:
            user_msg, bot_msg = msg
            if user_msg:
                normalized_history.append({"role": "user", "content": user_msg})
            if bot_msg:
                normalized_history.append({"role": "assistant", "content": bot_msg})
        elif isinstance(msg, dict):
            normalized_history.append(msg)
    
    # Process message through orchestrator
    results = await orchestrator.run_superstep(message, success_criteria, normalized_history)
    
    # Convert results back to Gradio tuple format
    formatted_results = []
    current_user_msg = None
    
    for msg in results:
        if isinstance(msg, dict):
            role = msg.get("role", "user")
            content = msg.get("content", "")
            
            if role == "user":
                if current_user_msg is not None:
                    # Add previous user message with empty bot response
                    formatted_results.append((current_user_msg, ""))
                current_user_msg = content
            elif role == "assistant":
                if current_user_msg is not None:
                    formatted_results.append((current_user_msg, content))
                    current_user_msg = None
                else:
                    # Bot message without preceding user message
                    formatted_results.append(("", content))
            elif role == "system":
                # System messages (evaluator feedback) as bot messages
                if current_user_msg is not None:
                    formatted_results.append((current_user_msg, content))
                    current_user_msg = None
                else:
                    formatted_results.append(("", content))
    
    # Handle any remaining user message
    if current_user_msg is not None:
        formatted_results.append((current_user_msg, ""))
    
    return formatted_results, orchestrator


async def reset() -> Tuple[str, str, List, FinancialConsultantOrchestrator]:
    """
    Reset the orchestrator and clear conversation.
    
    Creates a new FinancialConsultantOrchestrator instance and clears the UI inputs.
    Called when user clicks the Reset button.
    
    Returns:
        Tuple of empty strings and empty list to clear UI components, plus new orchestrator
    """
    new_orchestrator = FinancialConsultantOrchestrator()
    await new_orchestrator.setup()
    return "", "", [], new_orchestrator


def free_resources(orchestrator: FinancialConsultantOrchestrator) -> None:
    """
    Cleanup function called when orchestrator state is deleted.
    
    Ensures proper cleanup of resources when the Gradio interface
    is closed or orchestrator is reset. Called automatically by Gradio's
    State component delete_callback.
    
    Args:
        orchestrator: FinancialConsultantOrchestrator instance to clean up
    """
    print("Cleaning up Financial Consultant AI resources")
    try:
        if orchestrator:
            orchestrator.cleanup()
    except Exception as e:
        print(f"Exception during cleanup: {e}")


# Create Gradio interface
with gr.Blocks(title="Financial Consultant AI", theme=gr.themes.Soft()) as ui:
    gr.Markdown("""
    # 🤖 Financial Consultant AI Platform
    
    An intelligent multi-agent system that helps financial advisors:
    - **Construct portfolios** intelligently with AI-powered recommendations
    - **Discover investment solutions** using structured and unstructured data
    - **Analyze risk** with comprehensive stress testing and metrics
    - **Optimize taxes** through strategic planning and tax-loss harvesting
    - **Plan transitions** with step-by-step execution roadmaps
    - **Generate reports** customized to client preferences
    - **Manage accounts** with automated workflows
    
    ## Available Agents
    
    1. **Portfolio Architect** - Portfolio construction and optimization
    2. **Investment Research** - Investment solution discovery
    3. **Risk Analytics** - Risk assessment and stress testing
    4. **Tax Optimization** - Tax-efficient strategies
    5. **Transition Planning** - Portfolio transition execution
    6. **Reporting & Communication** - Client reports and documentation
    7. **Account Operations** - Account management workflows
    8. **Orchestrator** - Coordinates all agents intelligently
    
    ## How to Use
    
    Simply describe what you need help with, and the system will automatically:
    - Route your request to the appropriate specialized agent(s)
    - Access necessary data from Snowflake
    - Coordinate multiple agents for complex workflows
    - Provide comprehensive, actionable recommendations
    
    **Example requests:**
    - "Help me construct a portfolio for client ID 12345 with moderate risk tolerance"
    - "Find investment solutions for a tech-focused growth portfolio"
    - "Analyze the risk profile of portfolio PORT-001 and perform stress testing"
    - "Generate a detailed report for client ID 12345"
    """)
    
    orchestrator = gr.State(delete_callback=free_resources)
    
    with gr.Row():
        chatbot = gr.Chatbot(
            label="Financial Consultant AI",
            height=500,
            show_copy_button=True,
            avatar_images=(None, "🤖")
        )
    
    with gr.Group():
        with gr.Row():
            message = gr.Textbox(
                show_label=False,
                placeholder="Enter your request here... (e.g., 'Help me construct a portfolio for client ID 12345')",
                scale=4
            )
        with gr.Row():
            success_criteria = gr.Textbox(
                show_label=False,
                placeholder="Optional: Specify success criteria for this request (defaults to standard completion)",
                scale=4
            )
    
    with gr.Row():
        reset_button = gr.Button("🔄 Reset Conversation", variant="stop", scale=1)
        go_button = gr.Button("💬 Send Message", variant="primary", scale=1)
    
    # Load orchestrator on startup
    ui.load(setup, [], [orchestrator])
    
    # Event handlers
    message.submit(
        process_message,
        [orchestrator, message, success_criteria, chatbot],
        [chatbot, orchestrator]
    )
    
    success_criteria.submit(
        process_message,
        [orchestrator, message, success_criteria, chatbot],
        [chatbot, orchestrator]
    )
    
    go_button.click(
        process_message,
        [orchestrator, message, success_criteria, chatbot],
        [chatbot, orchestrator]
    )
    
    reset_button.click(
        reset,
        [],
        [message, success_criteria, chatbot, orchestrator]
    )
    
    gr.Markdown("""
    ---
    ### 💡 Tips
    
    - Be specific about client IDs, portfolio IDs, and requirements
    - The system will automatically determine which agents to use
    - Complex requests may involve multiple agents working together
    - All data access is integrated with Snowflake data warehouse
    - Reports can be customized (detailed, executive summary, or one-pager)
    """)


if __name__ == "__main__":
    ui.launch(
        inbrowser=True,
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )

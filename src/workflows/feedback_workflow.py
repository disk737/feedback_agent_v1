"""Main feedback classification workflow."""
from langgraph.graph import StateGraph, START, END

from src.workflows.state import MessagesState
from src.nodes import (
    load_feedback_data,
    classify_comments,
    export_classified_results,
    create_report
)


def create_feedback_workflow():
    """Create and compile the feedback classification workflow."""
    
    workflow = StateGraph(MessagesState)
    
    # Add nodes
    workflow.add_node("load_feedback_data", load_feedback_data)
    workflow.add_node("classify_comments", classify_comments)
    workflow.add_node("export_classified_results", export_classified_results)
    workflow.add_node("create_report", create_report)
    
    # Add edges
    workflow.add_edge(START, "load_feedback_data")
    workflow.add_edge("load_feedback_data", "classify_comments")
    workflow.add_edge("classify_comments", "export_classified_results")
    workflow.add_edge("export_classified_results", "create_report")
    workflow.add_edge("create_report", END)
    
    # Compile the workflow
    return workflow.compile()


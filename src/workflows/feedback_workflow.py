"""Main feedback classification workflow."""
from langgraph.graph import StateGraph, START, END

from src.workflows.state import MessagesState
from src.nodes import (
    load_data_from_hive,
    classify_comments,
    export_classified_results,
    create_report
)


def create_feedback_workflow():
    """Create and compile the feedback classification workflow."""
    
    workflow = StateGraph(MessagesState)
    
    # Add nodes
    workflow.add_node("load_data_from_hive", load_data_from_hive)
    workflow.add_node("classify_comments", classify_comments)
    workflow.add_node("export_classified_results", export_classified_results)
    workflow.add_node("create_report", create_report)
    
    # Add edges
    workflow.add_edge(START, "load_data_from_hive")
    workflow.add_edge("load_data_from_hive", "classify_comments")
    workflow.add_edge("classify_comments", "export_classified_results")
    workflow.add_edge("export_classified_results", "create_report")
    workflow.add_edge("create_report", END)
    
    # Compile the workflow
    return workflow.compile()


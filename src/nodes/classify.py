"""Classification node."""
from src.agents import create_classifier_agent
from src.config.settings import settings


# Create agent instance once
agent_classifier = create_classifier_agent()


def classify_comments(state):
    """Node with the classifier agent that classifies the feedback."""
    
    feedback_list = state["feedback_items"]
    classified_results = []
    
    for feedback in feedback_list:
        # Apply classification limit if set
        if settings.CLASSIFICATION_LIMIT and len(classified_results) >= settings.CLASSIFICATION_LIMIT:
            break
        
        inputs = {"messages": [{"role": "user", "content": feedback.feedback}]}
        response = agent_classifier.invoke(inputs)
        
        feedback.category = response["structured_response"].category
        feedback.rationale = response["structured_response"].rationale
        
        classified_results.append(feedback)
    
    print(f"✅ Classified {len(classified_results)} feedback items")
    
    return {
        "classified_results": classified_results,
        "node_calls": state.get('node_calls', 0) + 1
    }


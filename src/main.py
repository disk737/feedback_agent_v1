"""Main entry point for the feedback classification system."""
from datetime import datetime
from src.workflows import create_feedback_workflow
from src.utils import send_slack_message, format_slack_message
from src.config.settings import settings


def main():
    """Run the feedback classification workflow."""
    
    # Create workflow
    print("🔧 Creating workflow...")
    workflow = create_feedback_workflow()
    
    # Initial state
    initial_state = {
        "current_date": datetime.now().strftime("%Y-%m-%d"),
        "feedback_items": [],
        "classified_results": [],
        "final_report": "",
        "node_calls": 0
    }
    # Run workflow
    print("🚀 Starting feedback classification workflow...\n")
    result = workflow.invoke(initial_state)
    
    # Display results
    print(f"\n✨ Workflow Complete!")
    print(f"   Total items classified: {len(result['classified_results'])}")
    print(f"   Total node calls: {result['node_calls']}")
    
    # Format and display the Slack message
    print("\n" + "="*80)
    print("📱 SLACK MESSAGE (Ready to Copy & Paste)")
    print("="*80 + "\n")
    
    slack_message = format_slack_message(result['final_report'])
    print(slack_message)
    
    print("\n" + "="*80)
    print("✅ Copy the message above and paste it directly into Slack!")
    print("="*80)
    
    
    if settings.SEND_TO_SLACK:
        send_slack_message(slack_message, use_dev_channel=True)
        print("✅ Slack message sent")

if __name__ == "__main__":
    main()


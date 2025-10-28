"""Slack integration utilities."""
from datetime import datetime
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from src.config.settings import settings


def format_slack_message(report_response) -> str:
    """Format the report for Slack with header."""
    current_month = datetime.now().strftime('%B')
    current_year = datetime.now().year
    
    slack_message = f"""📊 *User Feedback Analysis Report - {current_month} {current_year}*

{report_response['structured_response'].slack_message}
"""
    return slack_message


def send_slack_message(message: str, use_dev_channel: bool = False) -> bool:
    """
    Send a message to Slack.
    
    Args:
        message: The message to send
        use_dev_channel: If True, use dev channel, otherwise use production channel
    
    Returns:
        True if successful, False otherwise
    """
    # Initialize the client with bot token
    client = WebClient(token=settings.SLACK_BOT_TOKEN)
    
    # Choose channel
    channel = settings.SLACK_CHANNEL_ID_DEV if use_dev_channel else settings.SLACK_CHANNEL_ID
    
    try:
        response = client.chat_postMessage(
            channel=channel,
            text=message
        )
        print(f"✅ Message sent to Slack: {response['ts']}")
        return True
        
    except SlackApiError as e:
        print(f"❌ Error sending message to Slack: {e.response['error']}")
        return False


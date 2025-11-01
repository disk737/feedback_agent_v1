"""Data loading node from Excel file.
    Currently not used, but kept for reference."""
import pandas as pd

from src.config.settings import settings
from src.models import FeedbackItem


def load_feedback_data(state):
    """Load the feedback data from the Excel file."""
    
    # Read Excel file
    excel_path = settings.DATA_DIR / 'feedback_insight_users_sep.xlsx'
    df = pd.read_excel(excel_path)
    
    # Filter to only needed columns
    df_filtered = df[['User ID', 'Translated Comment', 'Insight Sub Type', 'Insight', 'Product Line Name']]
    
    # Convert DataFrame to list of Feedback objects
    feedback_list = [
        FeedbackItem(
            user_id=row['User ID'],
            feedback=row['Translated Comment'],
            insight_sub_type=row['Insight Sub Type'],
            insight_type=row['Insight'],
            product_line_name=row['Product Line Name']
        )
        for row in df_filtered.to_dict('records')
    ]
    
    print(f"✅ Loaded {len(feedback_list)} feedback items from Excel")
    
    return {
        "feedback_items": feedback_list,
        "classified_results": []
    }


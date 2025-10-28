"""Export node."""
import pandas as pd
from datetime import datetime

from src.config.settings import settings


def export_classified_results(state):
    """Export classified feedback to Excel file."""
    
    classified_results = state["classified_results"]
    
    # Create output directory if it doesn't exist
    settings.OUTPUT_DIR.mkdir(exist_ok=True)
    
    # Convert to DataFrame
    data = []
    for item in classified_results:
        data.append({
            'User ID': item.user_id,
            'Feedback': item.feedback,
            'Insight Sub Type': item.insight_sub_type,
            'Insight Type': item.insight_type,
            'Product Line': item.product_line_name,
            'Category': item.category,
            'Rationale': item.rationale
        })
    
    df = pd.DataFrame(data)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = settings.OUTPUT_DIR / f'classified_feedback_{timestamp}.xlsx'
    
    # Export to Excel
    df.to_excel(filename, index=False)
    
    print(f"✅ Exported {len(classified_results)} classified items to: {filename}")
    
    return {
        "node_calls": state.get('node_calls', 0) + 1
    }


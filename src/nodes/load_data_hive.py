"""
LangGraph node to load negative feedback data from Hive/Presto database.
"""

import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

from src.models import FeedbackItem


def load_data_from_hive(state):
    """
    Load negative feedback comments from Hive/Presto database.
    
    Args:
        state: Current state containing month_analysis and year_analysis
        
    Returns:
        Updated state with feedback_items (List[FeedbackItem]) and classified_results
    """
    # Load environment variables
    load_dotenv()
    
    # Connection parameters
    PRESTO_HOST = "presto-gdc.adp.autodesk.com"
    PRESTO_PORT = 443
    PRESTO_USER = os.getenv("PRESTO_USER")
    PRESTO_PASSWORD = os.getenv("PRESTO_PASSWORD")
    PRESTO_CATALOG = os.getenv("PRESTO_CATALOG", "hive")
    PRESTO_SCHEMA = "desktop_product_intelligence_public"
    
    # Get month and year from state
    current_date = state.get("current_date","2025-09-01")
    month_analysis = int(current_date.split("-")[1]) - 1  # Subtract 1 to get previous month
    year_analysis = int(current_date.split("-")[0])   
    
    # Build the start date for the query (YYYY-MM-01)
    start_date = f"{year_analysis}-{month_analysis:02d}-01"
    
    print(f"📅 Loading data for: {start_date} (Month {month_analysis}, Year {year_analysis})")
    
    try:
        # Create SQLAlchemy engine
        connection_string = (
            f"trino://{PRESTO_USER}:{PRESTO_PASSWORD}@"
            f"{PRESTO_HOST}:{PRESTO_PORT}/"
            f"{PRESTO_CATALOG}/{PRESTO_SCHEMA}"
        )
        
        engine = create_engine(connection_string)
        
        # Dynamic query using month and year parameters
        query_comments = f"""
        SELECT DISTINCT
            DATE_FORMAT(parsed_date, '%Y-%m-%d') AS date_date,
            user_id,
            translated_comment,
            insight,
            insight_sub_type,
            product_line_name
        FROM (
            SELECT 
                DATE_PARSE(dt, '%Y%m%d') AS parsed_date,
                user_id,
                translated_comment,
                insight,
                insight_sub_type,
                product_line_name,
                delivery_channel,
                sentiment
            FROM desktop_product_intelligence_public.halley_feedback_qualtrics_comments
            WHERE delivery_channel IN ('account_portal', 'email')
                AND sentiment IN ('Negative', 'Very Negative')
        ) subquery
        WHERE parsed_date >= TIMESTAMP '{start_date}'
            AND parsed_date < DATE_ADD('month', 1, TIMESTAMP '{start_date}')
        ORDER BY 1 DESC
        LIMIT 500
        """
        
        # Execute query
        print("🔍 Executing query to fetch negative feedback comments...")
        df_comments = pd.read_sql(query_comments, engine)
        
        # Clean up connection
        engine.dispose()
        
        print(f"✅ Successfully fetched {len(df_comments)} rows")
        print(f"Date range: {df_comments['date_date'].min()} to {df_comments['date_date'].max()}")
        print(f"Unique users: {df_comments['user_id'].nunique()}")
        
      
        
    except Exception as e:
        error_msg = f"Failed to load data from Hive: {str(e)}"
        print(f"❌ {error_msg}")
        
        # Return empty state on error
        return {
            "feedback_items": [],
            "classified_results": []
        }
    
    # Convert DataFrame to list of FeedbackItem objects
    feedback_list = [
        FeedbackItem(
            user_id=row['user_id'] or 'EMPTY_USER_ID',
            feedback=row['translated_comment'] or 'EMPTY_FEEDBACK',
            insight_sub_type=row['insight_sub_type'] or 'EMPTY_INSIGHT_SUB_TYPE',
            insight_type=row['insight'] or 'EMPTY_INSIGHT_TYPE',
            product_line_name=row['product_line_name'] or 'EMPTY_PRODUCT_LINE_NAME'
        )
        for row in df_comments.to_dict('records')
    ]

    print(f"✅ Converted to {len(feedback_list)} feedback items")

    return {
        "feedback_items": feedback_list,
        "classified_results": []
    }

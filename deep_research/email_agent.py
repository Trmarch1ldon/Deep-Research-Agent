import os
from typing import Dict
import base64
import io
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

import sendgrid
from sendgrid.helpers.mail import Email, Mail, Content, To
from agents import Agent, function_tool

def extract_chart_data_from_content(content: str) -> list[str]:
    """Extract base64 chart data from content that includes charts"""
    import re
    
    # Look for base64 chart data in the content
    chart_pattern = r'data:image/png;base64,([A-Za-z0-9+/=]+)'
    matches = re.findall(chart_pattern, content)
    
    return matches if matches else []

@function_tool
def send_email_with_charts(subject: str, html_body: str, include_charts: bool = True) -> Dict[str, str]:
    """ Send an email with the given subject, HTML body, and charts embedded in the content """
    
    # Extract any charts that are already embedded in the content
    chart_html = ""
    if include_charts:
        try:
            # Look for embedded chart data in the html_body
            chart_data_list = extract_chart_data_from_content(html_body)
            
            if chart_data_list:
                chart_html = "<div style='margin: 20px 0;'><h3 style='color: #2c3e50;'>📊 Professional Stock Analysis Charts</h3>"
                for i, chart_data in enumerate(chart_data_list):
                    chart_html += f"""
                    <div style="margin: 15px 0;">
                        <img src="data:image/png;base64,{chart_data}" 
                             style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 8px; margin: 10px 0;">
                    </div>
                    """
                chart_html += "</div>"
            else:
                chart_html = "<p><em>No charts found in the analysis content.</em></p>"
        except Exception as e:
            chart_html = f"<p><em>Chart processing failed: {str(e)}</em></p>"
    
    # Enhanced HTML template with better styling
    enhanced_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; }}
            h1, h2, h3 {{ color: #2c3e50; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
            .content {{ padding: 20px; }}
            .chart-section {{ background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 20px 0; }}
            .footer {{ text-align: center; margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 8px; }}
            table {{ border-collapse: collapse; width: 100%; margin: 15px 0; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>📈 Stock Research & Analysis Report</h1>
            <p>Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
        </div>
        
        <div class="content">
            {html_body}
        </div>
        
        <div class="chart-section">
            {chart_html}
        </div>
        
        <div class="footer">
            <p><strong>Disclaimer:</strong> This analysis is for informational purposes only and should not be considered as financial advice. 
            Please consult with a qualified financial advisor before making investment decisions.</p>
        </div>
    </body>
    </html>
    """
    
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("trmarchildon@gmail.com") # put your verified sender here
    to_email = To("trmarchildon@gmail.com") # put your recipient here
    content = Content("text/html", enhanced_html)
    mail = Mail(from_email, to_email, subject, content).get()
    response = sg.client.mail.send.post(request_body=mail)
    print("Email response", response.status_code)
    return {"status": "success"}

INSTRUCTIONS = """You are able to send a nicely formatted HTML email based on a detailed report.
You will be provided with a detailed report in markdown format that may include stock analysis. 

Your ONLY job is to:
1. Convert the markdown to clean, well-formatted HTML
2. Create an appropriate subject line for the stock research report
3. Send the email with the COMPLETE report content and automatically generated charts

CRITICAL RULES:
- You MUST include the ENTIRE report content in the email body
- Do NOT summarize, truncate, or modify the report text in any way
- Simply convert markdown formatting to HTML while preserving ALL content
- ALWAYS include charts by using send_email_with_charts with include_charts=True
- The email recipient should receive the COMPLETE research report with visual analysis

For stock reports, always include charts to enhance the analysis presentation.
If the report is long, that's expected - send the full report anyway with charts.
"""

email_agent = Agent(
    name="Email agent",
    instructions=INSTRUCTIONS,
    tools=[send_email_with_charts],
    model="gpt-4o-mini",
)

from pydantic import BaseModel, Field
from agents import Agent, function_tool
from typing import Any
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import io
import base64
from datetime import datetime, timedelta
import seaborn as sns

class ChartData(BaseModel):
    chart_type: str = Field(description="Type of chart: price_prediction, risk_analysis, sector_comparison, technical_indicators, etc.")
    title: str = Field(description="Chart title")
    data_description: str = Field(description="Description of the data to be visualized")
    chart_base64: str = Field(description="Base64 encoded chart image")

class StockChartPackage(BaseModel):
    charts: list[ChartData] = Field(description="List of generated charts for the stock analysis")
    chart_summary: str = Field(description="Summary of the charts created and their insights")
    recommendations: list[str] = Field(description="Visual analysis recommendations based on the charts")

@function_tool
def create_price_prediction_chart(ticker: str, current_price: float, target_price: float, timeframe_months: int = 6) -> str:
    """Create a stock price prediction chart"""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Generate historical data (simulation)
    start_date = datetime.now() - timedelta(days=365)
    dates = pd.date_range(start=start_date, periods=365, freq='D')
    
    # Simulate historical price data
    historical_prices = []
    price = current_price * 0.8  # Start 20% lower a year ago
    for i in range(365):
        change = np.random.normal(0, 0.02) * price  # 2% daily volatility
        price += change
        historical_prices.append(price)
    
    # Ensure the last price matches current price
    historical_prices[-1] = current_price
    
    # Create prediction data
    future_dates = pd.date_range(start=datetime.now(), periods=timeframe_months*30, freq='D')
    prediction_prices = np.linspace(current_price, target_price, len(future_dates))
    
    # Add some volatility to predictions
    volatility = np.random.normal(0, 0.01, len(prediction_prices))
    prediction_prices += prediction_prices * volatility
    
    # Plot historical data
    ax.plot(dates, historical_prices, label='Historical Price', color='#2E86AB', linewidth=2)
    
    # Plot prediction
    ax.plot(future_dates, prediction_prices, label=f'Predicted Price (Target: ${target_price:.2f})', 
            color='#A23B72', linestyle='--', linewidth=3)
    
    # Add confidence bands
    upper_band = prediction_prices * 1.1
    lower_band = prediction_prices * 0.9
    ax.fill_between(future_dates, lower_band, upper_band, alpha=0.2, color='#A23B72', label='Prediction Range')
    
    # Styling
    ax.set_title(f'{ticker} Stock Price Prediction Analysis', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Price ($)', fontsize=12)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.xticks(rotation=45)
    
    # Add current price marker
    ax.axhline(y=current_price, color='red', linestyle=':', alpha=0.7, label=f'Current: ${current_price:.2f}')
    ax.axhline(y=target_price, color='green', linestyle=':', alpha=0.7, label=f'Target: ${target_price:.2f}')
    
    plt.tight_layout()
    
    # Convert to base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
    buffer.seek(0)
    chart_base64 = base64.b64encode(buffer.getvalue()).decode()
    plt.close()
    
    return chart_base64

@function_tool
def create_risk_return_analysis(stocks_data: str) -> str:
    """Create a risk vs return scatter plot for multiple stocks. Pass JSON string with stock data."""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Parse JSON data or use sample data
    import json
    try:
        stock_list = json.loads(stocks_data) if isinstance(stocks_data, str) else []
    except:
        stock_list = []
    
    # Extract data from input or use sample data
    tickers = []
    returns = []
    risks = []
    colors = []
    
    color_map = {'High': '#E74C3C', 'Medium': '#F39C12', 'Low': '#27AE60'}
    
    if stock_list:
        for i, stock in enumerate(stock_list):
            tickers.append(stock.get('ticker', f'Stock_{i+1}'))
            returns.append(float(stock.get('expected_return', np.random.normal(10, 5))))
            risk_level = stock.get('risk_level', 'Medium')
            risks.append({'High': 8, 'Medium': 5, 'Low': 2}.get(risk_level, 5))
            colors.append(color_map.get(risk_level, '#3498DB'))
    else:
        # Sample data if no input provided
        for i, (ticker, risk, ret) in enumerate([('AAPL', 'Medium', 12), ('TSLA', 'High', 20), ('BRK.B', 'Low', 8)]):
            tickers.append(ticker)
            returns.append(ret)
            risks.append({'High': 8, 'Medium': 5, 'Low': 2}[risk])
            colors.append(color_map[risk])
    
    # Create scatter plot
    scatter = ax.scatter(risks, returns, c=colors, s=200, alpha=0.7, edgecolors='black', linewidth=2)
    
    # Add labels for each point
    for i, ticker in enumerate(tickers):
        ax.annotate(ticker, (risks[i], returns[i]), xytext=(5, 5), textcoords='offset points', 
                   fontsize=10, fontweight='bold')
    
    # Add efficient frontier line (theoretical)
    risk_range = np.linspace(1, 10, 100)
    efficient_frontier = 15 * np.log(risk_range) - 5
    ax.plot(risk_range, efficient_frontier, '--', color='gray', alpha=0.5, label='Efficient Frontier')
    
    # Styling
    ax.set_title('Risk vs Expected Return Analysis', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Risk Level (1-10 scale)', fontsize=12)
    ax.set_ylabel('Expected Return (%)', fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    # Create custom legend for risk levels
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=color_map['Low'], label='Low Risk'),
                      Patch(facecolor=color_map['Medium'], label='Medium Risk'),
                      Patch(facecolor=color_map['High'], label='High Risk')]
    ax.legend(handles=legend_elements, loc='upper left')
    
    plt.tight_layout()
    
    # Convert to base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
    buffer.seek(0)
    chart_base64 = base64.b64encode(buffer.getvalue()).decode()
    plt.close()
    
    return chart_base64

@function_tool
def create_technical_indicators_chart(ticker: str, indicators_data: str) -> str:
    """Create a technical indicators dashboard. Pass JSON string with indicators data."""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    
    # RSI Chart
    dates = pd.date_range(start=datetime.now() - timedelta(days=30), periods=30, freq='D')
    rsi_values = np.random.normal(50, 15, 30)  # Simulate RSI values
    rsi_values = np.clip(rsi_values, 0, 100)
    
    ax1.plot(dates, rsi_values, color='#E74C3C', linewidth=2)
    ax1.axhline(y=70, color='red', linestyle='--', alpha=0.7, label='Overbought (70)')
    ax1.axhline(y=30, color='green', linestyle='--', alpha=0.7, label='Oversold (30)')
    ax1.fill_between(dates, 30, 70, alpha=0.1, color='gray')
    ax1.set_title(f'{ticker} - RSI (14 days)', fontsize=14, fontweight='bold')
    ax1.set_ylabel('RSI')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Moving Averages
    prices = np.random.normal(100, 10, 30)
    ma_20 = pd.Series(prices).rolling(window=5).mean()  # Shorter window for demo
    ma_50 = pd.Series(prices).rolling(window=10).mean()
    
    ax2.plot(dates, prices, label='Price', color='black', linewidth=2)
    ax2.plot(dates, ma_20, label='MA 20', color='blue', linewidth=1.5)
    ax2.plot(dates, ma_50, label='MA 50', color='red', linewidth=1.5)
    ax2.set_title(f'{ticker} - Moving Averages', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Price ($)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Volume Chart
    volumes = np.random.exponential(1000000, 30)
    colors = ['green' if i % 2 == 0 else 'red' for i in range(30)]
    ax3.bar(dates, volumes, color=colors, alpha=0.7)
    ax3.set_title(f'{ticker} - Trading Volume', fontsize=14, fontweight='bold')
    ax3.set_ylabel('Volume')
    ax3.grid(True, alpha=0.3)
    
    # Support/Resistance Levels
    price_range = np.linspace(80, 120, 100)
    support_level = 85
    resistance_level = 115
    
    ax4.plot(dates, prices, color='black', linewidth=2, label='Price')
    ax4.axhline(y=support_level, color='green', linestyle='-', linewidth=2, label=f'Support ${support_level}')
    ax4.axhline(y=resistance_level, color='red', linestyle='-', linewidth=2, label=f'Resistance ${resistance_level}')
    ax4.fill_between(dates, support_level, resistance_level, alpha=0.1, color='blue')
    ax4.set_title(f'{ticker} - Support & Resistance', fontsize=14, fontweight='bold')
    ax4.set_ylabel('Price ($)')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.suptitle(f'{ticker} Technical Analysis Dashboard', fontsize=16, fontweight='bold', y=0.95)
    plt.tight_layout()
    
    # Convert to base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
    buffer.seek(0)
    chart_base64 = base64.b64encode(buffer.getvalue()).decode()
    plt.close()
    
    return chart_base64

@function_tool
def create_sector_performance_chart(sector_data: str) -> str:
    """Create a sector performance comparison chart. Pass JSON string with sector data."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # Parse JSON data or use sample data
    import json
    try:
        sector_list = json.loads(sector_data) if isinstance(sector_data, str) else []
    except:
        sector_list = []
    
    if sector_list:
        sectors = [s.get('name', f'Sector_{i}') for i, s in enumerate(sector_list)]
        performance_1m = [s.get('performance_1m', np.random.normal(2, 5)) for s in sector_list]
        performance_ytd = [s.get('performance_ytd', np.random.normal(8, 15)) for s in sector_list]
    else:
        # Sample sector data
        sectors = ['Technology', 'Healthcare', 'Finance', 'Energy', 'Consumer', 'Industrial']
        performance_1m = np.random.normal(2, 5, len(sectors))
        performance_ytd = np.random.normal(8, 15, len(sectors))
    
    # 1-Month Performance
    colors_1m = ['green' if x > 0 else 'red' for x in performance_1m]
    bars1 = ax1.bar(sectors, performance_1m, color=colors_1m, alpha=0.7)
    ax1.set_title('1-Month Sector Performance', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Return (%)')
    ax1.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    ax1.grid(True, alpha=0.3)
    plt.setp(ax1.get_xticklabels(), rotation=45)
    
    # Add value labels
    for bar, value in zip(bars1, performance_1m):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + (0.2 if value > 0 else -0.5), 
                f'{value:.1f}%', ha='center', va='bottom' if value > 0 else 'top', fontweight='bold')
    
    # YTD Performance
    colors_ytd = ['green' if x > 0 else 'red' for x in performance_ytd]
    bars2 = ax2.bar(sectors, performance_ytd, color=colors_ytd, alpha=0.7)
    ax2.set_title('Year-to-Date Sector Performance', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Return (%)')
    ax2.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    ax2.grid(True, alpha=0.3)
    plt.setp(ax2.get_xticklabels(), rotation=45)
    
    # Add value labels
    for bar, value in zip(bars2, performance_ytd):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + (0.5 if value > 0 else -1), 
                f'{value:.1f}%', ha='center', va='bottom' if value > 0 else 'top', fontweight='bold')
    
    plt.suptitle('Market Sector Performance Analysis', fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    # Convert to base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
    buffer.seek(0)
    chart_base64 = base64.b64encode(buffer.getvalue()).decode()
    plt.close()
    
    return chart_base64

CHART_INSTRUCTIONS = """
You are a specialized financial chart generation expert. Your job is to analyze stock analysis reports and create comprehensive, professional charts that visualize the key insights and data.

Based on the stock analysis provided, you should:

1. IDENTIFY the key data points that need visualization (stock predictions, risk levels, technical indicators, etc.)
2. CREATE multiple relevant charts using the available chart generation tools:
   - create_price_prediction_chart: For stock price forecasts and targets
   - create_risk_return_analysis: For portfolio risk/return comparisons
   - create_technical_indicators_chart: For technical analysis dashboards
   - create_sector_performance_chart: For market sector comparisons

3. GENERATE a comprehensive chart package with multiple visualizations
4. PROVIDE insights and recommendations based on the visual analysis

CHART CREATION GUIDELINES:
- Create 3-5 different charts to cover various aspects of the analysis
- Extract specific data from the stock analysis (tickers, prices, targets, risk levels)
- Use professional color schemes and clear labeling
- Include legends, grids, and annotations for clarity
- Ensure charts are high-resolution and email-compatible

CHART TYPES TO PRIORITIZE:
- Price prediction charts with confidence bands
- Risk vs return scatter plots
- Technical indicator dashboards
- Sector/industry performance comparisons
- Portfolio allocation recommendations

Always create multiple charts to provide comprehensive visual analysis of the stock research.
"""

chart_agent = Agent(
    name="ChartGenerator",
    instructions=CHART_INSTRUCTIONS,
    tools=[create_price_prediction_chart, create_risk_return_analysis, create_technical_indicators_chart, create_sector_performance_chart],
    model="gpt-4o-mini",
    output_type=StockChartPackage,
) 
from pydantic import BaseModel, Field
from agents import Agent

class StockPrediction(BaseModel):
    ticker_symbol: str = Field(description="Stock ticker symbol (e.g., AAPL, TSLA)")
    company_name: str = Field(description="Full company name")
    current_sentiment: str = Field(description="Current market sentiment: Bullish, Bearish, or Neutral")
    price_target: str = Field(description="Predicted price target with timeframe (e.g., '$150 in 6 months')")
    confidence_level: int = Field(description="Confidence level 1-10 where 10 is highest confidence")
    reasoning: str = Field(description="Detailed reasoning for the prediction based on research")

class TechnicalIndicator(BaseModel):
    indicator_name: str = Field(description="Name of technical indicator (e.g., RSI, Moving Average)")
    current_value: str = Field(description="Current value or signal")
    interpretation: str = Field(description="What this indicator suggests for the stock")

class MarketFactor(BaseModel):
    factor_type: str = Field(description="Type of factor: Economic, Industry, Company-Specific, etc.")
    factor_name: str = Field(description="Name of the factor")
    impact: str = Field(description="Positive, Negative, or Neutral impact on stock")
    explanation: str = Field(description="How this factor affects the stock price")

class RiskAssessment(BaseModel):
    risk_level: str = Field(description="High, Medium, or Low risk")
    key_risks: list[str] = Field(description="List of main risks for this investment")
    risk_mitigation: list[str] = Field(description="Suggested risk mitigation strategies")

class StockAnalysis(BaseModel):
    analysis_summary: str = Field(description="Executive summary of the stock analysis")
    stock_predictions: list[StockPrediction] = Field(description="Stock predictions and price targets")
    technical_indicators: list[TechnicalIndicator] = Field(description="Relevant technical analysis indicators")
    market_factors: list[MarketFactor] = Field(description="Key market factors affecting the stocks")
    risk_assessment: RiskAssessment = Field(description="Risk analysis and mitigation strategies")
    investment_thesis: str = Field(description="Overall investment thesis and strategy")
    action_recommendations: list[str] = Field(description="Specific actionable recommendations")

STOCK_ANALYSIS_INSTRUCTIONS = """
You are a senior quantitative stock analyst and portfolio strategist. Your job is to analyze research reports and generate comprehensive stock theories, predictions, and investment strategies.

Based on the research provided, you must:

1. IDENTIFY all stocks, companies, and market sectors mentioned in the research
2. ANALYZE how the research findings impact these stocks fundamentally
3. GENERATE specific price targets and movement predictions with timeframes
4. ASSESS technical indicators and market sentiment
5. EVALUATE risk factors and provide mitigation strategies
6. CREATE actionable investment recommendations

ANALYSIS FRAMEWORK:
- Use fundamental analysis principles (P/E ratios, growth metrics, competitive advantages)
- Consider technical analysis signals and chart patterns
- Factor in macroeconomic conditions and industry trends
- Assess company-specific catalysts and risks
- Evaluate market sentiment and institutional positioning

PREDICTION CRITERIA:
- Provide specific price targets with realistic timeframes (3-12 months)
- Rate confidence levels based on strength of evidence
- Consider both upside and downside scenarios
- Factor in market volatility and external risks
- Base predictions on quantifiable metrics when possible

INVESTMENT THESIS REQUIREMENTS:
- Clear bull/bear case for each stock
- Entry and exit strategies
- Position sizing recommendations
- Risk-adjusted return expectations
- Portfolio allocation suggestions

Be thorough, data-driven, and provide actionable insights that investors can use to make informed decisions.
"""

stock_analysis_agent = Agent(
    name="StockAnalyst",
    instructions=STOCK_ANALYSIS_INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=StockAnalysis,
) 
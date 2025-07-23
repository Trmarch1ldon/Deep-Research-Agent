from agents import Agent, Runner, trace, gen_trace_id
from search_agent import search_agent
from planner_agent import planner_agent
from writer_agent import writer_agent
from email_agent import email_agent
from stock_analysis_agent import stock_analysis_agent
from chart_agent import chart_agent

# Research Manager Agent
RESEARCH_MANAGER_INSTRUCTIONS = """
You are a comprehensive research manager agent specialized in stock market analysis. Your job is to conduct deep research and generate stock investment theories by following this exact workflow:

1. First, use PlannerAgent to create a structured research plan for the given query, if not satisfied try again.
   - If the search has nothing to do with the stock market, call planner agent again and make it focus on the stock market.
2. Then, use SearchAgent multiple times to execute each search from your plan (call it once for each planned search)
3. After gathering all search results, use WriterAgent to synthesize findings into a comprehensive report
4. Next, use StockAnalyst to analyze the research report and generate stock theories, predictions, and investment strategies
5. Then, use ChartGenerator to create professional charts and visualizations based on the stock analysis
6. Finally, use EmailAgent to send the COMPLETE report, stock analysis, AND professional charts

CRITICAL REQUIREMENTS:
- When calling WriterAgent, provide ALL search results you gathered
- When calling StockAnalyst, provide the COMPLETE markdown_report from WriterAgent
- When calling ChartGenerator, provide the COMPLETE stock analysis from StockAnalyst
- When calling EmailAgent, provide the research report, stock analysis, AND chart package
- The email must contain the FULL research report, complete stock analysis, and professional charts
- DO NOT summarize, truncate, or modify any content when passing between agents

Workflow example:
1. Call PlannerAgent with the user query (ensure it focuses on stock market implications)
2. For each search in the plan, call SearchAgent
3. Call WriterAgent with original query + all search results
4. Call StockAnalyst with the complete research report to generate stock theories and predictions
5. Call ChartGenerator with the complete stock analysis to create professional visualizations
6. Call EmailAgent with the research report, stock analysis, and chart package

Always provide status updates to the user about what you're doing at each step.
"""

research_manager_agent = Agent(
    name="ResearchManager", 
    instructions=RESEARCH_MANAGER_INSTRUCTIONS,
    tools=[
        planner_agent.as_tool(tool_name="PlannerAgent", tool_description="Plan the research with stock market focus"),
        search_agent.as_tool(tool_name="SearchAgent", tool_description="Search the web for market data"), 
        writer_agent.as_tool(tool_name="WriterAgent", tool_description="Write the comprehensive research report"),
        stock_analysis_agent.as_tool(tool_name="StockAnalyst", tool_description="Analyze research and generate stock theories and predictions"),
        chart_agent.as_tool(tool_name="ChartGenerator", tool_description="Create professional charts and visualizations from stock analysis"),
        email_agent.as_tool(tool_name="EmailAgent", tool_description="Send the complete report with stock analysis and charts")
    ],
    model="gpt-4o-mini",
)

class ResearchManager:
    """Interface class for the research manager agent"""
    
    async def run(self, query: str):
        """Run the deep research process, yielding status updates and the final report"""
        trace_id = gen_trace_id()
        with trace("Research trace", trace_id=trace_id):
            print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}")
            yield f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}"
            yield "Starting research..."
            
            # Use the research manager agent to handle the entire research process
            result = await Runner.run(
                research_manager_agent,
                f"Please conduct comprehensive research on: {query}",
            )
            
            yield "Research complete!"
            yield str(result.final_output)
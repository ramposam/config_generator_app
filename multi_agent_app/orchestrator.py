import os
import logging
import time
from typing import TypedDict, Annotated, Sequence
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from agents import (
    create_tavily_agent,
    create_aviation_agent,
    create_weather_agent,
    create_ecommerce_agent,
    create_football_agent,
    create_ipl_agent
)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class AgentState(TypedDict):
    messages: Sequence[BaseMessage]
    next_agent: str


def create_multi_agent_graph(use_groq: bool = False):
    """Create a LangGraph multi-agent orchestration system"""
    logger.info(f"Creating multi-agent graph with use_groq={use_groq}")
    
    # Initialize LLM for routing
    if use_groq:
        router_llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0,
            max_retries=2,
            api_key=os.getenv("GROQ_API_KEY")
        )
        logger.info("Router LLM: Groq llama-3.3-70b-versatile")
    else:
        router_llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            max_retries=2,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        logger.info("Router LLM: OpenAI gpt-4o-mini")
    
    # Initialize individual agents
    logger.info("Initializing individual agents...")
    tavily_agent = create_tavily_agent(use_groq=use_groq)
    logger.info("Tavily agent created")
    
    aviation_agent = create_aviation_agent(use_groq=use_groq)
    logger.info("Aviation agent created")
    
    weather_agent = create_weather_agent(use_groq=use_groq)
    logger.info("Weather agent created")
    
    ecommerce_agent = create_ecommerce_agent(use_groq=use_groq)
    logger.info("E-commerce agent created")
    
    football_agent = create_football_agent(use_groq=use_groq)
    logger.info("Football agent created")
    
    ipl_agent = create_ipl_agent(use_groq=use_groq)
    logger.info("IPL agent created")
    
    # Define router function
    def route_agent(state: AgentState) -> str:
        """Route the query to the appropriate agent"""
        messages = state["messages"]
        last_message = messages[-1].content.lower()
        logger.info(f"Routing query: {messages[-1].content[:100]}...")
        
        # Simple keyword-based routing
        if any(keyword in last_message for keyword in ["flight", "airport", "airline", "departure", "arrival"]):
            logger.info("Routed to: Aviation Agent")
            return "aviation"
        elif any(keyword in last_message for keyword in ["weather", "forecast", "temperature", "rain", "wind"]):
            logger.info("Routed to: Weather Agent")
            return "weather"
        elif any(keyword in last_message for keyword in ["order", "product", "review", "customer", "revenue", "sales", "ecommerce"]):
            logger.info("Routed to: E-commerce Agent")
            return "ecommerce"
        elif any(keyword in last_message for keyword in ["ipl", "cricket", "batsman", "bowler", "wicket", "run", "stadium", "venue", "t20", "twenty20", "over", "innings", "six", "four", "century", "fifty", "duck", "maiden", "spinner", "pacer", "all-rounder", "wicketkeeper", "franchise", "auction", "tournament", "trophy", "orange cap", "purple cap", "boundary", "yorker", "bouncer", "googly", "doosra", "leg-spin", "off-spin", "fast bowling", "batting", "bowling", "fielding", "super over", "powerplay", "death overs", "batting order", "bowling spell", "run rate", "economy rate", "strike rate", "batting average", "bowling average"]):
            logger.info("Routed to: IPL Agent")
            return "ipl"
        elif any(keyword in last_message for keyword in ["player", "match", "team", "league", "football", "soccer", "goal"]):
            logger.info("Routed to: Football Agent")
            return "football"
        else:
            logger.info("Routed to: Tavily (Web Search) Agent")
            return "tavily"  # Default to web search
    
    # Define agent nodes
    def tavily_node(state: AgentState):
        """Execute Tavily web search agent"""
        logger.info("Executing Tavily agent...")
        logger.info(f"Input message: {state['messages'][-1].content[:200]}...")
        start_time = time.time()
        result = tavily_agent.invoke({"messages": [state["messages"][-1]]})
        end_time = time.time()
        duration = end_time - start_time
        logger.info(f"Tavily agent execution completed in {duration:.2f} seconds")
        logger.info(f"Output message count: {len(result['messages'])}")
        last_message = result["messages"][-1]
        logger.info(f"Output message (first 200 chars): {last_message.content[:200]}...")
        return {"messages": [last_message]}
    
    def aviation_node(state: AgentState):
        """Execute AviationStack agent"""
        logger.info("Executing Aviation agent...")
        logger.info(f"Input message: {state['messages'][-1].content[:200]}...")
        start_time = time.time()
        result = aviation_agent.invoke({"messages": [state["messages"][-1]]})
        end_time = time.time()
        duration = end_time - start_time
        logger.info(f"Aviation agent execution completed in {duration:.2f} seconds")
        logger.info(f"Output message count: {len(result['messages'])}")
        last_message = result["messages"][-1]
        logger.info(f"Output message (first 200 chars): {last_message.content[:200]}...")
        return {"messages": [last_message]}
    
    def weather_node(state: AgentState):
        """Execute OpenWeather agent"""
        logger.info("Executing Weather agent...")
        logger.info(f"Input message: {state['messages'][-1].content[:200]}...")
        start_time = time.time()
        result = weather_agent.invoke({"messages": [state["messages"][-1]]})
        end_time = time.time()
        duration = end_time - start_time
        logger.info(f"Weather agent execution completed in {duration:.2f} seconds")
        logger.info(f"Output message count: {len(result['messages'])}")
        last_message = result["messages"][-1]
        logger.info(f"Output message (first 200 chars): {last_message.content[:200]}...")
        return {"messages": [last_message]}
    
    def ecommerce_node(state: AgentState):
        """Execute E-commerce database agent"""
        logger.info("Executing E-commerce agent...")
        logger.info(f"Input message: {state['messages'][-1].content[:200]}...")
        start_time = time.time()
        result = ecommerce_agent.invoke({"messages": [state["messages"][-1]]})
        end_time = time.time()
        duration = end_time - start_time
        logger.info(f"E-commerce agent execution completed in {duration:.2f} seconds")
        logger.info(f"Output message count: {len(result['messages'])}")
        last_message = result["messages"][-1]
        logger.info(f"Output message (first 200 chars): {last_message.content[:200]}...")
        return {"messages": [last_message]}
    
    def football_node(state: AgentState):
        """Execute Football database agent"""
        logger.info("Executing Football agent...")
        logger.info(f"Input message: {state['messages'][-1].content[:200]}...")
        start_time = time.time()
        result = football_agent.invoke({"messages": [state["messages"][-1]]})
        end_time = time.time()
        duration = end_time - start_time
        logger.info(f"Football agent execution completed in {duration:.2f} seconds")
        logger.info(f"Output message count: {len(result['messages'])}")
        last_message = result["messages"][-1]
        logger.info(f"Output message (first 200 chars): {last_message.content[:200]}...")
        return {"messages": [last_message]}
    
    def ipl_node(state: AgentState):
        """Execute IPL Cricket database agent"""
        logger.info("Executing IPL agent...")
        logger.info(f"Input message: {state['messages'][-1].content[:200]}...")
        start_time = time.time()
        result = ipl_agent.invoke({"messages": [state["messages"][-1]]})
        end_time = time.time()
        duration = end_time - start_time
        logger.info(f"IPL agent execution completed in {duration:.2f} seconds")
        logger.info(f"Output message count: {len(result['messages'])}")
        last_message = result["messages"][-1]
        logger.info(f"Output message (first 200 chars): {last_message.content[:200]}...")
        return {"messages": [last_message]}
    
    # Build the graph
    logger.info("Building multi-agent graph...")
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("router", route_agent)
    workflow.add_node("tavily", tavily_node)
    workflow.add_node("aviation", aviation_node)
    workflow.add_node("weather", weather_node)
    workflow.add_node("ecommerce", ecommerce_node)
    workflow.add_node("football", football_node)
    workflow.add_node("ipl", ipl_node)
    logger.info("All nodes added to graph")
    
    # Set entry point
    workflow.set_entry_point("router")
    logger.info("Entry point set to router")
    
    # Add conditional edges from router
    workflow.add_conditional_edges(
        "router",
        lambda x: x,
        {
            "tavily": "tavily",
            "aviation": "aviation",
            "weather": "weather",
            "ecommerce": "ecommerce",
            "football": "football",
            "ipl": "ipl"
        }
    )
    logger.info("Conditional edges added from router")
    
    # All agent nodes lead to END
    workflow.add_edge("tavily", END)
    workflow.add_edge("aviation", END)
    workflow.add_edge("weather", END)
    workflow.add_edge("ecommerce", END)
    workflow.add_edge("football", END)
    workflow.add_edge("ipl", END)
    logger.info("All agent nodes connected to END")
    
    # Compile the graph
    app = workflow.compile()
    logger.info("Multi-agent graph compiled successfully")
    
    return app


def run_multi_agent_query(query: str, use_groq: bool = True) -> str:
    """Run a query through the multi-agent system"""
    logger.info(f"Starting multi-agent query processing: {query[:100]}...")
    start_time = time.time()
    
    app = create_multi_agent_graph(use_groq=use_groq)
    
    initial_state = {
        "messages": [HumanMessage(content=query)]
    }
    
    result = app.invoke(initial_state)
    
    end_time = time.time()
    duration = end_time - start_time
    logger.info(f"Multi-agent query completed in {duration:.2f} seconds")
    
    # Return the last AI message
    return result["messages"][-1].content


# Alternative: Simple agent selector (simpler than full LangGraph)
def select_and_run_agent(query: str, use_groq: bool = False) -> tuple:
    """Select appropriate agent using LLM-based routing and run it"""
    logger.info(f"Starting LLM-based agent selection for query: {query[:100]}...")
    
    # Initialize router LLM
    if use_groq:
        router_llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0,
            max_retries=2,
            api_key=os.getenv("GROQ_API_KEY")
        )
        logger.info("Router LLM: Groq llama-3.3-70b-versatile")
    else:
        router_llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            max_retries=2,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        logger.info("Router LLM: OpenAI gpt-4o-mini")
    
    # Define routing prompt
    routing_prompt = f"""You are an intelligent router that selects the most appropriate agent to handle a user query.

Available agents:
1. **aviation** - Flight status, airport information, airline data, departure/arrival times
2. **weather** - Current weather, forecasts, temperature, rain, wind conditions
3. **ecommerce** - Orders, products, reviews, customers, revenue, sales data
4. **football** - Football/soccer players, matches, teams, leagues, goals
5. **ipl** - IPL cricket matches, players, teams, statistics, runs, wickets
6. **tavily** - General web searches, news, research (default fallback)

User query: "{query}"

Respond with ONLY the agent name (aviation, weather, ecommerce, football, ipl, or tavily). No explanation."""
    
    # Get routing decision from LLM
    try:
        logger.info("Requesting routing decision from LLM...")
        routing_response = router_llm.invoke([HumanMessage(content=routing_prompt)])
        selected_agent = routing_response.content.strip().lower()
        logger.info(f"LLM routing decision: {selected_agent}")
        
        # Validate routing decision
        valid_agents = ["aviation", "weather", "ecommerce", "football", "ipl", "tavily"]
        if selected_agent not in valid_agents:
            logger.warning(f"Invalid agent '{selected_agent}' from LLM, defaulting to tavily")
            selected_agent = "tavily"
    except Exception as e:
        logger.error(f"Error during LLM routing: {str(e)}, defaulting to tavily")
        selected_agent = "tavily"
    
    # Route to appropriate agent
    if selected_agent == "aviation":
        logger.info("Selected: Aviation Agent")
        agent = create_aviation_agent(use_groq=use_groq)
        agent_name = "Aviation Agent"
    elif selected_agent == "weather":
        logger.info("Selected: Weather Agent")
        agent = create_weather_agent(use_groq=use_groq)
        agent_name = "Weather Agent"
    elif selected_agent == "ecommerce":
        logger.info("Selected: E-commerce Agent")
        agent = create_ecommerce_agent(use_groq=use_groq)
        agent_name = "E-commerce Agent"
    elif selected_agent == "ipl":
        logger.info("Selected: IPL Agent")
        agent = create_ipl_agent(use_groq=use_groq)
        agent_name = "IPL Agent"
    elif selected_agent == "football":
        logger.info("Selected: Football Agent")
        agent = create_football_agent(use_groq=use_groq)
        agent_name = "Football Agent"
    else:
        logger.info("Selected: Web Search Agent (Tavily)")
        agent = create_tavily_agent(use_groq=use_groq)
        agent_name = "Web Search Agent"
    
    # Execute agent
    logger.info(f"Executing {agent_name}...")
    logger.info(f"Input query for agent: {query[:200]}...")
    start_time = time.time()
    result = agent.invoke({"messages": [{"role": "user", "content": query}]})
    end_time = time.time()
    duration = end_time - start_time
    logger.info(f"{agent_name} execution completed in {duration:.2f} seconds")
    logger.info(f"Result message count: {len(result['messages'])}")
    
    # Get the last message from the result
    last_message = result["messages"][-1]
    logger.info(f"Final response (first 200 chars): {last_message.content[:200]}...")
    logger.info(f"Full response length: {len(last_message.content)} characters")
    return agent_name, last_message.content

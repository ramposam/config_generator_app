# Multi-Agent AI Assistant

A Streamlit-based multi-agent application built with LangChain, LangGraph, and specialized AI agents for different data sources and APIs. This application demonstrates the power of Generative AI in creating intelligent, domain-specific agents that can interact with databases, APIs, and web services.

## Features

- **Web Search Agent** (Tavily): General web searches, news, current events, and research
- **Aviation Agent** (AviationStack): Real-time flight status, airport information
- **Weather Agent** (OpenWeather): Current weather conditions and forecasts
- **E-commerce Agent** (ECOMMERCE_DB): Query e-commerce data (orders, products, reviews, customers)
- **Football Agent** (ETL_PIPELINES_DB): Query football/soccer data (players, matches, teams, leagues)
- **Intelligent Routing**: Automatic query routing to the most appropriate agent
- **Comprehensive Logging**: Detailed logging for all operations, timing, and debugging
- **Schema-Aware SQL**: Database agents include schema information and proper quoting rules

## Architecture

Built with:
- **Streamlit**: Web UI framework for interactive chat interface
- **LangChain**: LLM orchestration and tool integration
- **LangGraph**: Multi-agent workflow orchestration with create_react_agent
- **Groq or OpenAI**: LLM providers (configurable, defaults to OpenAI for better tool calling)
- **SQLAlchemy**: Database connection management
- **Python Logging**: Comprehensive logging system with timing information

## Prerequisites

- Python 3.9 or higher
- PostgreSQL databases (ETL_PIPELINES_DB and ECOMMERCE_DB)
- API keys for external services

## Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd c:\Users\Asus\PycharmProjects\config_generator_app
   ```

2. **Install dependencies**
   ```bash
   pip install -r multi_agent_requirements.txt
   ```

3. **Set up environment variables**

   Create a `.env` file in the project root or set the following environment variables:

   ```env
   # LLM Providers (at least one required)
   GROQ_API_KEY=your_groq_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here

   # External APIs
   TAVILY_API_KEY=your_tavily_api_key_here
   AVIATIONSTACK_API_KEY=your_aviationstack_api_key_here
   OPENWEATHER_API_KEY=your_openweather_api_key_here

   # Database Connections
   POSTGRES_DB_URL=postgresql://etl_pipeline:etl_pipeline@localhost:5432/ETL_PIPELINES_DB
   ECOMMERCE_DB_URL=postgresql://etl_pipeline:etl_pipeline@localhost:5432/ECOMMERCE_DB
   ```

4. **Verify database schemas**

   Ensure your PostgreSQL databases have the following tables:

   **ETL_PIPELINES_DB (public schema):**
   - PLAYER
   - MATCH
   - LEAGUE
   - TEAM
   - COUNTRY
   - TEAM_ATTRIBUTES
   - PLAYER_ATTRIBUTES

   **ECOMMERCE_DB (SILVER schema):**
   - T_STG_ORDERS
   - T_STG_REVIEWS
   - T_STG_EVENTS
   - T_STG_ORDER_ITEMS
   - T_STG_PRODUCTS
   - T_STG_USERS

## Usage

1. **Run the Streamlit application**
   ```bash
   streamlit run multi_agent_app/app.py
   ```

2. **Access the application**
   Open your browser and navigate to `http://localhost:8501`

3. **Select LLM Provider**
   - Choose between Groq (Llama3) or OpenAI (GPT-4o) in the sidebar

4. **Ask questions**
   - Type your query in the chat input
   - The system will automatically route to the appropriate agent
   - View the agent badge to see which agent handled your query

## Example Queries

### Web Search Agent
- "Search for latest AI trends"
- "What are the top news stories today?"
- "Find information about quantum computing"

### Aviation Agent
- "Check flight status for BA123"
- "Get airports in London"
- "Show me flights from New York to Paris"

### Weather Agent
- "What's the weather in London?"
- "Get 5-day forecast for Tokyo"
- "Current temperature in New York"

### E-commerce Agent
- "Show me total revenue"
- "How many products do we have?"
- "Get customer statistics"
- "What's the average order value?"
- "Show me review ratings"

### Football Agent
- "How many players in the database?"
- "Get match statistics"
- "Show me team information"
- "How many leagues are there?"

## Project Structure

```
multi_agent_app/
├── __init__.py
├── app.py                 # Streamlit application with chat interface
├── orchestrator.py        # Multi-agent orchestration logic and routing
├── db_utils.py            # Database connection utilities (SQLAlchemy)
├── agents/
│   ├── __init__.py
│   ├── tavily_agent.py    # Web search agent using Tavily API
│   ├── aviation_agent.py  # Flight status agent using AviationStack API
│   ├── weather_agent.py   # Weather forecast agent using OpenWeather API
│   ├── ecommerce_agent.py # E-commerce database agent with schema-aware SQL
│   └── football_agent.py # Football database agent with schema-aware SQL
└── README.md
```

## Key Components

### Agent Architecture
Each agent is built using LangGraph's `create_react_agent` which provides:
- Automatic tool calling and execution
- Built-in conversation memory
- Error handling and retry logic
- Structured tool outputs

### Database Agents (E-commerce & Football)
Database agents include:
- **Schema Information**: System prompts contain database name, schema name, and available tables
- **SQL Quoting Rules**: Instructions to wrap table names, schema names, and database names in double quotes
- **Example Queries**: Properly formatted SQL examples for the LLM to follow
- **Tool Functions**: 
  - `query_*_database`: Execute SQL queries
  - `get_*_schema_info`: Get table schemas
  - `get_*_insights`: Pre-built analytical queries

### Logging System
Comprehensive logging is implemented throughout the application:
- **Agent Creation**: Logs LLM selection, model choice, and initialization
- **Query Routing**: Logs which agent is selected for each query
- **Tool Execution**: Logs database queries, API calls with timing
- **Response Generation**: Logs execution time for each agent
- **User Interactions**: Logs button clicks, query submissions, and errors
- **Format**: `%(asctime)s - %(name)s - %(levelname)s - %(message)s`

### Intelligent Routing
The orchestrator uses keyword-based routing to select the appropriate agent:
- Aviation keywords: flight, airport, airline, departure, arrival
- Weather keywords: weather, forecast, temperature, rain, wind
- E-commerce keywords: order, product, review, customer, revenue, sales
- Football keywords: player, match, team, league, football, soccer, goal
- Default: Web search (Tavily)

## Configuration

### LLM Provider Selection

The application supports two LLM providers:

- **Groq (Llama-3.3-70b-versatile)**: Free tier available, fast inference
- **OpenAI (GPT-4o)**: Paid service, requires API key, better tool calling support

**Note**: The application defaults to OpenAI (GPT-4o) for better tool calling compatibility. Groq can be selected via the sidebar but may have limitations with certain tool formats.

Switch between providers using the sidebar in the Streamlit UI.

### Database Configuration

Update the database URLs in `.env` or directly in `db_utils.py`:

```python
FOOTBALL_DB_URL = "postgresql://user:password@host:port/database"
ECOMMERCE_DB_URL = "postgresql://user:password@host:port/database"
```

## Troubleshooting

### Database Connection Issues
- Verify PostgreSQL is running
- Check database credentials
- Ensure databases and schemas exist
- Test connection with `psql` or pgAdmin
- Check that tables exist in the correct schemas (public for Football, SILVER for E-commerce)

### API Key Errors
- Verify all API keys are set in environment variables
- Check API key validity and quotas
- Ensure keys have necessary permissions
- For Groq: Note that some models may be decommissioned; the app uses llama-3.3-70b-versatile

### Tool Calling Errors
- If you see tool validation errors, ensure you're using OpenAI (GPT-4o) as it has better tool calling support
- Groq may have limitations with certain tool formats
- Check the logs for detailed error messages

### Import Errors
- Ensure all dependencies are installed via `pip install -r multi_agent_requirements.txt`
- Check Python version compatibility (3.9+)
- Verify virtual environment is activated
- If you see langchain import errors, ensure langchain-classic is installed

### Logging
To view detailed logs:
- Logs are printed to the console with format: `%(asctime)s - %(name)s - %(levelname)s - %(message)s`
- Logs include timing information for all operations
- Check logs for debugging agent selection, tool execution, and errors

## API Key Setup

### Groq
1. Sign up at https://groq.com/
2. Get API key from dashboard
3. Set `GROQ_API_KEY` environment variable

### OpenAI
1. Sign up at https://openai.com/
2. Get API key from dashboard
3. Set `OPENAI_API_KEY` environment variable

### Tavily
1. Sign up at https://tavily.com/
2. Get API key from dashboard
3. Set `TAVILY_API_KEY` environment variable

### AviationStack
1. Sign up at https://aviationstack.com/
2. Get API key from dashboard
3. Set `AVIATIONSTACK_API_KEY` environment variable

### OpenWeather
1. Sign up at https://openweathermap.org/
2. Get API key from dashboard
3. Set `OPENWEATHER_API_KEY` environment variable

## License

This project is provided as-is for educational and development purposes.

## Support

For issues or questions, please check the troubleshooting section or verify your environment variables and database connections.

## Technical Details

### LangGraph Integration
The application uses LangGraph's `create_react_agent` for building agents:
- **ReAct Pattern**: Agents use Reasoning + Acting to solve queries
- **Tool Integration**: Tools are automatically bound to the LLM
- **State Management**: Conversation state is maintained across tool calls
- **Error Handling**: Built-in error handling for tool failures

### Custom Prompts
Database agents use custom system prompts with:
- Database and schema information
- Available tables with descriptions
- SQL formatting rules (double quotes for identifiers)
- Example queries to guide the LLM

### Dependencies
Key dependencies include:
- `langchain`: LLM orchestration framework
- `langchain-core`: Core LangChain components
- `langchain-community`: Community integrations
- `langchain-classic`: Classic LangChain agent implementations
- `langchain-groq`: Groq LLM provider
- `langchain-openai`: OpenAI LLM provider
- `langgraph`: Multi-agent orchestration
- `streamlit`: Web UI framework
- `sqlalchemy`: Database ORM
- `psycopg2-binary`: PostgreSQL adapter
- `python-dotenv`: Environment variable management
- `tavily-python`: Web search API client

### Performance Considerations
- **LLM Choice**: OpenAI (GPT-4o) provides better tool calling but costs money; Groq is free but may have limitations
- **Database Queries**: Use indexed columns for better performance
- **API Rate Limits**: Be aware of rate limits for external APIs (Tavily, AviationStack, OpenWeather)
- **Caching**: Consider implementing response caching for repeated queries

### Security Best Practices
- Never commit API keys to version control
- Use environment variables for sensitive configuration
- Rotate API keys regularly
- Implement rate limiting for production deployments
- Validate user inputs before database queries

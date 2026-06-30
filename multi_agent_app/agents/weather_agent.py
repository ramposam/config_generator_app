import os
import logging
from pathlib import Path
import requests
from langchain.tools import tool
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

# Configure logging
logger = logging.getLogger(__name__)

# Load schema documentation
def load_weather_schema() -> str:
    """Load Weather agent schema from markdown file"""
    schema_path = Path(__file__).parent / "weather_agent.md"
    if schema_path.exists():
        with open(schema_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "Schema documentation not found"


@tool
def get_current_weather(city: str) -> str:
    """Get current weather information using OpenWeather API.

    IMPORTANT: Review schema documentation for complete weather data reference.

    Use this when user asks about:
    - Current weather conditions
    - Temperature and "feels like" temperature
    - Wind speed and atmospheric pressure
    - Humidity levels
    - Real-time conditions (not forecast)

    Location Parameters:
    - city (required): City name
      Examples: "London", "New York", "Tokyo"
      Format: "City" or "City, Country Code" (e.g., "London, GB")

    Returned Data:
    - Condition: Weather description (Clear, Cloudy, Rainy, etc.)
    - Temperature: Current temperature in Celsius
    - Feels Like: Temperature adjusted for wind chill/humidity
    - Humidity: Relative humidity (0-100%)
    - Wind Speed: Speed in meters per second
    - Pressure: Atmospheric pressure in hPa

    Unit Reference:
    - Temperature: °C (convert: °F = °C × 9/5 + 32)
    - Wind: m/s (convert: 1 m/s ≈ 3.6 km/h ≈ 2.24 mph)
    - Pressure: hPa (normal: ~1010 hPa)

    Example Response:
    Current Weather for London:
    - Condition: Partly Cloudy
    - Temperature: 15.5°C
    - Feels Like: 14.2°C
    - Humidity: 65%
    - Wind Speed: 5.2 m/s
    - Pressure: 1013 hPa

    Args:
        city: The city name (e.g., 'London', 'New York')
        
    Returns:
        Current weather information as a formatted string
    """
    logger.info(f"Fetching current weather for: {city}")
    try:
        api_key = os.getenv("OPENWEATHER_API_KEY")
        url = f"http://api.openweathermap.org/data/2.5/weather"
        
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric"
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        weather = data.get("weather", [{}])[0]
        main = data.get("main", {})
        wind = data.get("wind", {})
        
        result = f"""
Current Weather for {data.get('name', city)}:
- Condition: {weather.get('description', 'N/A').title()}
- Temperature: {main.get('temp', 'N/A')}°C
- Feels Like: {main.get('feels_like', 'N/A')}°C
- Humidity: {main.get('humidity', 'N/A')}%
- Wind Speed: {wind.get('speed', 'N/A')} m/s
- Pressure: {main.get('pressure', 'N/A')} hPa
"""
        return result.strip()
    except Exception as e:
        logger.error(f"Error getting current weather: {str(e)}")
        return f"Error getting current weather: {str(e)}"


@tool
def get_weather_forecast(city: str, days: int = 5) -> str:
    """Get weather forecast using OpenWeather API.

    IMPORTANT: Review schema documentation for complete forecast data reference.

    Use this when user asks about:
    - Weather forecast for upcoming days
    - Daily temperature highs/lows
    - Rain or snow in the forecast
    - Planning for weather conditions
    - Multi-day predictions

    Location Parameters:
    - city (required): City name
      Examples: "London", "New York", "Tokyo"
      Format: "City" or "City, Country Code"
    - days (optional): Number of forecast days
      Default: 5
      Valid range: 1-5
      Max: 5 days

    Returned Data (per day):
    - Date: Forecast date (YYYY-MM-DD format)
    - Condition: Weather description
    - Temperature: Forecasted temperature at noon
    - Min Temperature: Forecasted low
    - Max Temperature: Forecasted high
    - Humidity: Relative humidity percentage

    Unit Reference:
    - Temperature: °C (convert: °F = °C × 9/5 + 32)
    - Humidity: percentage (0-100%)

    Common Conditions:
    - Clear: ☀️ Clear sky
    - Clouds: ☁️ Cloudy
    - Rain: 🌧️ Rainy
    - Drizzle: 🌦️ Light rain
    - Thunderstorm: ⛈️ Storm
    - Snow: ❄️ Snowy
    - Mist: 🌫️ Fog/Mist

    Example Response:
    Weather Forecast for London:

    Date: 2024-07-01
    - Condition: Partly Cloudy
    - Temperature: 18.5°C (min: 14.2°C, max: 20.1°C)
    - Humidity: 60%

    Args:
        city: The city name (e.g., 'London', 'New York')
        days: Number of days for forecast (default: 5, max: 5)
        
    Returns:
        Weather forecast information as a formatted string
    """
    logger.info(f"Fetching weather forecast for: {city} ({days} days)")
    try:
        api_key = os.getenv("OPENWEATHER_API_KEY")
        url = f"http://api.openweathermap.org/data/2.5/forecast"
        
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric",
            "cnt": days * 8  # 8 forecasts per day (3-hour intervals)
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        forecasts = data.get("list", [])
        results = [f"Weather Forecast for {data.get('city', {}).get('name', city)}:\n"]
        
        # Group by day
        daily_forecasts = {}
        for forecast in forecasts:
            date = forecast.get("dt_txt", "").split(" ")[0]
            if date not in daily_forecasts:
                daily_forecasts[date] = []
            daily_forecasts[date].append(forecast)
        
        # Get one forecast per day (around noon)
        for date, day_forecasts in list(daily_forecasts.items())[:days]:
            # Pick forecast closest to 12:00
            noon_forecast = min(day_forecasts, key=lambda x: abs(int(x.get("dt_txt", "").split(" ")[1][:2]) - 12))
            
            weather = noon_forecast.get("weather", [{}])[0]
            main = noon_forecast.get("main", {})
            
            results.append(f"Date: {date}")
            results.append(f"- Condition: {weather.get('description', 'N/A').title()}")
            results.append(f"- Temperature: {main.get('temp', 'N/A')}°C (min: {main.get('temp_min', 'N/A')}°C, max: {main.get('temp_max', 'N/A')}°C)")
            results.append(f"- Humidity: {main.get('humidity', 'N/A')}%")
            results.append("---")
        
        return "\n".join(results)
    except Exception as e:
        logger.error(f"Error getting weather forecast: {str(e)}")
        return f"Error getting weather forecast: {str(e)}"


def create_weather_agent(use_groq: bool = False):
    """Create an OpenWeather weather agent with schema context"""
    logger.info(f"Creating Weather agent with use_groq={use_groq}")
    
    # Load schema documentation for logging purposes
    schema_doc = load_weather_schema()
    logger.debug("Weather API schema documentation loaded")

    # Choose LLM
    if use_groq:
        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0,
            max_retries=2,
            api_key=os.getenv("GROQ_API_KEY")
        )
        logger.info("Weather agent using Groq llama-3.3-70b-versatile")
    else:
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            max_retries=2,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        logger.info("Weather agent using OpenAI gpt-4o-mini")
    
    # Tools with detailed API descriptions
    tools = [get_current_weather, get_weather_forecast]
    
    # Create agent using LangGraph
    agent = create_react_agent(llm, tools)
    logger.info("Weather agent created successfully with schema-aware tools")

    return agent

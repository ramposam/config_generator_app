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
def load_aviation_schema() -> str:
    """Load Aviation agent schema from markdown file"""
    schema_path = Path(__file__).parent / "aviation_agent.md"
    if schema_path.exists():
        with open(schema_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "Schema documentation not found"


@tool
def get_flight_status(flight_number: str) -> str:
    """Get real-time flight status using AviationStack API.

    IMPORTANT: Review schema documentation for complete flight data reference.

    Use this when user asks about:
    - Flight status (scheduled, departed, landed, delayed, cancelled)
    - Departure and arrival times
    - Airport information
    - Flight delays or cancellations
    - Real-time flight tracking

    Flight Number Format:
    - Format: [Airline IATA Code][Flight Number]
    - Examples: "BA123" (British Airways), "AA500" (American Airlines)
    - Must be uppercase IATA codes
    - Note: Flight codes are case-insensitive but API prefers uppercase

    Returned Data (per flight):
    - Flight: IATA flight code (e.g., BA123)
    - Airline: Full airline name
    - Departure: Airport name and IATA code
    - Departure Time: Scheduled departure datetime
    - Arrival: Airport name and IATA code
    - Arrival Time: Scheduled arrival datetime
    - Status: Flight status (Scheduled, Departed, Landed, Delayed, Cancelled)

    Flight Status Values:
    - Scheduled: Flight booked, awaiting departure
    - Departed: Aircraft has left origin
    - In-Air: Currently flying
    - Landed: Aircraft has touched down
    - Cancelled: Flight cancelled
    - Delayed: Departure delayed
    - Diverted: Redirected to alternative airport

    Common Airline Codes:
    - BA: British Airways
    - AA: American Airlines
    - AF: Air France
    - LH: Lufthansa
    - UA: United Airlines
    - DL: Delta Air Lines
    - EK: Emirates
    - NH: All Nippon Airways

    Example Response:
    Flight: BA123
    Airline: British Airways
    Departure: London Heathrow (LHR)
    Departure Time: 2024-07-01 14:30:00
    Arrival: Paris Charles de Gaulle (CDG)
    Arrival Time: 2024-07-01 16:15:00
    Status: Scheduled

    Args:
        flight_number: The flight number (e.g., 'AA123', 'BA456')
        
    Returns:
        Flight status information as a formatted string
    """
    logger.info(f"[TOOL CALL] get_flight_status called with flight_number: {flight_number}")
    try:
        api_key = os.getenv("AVIATIONSTACK_API_KEY")
        url = f"http://api.aviationstack.com/v1/flights"
        
        params = {
            "access_key": api_key,
            "flight_iata": flight_number.upper()
        }
        
        logger.info("[TOOL LOG] Calling AviationStack API...")
        response = requests.get(url, params=params)
        response.raise_for_status()
        logger.info(f"[TOOL SUCCESS] AviationStack API returned status {response.status_code}")
        data = response.json()
        logger.info(f"[TOOL LOG] API response data: {data}")
        if "data" not in data or not data["data"]:
            logger.warning(f"[TOOL WARNING] No flight information found for {flight_number}")
            return f"No flight information found for {flight_number}"
        
        flights = data["data"]
        logger.info(f"[TOOL SUCCESS] Found {len(flights)} flights")
        results = []
        
        for flight in flights[:3]:  # Limit to 3 results
            results.append(f"Flight: {flight.get('flight', {}).get('iata', 'N/A')}")
            results.append(f"Airline: {flight.get('airline', {}).get('name', 'N/A')}")
            results.append(f"Departure: {flight.get('departure', {}).get('airport', 'N/A')} ({flight.get('departure', {}).get('iata', 'N/A')})")
            results.append(f"Departure Time: {flight.get('departure', {}).get('scheduled', 'N/A')}")
            results.append(f"Arrival: {flight.get('arrival', {}).get('airport', 'N/A')} ({flight.get('arrival', {}).get('iata', 'N/A')})")
            results.append(f"Arrival Time: {flight.get('arrival', {}).get('scheduled', 'N/A')}")
            results.append(f"Status: {flight.get('flight_status', 'N/A')}")
            results.append("---")
        
        logger.info("[TOOL SUCCESS] Flight data formatted successfully")
        return "\n".join(results)
    except Exception as e:
        logger.error(f"[TOOL ERROR] Exception getting flight status: {str(e)}")
        return f"Error getting flight status: {str(e)}"


@tool
def get_airports_by_city(city: str) -> str:
    """Get airport information for a specific city using AviationStack API.
    
    IMPORTANT: Review schema documentation for complete airport data reference.

    Use this when user asks about:
    - Airports in a city or region
    - Airport codes (IATA and ICAO)
    - Which airports serve a location
    - Airport information

    Location Parameters:
    - city (required): City name
      Examples: "London", "New York", "Tokyo", "Paris"
      Format: City name (can be partial)

    Returned Data (per airport, max 5):
    - Airport: Full airport name
    - IATA Code: 3-letter IATA code (used for ticketing)
    - ICAO Code: 4-letter ICAO code (used for operations)
    - Country: Country name

    Code Reference:
    - IATA: 3-letter codes (e.g., LHR, JFK, CDG)
      Used by: Airlines, passengers, booking systems
    - ICAO: 4-letter codes (e.g., EGLL, KJFK, LFPG)
      Used by: Pilots, air traffic control, technical operations

    Common Airport Codes:
    London:
    - LHR / EGLL: Heathrow (major international)
    - LGW / EGKK: Gatwick
    - STN: Stansted
    - LTN: Luton

    New York:
    - JFK / KJFK: John F. Kennedy
    - LGA / KLGA: LaGuardia
    - EWR: Newark

    Paris:
    - CDG / LFPG: Charles de Gaulle (major international)
    - ORY / LFPO: Orly

    Tokyo:
    - NRT / RJAA: Narita
    - HND / RJTT: Haneda (major)

    Example Response:
    Airport: London Heathrow
    IATA Code: LHR
    ICAO Code: EGLL
    Country: United Kingdom
    ---
    Airport: London Gatwick
    IATA Code: LGW
    ICAO Code: EGKK
    Country: United Kingdom

    Args:
        city: The city name (e.g., 'London', 'New York')
        
    Returns:
        Airport information as a formatted string
    """
    logger.info(f"[TOOL CALL] get_airports_by_city called with city: {city}")
    try:
        api_key = os.getenv("AVIATIONSTACK_API_KEY")
        url = f"http://api.aviationstack.com/v1/airports"
        
        params = {
            "access_key": api_key,
            "city": city
        }
        
        logger.info("[TOOL LOG] Calling AviationStack Airports API...")
        response = requests.get(url, params=params)
        response.raise_for_status()
        logger.info(f"[TOOL SUCCESS] AviationStack API returned status {response.status_code}")
        data = response.json()
        
        if "data" not in data or not data["data"]:
            logger.warning(f"[TOOL WARNING] No airports found for {city}")
            return f"No airports found for {city}"
        
        airports = data["data"]
        logger.info(f"[TOOL SUCCESS] Found {len(airports)} airports")
        results = []
        
        for airport in airports[:5]:  # Limit to 5 results
            results.append(f"Airport: {airport.get('airport_name', 'N/A')}")
            results.append(f"IATA Code: {airport.get('iata_code', 'N/A')}")
            results.append(f"ICAO Code: {airport.get('icao_code', 'N/A')}")
            results.append(f"Country: {airport.get('country_name', 'N/A')}")
            results.append("---")
        
        logger.info("[TOOL SUCCESS] Airport data formatted successfully")
        return "\n".join(results)
    except Exception as e:
        logger.error(f"[TOOL ERROR] Exception getting airport information: {str(e)}")
        return f"Error getting airport information: {str(e)}"


def create_aviation_agent(use_groq: bool = False):
    """Create an AviationStack flight status agent with schema context"""
    logger.info(f"Creating Aviation agent with use_groq={use_groq}")
    
    # Load schema documentation for logging purposes
    schema_doc = load_aviation_schema()
    logger.debug("Aviation API schema documentation loaded")

    # Choose LLM
    if use_groq:
        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0,
            max_retries=2,
            api_key=os.getenv("GROQ_API_KEY")
        )
        logger.info("Aviation agent using Groq llama-3.3-70b-versatile")
    else:
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            max_retries=2,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        logger.info("Aviation agent using OpenAI gpt-4o-mini")
    
    # Tools with detailed API descriptions
    tools = [get_flight_status, get_airports_by_city]
    
    # Create agent using LangGraph
    agent = create_react_agent(llm, tools)
    logger.info("Aviation agent created successfully with schema-aware tools")

    return agent

# Weather Agent (OpenWeather API)

## API Connection Details
- **Service**: OpenWeather Map API
- **Endpoint**: https://api.openweathermap.org/data/2.5/
- **Authentication**: OPENWEATHER_API_KEY (environment variable)
- **Units**: Metric (Celsius, m/s, hPa)
- **Available Endpoints**: weather (current), forecast (5-day)

---

## Tools

### 1. get_current_weather

**Purpose**: Get real-time weather for a specific city

**Parameters**:
- `city` (required, string): City name
  - Example: "London", "New York", "Tokyo"
  - Format: City name or "City, Country Code" (e.g., "London, GB")

**Return Data**:
```
Current Weather for [City]:
- Condition: [Weather description]
- Temperature: [°C]
- Feels Like: [°C]
- Humidity: [%]
- Wind Speed: [m/s]
- Pressure: [hPa]
```

**Response Fields**:

| Field | Type | Unit | Range | Description |
|-------|------|------|-------|-------------|
| Condition | string | - | - | Weather description (Cloudy, Rainy, Sunny, etc.) |
| Temperature | number | °C | -50 to 50+ | Actual air temperature |
| Feels Like | number | °C | -50 to 50+ | Temperature adjusted for wind chill/humidity |
| Humidity | number | % | 0-100 | Relative humidity |
| Wind Speed | number | m/s | 0-40+ | Wind speed |
| Pressure | number | hPa | 900-1050 | Atmospheric pressure |

**Sample Response**:
```
Current Weather for London:
- Condition: Partly Cloudy
- Temperature: 15.5°C
- Feels Like: 14.2°C
- Humidity: 65%
- Wind Speed: 5.2 m/s
- Pressure: 1013 hPa
```

---

### 2. get_weather_forecast

**Purpose**: Get 5-day weather forecast for a specific city

**Parameters**:
- `city` (required, string): City name
  - Example: "London", "New York", "Tokyo"
  - Format: City name or "City, Country Code"
- `days` (optional, integer): Number of forecast days
  - Default: 5
  - Max: 5
  - Valid range: 1-5

**Return Data**:
```
Weather Forecast for [City]:

Date: YYYY-MM-DD
- Condition: [Weather description]
- Temperature: [°C] (min: [°C], max: [°C])
- Humidity: [%]
---
[Next day...]
```

**Forecast Details**:

| Field | Type | Unit | Description |
|-------|------|------|-------------|
| Date | date | YYYY-MM-DD | Date of forecast |
| Condition | string | - | Weather description |
| Temperature | number | °C | Forecasted temperature (noon) |
| Min Temperature | number | °C | Forecasted minimum temperature |
| Max Temperature | number | °C | Forecasted maximum temperature |
| Humidity | number | % | Forecasted relative humidity |

**Sample Response**:
```
Weather Forecast for London:

Date: 2024-07-01
- Condition: Partly Cloudy
- Temperature: 18.5°C (min: 14.2°C, max: 20.1°C)
- Humidity: 60%
---
Date: 2024-07-02
- Condition: Rainy
- Temperature: 16.3°C (min: 13.0°C, max: 18.5°C)
- Humidity: 80%
```

---

## Weather Conditions Reference

| Condition | Description | Icon |
|-----------|-------------|------|
| Clear | Clear sky | ☀️ |
| Clouds | Cloudy | ☁️ |
| Rain | Rainy | 🌧️ |
| Drizzle | Light rain | 🌦️ |
| Thunderstorm | Storm with lightning | ⛈️ |
| Snow | Snowy | ❄️ |
| Mist/Fog | Fog/Mist | 🌫️ |
| Haze | Atmospheric haze | 🌫️ |

---

## API Details

### Temperature Conversions
- Metric (used): Celsius (°C)
- For Fahrenheit: °F = (°C × 9/5) + 32
- For Kelvin: K = °C + 273.15

### Wind Speed
- Unit: meters per second (m/s)
- Conversion: 1 m/s ≈ 3.6 km/h ≈ 2.24 mph

### Pressure
- Unit: hectopascals (hPa)
- Normal range: ~1010 hPa (sea level)
- High pressure: > 1013 hPa
- Low pressure: < 1013 hPa (storm risk)

### Humidity
- Range: 0-100%
- Dry: < 40%
- Comfortable: 40-60%
- Humid: > 60%

---

## Common Use Cases

### Current Weather
```
User: "What's the weather in Paris?"
→ get_current_weather("Paris")
→ Returns: Current temperature, conditions, wind speed
```

### Trip Planning
```
User: "What's the weather forecast for Tokyo next week?"
→ get_weather_forecast("Tokyo", days=5)
→ Returns: 5-day forecast for trip planning
```

### Outfit Selection
```
User: "Should I bring an umbrella to London tomorrow?"
→ get_weather_forecast("London", days=1)
→ Returns: Forecast to check for rain
```

### Severe Weather Alert
```
User: "Is there a storm coming to Miami?"
→ get_weather_forecast("Miami", days=3)
→ Returns: Forecast showing thunderstorms or severe weather
```

---

## Location Handling

### City Name Formats
- **Simple**: "London" → Finds first match (usually largest city)
- **Specific**: "London, GB" → Specific country (ISO 3166 code)
- **State/Province**: "New York, US" → US state
- **Alternative**: "Paris, FR" → French cities

### Multiple Results
If city name is ambiguous:
- Agent returns largest city with that name
- Specify country code for exact match
- Example: "Springfield" → largest Springfield

---

## Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| City not found | Invalid city name | Check spelling, use country code |
| API Key Invalid | OPENWEATHER_API_KEY not set | Set environment variable |
| Network Error | Connection issue | Check internet connection |
| Rate Limited | Too many requests | Wait before retrying |

### Error Response
```
Error getting [current] weather: [error message]
```

---

## API Limitations

- **Rate Limiting**: Depends on API tier
- **Forecast Range**: 5 days maximum
- **Update Frequency**: Data updated every 10 minutes
- **Accuracy**: ±1-2°C typical
- **Coverage**: Global (180+ countries)

---

## Integration Notes

### With LLM Agent
The Weather agent automatically:
1. Validates city names
2. Formats API responses into readable format
3. Converts units appropriately
4. Handles errors gracefully
5. Provides complete weather context

### Query Processing
```
User: "What's the weather like tomorrow?"
  ↓
Agent: Infers city (if not specified, might ask)
  ↓
API Call: get_weather_forecast(city, days=1)
  ↓
Response: Formatted weather data
  ↓
LLM: Processes and provides natural response
```

---

## Performance Characteristics

| Metric | Value |
|--------|-------|
| Response Time | 0.5-2 seconds |
| Data Accuracy | ±1-2°C typical |
| Update Frequency | Every 10 minutes |
| Availability | 99%+ uptime |
| Global Coverage | 180+ countries |

---

## Best Practices

1. **City Specification**: Always include country for accuracy
   - ✅ "London, GB" instead of "London"
   - ✅ "Paris, FR" instead of "Paris"

2. **Forecast Planning**: Use 5-day forecast for planning
   - ✅ "What's the weather forecast for my trip?"
   - ❌ "Weather" (too vague)

3. **Condition Checking**: Look for rain/storm warnings
   - "Rainy" or "Drizzle" → Bring umbrella
   - "Thunderstorm" → Be cautious outdoors
   - "Snow" → Heavy clothing needed

4. **Temperature Context**: Consider feels-like temperature
   - Actual: 5°C, Feels Like: -5°C → Very cold
   - Wind chill matters for outdoor activities

5. **Humidity Awareness**: High humidity = discomfort
   - > 70% with high temp = very uncomfortable
   - < 30% = very dry conditions

---

## Sample Queries

### Basic Weather
```
"Current weather in London"
"What's the weather in New York?"
"Weather in Tokyo"
```

### Forecasts
```
"5-day forecast for Paris"
"Weather forecast for next week in Berlin"
"Will it rain this weekend in Seattle?"
```

### Travel Planning
```
"What's the weather in Barcelona next month?"
"Temperature in Sydney in August"
"Is it hot in Dubai right now?"
```

### Outdoor Activities
```
"Is it good weather for hiking in Denver?"
"Can I go swimming in Miami today?"
"Should I bring a jacket to Boston?"
```

---

## Troubleshooting

### City Not Found
- Check spelling
- Try adding country code (e.g., "London, GB")
- Try alternative city name
- Verify city exists in OpenWeather database

### Unexpected Weather
- Check coordinates (sometimes returns wrong location)
- Specify country code for uniqueness
- Remember: API provides current forecast, not always 100% accurate

### API Connection Issues
- Verify OPENWEATHER_API_KEY is set
- Check internet connection
- Verify API service is online
- Check for rate limiting

---

## API Documentation References

- **OpenWeather Docs**: https://openweathermap.org/api
- **Current Weather API**: https://openweathermap.org/current
- **5-Day Forecast**: https://openweathermap.org/forecast5
- **Weather Conditions**: https://openweathermap.org/weather-conditions
- **Units Documentation**: https://openweathermap.org/api/standards



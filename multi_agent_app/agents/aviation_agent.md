# Aviation Agent (AviationStack API)

## API Connection Details
- **Service**: AviationStack API
- **Endpoint**: http://api.aviationstack.com/v1/
- **Authentication**: AVIATIONSTACK_API_KEY (access_key parameter)
- **Endpoints**: flights, airports
- **Response Format**: JSON

---

## Tools

### 1. get_flight_status

**Purpose**: Get real-time flight status using AviationStack API

**Parameters**:
- `flight_number` (required, string): IATA flight number
  - Format: 2-letter airline code + flight number
  - Example: "BA123" (British Airways flight 123)
  - Example: "AA500" (American Airlines flight 500)
  - Format: Uppercase IATA code

**Return Data**:
```
Flight: [IATA code]
Airline: [Airline name]
Departure: [Airport name] ([IATA code])
Departure Time: [Scheduled departure time]
Arrival: [Airport name] ([IATA code])
Arrival Time: [Scheduled arrival time]
Status: [Flight status]
---
[Next flight result...]
```

**Response Fields**:

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| Flight | string | IATA flight code | BA123 |
| Airline | string | Full airline name | British Airways |
| Departure | string | Departure airport | London Heathrow |
| Departure IATA | string | Departure airport code | LHR |
| Departure Time | datetime | Scheduled departure | 2024-07-01 14:30:00 |
| Arrival | string | Arrival airport | Paris Charles de Gaulle |
| Arrival IATA | string | Arrival airport code | CDG |
| Arrival Time | datetime | Scheduled arrival | 2024-07-01 16:15:00 |
| Status | string | Flight status | Scheduled, Departed, Landed |

**Sample Response**:
```
Flight: BA123
Airline: British Airways
Departure: London Heathrow (LHR)
Departure Time: 2024-07-01 14:30:00
Arrival: Paris Charles de Gaulle (CDG)
Arrival Time: 2024-07-01 16:15:00
Status: Scheduled
---
```

**Flight Status Values**:

| Status | Meaning | Description |
|--------|---------|-------------|
| Scheduled | Flight booked | Aircraft assigned, awaiting departure |
| Departed | Flight left | Aircraft has left origin airport |
| In-Air | Currently flying | Aircraft is in flight |
| Landed | Flight arrived | Aircraft has touched down |
| Cancelled | Flight cancelled | Flight cancelled or not operating |
| Delayed | Flight delayed | Departure time delayed |
| Diverted | Flight diverted | Redirected to alternative airport |

---

### 2. get_airports_by_city

**Purpose**: Get airport information for a specific city

**Parameters**:
- `city` (required, string): City name
  - Example: "London", "New York", "Tokyo"
  - Format: City name (can be partial)

**Return Data**:
```
Airport: [Airport name]
IATA Code: [3-letter code]
ICAO Code: [4-letter code]
Country: [Country name]
---
[Next airport...]
```

**Response Fields**:

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| Airport | string | Full airport name | London Heathrow |
| IATA Code | string | 3-letter IATA code | LHR |
| ICAO Code | string | 4-letter ICAO code | EGLL |
| Country | string | Country name | United Kingdom |

**Sample Response**:
```
Airport: London Heathrow
IATA Code: LHR
ICAO Code: EGLL
Country: United Kingdom
---
Airport: London Gatwick
IATA Code: LGW
ICAO Code: EGKK
Country: United Kingdom
---
```

---

## Airport Code Reference

### IATA vs ICAO Codes

| Type | Format | Example | Use |
|------|--------|---------|-----|
| IATA | 3 letters | LHR, JFK, CDG | Airline ticketing, passenger use |
| ICAO | 4 letters | EGLL, KJFK, LFPG | Aviation operations, technical use |

### Common Airport Codes

| City | IATA | ICAO | Airline |
|------|------|------|---------|
| London | LHR | EGLL | Heathrow (major) |
| London | LGW | EGKK | Gatwick |
| New York | JFK | KJFK | Kennedy |
| New York | LGA | KLGA | LaGuardia |
| Paris | CDG | LFPG | Charles de Gaulle |
| Tokyo | NRT | RJAA | Narita |
| Tokyo | HND | RJTT | Haneda |
| Dubai | DXB | OMDB | Dubai Intl |

---

## Airline Code Reference

### Common Airline IATA Codes

| Code | Airline | Country |
|------|---------|---------|
| BA | British Airways | United Kingdom |
| AA | American Airlines | USA |
| AF | Air France | France |
| LH | Lufthansa | Germany |
| UA | United Airlines | USA |
| DL | Delta Air Lines | USA |
| EK | Emirates | UAE |
| NH | All Nippon Airways | Japan |
| CA | Air China | China |
| SQ | Singapore Airlines | Singapore |

---

## API Response Details

### Flight Number Format
```
[IATA Airline Code][Flight Number]

Examples:
- BA123: British Airways flight 123
- AA500: American Airlines flight 500
- AF1234: Air France flight 1234
- LH456: Lufthansa flight 456
```

### Time Format
- Format: ISO 8601 (YYYY-MM-DD HH:MM:SS)
- Timezone: UTC/GMT
- Example: 2024-07-01 14:30:00

### Result Limits
- Flight Status: Returns up to 3 results per query
- Airports: Returns up to 5 results per query
- Multiple flights: Same flight number may have multiple instances

---

## Common Use Cases

### Flight Check-in/Status
```
User: "What's the status of flight BA123?"
→ get_flight_status("BA123")
→ Returns: Current status, departure/arrival info
```

### Airport Information
```
User: "What airports are in London?"
→ get_airports_by_city("London")
→ Returns: LHR, LGW, STN, LTN, etc.
```

### Flight Delay Information
```
User: "Is flight AA500 delayed?"
→ get_flight_status("AA500")
→ Returns: Status showing delayed, cancelled, or on-time
```

### Travel Planning
```
User: "Which airports can I fly from in New York?"
→ get_airports_by_city("New York")
→ Returns: JFK, LGA, EWR airport options
```

---

## Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| No flight found | Wrong flight number | Check airline and flight number |
| Invalid format | Flight code format wrong | Use "AA123" format |
| No airports | City name not found | Try alternative name or spelling |
| API Key Invalid | AVIATIONSTACK_API_KEY not set | Set environment variable |
| Rate Limited | Too many requests | Wait before retrying |

### Error Response
```
No flight information found for [flight_number]
No airports found for [city]
Error getting flight status: [error message]
Error getting airport information: [error message]
```

---

## API Limitations

- **Flight Results**: Max 3 flights per query
- **Airport Results**: Max 5 airports per query
- **Rate Limiting**: Depends on API tier
- **Real-time Data**: Updated regularly (frequency varies)
- **Historical Data**: Limited for past flights
- **Coverage**: Most international airports and flights

---

## Data Accuracy

### Factors Affecting Accuracy
- Real-time status: Generally accurate within 5-15 minutes
- Small regional flights: May have limited data
- International flights: Subject to data sharing agreements
- Private flights: Not typically included
- Military flights: Not included

### Best Practices
1. **Verify Critical Info**: Confirm important details (gate, terminal) at airport
2. **Allow Delays**: Status may lag real-time by 5-15 minutes
3. **Regional Variations**: Some regions have better data coverage
4. **Check Official Source**: For official schedules, check airline website

---

## Integration Notes

### With LLM Agent
The Aviation agent automatically:
1. Parses IATA flight codes
2. Calls API with proper parameters
3. Formats responses into readable format
4. Handles multiple results
5. Manages error cases gracefully

### Query Processing
```
User: "Check flight BA123 status"
  ↓
Agent: Parses "BA123" as flight number
  ↓
API Call: get_flight_status("BA123")
  ↓
Response: Flight status, departure, arrival info
  ↓
LLM: Processes and provides natural response
```

---

## Performance Characteristics

| Metric | Value |
|--------|-------|
| Response Time | 1-3 seconds |
| Data Freshness | Updated every 5-15 minutes |
| Availability | 95%+ uptime |
| Coverage | 10,000+ airports globally |
| Accuracy | Generally high (±5-15 min lag) |

---

## Best Practices

1. **Flight Number Format**: Always use IATA codes
   - ✅ "BA123" (correct)
   - ❌ "British Airways 123" (incorrect)
   - ❌ "BA0123" (incorrect format)

2. **City Names**: Try common names first
   - ✅ "London" → Returns major London airports
   - ✅ "New York" → Returns NYC area airports
   - ✅ Use full name if needed

3. **Multiple Airports**: Cities may have several airports
   - Check all returned results
   - Use IATA code if you know it
   - UK example: LHR, LGW, STN, LTN, LCY

4. **Real-time vs Schedule**: API shows real-time status
   - May differ from airline website during disruptions
   - For official info, check airline directly
   - Use for quick status checks

5. **Time Zones**: Understand timezone display
   - Times shown in UTC/GMT
   - Convert to local timezone for clarity
   - Departure vs arrival in different zones

---

## Sample Queries

### Flight Status
```
"Check flight BA123"
"Status of flight AA500"
"Where is flight LH456?"
```

### Airport Information
```
"Airports in London"
"Where can I fly from in New York?"
"Airports serving Paris"
```

### Travel Planning
```
"What airlines fly from London?"
"Which airports in Tokyo?"
"Flight BA100 status?"
```

### Real-time Info
```
"Is flight delayed?"
"Has the flight landed?"
"What's the arrival time for flight?"
```

---

## Troubleshooting

### Flight Not Found
- Check airline IATA code is correct
- Verify flight number (numeric part)
- Try uppercase: "BA123" not "ba123"
- Flight may not exist for that date

### No Airports Found
- Check city spelling
- Try alternative name (e.g., "Tokyo" vs "Edo")
- Use English name for foreign cities
- Major city may have multiple airports

### Wrong Airport/Flight
- Specify full IATA code
- Use country code with city name
- Check multiple results returned
- Verify against official sources

### API Connection Issues
- Verify AVIATIONSTACK_API_KEY is set
- Check internet connection
- Verify API service is online
- Check for rate limiting

---

## API Documentation References

- **AviationStack API**: http://aviationstack.com/documentation
- **Flight Endpoint**: /flights endpoint
- **Airport Endpoint**: /airports endpoint
- **IATA Codes**: https://www.iata.org/
- **ICAO Codes**: https://www.icao.int/



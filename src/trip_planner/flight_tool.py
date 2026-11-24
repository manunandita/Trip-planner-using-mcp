import os
import httpx
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("AVIATIONSTACK_API_KEY")
# The free plan may only allow plain http. If your plan supports HTTPS, use https://
BASE_URL = "http://api.aviationstack.com/v1/flights"


def get_flights(dep_iata=None, arr_iata=None, flight_iata=None, status=None, limit=10):
    """Fetch real-time flights.

    dep_iata:    departure airport code, e.g. "DEL"
    arr_iata:    arrival airport code, e.g. "BOM"
    flight_iata: flight number, e.g. "AI101"
    status:      scheduled | active | landed | cancelled | incident | diverted
    limit:       max results (each call counts as one request on your quota)
    """
    if not API_KEY:
        raise RuntimeError("AVIATIONSTACK_API_KEY is missing in .env")

    params = {"access_key": API_KEY, "limit": limit}
    if dep_iata:
        params["dep_iata"] = dep_iata
    if arr_iata:
        params["arr_iata"] = arr_iata
    if flight_iata:
        params["flight_iata"] = flight_iata
    if status:
        params["flight_status"] = status

    response = httpx.get(BASE_URL, params=params, timeout=30)
    response.raise_for_status()
    payload = response.json()

    # The API returns errors inside the JSON body, not only as HTTP codes
    if "error" in payload:
        raise RuntimeError(f"Aviationstack error: {payload['error'].get('message')}")

    flights = []
    for f in payload.get("data", []):
        dep = f.get("departure") or {}
        arr = f.get("arrival") or {}
        flights.append({
            "flight": (f.get("flight") or {}).get("iata"),
            "airline": (f.get("airline") or {}).get("name"),
            "status": f.get("flight_status"),
            "date": f.get("flight_date"),
            "from": dep.get("iata"),
            "to": arr.get("iata"),
            "departure_scheduled": dep.get("scheduled"),
            "departure_estimated": dep.get("estimated"),
            "departure_delay_min": dep.get("delay"),
            "departure_terminal": dep.get("terminal"),
            "departure_gate": dep.get("gate"),
            "arrival_scheduled": arr.get("scheduled"),
            "arrival_estimated": arr.get("estimated"),
        })
    return flights


if __name__ == "__main__":
    for flight in get_flights(dep_iata="DEL", arr_iata="BOM", limit=5):
        print(flight)
"""
client.py
A command-line client to test the GeoCDN simulator.
Allows changing locations to see geographic routing and caching in action.
"""

import sys
import requests
import config

PREDEFINED_LOCATIONS = {
    "1": {"name": "Bangalore", "lat": 12.9716, "lon": 77.5946},
    "2": {"name": "Chennai", "lat": 13.0827, "lon": 80.2707},
    "3": {"name": "Mumbai", "lat": 19.0760, "lon": 72.8777},
    "4": {"name": "Delhi", "lat": 28.7041, "lon": 77.1025},
    "5": {"name": "Kolkata", "lat": 22.5726, "lon": 88.3639},
    "6": {"name": "Hyderabad", "lat": 17.3850, "lon": 78.4867},
}

def print_separator():
    print("=" * 50)

def main():
    while True:
        print_separator()
        print("GeoCDN Simulator - Client Menu")
        print_separator()
        for key, loc in PREDEFINED_LOCATIONS.items():
            print(f"{key}. {loc['name']} ({loc['lat']}, {loc['lon']})")
        print("7. Custom coordinates")
        print("8. Exit")
        print_separator()
        
        choice = input("Select your location (1-8): ").strip()
        
        if choice == "8":
            print("Exiting...")
            sys.exit(0)
            
        lat, lon = None, None
        
        if choice in PREDEFINED_LOCATIONS:
            loc = PREDEFINED_LOCATIONS[choice]
            lat, lon = loc["lat"], loc["lon"]
            print(f"Selected: {loc['name']}")
        elif choice == "7":
            try:
                lat = float(input("Enter latitude: "))
                lon = float(input("Enter longitude: "))
            except ValueError:
                print("Invalid coordinates. Please enter numbers.")
                continue
        else:
            print("Invalid choice.")
            continue
            
        content_id = input("Enter content ID (e.g., 101, 102, 103): ").strip()
        if not content_id:
            content_id = "101"
            
        print("\nSending request to Router...")
        
        try:
            url = f"{config.ROUTER_URL}/route?lat={lat}&lon={lon}&content_id={content_id}"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                print_separator()
                print("RESPONSE RECEIVED")
                print_separator()
                print("Client Location:")
                print(f"Latitude: {data['client_location']['lat']}")
                print(f"Longitude: {data['client_location']['lon']}\n")
                
                print("Distance:")
                print(f"Bangalore: {data['distances_km']['Bangalore']} km")
                print(f"North India: {data['distances_km']['North_India']} km\n")
                
                print("Selected CDN:")
                print(data['selected_cdn'], "\n")
                
                print("Cache Status:")
                print(f"[{data['cache_status']}]\n")
                
                print("Content:")
                print(data['content'].get('message', 'No message body'), "\n")
                
                print("Response Time:")
                print(f"{data['response_time_ms']} ms")
                print_separator()
            else:
                print(f"Error: HTTP {response.status_code}")
                print(response.text)
                
        except requests.exceptions.ConnectionError:
            print("Error: Could not connect to the Router. Is router.py running?")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
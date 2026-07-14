import json
import urllib.request
import csv
from urllib.parse import urlencode

# INDOT Interchanges query endpoint (Requesting WGS84 / Lat-Lon)
url = "https://gis.indot.in.gov/ro/rest/services/DOT/Interchanges/MapServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json"

try:
    print("Fetching interchange data from INDOT servers...")
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())
        
    features = data.get("features", [])
    
    if not features:
        print("No features returned. Check if the layer index (0) is correct for this MapServer.")
    else:
        output_file = "indot_interchanges_draft.csv"
        with open(output_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            
            # Expanded headers to include Highway_Name and Mile_Marker rows/columns
            writer.writerow(["Interchange_Name", "Highway_Name", "Mile_Marker", "Latitude", "Longitude", "Permalink"])
            
            for f in features:
                attributes = f.get("attributes", {})
                geometry = f.get("geometry", {})
                
                # Fetch raw string (e.g., "IC_I-70_123")
                name = attributes.get("IC_NAME") or "Unknown Location"
                
                # Initialize parsed output placeholders
                highway_name = "N/A"
                mile_marker = "N/A"
                
                # String Parsing logic for IC_<highway_name>_<mile_marker>
                if name.startswith("IC_"):
                    # Remove the prefix "IC_"
                    clean_name = name[3:]
                    
                    if clean_name.startswith("S"):
                        clean_name = "IN-" + clean_name[1:]
                    elif clean_name.startswith("U"):
                        clean_name = "US-" + clean_name[1:]
                    elif clean_name.startswith("I"):
                        clean_name = "I-" + clean_name[1:]
                    
                    # Rsplit handles the last underscore separation to safely split highway from mile marker
                    if "_" in clean_name:
                        highway_name, mile_marker = clean_name.rsplit("_", 1)
                
                # ArcGIS Point geometries return 'x' (Longitude) and 'y' (Latitude)
                lon = geometry.get("x")
                lat = geometry.get("y")
                
                if lat and lon:
                    params = urlencode({"env": "usa", "lat": lat, "lon": lon, "zoom": 5})
                    permalink = f"https://www.waze.com/editor?{params}"
                    
                    # Output all structural components to your row
                    writer.writerow([name, highway_name, mile_marker, lat, lon, permalink])
                    
        print(f"Success! Created '{output_file}' with {len(features)} parsed interchanges.")

except Exception as e:
    print(f"An error occurred: {e}")
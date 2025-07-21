import pandas as pd
import folium

# === Load ZIP -> lat/lng lookup ===
# Download this ZIP code dataset (one-time setup):
# https://public.opendatasoft.com/explore/dataset/us-zip-code-latitude-and-longitude/export/
# Save as 'zip_lat_lon.csv'
zip_db = pd.read_csv("zip_lat_lon.csv")

# Optional: make sure ZIPs are treated as strings with leading zeros
zip_db['Zip'] = zip_db['Zip'].astype(str).str.zfill(5)

# === Your input ZIP codes ===
# Replace this with reading from your Excel/Google Sheet
input_zip_codes = ['10001', '30301', '60601', '94105']

# Filter the ZIP database for your input ZIPs
zip_subset = zip_db[zip_db['Zip'].isin(input_zip_codes)].copy()

# Check for missing ZIPs
missing_zips = set(input_zip_codes) - set(zip_subset['Zip'])
if missing_zips:
    print("Missing ZIP codes in database:", missing_zips)

# === Create the Folium map ===
# Center the map on the average location
center_lat = zip_subset['Latitude'].mean()
center_lon = zip_subset['Longitude'].mean()
m = folium.Map(location=[center_lat, center_lon], zoom_start=4)

# Add a marker for each ZIP code
for _, row in zip_subset.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=f"ZIP: {row['Zip']}",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# === Save the map to HTML ===
m.save("zip_map.html")
print("Map saved to zip_map.html")

import pandas as pd
import folium

# === Load ZIP → lat/lon directory ===
zip_lookup = pd.read_csv("zip_lat_lon.csv")
zip_lookup["zip"] = zip_lookup["Zip"].astype(str).str.zfill(5)

# === Load input ZIP codes from form ===
df_zips = pd.read_csv("zip_codes.csv")
df_zips["zip"] = df_zips["zip"].astype(str).str.zfill(5)

# === Join and filter for valid lat/lon ===
merged = pd.merge(df_zips, zip_lookup, how="left", left_on="zip", right_on="zip")

missing = merged[merged["Latitude"].isna()]
if not missing.empty:
    print("ZIP(s) missing from directory:", missing["zip"].tolist())

valid = merged.dropna(subset=["Latitude", "Longitude"])

# === Create map ===
if valid.empty:
    print("No valid ZIP codes found.")
    exit()

center_lat = valid["Latitude"].mean()
center_lon = valid["Longitude"].mean()
m = folium.Map(location=[center_lat, center_lon], zoom_start=4)

# Add each ZIP as a marker
for _, row in valid.iterrows():
    folium.Marker(
        location=[row["Latitude"], row["Longitude"]],
        popup=f"ZIP: {row['zip']}",
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)

# === Save map ===
m.save("zip_map.html")
print("Map saved to zip_map.html")
import pandas as pd
import json
from pathlib import Path

csv_path = Path("zip_codes.csv")
incoming_dir = Path("incoming")
incoming_files = list(incoming_dir.glob("entry_*.json"))

if not incoming_files:
    print("No incoming files found.")
    exit(0)

# Load existing ZIPs
if csv_path.exists():
    df = pd.read_csv(csv_path)
else:
    df = pd.DataFrame(columns=["zip"])

# Process each entry file
for file in incoming_files:
    try:
        with open(file) as f:
            content = f.read().strip()
            if content.startswith("{"):
                entry = json.loads(content)
                zip_code = str(entry.get("zip", "")).zfill(5)
            else:
                zip_code = str(content).zfill(5)
        if zip_code:
            df.loc[len(df)] = {"zip": zip_code}
            print(f"Added ZIP: {zip_code}")
        else:
            print(f"No valid ZIP in {file.name}")
    except Exception as e:
        print(f”Error reading {file.name}: {e}")
    file.unlink()

# Remove duplicates and save
df.drop_duplicates().to_csv(csv_path, index=False)
print("zip_codes.csv updated.")

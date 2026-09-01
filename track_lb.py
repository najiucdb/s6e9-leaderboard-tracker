import os
import sys
import pandas as pd
from datetime import datetime
import zipfile

comp_name = "playground-series-s6e9"
zip_path = f"{comp_name}.zip"

print("Downloading leaderboard from Kaggle...")
os.system(f"kaggle competitions leaderboard {comp_name} -d")

# SAFETY CHECK: Did the file actually download?
if not os.path.exists(zip_path):
    print(f"ERROR: {zip_path} failed to download.")
    sys.exit(1)

print("Extracting and reading data...")
with zipfile.ZipFile(zip_path, 'r') as z:
    # 1. Look inside the zip file and get a list of all file names
    zip_contents = z.namelist()
    print(f"Files found inside the zip: {zip_contents}")
    
    # 2. Find the first file that ends with '.csv'
    csv_files = [f for f in zip_contents if f.endswith('.csv')]
    
    if not csv_files:
        print("ERROR: No CSV file found inside the zip!")
        sys.exit(1)
        
    actual_csv_name = csv_files[0]
    print(f"Dynamically selecting and opening: {actual_csv_name}")
    
    # 3. Open that specific file
    with z.open(actual_csv_name) as f:
        df = pd.read_csv(f)

# Add the timestamp
df['Scrape_Time_UTC'] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

# Save and append to history
if os.path.exists("lb_history.csv"):
    history_df = pd.read_csv("lb_history.csv")
    combined_df = pd.concat([history_df, df], ignore_index=True)
else:
    combined_df = df

combined_df.to_csv("lb_history.csv", index=False)
print(f"Success! {len(df)} teams currently on the leaderboard.")

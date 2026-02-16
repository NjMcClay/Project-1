import os
import csv
import json
from azure.storage.blob import BlobServiceClient

# ----------------------------
# CONFIGURATION
# ----------------------------

CONNECTION_STRING = (
    "DefaultEndpointsProtocol=http;"
    "AccountName=devstoreaccount1;"
    "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;"
    "BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
)

CONTAINER_NAME = "datasets"
BLOB_NAME = "All_Diets.csv"

LOCAL_CSV_PATH = "data/All_Diets.csv"
OUTPUT_JSON_PATH = "data/diet_averages.json"

# ----------------------------
# CONNECT TO AZURITE
# ----------------------------

print("Connecting to Azurite...")
blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)
blob_client = container_client.get_blob_client(BLOB_NAME)

# ----------------------------
# DOWNLOAD CSV FROM BLOB STORAGE
# ----------------------------

print("Downloading CSV from Azurite...")

os.makedirs("data", exist_ok=True)

with open(LOCAL_CSV_PATH, "wb") as file:
    download_stream = blob_client.download_blob()
    file.write(download_stream.readall())

print("Download complete.")

# ----------------------------
# PROCESS CSV DATA
# ----------------------------

averages = {}

print("Processing dataset...")

with open(LOCAL_CSV_PATH, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        diet_type = row["Diet_type"]

        # if diet_type not in averages:
        #     averages[diet_type] = {
        #         "Protein": 0,
        #         "Carbs": 0,
        #         "Fat": 0,
        #         "count": 0
        #     }

        averages[diet_type]["Protein"] += float(row["Protein(g)"])
        averages[diet_type]["Carbs"] += float(row["Carbs(g)"])
        averages[diet_type]["Fat"] += float(row["Fat(g)"])
        averages[diet_type]["count"] += 1

# ----------------------------
# CALCULATE AVERAGES
# ----------------------------

for diet in averages:
    count = averages[diet]["count"]
    averages[diet]["Protein"] /= count
    averages[diet]["Carbs"] /= count
    averages[diet]["Fat"] /= count
    del averages[diet]["count"]

# ----------------------------
# SAVE RESULTS (SIMULATED NOSQL)
# ----------------------------

with open(OUTPUT_JSON_PATH, "w") as json_file:
    json.dump(averages, json_file, indent=4)

print("Averages saved to diet_averages.json")
print(json.dumps(averages, indent=4))

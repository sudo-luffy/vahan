import csv
import requests
import json

# Define the API endpoint and headers
api_url = "https://kyc-api.surepass.io/api/v1/rc/rc"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY3NDgyMjQwMSwianRpIjoiZDgxOGU4YTgtZDBkZS00NGQ0LWI2NWEtMDI3N2QxOTYwYzlhIiwidHlwZSI6ImFjY2VzcyIsImlkZW50aXR5IjoiZGV2LnNob29yYUBzdXJlcGFzcy5pbyIsIm5iZiI6MTY3NDgyMjQwMSwiZXhwIjoxOTkwMTgyNDAxLCJ1c2VyX2NsYWltcyI6eyJzY29wZXMiOlsidXNlciJdfX0.kp1ZJg54uokB7-4JqXRSdQPp468NsKsWlB_f0ZeOeZc"
}

# Function to get vehicle details from the API
def fetch_vehicle_details(vehicle_id):
    response = requests.post(api_url, headers=headers, json={"id_number": vehicle_id})
    if response.status_code == 200 and response.json().get("success"):
        return response.json()["data"]
    else:
        print(f"Error fetching details for Vehicle ID {vehicle_id}: {response.text}")
        return None

# Function to read vehicle IDs from CSV file
def read_vehicle_ids(file_path):
    vehicle_ids = []
    with open(file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[0].strip():  # Check if the row is not empty and has a valid ID
                vehicle_ids.append(row[0].strip())
    return vehicle_ids

# Function to write vehicle details to CSV file
def write_vehicle_details_to_csv(file_path, vehicle_data):
    # Get the headers from the first vehicle's data
    headers = vehicle_data[0].keys() if vehicle_data else []

    with open(file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        for data in vehicle_data:
            # Fill empty fields with a placeholder (e.g., "N/A")
            data = {key: (value if value is not None else "N/A") for key, value in data.items()}
            writer.writerow(data)

# def main():
#     # Input CSV file path with vehicle IDs
#     input_file_path = "vehicle_ids.csv"
#     # Output CSV file path for vehicle details
#     output_file_path = "vehicle_details.csv"
    
#     # Read vehicle IDs from CSV
#     vehicle_ids = read_vehicle_ids(input_file_path)

#     # Fetch details for each vehicle
#     vehicle_data = []
#     for vehicle_id in vehicle_ids:
#         data = fetch_vehicle_details(vehicle_id)
#         if data:
#             vehicle_data.append(data)

#     # Write the vehicle details to output CSV
#     write_vehicle_details_to_csv(output_file_path, vehicle_data)
#     print(f"Vehicle details have been written to {output_file_path}")

# if __name__ == "__main__":
#     main()

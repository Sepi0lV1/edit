# edit/views.py
from django.shortcuts import render
import requests
import pandas as pd

# URL of the API endpoint for editing device data
url_edit_device = 'https://client.fleettrack.ma/api/edit_device'

# Replace 'your_user_api_hash' with your actual API hash
user_api_hash = '$2y$10$WWlBSFCif5bK2ibGfcUbWeEsABymX3b.lri/E57t/oIXfycaDhphy'

# Function to get device information based on the old name
def get_device_info(ancien_nom):
    try:
        url_get_devices = "https://client.fleettrack.ma/api/get_devices?user_api_hash=" + user_api_hash
        response = requests.get(url_get_devices)

        if response.status_code == 200:
            data = response.json()

            for item in data[0]['items']:
                if "name" in item and item["name"] == ancien_nom:
                    return item
        else:
            print("Failed to fetch device information. Status code:", response.status_code)
            return None

    except requests.exceptions.RequestException as e:
        print("Error while connecting to the API:", e)
        return None

# Function to upload vehicle data from an Excel file
def upload_vehicle_data(request):
    if request.method == 'POST':
        excel_file = request.FILES['file']

        # Read the Excel file using pandas
        df = pd.read_excel(excel_file)

        # Iterate through the rows of the DataFrame (Excel file)
        for index, row in df.iterrows():
            ancien_nom = row['Ancien_Nom']
            nouveau_nom = row['Nouveau_Nom']

            # Get device information based on the old name
            device_data = get_device_info(ancien_nom)
            if device_data:
                device_id = device_data["id"]
                imei = device_data["device_data"].get("imei")
                icon_id = device_data["device_data"].get("icon_id")
                fuel_measurement_id = device_data["device_data"].get("fuel_measurement_id")

                # Update the device data with the new name
                data = {
                    "name": nouveau_nom,
                    "imei": imei,
                    "icon_id": icon_id,
                    "fuel_measurement_id": fuel_measurement_id
                }

                try:
                    params = {
                        "lang": "fr",
                        "user_api_hash": user_api_hash,
                        "device_id": device_id
                    }

                    # Make the POST request to edit the device data
                    response = requests.post(url_edit_device, params=params, json=data)

                    if response.status_code == 200:
                        print(f"Modifications for '{nouveau_nom}' (device_id: {device_id}) saved successfully online.")
                    else:
                        print(f"Failed to send modifications for '{nouveau_nom}' (device_id: {device_id}). Status code:", response.status_code)
                except requests.exceptions.RequestException as e:
                    print(f"An error occurred while sending modifications for '{nouveau_nom}' (device_id: {device_id}): {e}")
            else:
                print(f"Unable to fetch device information for old name: {ancien_nom}")

        return render(request, 'result.html', {'result': 'Data uploaded and processed successfully.'})
    else:
        return render(request, 'upload_vehicle_data.html')

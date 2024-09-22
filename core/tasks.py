import csv
from celery import shared_task
from django.core.mail import EmailMessage
from django.conf import settings
import os
from fetch.utils import read_vehicle_ids, fetch_vehicle_details, write_vehicle_details_to_csv

@shared_task
def process_csv_task(filename, email):
    file_path = os.path.join(settings.MEDIA_ROOT, filename)
    processed_data = []
    vehicle_ids = read_vehicle_ids(file_path)
    vehicle_data = []
    for vehicle_id in vehicle_ids:
        data = fetch_vehicle_details(vehicle_id)
        if data:
            print(data)
            vehicle_data.append(data)

    # Write the vehicle details to output CSV
    new_file_path = os.path.join(settings.MEDIA_ROOT, f'processed_{filename}')
    write_vehicle_details_to_csv(new_file_path, vehicle_data)
        # Send the new file via email
    email_message = EmailMessage(
        subject='Processed CSV',
        body='Please find the processed CSV attached.',
        from_email="sudo.luffy@gmail.com",
        to=[email]
    )
    email_message.attach_file(new_file_path)
    email_message.send()

    # Cleanup: remove the original and processed files if needed
    os.remove(file_path)
    os.remove(new_file_path)

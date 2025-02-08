
import shutil
import os

def migrate_data(source, destination):
    try:
        if not os.path.exists(destination):
            os.makedirs(destination)
        for filename in os.listdir(source):
            full_file_name = os.path.join(source, filename)
            if os.path.isfile(full_file_name):
                shutil.copy(full_file_name, destination)
        print(f"Data migration from {source} to {destination} completed successfully.")
    except Exception as e:
        print(f"Error during data migration: {e}")

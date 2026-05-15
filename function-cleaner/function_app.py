import datetime
import logging
import os
import azure.functions as func
from azure.storage.blob import BlobServiceClient

app = func.FunctionApp()

@app.timer_trigger(schedule="0 */15 * * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False)
def blob_cleaner(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    connection_string = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
    container_name = os.environ.get("CONTAINER_NAME", "tempfiles")

    if not connection_string:
        logging.error("AZURE_STORAGE_CONNECTION_STRING not set")
        return

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)

    now = datetime.datetime.now(datetime.timezone.utc)
    deleted_count = 0

    logging.info(f"Starting cleanup scan at {now.isoformat()}")

    try:
        blobs = container_client.list_blobs(include=['metadata'])
        for blob in blobs:
            expiry_str = blob.metadata.get('expiry')
            if expiry_str:
                try:
                    expiry_time = datetime.datetime.fromisoformat(expiry_str)
                    if now > expiry_time:
                        logging.info(f"Deleting expired blob: {blob.name} (Expired at: {expiry_str})")
                        container_client.delete_blob(blob.name)
                        deleted_count += 1
                except ValueError:
                    logging.warning(f"Invalid expiry format for blob {blob.name}: {expiry_str}")
            else:
                # Optional: Handle blobs without expiry metadata (e.g., delete if older than 24h)
                pass

    except Exception as e:
        logging.error(f"Error during cleanup: {str(e)}")

    logging.info(f"Cleanup finished. Deleted {deleted_count} blobs.")

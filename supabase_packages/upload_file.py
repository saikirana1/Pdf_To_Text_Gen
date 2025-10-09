from io import BufferedReader
from tusclient import client
from supabase import create_client
from dotenv import load_dotenv
import os
import asyncio
from database_sql.insert_and_get_file_data import (
    insert_file_record,
)

load_dotenv()


BUCKET_NAME = os.getenv("Bucket_Name")
FOLDER_PATH = os.getenv("folder_path", "")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")


supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
STORAGE_URL = SUPABASE_URL.replace("supabase.co", "storage.supabase.co")


async def upload_file_to_supabase(file_name: str, file_stream):
    tus = client.TusClient(
        f"{STORAGE_URL}/storage/v1/upload/resumable",
        headers={"Authorization": f"Bearer {SUPABASE_KEY}", "x-upsert": "true"},
    )

    object_name = f"{FOLDER_PATH}/{file_name}" if FOLDER_PATH else file_name
    uploader = tus.uploader(
        file_stream=file_stream,
        chunk_size=6 * 1024 * 1024,
        metadata={
            "bucketName": BUCKET_NAME,
            "objectName": object_name,
            # "contentType": "application/pdf",
            "cacheControl": "3600",
        },
    )
    uploader.upload()

    public_url = (
        supabase.storage.from_(BUCKET_NAME).get_public_url(object_name).rstrip("?")
    )
    return public_url


async def uplod_file_details_sql(file):
    contents = await file.read()
    from io import BytesIO

    file_stream = BytesIO(contents)
    public_url = await upload_file_to_supabase(file.filename, file_stream)
    print(public_url)
    file_record = await insert_file_record(
        file_name=file.filename,
        file_url=public_url,
        file_index="",
    )
    print(file_record)

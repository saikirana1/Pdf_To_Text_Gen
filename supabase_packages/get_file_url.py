from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()


def get_file_url(file_name):
    bucket_name = os.getenv("Bucket_Name")
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

    supabase = create_client(supabase_url, supabase_key)
    public_url = supabase.storage.from_(bucket_name).get_public_url(file_name)
    return public_url.rstrip("?")

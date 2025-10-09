from dotenv import load_dotenv
import os

load_dotenv()


def get_db_table():
    index_name = os.getenv("index_name")
    index_namespace = os.getenv("namespace")
    return index_name, index_namespace

def dense_get_db_table():
    index_name = os.getenv("dense_db")
    index_namespace = os.getenv("dense_table")
    return index_name, index_namespace
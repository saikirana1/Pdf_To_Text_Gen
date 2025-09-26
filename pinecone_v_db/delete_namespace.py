from .get_db_table import get_db_table
from .pinecone_api_client import pinecone_client

def delete_namespace():

    index_name, index_namespace=get_db_table()
    client=pinecone_client()


    index = client.Index(host="knowledge-5r35xxm.svc.aped-4627-b74a.pinecone.io")

    result=index.delete_namespace(namespace=index_namespace)
    return result
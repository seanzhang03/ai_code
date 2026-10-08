import chromadb

client = chromadb.HttpClient(
    host="192.168.2.40",
    port = 9000
)
print(client)
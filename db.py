from pymongo import MongoClient
import certifi

MongoDB_URI  = 'mongodb+srv://admin:admin@cluster0.hqanw6f.mongodb.net/?retryWrites=true&w=majority'
cert = certifi.where()

def conectionDb():
  try:
    client = MongoClient.connect(mongodb_url, tlsCAFile=cert)
    db = client["db_products_application"]
  except ConnectionError:
    print("Error de conexion con la base de datos")
  return db
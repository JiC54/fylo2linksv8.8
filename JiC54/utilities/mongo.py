import asyncio
import sys
from motor import motor_asyncio
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from JiC54.vars import Var
from JiC54.utils.database import Database



from JiC54.confing import get_int_key, get_str_key


MONGO_PORT = get_int_key("27017")
MONGO_DB_URI = "mongodb+srv://jic54autofilter:jic54autofilter@cluster0.nbp6y.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
MONGO_DB = "JiC54"


client = MongoClient()
client = MongoClient(MONGO_DB_URI, MONGO_PORT)[MONGO_DB]
motor = motor_asyncio.AsyncIOMotorClient(MONGO_DB_URI, MONGO_PORT)
db = motor[MONGO_DB]
db = client["VainBot"]
try:
    asyncio.get_event_loop().run_until_complete(motor.server_info())
except ServerSelectionTimeoutError:
    sys.exit(log.critical("Can't connect to mongodb! Exiting..."))
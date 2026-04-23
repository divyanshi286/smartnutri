import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import asyncio

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "smartnutri")
USE_MONGOMOCK = os.getenv("USE_MONGOMOCK", "true").lower() == "true"

client: AsyncIOMotorClient = None
db = None

class AsyncMongoMockWrapper:
    """Wrapper to make mongomock operations awaitable"""
    def __init__(self, db_obj):
        self._db = db_obj
    
    def __getattr__(self, name):
        collection = getattr(self._db, name)
        return AsyncCollectionWrapper(collection)

class AsyncCollectionWrapper:
    """Wrapper to make mongomock collection operations awaitable"""
    def __init__(self, collection):
        self._collection = collection
    
    async def find_one(self, *args, **kwargs):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: self._collection.find_one(*args, **kwargs))
    
    async def insert_one(self, *args, **kwargs):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: self._collection.insert_one(*args, **kwargs))
    
    async def insert_many(self, *args, **kwargs):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: self._collection.insert_many(*args, **kwargs))
    
    async def update_one(self, *args, **kwargs):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: self._collection.update_one(*args, **kwargs))
    
    async def delete_one(self, *args, **kwargs):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: self._collection.delete_one(*args, **kwargs))
    
    def find(self, *args, **kwargs):
        # find returns a cursor, wrap it (but find itself is sync)
        cursor = self._collection.find(*args, **kwargs)
        return AsyncCursorWrapper(cursor)
    
    def create_index(self, *args, **kwargs):
        return self._collection.create_index(*args, **kwargs)

class AsyncCursorWrapper:
    """Wrapper to make mongomock cursor operations awaitable"""
    def __init__(self, cursor):
        self._cursor = cursor
    
    def sort(self, *args, **kwargs):
        self._cursor = self._cursor.sort(*args, **kwargs)
        return self
    
    def limit(self, *args, **kwargs):
        self._cursor = self._cursor.limit(*args, **kwargs)
        return self
    
    async def to_list(self, *args, **kwargs):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: list(self._cursor))

async def connect_db():
    """Connect to MongoDB"""
    global client, db
    try:
        if USE_MONGOMOCK:
            # Use in-memory mock MongoDB for development
            import mongomock
            client = mongomock.MongoClient()
            db = AsyncMongoMockWrapper(client[DB_NAME])
            print("[OK] Connected to MockMongo (in-memory)")
        else:
            # Use real MongoDB
            client = AsyncIOMotorClient(
                MONGO_URL,
                serverSelectionTimeoutMS=10000,
                connectTimeoutMS=10000,
            )
            db = client[DB_NAME]
            # Test the connection
            await db.command("ping")
            print("[OK] Connected to MongoDB Atlas")
        
        # Create indexes
        await create_indexes()
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        raise

async def close_db():
    """Close MongoDB connection"""
    global client
    if client:
        client.close()

async def create_indexes():
    """Create necessary MongoDB indexes"""
    if db:
        try:
            # Mongomock doesn't need async/await for indexes
            if USE_MONGOMOCK:
                db.users.create_index("email", unique=True, sparse=True)
                db.profiles.create_index("user_id")
                db.cycle_records.create_index("user_id")
                db.cycle_mood_logs.create_index("user_id")
                db.cycle_mood_logs.create_index([("user_id", 1), ("date", -1)])
                db.nutrition_targets.create_index("user_id", unique=True)
                db.meal_logs.create_index([("user_id", 1), ("date", -1)])
                db.meal_logs.create_index("date")
                db.progress_logs.create_index("user_id")
                db.progress_logs.create_index([("user_id", 1), ("date", -1)])
                db.food_database.create_index("name")
                db.chat_messages.create_index("user_id")
                db.chat_messages.create_index([("user_id", 1), ("created_at", -1)])
                db.achievements.create_index("user_id")
            else:
                # Real MongoDB
                await db.users.create_index("email", unique=True, sparse=True)
                await db.profiles.create_index("user_id")
                await db.cycle_records.create_index("user_id")
                await db.cycle_mood_logs.create_index("user_id")
                await db.cycle_mood_logs.create_index([("user_id", 1), ("date", -1)])
                await db.nutrition_targets.create_index("user_id", unique=True)
                await db.meal_logs.create_index([("user_id", 1), ("date", -1)])
                await db.meal_logs.create_index("date")
                await db.progress_logs.create_index("user_id")
                await db.progress_logs.create_index([("user_id", 1), ("date", -1)])
                await db.food_database.create_index("name")
                await db.achievements.create_index("user_id")
                await db.chat_messages.create_index("user_id")
                await db.chat_messages.create_index([("user_id", 1), ("created_at", -1)])
        except Exception as e:
            print(f"Note: Index creation not critical: {e}")

def get_db():
    """Get database instance for dependency injection"""
    return db

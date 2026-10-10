import sys
import os
import asyncio

# Automatically add project root (cognitivepulse_pro) to Python's path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.db.session import engine, Base
from backend.app.db import models 

async def init_tables():
    print("Connecting to database and creating tables...")
    async with engine.begin() as conn:
        # Create all tables defined in models.py
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created successfully!")

if __name__ == "__main__":
    asyncio.run(init_tables())
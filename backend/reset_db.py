#!/usr/bin/env python3
"""
Script to reset the database.
Usage: python reset_db.py
"""

import asyncio
from app.db.database import reset_db

if __name__ == "__main__":
    print("Resetting database...")
    asyncio.run(reset_db())
    print("Database reset complete!")


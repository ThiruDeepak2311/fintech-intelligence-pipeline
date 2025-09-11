import os
import psycopg2
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

class DailyMetrics(Base):
    __tablename__ = 'daily_metrics'
    
    id = Column(Integer, primary_key=True)
    date = Column(String, nullable=False)
    symbol = Column(String, nullable=False) 
    open_price = Column(Float)
    close_price = Column(Float)
    high_price = Column(Float)
    low_price = Column(Float)
    volume = Column(Integer)
    vwap = Column(Float)
    transactions = Column(Integer)
    raw_data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

class AIRecommendations(Base):
    __tablename__ = 'ai_recommendations'
    
    id = Column(Integer, primary_key=True)
    date = Column(String, nullable=False)
    metrics_id = Column(Integer, ForeignKey('daily_metrics.id'))
    sentiment = Column(String)  # bullish/bearish/neutral
    recommendations = Column(JSON)  # array of recommendations
    risk_score = Column(Integer)  # 1-10
    price_prediction = Column(Float)
    full_analysis = Column(Text)
    model_used = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class DatabaseManager:
    def __init__(self):
        self.database_url = os.getenv('DATABASE_URL')
        
        # Handle missing DATABASE_URL gracefully
        if not self.database_url:
            print("⚠️  No DATABASE_URL found - running in analysis-only mode")
            self.engine = None
            self.SessionLocal = None
            return
            
        try:
            self.engine = create_engine(self.database_url)
            self.SessionLocal = sessionmaker(bind=self.engine)
            print("✅ Database connection established")
        except Exception as e:
            print(f"⚠️  Database connection failed: {e}")
            self.engine = None
            self.SessionLocal = None
    
    def create_tables(self):
        """Create all tables"""
        if not self.engine:
            print("⚠️  Skipping table creation - no database connection")
            return False
            
        try:
            Base.metadata.create_all(bind=self.engine)
            print("✅ Database tables created successfully!")
            return True
        except Exception as e:
            print(f"❌ Failed to create tables: {e}")
            return False
    
    def get_session(self):
        """Get database session"""
        if not self.SessionLocal:
            return None
        return self.SessionLocal()
    
    def is_connected(self):
        """Check if database is connected"""
        return self.engine is not None

# Test function
def test_database():
    print("🔧 Testing database connection...")
    try:
        db = DatabaseManager()
        if db.is_connected():
            print("✅ Database manager created and connected!")
        else:
            print("⚠️  Database manager created but not connected")
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

if __name__ == "__main__":
    test_database()
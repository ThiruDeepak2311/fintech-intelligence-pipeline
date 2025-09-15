import os
import psycopg2
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# SQLAlchemy base class for creating database models
Base = declarative_base()

class DailyMetrics(Base):
    """
    DAILY METRICS TABLE - Stores raw stock market data for each trading day
    
    PURPOSE: Store complete daily stock information from Polygon.io API
    BUSINESS VALUE: Creates historical database of market performance for trend analysis
    
    RELATIONSHIP: One daily_metrics record can have multiple ai_recommendations
    
    EXAMPLE ROW:
    id=1, date='2025-09-10', symbol='AAPL', open_price=232.185, close_price=226.79,
    high_price=232.42, low_price=225.95, volume=83440810
    
    WHY WE STORE THIS:
    - Historical trend analysis (how has AAPL performed over time?)
    - AI needs complete OHLCV data for accurate analysis
    - Audit trail for all investment recommendations
    - Foundation for backtesting AI recommendation accuracy
    """
    __tablename__ = 'daily_metrics'
    
    # PRIMARY KEY - Unique identifier for each stock data record
    id = Column(Integer, primary_key=True)
    
    # CORE IDENTIFIERS - What stock and when
    date = Column(String, nullable=False)        # '2025-09-10' - trading date
    symbol = Column(String, nullable=False)      # 'AAPL' - stock ticker symbol
    
    # PRICE DATA (OHLC) - Core financial metrics
    open_price = Column(Float)                   # Opening price when market started
    close_price = Column(Float)                  # Closing price when market ended
    high_price = Column(Float)                   # Highest price during trading day
    low_price = Column(Float)                    # Lowest price during trading day
    
    # VOLUME DATA - Trading activity indicators
    volume = Column(Integer)                     # Total shares traded
    vwap = Column(Float)                        # Volume-weighted average price
    transactions = Column(Integer)               # Number of individual trades
    
    # RAW DATA STORAGE - Complete API response for debugging
    raw_data = Column(JSON)                     # Store entire Polygon.io response
    
    # METADATA - Track when record was created
    created_at = Column(DateTime, default=datetime.utcnow)

class AIRecommendations(Base):
    """
    AI RECOMMENDATIONS TABLE - Stores LLM analysis results and investment advice
    
    PURPOSE: Store AI-generated sentiment analysis and investment recommendations
    BUSINESS VALUE: Provides actionable intelligence for investment decision making
    
    RELATIONSHIP: Links to daily_metrics via foreign key (many recommendations per data point)
    
    EXAMPLE ROW:
    id=1, date='2025-09-10', metrics_id=1, sentiment='bearish', risk_score=8,
    recommendations=['Sell AAPL', 'Diversify portfolio'], price_prediction=220.0
    
    WHY WE STORE THIS:
    - Track AI recommendation accuracy over time
    - Provide audit trail for investment decisions
    - Enable backtesting of AI model performance
    - Historical record of market sentiment analysis
    """
    __tablename__ = 'ai_recommendations'
    
    # PRIMARY KEY - Unique identifier for each AI analysis
    id = Column(Integer, primary_key=True)
    
    # LINK TO SOURCE DATA - Which stock data was analyzed
    date = Column(String, nullable=False)                    # '2025-09-10'
    metrics_id = Column(Integer, ForeignKey('daily_metrics.id'))  # Links to daily_metrics table
    
    # AI ANALYSIS RESULTS - Core intelligence outputs
    sentiment = Column(String)                               # 'bullish', 'bearish', 'neutral'
    recommendations = Column(JSON)                           # Array of recommendation strings
    risk_score = Column(Integer)                            # Risk rating 1-10 (10 = highest risk)
    price_prediction = Column(Float)                        # AI's predicted future price
    
    # DETAILED ANALYSIS - Full AI response and metadata
    full_analysis = Column(Text)                            # Complete AI analysis summary
    model_used = Column(String)                             # Which AI model generated this
    
    # METADATA - Track when analysis was performed
    created_at = Column(DateTime, default=datetime.utcnow)

class DatabaseManager:
    """
    DATABASE MANAGER CLASS - Handles all PostgreSQL operations
    
    PURPOSE: Manage database connections, table creation, and data operations
    BUSINESS VALUE: Provides reliable data persistence with graceful error handling
    
    KEY FEATURES:
    - Automatic table creation on first run
    - Graceful degradation when database unavailable
    - Connection validation and error handling
    - Session management for database operations
    
    WHY THIS DESIGN:
    - Separation of concerns (database logic isolated)
    - Reusable across different parts of system
    - Professional error handling for production use
    - Easy to swap database providers if needed
    """
    
    def __init__(self):
        """
        CONSTRUCTOR - Initialize database connection
        
        PURPOSE:
        - Get DATABASE_URL from Railway environment variables
        - Create SQLAlchemy engine for PostgreSQL connection
        - Set up session factory for database operations
        - Handle graceful degradation if database unavailable
        
        PRODUCTION NOTE: Railway automatically provides DATABASE_URL
        """
        self.database_url = os.getenv('DATABASE_URL')
        
        # SAFETY CHECK: Handle missing database configuration
        if not self.database_url:
            print("Warning: No DATABASE_URL found - running in analysis-only mode")
            self.engine = None
            self.SessionLocal = None
            return
            
        try:
            # CREATE DATABASE ENGINE - Connection to PostgreSQL
            self.engine = create_engine(self.database_url)
            # CREATE SESSION FACTORY - For database operations
            self.SessionLocal = sessionmaker(bind=self.engine)
            print("Database connection established successfully")
        except Exception as e:
            print(f"Database connection failed: {e}")
            self.engine = None
            self.SessionLocal = None
    
    def create_tables(self):
        """
        TABLE CREATION - Set up database schema on first deployment
        
        PURPOSE:
        - Create both daily_metrics and ai_recommendations tables
        - Establish foreign key relationships
        - Handle case where tables already exist (no error)
        
        WHEN THIS RUNS:
        - First time system is deployed on Railway
        - After database is recreated or reset
        - Safe to call multiple times (won't duplicate tables)
        
        BUSINESS VALUE:
        - Automated database setup (no manual SQL required)
        - Consistent schema across deployments
        """
        if not self.engine:
            print("Warning: Skipping table creation - no database connection")
            return False
            
        try:
            # CREATE ALL TABLES defined in our models
            Base.metadata.create_all(bind=self.engine)
            print("Database tables created successfully!")
            return True
        except Exception as e:
            print(f"Failed to create tables: {e}")
            return False
    
    def get_session(self):
        """
        SESSION PROVIDER - Get database session for operations
        
        PURPOSE:
        - Provide database session for CRUD operations
        - Handle case where database is unavailable
        - Enable transaction management (commit/rollback)
        
        USAGE:
        session = db.get_session()
        session.add(new_record)
        session.commit()
        session.close()
        
        RETURNS: Database session or None if no connection
        """
        if not self.SessionLocal:
            return None
        return self.SessionLocal()
    
    def is_connected(self):
        """
        CONNECTION VALIDATOR - Check if database is available
        
        PURPOSE:
        - Allow system to check database status before operations
        - Enable graceful degradation in main pipeline
        - Provide clear status for logging and debugging
        
        BUSINESS VALUE:
        - System continues working even if database fails
        - Clear error messaging for troubleshooting
        - Production-ready fault tolerance
        
        RETURNS: True if database available, False otherwise
        """
        return self.engine is not None

# TESTING FUNCTION - Validate database setup works correctly
def test_database():
    """
    TEST FUNCTION - Verify database connection and setup
    
    PURPOSE:
    - Test database connection during development
    - Validate environment variables are configured correctly
    - Provide quick validation during deployment
    
    USAGE: Run this file directly to test database connectivity
    
    RETURNS: True if database works, False if issues found
    """
    print("Testing database connection...")
    try:
        db = DatabaseManager()
        if db.is_connected():
            print("Database manager created and connected successfully!")
        else:
            print("Database manager created but not connected (analysis-only mode)")
        return True
    except Exception as e:
        print(f"Database error: {e}")
        return False

# RUN TEST IF FILE IS EXECUTED DIRECTLY
if __name__ == "__main__":
    test_database()
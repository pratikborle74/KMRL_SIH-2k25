#!/usr/bin/env python3
"""
🚆 KMRL MongoDB Connection Test
================================
Test script to verify MongoDB connection and basic operations
for the KMRL fleet optimization system.
"""

import pymongo
from pymongo import MongoClient
from datetime import datetime
import sys

def test_mongodb_connection():
    """Test MongoDB connection and basic operations"""
    
    print("🚆 KMRL MongoDB Connection Test")
    print("=" * 40)
    
    try:
        # Connect to MongoDB
        print("📡 Connecting to MongoDB...")
        client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
        
        # Test the connection
        client.admin.command('ping')
        print("✅ Successfully connected to MongoDB!")
        
        # Get server info
        server_info = client.server_info()
        print(f"📊 MongoDB Version: {server_info['version']}")
        print(f"🖥️  Platform: {server_info.get('os', {}).get('name', 'Unknown')}")
        
        # Create/access KMRL database
        db = client['kmrl_fleet_optimization']
        print(f"🗄️  Accessing database: {db.name}")
        
        # Test collection operations
        test_collection = db['connection_test']
        
        # Insert a test document
        test_doc = {
            'test_type': 'connection_test',
            'timestamp': datetime.now(),
            'status': 'success',
            'message': 'KMRL MongoDB connection verified'
        }
        
        result = test_collection.insert_one(test_doc)
        print(f"✅ Test document inserted with ID: {result.inserted_id}")
        
        # Query the test document
        found_doc = test_collection.find_one({'_id': result.inserted_id})
        if found_doc:
            print("✅ Successfully queried test document")
            print(f"📄 Document: {found_doc['message']}")
        
        # Clean up test document
        test_collection.delete_one({'_id': result.inserted_id})
        print("🧹 Test document cleaned up")
        
        # List existing collections
        collections = db.list_collection_names()
        if collections:
            print(f"📚 Existing collections in {db.name}:")
            for col in collections:
                count = db[col].count_documents({})
                print(f"   - {col}: {count} documents")
        else:
            print(f"📚 No existing collections in {db.name}")
        
        # Close connection
        client.close()
        print("🔐 Connection closed successfully")
        
        print("\n🎉 MongoDB is ready for KMRL fleet optimization!")
        return True
        
    except pymongo.errors.ServerSelectionTimeoutError:
        print("❌ Error: Could not connect to MongoDB server")
        print("💡 Make sure MongoDB service is running")
        return False
        
    except ImportError:
        print("❌ Error: pymongo not installed")
        print("💡 Install with: pip install pymongo")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False

def show_mongodb_info():
    """Show helpful MongoDB information for KMRL project"""
    
    print("\n📚 KMRL MongoDB Setup Information")
    print("=" * 40)
    print("🔗 Connection String: mongodb://localhost:27017")
    print("🗄️  Database Name: kmrl_fleet_optimization")
    print("📊 Suggested Collections:")
    print("   - trains: Train fleet information")
    print("   - schedules: Route schedules")
    print("   - maintenance: Maintenance records")
    print("   - optimization_results: ML optimization results")
    print("   - fitness_certificates: Fitness tracking")
    print("   - performance_metrics: System performance data")

if __name__ == "__main__":
    success = test_mongodb_connection()
    show_mongodb_info()
    
    if not success:
        sys.exit(1)
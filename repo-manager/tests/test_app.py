#!/usr/bin/env python3
"""
Test script to verify Repo Manager functionality without GUI
"""

import sys
import os
import json

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_data_loading():
    """Test loading data from repo.json"""
    repo_file_path = "../data/REPOSITORY/repo.json"
    
    try:
        if os.path.exists(repo_file_path):
            with open(repo_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"✅ Successfully loaded {len(data)} ideas from {repo_file_path}")
            
            # Print first idea as example
            if data:
                first_idea = data[0]
                print(f"📋 Example idea: {first_idea.get('idea_id')} - {first_idea.get('title')}")
                print(f"   Maturity: {first_idea.get('maturity_score')}")
                print(f"   Interest: {first_idea.get('personal_interest_score')}")
                print(f"   Trend: {first_idea.get('trend_score')}")
                print(f"   Tags: {', '.join(first_idea.get('tags', []))}")
            
            return True
        else:
            print(f"⚠️  Repository file not found: {repo_file_path}")
            return False
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return False

def test_data_structure():
    """Test that data structure is valid"""
    repo_file_path = "../data/REPOSITORY/repo.json"
    
    try:
        if os.path.exists(repo_file_path):
            with open(repo_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            required_fields = ['idea_id', 'title', 'description', 'maturity_score', 
                              'personal_interest_score', 'trend_score', 'tags', 'related_items']
            
            for i, idea in enumerate(data):
                missing_fields = [field for field in required_fields if field not in idea]
                if missing_fields:
                    print(f"❌ Idea {i} missing fields: {missing_fields}")
                    return False
            
            print("✅ All ideas have required fields")
            return True
        else:
            print("⚠️  No repository file to test")
            return False
    except Exception as e:
        print(f"❌ Error testing data structure: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Repo Manager functionality...")
    print("=" * 50)
    
    # Test data loading
    print("\n1. Testing data loading...")
    load_success = test_data_loading()
    
    # Test data structure
    print("\n2. Testing data structure...")
    structure_success = test_data_structure()
    
    # Summary
    print("\n" + "=" * 50)
    if load_success and structure_success:
        print("🎉 All tests passed! The application should work correctly.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    print("\nTo run the GUI application:")
    print("1. Activate virtual environment: source venv/bin/activate")
    print("2. Run the app: python run.py")

if __name__ == "__main__":
    main() 
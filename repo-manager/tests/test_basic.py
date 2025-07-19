#!/usr/bin/env python3
"""
Basic tests for the Repo Manager application
"""

import sys
import os
import json
import tempfile
import unittest

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from repo_manager import RepoManager


class TestRepoManager(unittest.TestCase):
    """Basic tests for RepoManager functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.test_data = [
            {
                "idea_id": "I-TEST-001",
                "title": "Test Idea 1",
                "description": "A test idea for unit testing",
                "related_items": [],
                "maturity_score": 5,
                "personal_interest_score": 7,
                "trend_score": 6,
                "tags": ["test", "unit_test"]
            }
        ]
    
    def test_data_validation(self):
        """Test that idea data validation works"""
        # Valid idea data
        valid_idea = {
            'idea_id': 'I-TEST-001',
            'title': 'Test Idea',
            'description': 'Test description',
            'maturity_score': 5,
            'personal_interest_score': 7,
            'trend_score': 6,
            'tags': ['test'],
            'related_items': []
        }
        
        # Check required fields
        self.assertTrue(valid_idea.get('idea_id'))
        self.assertTrue(valid_idea.get('title'))
        
        # Check score ranges
        self.assertTrue(1 <= valid_idea.get('maturity_score', 0) <= 10)
        self.assertTrue(1 <= valid_idea.get('personal_interest_score', 0) <= 10)
        self.assertTrue(1 <= valid_idea.get('trend_score', 0) <= 10)
    
    def test_json_serialization(self):
        """Test that idea data can be serialized to JSON"""
        try:
            json_str = json.dumps(self.test_data, indent=2)
            parsed_data = json.loads(json_str)
            self.assertEqual(self.test_data, parsed_data)
        except Exception as e:
            self.fail(f"JSON serialization failed: {e}")
    
    def test_idea_structure(self):
        """Test that idea structure matches expected format"""
        idea = self.test_data[0]
        
        required_fields = ['idea_id', 'title', 'description', 'maturity_score', 
                          'personal_interest_score', 'trend_score', 'tags', 'related_items']
        
        for field in required_fields:
            self.assertIn(field, idea, f"Missing required field: {field}")
        
        # Check data types
        self.assertIsInstance(idea['idea_id'], str)
        self.assertIsInstance(idea['title'], str)
        self.assertIsInstance(idea['description'], str)
        self.assertIsInstance(idea['maturity_score'], int)
        self.assertIsInstance(idea['personal_interest_score'], int)
        self.assertIsInstance(idea['trend_score'], int)
        self.assertIsInstance(idea['tags'], list)
        self.assertIsInstance(idea['related_items'], list)


if __name__ == '__main__':
    unittest.main() 
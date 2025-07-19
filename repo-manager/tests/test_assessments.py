#!/usr/bin/env python3
"""
Test script to verify AI assessment functionality
"""

import sys
import os
import json

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_assessment_file_structure():
    """Test the assessment file structure and naming"""
    print("🧪 Testing Assessment File Structure...")
    print("=" * 60)
    
    evaluations_path = "../data/evaluations"
    
    # Check if evaluations directory exists
    if not os.path.exists(evaluations_path):
        print(f"❌ Evaluations directory not found: {evaluations_path}")
        return False
    
    print(f"✅ Evaluations directory found: {evaluations_path}")
    
    # List all assessment files
    assessment_files = []
    for file in os.listdir(evaluations_path):
        if file.endswith('.json'):
            assessment_files.append(file)
    
    print(f"📁 Found {len(assessment_files)} assessment files:")
    for file in assessment_files:
        print(f"   - {file}")
    
    return len(assessment_files) > 0

def test_trend_assessment_format():
    """Test trend assessment JSON format"""
    print("\n📈 Testing Trend Assessment Format...")
    
    trend_file = "../data/evaluations/I-FUNC-ARCH-VERBS_trend.json"
    
    try:
        with open(trend_file, 'r', encoding='utf-8') as f:
            trend_data = json.load(f)
        
        # Validate required fields
        required_fields = ['trend_score', 'justification', 'suggested_tags']
        missing_fields = [field for field in required_fields if field not in trend_data]
        
        if missing_fields:
            print(f"❌ Missing required fields: {missing_fields}")
            return False
        
        print(f"✅ Trend assessment loaded successfully")
        print(f"   - Trend Score: {trend_data['trend_score']}")
        print(f"   - Justification: {trend_data['justification'][:100]}...")
        print(f"   - Suggested Tags: {', '.join(trend_data['suggested_tags'])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading trend assessment: {e}")
        return False

def test_maturity_assessment_format():
    """Test maturity assessment JSON format"""
    print("\n🔬 Testing Maturity Assessment Format...")
    
    maturity_file = "../data/evaluations/I-FUNC-ARCH-VERBS_maturity.json"
    
    try:
        with open(maturity_file, 'r', encoding='utf-8') as f:
            maturity_data = json.load(f)
        
        # Validate required fields
        required_fields = ['maturity_score', 'justification', 'suggested_next_steps']
        missing_fields = [field for field in required_fields if field not in maturity_data]
        
        if missing_fields:
            print(f"❌ Missing required fields: {missing_fields}")
            return False
        
        print(f"✅ Maturity assessment loaded successfully")
        print(f"   - Maturity Score: {maturity_data['maturity_score']}")
        print(f"   - Justification: {maturity_data['justification'][:100]}...")
        print(f"   - Next Steps: {len(maturity_data['suggested_next_steps'])} items")
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading maturity assessment: {e}")
        return False

def test_assessment_file_naming():
    """Test assessment file naming convention"""
    print("\n📝 Testing Assessment File Naming Convention...")
    
    evaluations_path = "../data/evaluations"
    
    # Expected naming pattern: {idea_id}_{assessment_type}.json
    expected_files = [
        "I-FUNC-ARCH-VERBS_trend.json",
        "I-FUNC-ARCH-VERBS_maturity.json"
    ]
    
    for expected_file in expected_files:
        file_path = os.path.join(evaluations_path, expected_file)
        if os.path.exists(file_path):
            print(f"✅ Found expected file: {expected_file}")
            
            # Parse the filename
            parts = expected_file.replace('.json', '').split('_')
            if len(parts) >= 2:
                idea_id = '_'.join(parts[:-1])
                assessment_type = parts[-1]
                print(f"   - Idea ID: {idea_id}")
                print(f"   - Assessment Type: {assessment_type}")
        else:
            print(f"❌ Missing expected file: {expected_file}")
    
    return True

def test_assessment_integration():
    """Test how assessments integrate with idea data"""
    print("\n🔗 Testing Assessment Integration...")
    
    # Load repo data
    repo_file_path = "../data/REPOSITORY/repo.json"
    try:
        with open(repo_file_path, 'r', encoding='utf-8') as f:
            repo_data = json.load(f)
    except Exception as e:
        print(f"❌ Error loading repo data: {e}")
        return False
    
    # Find the test idea
    test_idea = None
    for idea in repo_data:
        if idea.get('idea_id') == 'I-FUNC-ARCH-VERBS':
            test_idea = idea
            break
    
    if not test_idea:
        print("❌ Test idea I-FUNC-ARCH-VERBS not found")
        return False
    
    print(f"✅ Found test idea: {test_idea.get('title')}")
    
    # Check if assessment files exist for this idea
    idea_id = test_idea.get('idea_id')
    evaluations_path = "../data/evaluations"
    
    trend_file = os.path.join(evaluations_path, f"{idea_id}_trend.json")
    maturity_file = os.path.join(evaluations_path, f"{idea_id}_maturity.json")
    
    if os.path.exists(trend_file):
        print(f"✅ Trend assessment exists for {idea_id}")
    else:
        print(f"⚠️  No trend assessment found for {idea_id}")
    
    if os.path.exists(maturity_file):
        print(f"✅ Maturity assessment exists for {idea_id}")
    else:
        print(f"⚠️  No maturity assessment found for {idea_id}")
    
    return True

def main():
    """Run all assessment tests"""
    print("🧪 Testing AI Assessment Functionality...")
    print("=" * 60)
    
    # Test 1: File structure
    print("\n1. Testing assessment file structure...")
    structure_success = test_assessment_file_structure()
    
    # Test 2: Trend assessment format
    print("\n2. Testing trend assessment format...")
    trend_success = test_trend_assessment_format()
    
    # Test 3: Maturity assessment format
    print("\n3. Testing maturity assessment format...")
    maturity_success = test_maturity_assessment_format()
    
    # Test 4: File naming convention
    print("\n4. Testing file naming convention...")
    naming_success = test_assessment_file_naming()
    
    # Test 5: Integration with ideas
    print("\n5. Testing assessment integration...")
    integration_success = test_assessment_integration()
    
    # Summary
    print("\n" + "=" * 60)
    if all([structure_success, trend_success, maturity_success, naming_success, integration_success]):
        print("🎉 All assessment tests passed!")
        print("✅ The AI assessment feature should work correctly in the GUI.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    print(f"\n📊 Summary:")
    print(f"   - File structure: {'✅' if structure_success else '❌'}")
    print(f"   - Trend format: {'✅' if trend_success else '❌'}")
    print(f"   - Maturity format: {'✅' if maturity_success else '❌'}")
    print(f"   - Naming convention: {'✅' if naming_success else '❌'}")
    print(f"   - Integration: {'✅' if integration_success else '❌'}")
    
    print(f"\n🎯 Next Steps:")
    print(f"   1. Run the GUI application: python run.py")
    print(f"   2. Select an idea with assessments")
    print(f"   3. Click 📊 to view assessments")
    print(f"   4. Click 📁 to upload new assessments")

if __name__ == "__main__":
    main() 
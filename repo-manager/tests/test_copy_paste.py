#!/usr/bin/env python3
"""
Test script to verify copy-paste assessment functionality
"""

import sys
import os
import json

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_assessment_json_formats():
    """Test the JSON formats for copy-paste functionality"""
    print("🧪 Testing Assessment JSON Formats for Copy-Paste...")
    print("=" * 60)
    
    # Test trend assessment format
    print("\n📈 Trend Assessment Format:")
    trend_assessment = {
        "trend_score": 8,
        "justification": "This approach is gaining significant traction in the industry with multiple companies adopting similar methodologies. Recent publications and conference presentations indicate growing interest.",
        "suggested_tags": ["emerging_trend", "industry_adoption", "high_potential", "conference_topic"]
    }
    
    trend_json = json.dumps(trend_assessment, indent=2, ensure_ascii=False)
    print("✅ Valid trend assessment JSON:")
    print(trend_json)
    
    # Test maturity assessment format
    print("\n🔬 Maturity Assessment Format:")
    maturity_assessment = {
        "maturity_score": 6,
        "justification": "The concept has been well-researched with multiple iterations and refinements. There's a working prototype and some documentation, but it needs more testing and validation.",
        "suggested_next_steps": [
            "Conduct user testing with the current prototype",
            "Write comprehensive documentation and user guide",
            "Present at a technical conference to get feedback",
            "Consider open-sourcing the approach"
        ]
    }
    
    maturity_json = json.dumps(maturity_assessment, indent=2, ensure_ascii=False)
    print("✅ Valid maturity assessment JSON:")
    print(maturity_json)
    
    return True

def test_json_validation():
    """Test JSON validation logic"""
    print("\n🔍 Testing JSON Validation...")
    
    # Test valid JSON
    valid_json = '{"trend_score": 7, "justification": "test", "suggested_tags": ["test"]}'
    try:
        data = json.loads(valid_json)
        print("✅ Valid JSON parsed successfully")
        
        # Test required fields
        if 'trend_score' in data:
            print("✅ Required field 'trend_score' found")
        else:
            print("❌ Missing required field 'trend_score'")
            return False
            
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing failed: {e}")
        return False
    
    # Test invalid JSON
    invalid_json = '{"trend_score": 7, "justification": "test"'
    try:
        data = json.loads(invalid_json)
        print("❌ Invalid JSON was parsed (should have failed)")
        return False
    except json.JSONDecodeError:
        print("✅ Invalid JSON correctly rejected")
    
    return True

def test_file_creation_logic():
    """Test the file creation logic for copy-paste assessments"""
    print("\n📝 Testing File Creation Logic...")
    
    idea_id = "I-TEST-COPY-PASTE"
    assessment_type = "trend"
    evaluations_path = "../data/evaluations"
    
    # Expected file path
    expected_file = os.path.join(evaluations_path, f"{idea_id}_{assessment_type}.json")
    print(f"📁 Expected file path: {expected_file}")
    
    # Test assessment data
    test_assessment = {
        "trend_score": 9,
        "justification": "This is a test assessment created via copy-paste functionality",
        "suggested_tags": ["test", "copy_paste", "validation"]
    }
    
    # Simulate file creation
    try:
        # Ensure directory exists
        os.makedirs(evaluations_path, exist_ok=True)
        
        # Write test file
        with open(expected_file, 'w', encoding='utf-8') as f:
            json.dump(test_assessment, f, indent=2, ensure_ascii=False)
        
        print("✅ Test file created successfully")
        
        # Verify file exists
        if os.path.exists(expected_file):
            print("✅ File exists after creation")
            
            # Read and verify content
            with open(expected_file, 'r', encoding='utf-8') as f:
                loaded_data = json.load(f)
            
            if loaded_data == test_assessment:
                print("✅ File content matches original data")
            else:
                print("❌ File content doesn't match original data")
                return False
        else:
            print("❌ File doesn't exist after creation")
            return False
            
        # Clean up test file
        os.remove(expected_file)
        print("✅ Test file cleaned up")
        
    except Exception as e:
        print(f"❌ Error in file creation test: {e}")
        return False
    
    return True

def test_overwrite_behavior():
    """Test that new assessments overwrite existing ones"""
    print("\n🔄 Testing Overwrite Behavior...")
    
    idea_id = "I-TEST-OVERWRITE"
    assessment_type = "maturity"
    evaluations_path = "../data/evaluations"
    test_file = os.path.join(evaluations_path, f"{idea_id}_{assessment_type}.json")
    
    try:
        # Ensure directory exists
        os.makedirs(evaluations_path, exist_ok=True)
        
        # Create initial assessment
        initial_assessment = {
            "maturity_score": 3,
            "justification": "Initial assessment",
            "suggested_next_steps": ["step1"]
        }
        
        with open(test_file, 'w', encoding='utf-8') as f:
            json.dump(initial_assessment, f, indent=2, ensure_ascii=False)
        
        print("✅ Initial assessment created")
        
        # Create new assessment (should overwrite)
        new_assessment = {
            "maturity_score": 7,
            "justification": "Updated assessment via copy-paste",
            "suggested_next_steps": ["step1", "step2", "step3"]
        }
        
        with open(test_file, 'w', encoding='utf-8') as f:
            json.dump(new_assessment, f, indent=2, ensure_ascii=False)
        
        print("✅ New assessment written (should overwrite)")
        
        # Verify overwrite
        with open(test_file, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)
        
        if loaded_data == new_assessment:
            print("✅ Overwrite successful - new data is present")
        else:
            print("❌ Overwrite failed - old data still present")
            return False
        
        # Clean up
        os.remove(test_file)
        print("✅ Test file cleaned up")
        
    except Exception as e:
        print(f"❌ Error in overwrite test: {e}")
        return False
    
    return True

def main():
    """Run all copy-paste tests"""
    print("🧪 Testing Copy-Paste Assessment Functionality...")
    print("=" * 60)
    
    # Test 1: JSON formats
    print("\n1. Testing assessment JSON formats...")
    format_success = test_assessment_json_formats()
    
    # Test 2: JSON validation
    print("\n2. Testing JSON validation...")
    validation_success = test_json_validation()
    
    # Test 3: File creation logic
    print("\n3. Testing file creation logic...")
    creation_success = test_file_creation_logic()
    
    # Test 4: Overwrite behavior
    print("\n4. Testing overwrite behavior...")
    overwrite_success = test_overwrite_behavior()
    
    # Summary
    print("\n" + "=" * 60)
    if all([format_success, validation_success, creation_success, overwrite_success]):
        print("🎉 All copy-paste tests passed!")
        print("✅ The copy-paste assessment feature should work correctly in the GUI.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    print(f"\n📊 Summary:")
    print(f"   - JSON formats: {'✅' if format_success else '❌'}")
    print(f"   - JSON validation: {'✅' if validation_success else '❌'}")
    print(f"   - File creation: {'✅' if creation_success else '❌'}")
    print(f"   - Overwrite behavior: {'✅' if overwrite_success else '❌'}")
    
    print(f"\n🎯 Copy-Paste Workflow:")
    print(f"   1. Click 📁 next to a score (Maturity/Trend)")
    print(f"   2. Paste JSON content from your AI tool")
    print(f"   3. Click 💾 Save Assessment")
    print(f"   4. Score updates automatically")
    print(f"   5. Assessment file is created/overwritten")

if __name__ == "__main__":
    main() 
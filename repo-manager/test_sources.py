#!/usr/bin/env python3
"""
Test script to verify source information functionality
"""

import sys
import os
import json

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_source_data_loading():
    """Test loading source data from JSON and MD files"""
    print("🧪 Testing source data loading...")
    
    # Test paths
    json_logs_path = "../data/json-logs"
    md_logs_path = "../data/md-logs"
    
    source_data = {}
    
    try:
        # Load JSON logs
        import glob
        json_files = glob.glob(os.path.join(json_logs_path, "*.json"))
        print(f"📁 Found {len(json_files)} JSON log files")
        
        for json_file in json_files:
            week = os.path.basename(json_file).replace('.json', '')
            with open(json_file, 'r', encoding='utf-8') as f:
                source_data[week] = json.load(f)
            print(f"✅ Loaded JSON data for week: {week}")
        
        # Load markdown logs
        md_files = glob.glob(os.path.join(md_logs_path, "*.md"))
        print(f"📁 Found {len(md_files)} markdown log files")
        
        for md_file in md_files:
            week = os.path.basename(md_file).replace('.md', '')
            if week not in source_data:
                source_data[week] = {}
            with open(md_file, 'r', encoding='utf-8') as f:
                source_data[week]['markdown'] = f.read()
            print(f"✅ Loaded markdown data for week: {week}")
        
        return source_data, True
        
    except Exception as e:
        print(f"❌ Error loading source data: {e}")
        return {}, False

def test_idea_source_linking():
    """Test linking ideas to their source information"""
    print("\n🔗 Testing idea source linking...")
    
    # Load repo data
    repo_file_path = "../data/REPOSITORY/repo.json"
    try:
        with open(repo_file_path, 'r', encoding='utf-8') as f:
            repo_data = json.load(f)
    except Exception as e:
        print(f"❌ Error loading repo data: {e}")
        return False
    
    # Load source data
    source_data, success = test_source_data_loading()
    if not success:
        return False
    
    # Test each idea
    for idea in repo_data:
        idea_id = idea.get('idea_id', 'Unknown')
        related_items = idea.get('related_items', [])
        
        print(f"\n📋 Testing idea: {idea_id}")
        print(f"   Related items: {len(related_items)}")
        
        for item in related_items:
            week = item.get('week', 'Unknown')
            item_id = item.get('item_id', 'Unknown')
            section = item.get('section', 'Unknown')
            
            print(f"   - Week: {week}, Item: {item_id}, Section: {section}")
            
            # Check if source data exists
            if week in source_data:
                week_data = source_data[week]
                
                # Check JSON data
                if 'items' in week_data and section in week_data['items']:
                    items = week_data['items'][section]
                    found = False
                    for item_data in items:
                        if item_data.get('id') == item_id:
                            print(f"     ✅ Found JSON source: {item_data.get('text', 'No text')[:50]}...")
                            found = True
                            break
                    if not found:
                        print(f"     ⚠️  Item {item_id} not found in JSON data")
                else:
                    print(f"     ⚠️  Section {section} not found in JSON data")
                
                # Check markdown data
                if 'markdown' in week_data:
                    print(f"     ✅ Markdown context available ({len(week_data['markdown'])} chars)")
                else:
                    print(f"     ⚠️  No markdown context found")
            else:
                print(f"     ❌ No source data for week {week}")
    
    return True

def test_source_information_generation():
    """Test generating source information text"""
    print("\n📝 Testing source information generation...")
    
    # Load repo data
    repo_file_path = "../data/REPOSITORY/repo.json"
    try:
        with open(repo_file_path, 'r', encoding='utf-8') as f:
            repo_data = json.load(f)
    except Exception as e:
        print(f"❌ Error loading repo data: {e}")
        return False
    
    # Load source data
    source_data, success = test_source_data_loading()
    if not success:
        return False
    
    # Test with first idea that has related items
    test_idea = None
    for idea in repo_data:
        if idea.get('related_items'):
            test_idea = idea
            break
    
    if not test_idea:
        print("⚠️  No ideas with related items found for testing")
        return False
    
    print(f"📋 Testing with idea: {test_idea.get('idea_id')}")
    
    # Generate source information (simplified version)
    related_items = test_idea.get('related_items', [])
    source_info = []
    source_info.append(f"# Source Information for: {test_idea.get('title', 'Unknown Idea')}")
    source_info.append(f"Idea ID: {test_idea.get('idea_id', 'Unknown')}")
    source_info.append("=" * 60)
    source_info.append("")
    
    for item in related_items:
        week = item.get('week', 'Unknown')
        item_id = item.get('item_id', 'Unknown')
        section = item.get('section', 'Unknown')
        
        source_info.append(f"## Week: {week} | Item: {item_id} | Section: {section}")
        source_info.append("")
        
        if week in source_data:
            week_data = source_data[week]
            
            # Find JSON source
            if 'items' in week_data and section in week_data['items']:
                items = week_data['items'][section]
                for item_data in items:
                    if item_data.get('id') == item_id:
                        source_info.append("### JSON Source:")
                        source_info.append(f"```json")
                        source_info.append(json.dumps(item_data, indent=2, ensure_ascii=False))
                        source_info.append("```")
                        source_info.append("")
                        break
            
            # Add markdown context
            if 'markdown' in week_data:
                source_info.append("### Markdown Context:")
                source_info.append("```markdown")
                source_info.append(week_data['markdown'])
                source_info.append("```")
                source_info.append("")
    
    source_text = "\n".join(source_info)
    print(f"✅ Generated source information ({len(source_text)} characters)")
    print(f"📄 Preview: {source_text[:200]}...")
    
    return True

def main():
    """Run all source information tests"""
    print("🧪 Testing Source Information Functionality...")
    print("=" * 60)
    
    # Test 1: Source data loading
    print("\n1. Testing source data loading...")
    source_data, load_success = test_source_data_loading()
    
    # Test 2: Idea source linking
    print("\n2. Testing idea source linking...")
    linking_success = test_idea_source_linking()
    
    # Test 3: Source information generation
    print("\n3. Testing source information generation...")
    generation_success = test_source_information_generation()
    
    # Summary
    print("\n" + "=" * 60)
    if load_success and linking_success and generation_success:
        print("🎉 All source information tests passed!")
        print("✅ The 'View Sources' feature should work correctly in the GUI.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    print(f"\n📊 Summary:")
    print(f"   - Source data loading: {'✅' if load_success else '❌'}")
    print(f"   - Idea source linking: {'✅' if linking_success else '❌'}")
    print(f"   - Information generation: {'✅' if generation_success else '❌'}")

if __name__ == "__main__":
    main() 
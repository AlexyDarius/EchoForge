#!/usr/bin/env python3
"""
Test script to show the new clean source information output
"""

import sys
import os
import json

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def show_clean_output():
    """Show the new clean output format"""
    print("🧪 Testing Clean Source Information Output...")
    print("=" * 60)
    
    # Load repo data
    repo_file_path = "../data/REPOSITORY/repo.json"
    try:
        with open(repo_file_path, 'r', encoding='utf-8') as f:
            repo_data = json.load(f)
    except Exception as e:
        print(f"❌ Error loading repo data: {e}")
        return
    
    # Load source data
    json_logs_path = "../data/json-logs"
    md_logs_path = "../data/md-logs"
    source_data = {}
    
    try:
        import glob
        # Load JSON logs
        json_files = glob.glob(os.path.join(json_logs_path, "*.json"))
        for json_file in json_files:
            week = os.path.basename(json_file).replace('.json', '')
            with open(json_file, 'r', encoding='utf-8') as f:
                source_data[week] = json.load(f)
        
        # Load markdown logs
        md_files = glob.glob(os.path.join(md_logs_path, "*.md"))
        for md_file in md_files:
            week = os.path.basename(md_file).replace('.md', '')
            if week not in source_data:
                source_data[week] = {}
            with open(md_file, 'r', encoding='utf-8') as f:
                source_data[week]['markdown'] = f.read()
    except Exception as e:
        print(f"❌ Error loading source data: {e}")
        return
    
    # Test with the first idea that has related items
    test_idea = None
    for idea in repo_data:
        if idea.get('related_items'):
            test_idea = idea
            break
    
    if not test_idea:
        print("⚠️  No ideas with related items found for testing")
        return
    
    print(f"📋 Testing with idea: {test_idea.get('idea_id')}")
    print(f"   Title: {test_idea.get('title')}")
    print(f"   Related items: {len(test_idea.get('related_items', []))}")
    print()
    
    # Generate clean source information
    related_items = test_idea.get('related_items', [])
    
    # Group items by week to avoid repetition
    weeks_data = {}
    for item in related_items:
        week = item.get('week', 'Unknown')
        if week not in weeks_data:
            weeks_data[week] = []
        weeks_data[week].append(item)
    
    source_info = []
    source_info.append(f"# Source Information for: {test_idea.get('title', 'Unknown Idea')}")
    source_info.append(f"Idea ID: {test_idea.get('idea_id', 'Unknown')}")
    source_info.append("=" * 60)
    source_info.append("")
    
    for week, items in weeks_data.items():
        source_info.append(f"## Week: {week}")
        source_info.append("")
        
        if week in source_data:
            week_data = source_data[week]
            
            # Add metadata once per week
            if 'metadata' in week_data:
                source_info.append("### Week Metadata:")
                source_info.append(f"- Tools Used: {', '.join(week_data['metadata'].get('tools_used', []))}")
                source_info.append(f"- Tags: {', '.join(week_data['metadata'].get('tags', []))}")
                source_info.append(f"- Generated: {week_data['metadata'].get('generated_at', 'Unknown')}")
                source_info.append("")
            
            # Add all JSON sources for this week
            source_info.append("### JSON Sources:")
            source_info.append("")
            
            for item in items:
                item_id = item.get('item_id', 'Unknown')
                section = item.get('section', 'Unknown')
                
                source_info.append(f"**Item: {item_id} | Section: {section}**")
                
                # Find the specific item in JSON data
                if 'items' in week_data and section in week_data['items']:
                    items_data = week_data['items'][section]
                    for item_data in items_data:
                        if item_data.get('id') == item_id:
                            source_info.append("```json")
                            source_info.append(json.dumps(item_data, indent=2, ensure_ascii=False))
                            source_info.append("```")
                            source_info.append("")
                            break
                else:
                    source_info.append(f"⚠️ Item {item_id} not found in section {section}")
                    source_info.append("")
        else:
            source_info.append(f"⚠️ No source data found for week: {week}")
            source_info.append("")
        
        source_info.append("-" * 40)
        source_info.append("")
    
    source_text = "\n".join(source_info)
    
    print("📄 NEW CLEAN OUTPUT FORMAT:")
    print("=" * 60)
    print(source_text)
    print("=" * 60)
    print(f"📊 Output length: {len(source_text)} characters")
    print("✅ No repetitive markdown content!")
    print("✅ Only JSON sources and metadata shown")
    print("✅ Grouped by week to avoid duplication")

if __name__ == "__main__":
    show_clean_output() 
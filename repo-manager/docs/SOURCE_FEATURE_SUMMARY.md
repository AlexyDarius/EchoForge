# Source Information Linking Feature

## 🎯 What's New

The EchoForge Repo Manager now includes **automatic source information linking** that connects your ideas back to their original source data from JSON logs and markdown files.

## 🔗 How It Works

### 1. **Automatic Data Loading**
- Loads all `*.json` files from `../data/json-logs/`
- Loads all `*.md` files from `../data/md-logs/`
- Creates a complete source data index

### 2. **Idea-Source Linking**
- Each idea's `related_items` array links to specific source items
- Format: `{"week": "2025-W29", "item_id": "e1", "section": "experiments_and_research"}`
- Automatically finds the corresponding JSON and markdown data

### 3. **Source Information Display**
- **"View Sources"** button in the main interface
- Opens a new window with clean, organized source information
- Shows:
  - Original JSON source data for each related item (no repetition)
  - Week metadata (tools used, tags, generation date) shown once per week
  - Grouped by week to avoid duplication

## 📋 Example Output

When you click "View Sources" for the "Functional Architecture with Verb-Based Decomposition" idea, you'll see:

```
# Source Information for: Functional Architecture with Verb-Based Decomposition
Idea ID: I-FUNC-ARCH-VERBS
============================================================

## Week: 2025-W29

### Week Metadata:
- Tools Used: Supabase, Postgres, React, GPS Tracking, Capella
- Tags: systems_engineering, functional_architecture, sso, gps_tracking, week-review
- Generated: 2025-07-21T17:42:00Z

### JSON Sources:

**Item: e1 | Section: experiments_and_research**
```json
{
  "id": "e1",
  "text": "Exploré une méthode de décomposition fonctionnelle à logique basée sur un glossaire structuré de verbes par niveau d'architecture"
}
```

**Item: e2 | Section: experiments_and_research**
```json
{
  "id": "e2",
  "text": "Clarifié les transitions entre fonctions système, sous-systèmes logiques et implémentations physiques grâce à des patterns de verbes génériques comme *Input, Process, Control*, etc"
}
```

**Item: n1 | Section: notes_and_observations**
```json
{
  "id": "n1",
  "text": "Standardiser les verbes par niveau d'architecture améliore la cohérence, la détection d'erreurs, et facilite la transition vers l'architecture physique"
}
```
```

## 🎉 Benefits for Content Generation

### **Preserve Original Context**
- Never lose the original source information
- See the full context around each idea
- Understand the progression and evolution of ideas

### **Complete Source Tracking**
- Link back to specific items in your weekly logs
- Access structured JSON data without repetition
- Maintain traceability from idea to source

### **Content Creation Ready**
- Copy source information to clipboard
- Use original text for content generation
- Reference specific weeks and items in your content

## 🔧 Technical Implementation

### **Data Loading**
```python
def load_source_data(self):
    # Load JSON logs
    json_files = glob.glob(os.path.join(self.json_logs_path, "*.json"))
    for json_file in json_files:
        week = os.path.basename(json_file).replace('.json', '')
        with open(json_file, 'r', encoding='utf-8') as f:
            self.source_data[week] = json.load(f)
    
    # Load markdown logs
    md_files = glob.glob(os.path.join(self.md_logs_path, "*.md"))
    for md_file in md_files:
        week = os.path.basename(md_file).replace('.md', '')
        with open(md_file, 'r', encoding='utf-8') as f:
            self.source_data[week]['markdown'] = f.read()
```

### **Source Information Generation**
```python
def get_source_information(self, idea: Dict[str, Any]) -> str:
    # For each related item in the idea
    for item in related_items:
        week = item.get('week')
        item_id = item.get('item_id')
        section = item.get('section')
        
        # Find corresponding JSON data
        # Find corresponding markdown context
        # Generate formatted output
```

## 🚀 Usage

1. **Select an idea** from the left panel
2. **Click "View Sources"** button
3. **Review the source information** in the new window
4. **Copy to clipboard** if needed for content generation
5. **Close the window** when done

## 📊 Current Status

✅ **Fully Implemented and Tested**
- All 5 ideas in your repo.json are properly linked
- Source data from 2025-W29 is loaded and accessible
- Source information generation works correctly
- GUI integration is complete

## 🔮 Future Enhancements

- **Search functionality** within source information
- **Export source data** to different formats
- **Direct content generation** from source information
- **Source data visualization** and analytics 
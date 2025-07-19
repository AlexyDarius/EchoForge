# AI Assessment Feature Guide

## 🎯 Overview

The EchoForge Repo Manager now includes **AI Assessment Integration** that allows you to upload external AI-generated assessments for trend and maturity scores, automatically updating your idea scores and storing detailed justifications.

## 🔧 How It Works

### 1. **Assessment File Structure**
Assessments are stored as JSON files in `../data/evaluations/` with the naming convention:
```
{idea_id}_{assessment_type}.json
```

Examples:
- `I-FUNC-ARCH-VERBS_trend.json`
- `I-FUNC-ARCH-VERBS_maturity.json`

### 2. **Trend Assessment Format**
```json
{
  "trend_score": 7,
  "justification": "Verb‑based functional decomposition and functional architecture remain well‑established in model‑based systems engineering (MBSE). Recent research (e.g., SSFD heuristics and guidelines in 2023) reinforces structured functional modeling using verb‑noun patterns and flow heuristics...",
  "suggested_tags": ["MBSE", "functional_decomposition", "systems_engineering", "SSFD", "IDEF0"]
}
```

### 3. **Maturity Assessment Format**
```json
{
  "maturity_score": 5,
  "justification": "The idea has conceptual clarity and multiple weekly notes indicating sustained research. It demonstrates structured thinking and pattern definition, especially in the use of verb glossaries and functional transition logic...",
  "suggested_next_steps": [
    "Draft a short blog article demonstrating the approach with diagrams or patterns.",
    "Create a verb-pattern glossary table mapped to architecture levels (Functional, Logical, Physical).",
    "Implement a basic prototype or template using SysML/Capella or custom tool."
  ]
}
```

## 🎮 Using the Feature

### **Uploading Assessments**

1. **Select an idea** from the left panel
2. **Click the 📁 button** next to the score you want to update:
   - 📁 next to Maturity → Upload maturity assessment
   - 📁 next to Trend → Upload trend assessment
3. **Select your JSON file** in the file dialog
4. **Scores update automatically** when valid assessment is uploaded

### **Viewing Assessments**

1. **Select an idea** from the left panel
2. **Click the 📊 button** next to the score you want to view:
   - 📊 next to Maturity → View maturity assessment details
   - 📊 next to Trend → View trend assessment details
3. **Review the full assessment** in a new window
4. **Copy to clipboard** if needed

## 🎯 Interface Changes

### **New Score Controls**
Each score row now includes assessment buttons:

```
Maturity: [=====●=====] 5 📊 📁
Interest:  [=====●=====] 7
Trend:     [======●====] 6 📊 📁
```

- **📊** = View existing assessment
- **📁** = Upload new assessment

### **Assessment Viewer Window**
When viewing assessments, you'll see:
- **Full JSON content** with proper formatting
- **Copy to clipboard** button
- **Read-only display** to prevent accidental changes

## 🔄 Workflow Integration

### **Automatic Score Updates**
- When you upload a valid assessment, the corresponding score automatically updates
- The score slider and label reflect the new assessment value
- Changes are saved when you click "Save Changes"

### **Overwrite Behavior**
- **New assessments overwrite previous ones** for the same idea and type
- Files are saved as `{idea_id}_{assessment_type}.json`
- No versioning - latest assessment replaces the previous one

### **Validation**
- **Required fields** are validated on upload
- **JSON format** is checked
- **Score ranges** (1-10) are enforced
- **Error messages** guide you if validation fails

## 📁 File Organization

```
data/
├── evaluations/
│   ├── I-FUNC-ARCH-VERBS_trend.json
│   ├── I-FUNC-ARCH-VERBS_maturity.json
│   ├── I-GPS-MULTI-TRACKER_trend.json
│   └── I-SSO-TOKEN-SYSTEM_maturity.json
├── json-logs/
├── md-logs/
└── REPOSITORY/
    └── repo.json
```

## 🎯 Benefits

### **AI Integration Ready**
- **External AI tools** can generate assessment JSON files
- **Standardized format** ensures compatibility
- **Automatic score updates** reduce manual work

### **Detailed Justifications**
- **Store full AI reasoning** for each score
- **Suggested tags** help with categorization
- **Next steps** guide idea development

### **Seamless Workflow**
- **One-click upload** from AI tool outputs
- **Immediate score updates** in the interface
- **Full assessment history** preserved in files

## 🔧 Technical Details

### **File Naming Convention**
```python
def get_assessment_file_path(self, idea_id: str, assessment_type: str) -> str:
    return os.path.join(self.evaluations_path, f"{idea_id}_{assessment_type}.json")
```

### **Validation Rules**
- **Trend assessments** must contain `trend_score`, `justification`, `suggested_tags`
- **Maturity assessments** must contain `maturity_score`, `justification`, `suggested_next_steps`
- **Scores** must be integers between 1-10

### **Integration Points**
- **Automatic loading** when selecting ideas
- **Score synchronization** between assessments and form
- **File management** with proper error handling

## 🚀 Getting Started

### **1. Prepare Your AI Assessment**
Create a JSON file with the required format (see examples above)

### **2. Upload to the Application**
1. Run the application: `python run.py`
2. Select your idea
3. Click 📁 next to the appropriate score
4. Select your JSON file

### **3. Verify the Results**
1. Check that the score updated automatically
2. Click 📊 to view the full assessment
3. Save changes to persist the updates

## 🔮 Future Enhancements

- **Assessment history** with versioning
- **Bulk assessment upload** for multiple ideas
- **Assessment templates** for different AI tools
- **Assessment analytics** and trends
- **Export assessments** to different formats

## 📝 Example Workflow

1. **AI Tool Generates Assessment**
   ```json
   {
     "trend_score": 8,
     "justification": "Strong market interest in this approach...",
     "suggested_tags": ["emerging_trend", "high_potential"]
   }
   ```

2. **Save as JSON File**
   - Save as `I-MY-IDEA_trend.json`

3. **Upload to Application**
   - Select idea "I-MY-IDEA"
   - Click 📁 next to Trend score
   - Select the JSON file

4. **Automatic Update**
   - Trend score updates to 8
   - Full assessment stored in `data/evaluations/`
   - View details with 📊 button

The AI assessment feature makes it easy to integrate external AI analysis into your idea management workflow! 🎉 
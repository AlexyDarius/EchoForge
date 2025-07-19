# EchoForge Repository Manager

A Python Tkinter GUI application for managing your EchoForge idea repository (`repo.json`).

## Features

- **View Ideas**: Browse all ideas in your repository with a clean list interface
- **Create New Ideas**: Add new ideas with auto-generated IDs
- **Edit Ideas**: Modify existing ideas including all fields:
  - Idea ID and Title
  - Description (multi-line text)
  - Scores (Maturity, Personal Interest, Trend) with slider controls
  - Tags (comma-separated)
  - Related Items (JSON format)
- **Delete Ideas**: Remove ideas with confirmation
- **Save Changes**: Save modifications to the repository file
- **Real-time Updates**: See changes immediately in the interface
- **View Sources**: Link back to original source information from JSON logs and markdown files
- **AI Assessments**: Upload external AI-generated assessments for trend and maturity scores

## Project Structure

```
repo-manager/
├── src/
│   └── repo_manager.py      # Main application code
├── tests/                   # Test files (future)
├── docs/                    # Documentation (future)
├── venv/                    # Python virtual environment
├── requirements.txt         # Python dependencies
├── run.py                   # Application launcher
└── README.md               # This file
```

## Prerequisites

- Python 3.7 or higher
- macOS, Linux, or Windows

## Installation & Setup

### 1. Navigate to the project directory

```bash
cd repo-manager
```

### 2. Activate the virtual environment

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Running the Application

### Method 1: Using the launcher script (Recommended)

```bash
python run.py
```

### Method 2: Running directly from src

```bash
cd src
python repo_manager.py
```

## Usage Guide

### Getting Started

1. **Launch the application** using one of the methods above
2. **View existing ideas** in the left panel - click on any idea to load its details
3. **Create a new idea** by clicking the "New Idea" button
4. **Edit idea details** in the right panel form
5. **Save changes** using the "Save Changes" button
6. **Save to file** using the "Save to File" button to persist changes to `repo.json`

### Interface Overview

#### Left Panel - Ideas List
- **New Idea**: Create a new idea with auto-generated ID
- **Delete**: Remove the selected idea (with confirmation)
- **Refresh**: Reload the idea list
- **Idea List**: Shows all ideas in format "ID: Title"

#### Right Panel - Idea Details
- **Idea ID**: Unique identifier for the idea
- **Title**: Short descriptive title
- **Description**: Multi-line description of the idea
- **Scores**: Three sliders for:
  - **Maturity**: How developed the idea is (1-10)
  - **Interest**: Personal interest level (1-10)
  - **Trend**: Market/trend relevance (1-10)
- **Tags**: Comma-separated list of tags
- **Related Items**: JSON array of related items (week, item_id, section)
- **View Sources**: Button to see all original source information from JSON logs and markdown files
- **Assessment Buttons**: 📊 to view AI assessments, 📁 to upload new assessments

### Working with Ideas

#### Creating a New Idea
1. Click "New Idea" button
2. Fill in the required fields (ID and Title are mandatory)
3. Adjust scores using the sliders
4. Add tags (comma-separated)
5. Add related items in JSON format
6. Click "Save Changes"

#### Editing an Existing Idea
1. Select an idea from the left panel
2. Modify any fields in the right panel
3. Click "Save Changes" to update the idea
4. Click "Save to File" to persist changes to disk

#### Viewing Source Information
1. Select an idea from the left panel
2. Click "View Sources" button
3. A new window opens showing:
   - Original JSON source data for each related item
   - Full markdown context from the week
   - Week metadata (tools used, tags, generation date)
4. Use "Copy to Clipboard" to copy the source information

#### Working with AI Assessments
1. **Add Assessment**: Click 📁 next to Maturity or Trend score
2. **Choose input method**:
   - **📁 Upload JSON File**: Select a JSON file from your computer
   - **Paste JSON**: Copy-paste JSON content directly from your AI tool
3. **Score updates automatically** when valid assessment is saved
4. **View Assessment**: Click 📊 to see full assessment details
5. **Overwrite previous** assessments for the same idea and type

#### Deleting an Idea
1. Select the idea to delete
2. Click "Delete" button
3. Confirm the deletion in the dialog

### Source Information Linking

The application automatically links ideas to their source information:

- **JSON Logs**: Loads all `*.json` files from `../data/json-logs/`
- **Markdown Logs**: Loads all `*.md` files from `../data/md-logs/`
- **Related Items**: Each idea's `related_items` array links to specific items in the source data
- **Context Preservation**: Shows both the specific item and full week context

This ensures you never lose the original source information when generating content from ideas.

### Data Format

The application works with the existing `repo.json` format:

```json
[
  {
    "idea_id": "I-FUNC-ARCH-VERBS",
    "title": "Functional Architecture with Verb-Based Decomposition",
    "description": "Description text...",
    "related_items": [
      {
        "week": "2025-W29",
        "item_id": "e1",
        "section": "experiments_and_research"
      }
    ],
    "maturity_score": 3,
    "personal_interest_score": 8,
    "trend_score": 6,
    "tags": ["systems_engineering", "functional_architecture"]
  }
]
```

## Troubleshooting

### Common Issues

1. **"Repository file not found" warning**
   - The application looks for `../data/REPOSITORY/repo.json`
   - Ensure the file exists or create it manually

2. **Permission errors when saving**
   - Check file permissions on the repository directory
   - Ensure you have write access to the parent directory

3. **Invalid JSON in Related Items**
   - The Related Items field must contain valid JSON
   - Use the format shown in the data format section above

4. **Application won't start**
   - Ensure virtual environment is activated
   - Check Python version (3.7+ required)
   - Verify all dependencies are installed

### File Path Configuration

The application is configured to look for the repository file at:
```
../data/REPOSITORY/repo.json
```

If your file structure is different, modify the `repo_file_path` variable in `src/repo_manager.py`.

## Development

### Adding New Features

1. Modify `src/repo_manager.py`
2. Test your changes
3. Update this README if needed

### Running Tests

```bash
# Future: Add test files to tests/ directory
python -m pytest tests/
```

### Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Add docstrings to functions and classes

## License

This project is part of the EchoForge repository management system.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the code comments in `src/repo_manager.py`
3. Ensure your `repo.json` file follows the expected format 
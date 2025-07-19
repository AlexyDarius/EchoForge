# Quick Start Guide - EchoForge Repo Manager

## 🚀 Get Started in 3 Steps

### 1. Setup (One-time)
```bash
cd repo-manager
./setup.sh
```

### 2. Run the Application
```bash
source venv/bin/activate
python run.py
```

### 3. Use the GUI
- **Left Panel**: Browse and select ideas
- **Right Panel**: Edit idea details
- **Buttons**: Create, save, delete ideas

## 📋 What You Can Do

✅ **View Ideas**: See all your ideas in a clean list  
✅ **Create New Ideas**: Add ideas with auto-generated IDs  
✅ **Edit Everything**: Title, description, scores, tags, related items  
✅ **Save Changes**: Persist modifications to your repo.json  
✅ **Delete Ideas**: Remove ideas with confirmation  
✅ **View Sources**: Link back to original source information from JSON and markdown logs  

## 🎯 Key Features

- **Intuitive Interface**: Two-panel layout for easy navigation
- **Real-time Updates**: See changes immediately
- **Score Sliders**: Easy adjustment of maturity, interest, and trend scores
- **JSON Support**: Full support for related items in JSON format
- **Auto-save**: Prompts to save when closing
- **Source Linking**: Automatic linking to original JSON logs and markdown files
- **Content Generation Ready**: Preserve all source information for content creation

## 🔧 Troubleshooting

**If the app won't start:**
```bash
# Reinstall tkinter
brew install python-tk@3.13

# Reactivate environment
source venv/bin/activate
python run.py
```

**If you get permission errors:**
```bash
chmod +x setup.sh
./setup.sh
```

## 📁 File Structure
```
repo-manager/
├── src/repo_manager.py    # Main application
├── run.py                 # Launcher script
├── setup.sh              # Setup script
├── test_app.py           # Test script
├── requirements.txt      # Dependencies
└── README.md            # Full documentation
```

## 🎉 You're Ready!

The application is now ready to manage your EchoForge repository. Enjoy organizing your ideas! 
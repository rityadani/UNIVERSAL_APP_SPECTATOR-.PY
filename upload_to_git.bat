@echo off
echo Uploading Universal RL Project to GitHub...

REM Initialize git repository
git init

REM Add remote repository
git remote add origin https://github.com/rityadani/UNIVERSAL_APP_SPECTATOR-.PY.git

REM Add all files
git add .

REM Commit with message
git commit -m "Universal RL System - Complete 7-Day Project

- Universal App Specification format for any application
- Auto-generation of app specs from repositories  
- RL state/action mapping for universal compatibility
- Multi-app support (Flask, Django, FastAPI, Spring Boot, React, Next.js, Docker)
- Advanced web dashboard with modern UI
- Complete integration testing
- 8 different app types supported with same RL brain

Features:
✅ Universal app spec schema
✅ Automatic repo scanning
✅ Generic RL state/action mapping  
✅ Multi-framework support
✅ Advanced dashboard interface
✅ Complete documentation
✅ Integration with existing RL systems

Commands:
- python dashboard.py (Main dashboard)
- python run_universal_demo.py (RL demo)
- python all_apps_demo.py (Test all apps)
- python connect_all.py (System integration)"

REM Push to GitHub
git branch -M main
git push -u origin main

echo Upload complete!
pause
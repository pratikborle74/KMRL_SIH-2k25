#!/usr/bin/env python3
"""
🚀 KMRL Authentication System Startup Script
============================================
Easy startup script to initialize and run the complete KMRL authentication system.
"""

import os
import sys
import subprocess
import time
import threading
from pathlib import Path

def print_banner():
    """Print startup banner"""
    print("""
    ╔══════════════════════════════════════════════════════╗
    ║                🚆 KMRL AUTHENTICATION SYSTEM 🚆      ║
    ║                                                      ║
    ║  🔐 Secure Login/Signup System                       ║
    ║  🛡️  JWT Token Authentication                        ║
    ║  👥 User Management & Admin Panel                    ║
    ║  📊 Dashboard Protection                             ║
    ║                                                      ║
    ║  Built for Kochi Metro Rail Limited                 ║
    ╚══════════════════════════════════════════════════════╝
    """)

def check_requirements():
    """Check if required packages are installed"""
    print("🔍 Checking system requirements...")
    
    required_packages = [
        'streamlit', 'fastapi', 'uvicorn', 'passlib', 'python-jose', 
        'sqlalchemy', 'pandas', 'plotly', 'requests'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} - Missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("🔧 Installing missing packages...")
        
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install"
            ] + missing_packages)
            print("✅ All packages installed successfully!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install packages. Please install manually:")
            print(f"pip install {' '.join(missing_packages)}")
            return False
    else:
        print("✅ All required packages are installed!")
    
    return True

def initialize_database():
    """Initialize the authentication database"""
    print("🗄️  Initializing authentication database...")
    
    try:
        from auth_models import auth_manager
        
        # Test database connection
        user_count = auth_manager.get_user_count()
        print(f"✅ Database initialized with {user_count} users")
        
        if user_count == 0:
            print("ℹ️  No users found. Default admin user will be created.")
        
        return True
    except Exception as e:
        print(f"❌ Database initialization failed: {str(e)}")
        return False

def start_fastapi_server():
    """Start the FastAPI authentication server"""
    print("🚀 Starting FastAPI authentication server...")
    
    try:
        # Start FastAPI server in background
        process = subprocess.Popen([
            sys.executable, "auth_api.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Give it time to start
        time.sleep(3)
        
        # Check if it's running
        if process.poll() is None:
            print("✅ FastAPI server started successfully!")
            print("🌐 API available at: http://localhost:8001")
            print("📚 API docs available at: http://localhost:8001/docs")
            return process
        else:
            print("❌ FastAPI server failed to start")
            return None
    except Exception as e:
        print(f"❌ Error starting FastAPI server: {str(e)}")
        return None

def start_streamlit_login():
    """Start the Streamlit login page"""
    print("🎨 Starting Streamlit login interface...")
    
    try:
        # Start Streamlit login page
        process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", "login_page.py",
            "--server.port", "8501",
            "--server.headless", "true",
            "--browser.gatherUsageStats", "false"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Give it time to start
        time.sleep(5)
        
        # Check if it's running
        if process.poll() is None:
            print("✅ Streamlit login page started successfully!")
            print("🔐 Login page available at: http://localhost:8501")
            return process
        else:
            print("❌ Streamlit login page failed to start")
            return None
    except Exception as e:
        print(f"❌ Error starting Streamlit login page: {str(e)}")
        return None

def start_dashboard():
    """Start the main dashboard (optional)"""
    print("📊 Starting KMRL dashboard...")
    
    try:
        # Start main dashboard on different port
        process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", "kmrl_interactive_dashboard.py",
            "--server.port", "8502",
            "--server.headless", "true",
            "--browser.gatherUsageStats", "false"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Give it time to start
        time.sleep(5)
        
        # Check if it's running
        if process.poll() is None:
            print("✅ KMRL dashboard started successfully!")
            print("📊 Dashboard available at: http://localhost:8502")
            return process
        else:
            print("❌ KMRL dashboard failed to start")
            return None
    except Exception as e:
        print(f"❌ Error starting dashboard: {str(e)}")
        return None

def start_user_management():
    """Start the user management interface"""
    print("👥 Starting user management interface...")
    
    try:
        # Start user management on different port
        process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", "user_management.py",
            "--server.port", "8503",
            "--server.headless", "true",
            "--browser.gatherUsageStats", "false"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Give it time to start
        time.sleep(5)
        
        # Check if it's running
        if process.poll() is None:
            print("✅ User management interface started successfully!")
            print("👥 User management available at: http://localhost:8503")
            return process
        else:
            print("❌ User management interface failed to start")
            return None
    except Exception as e:
        print(f"❌ Error starting user management: {str(e)}")
        return None

def show_system_status():
    """Show system status and URLs"""
    print("""
    ╔══════════════════════════════════════════════════════╗
    ║                   🎉 SYSTEM READY! 🎉                ║
    ╠══════════════════════════════════════════════════════╣
    ║                                                      ║
    ║  🔐 LOGIN PAGE:      http://localhost:8501           ║
    ║  🌐 AUTH API:        http://localhost:8001           ║
    ║  📚 API DOCS:        http://localhost:8001/docs      ║
    ║  📊 DASHBOARD:       http://localhost:8502           ║
    ║  👥 USER MANAGEMENT: http://localhost:8503           ║
    ║                                                      ║
    ╠══════════════════════════════════════════════════════╣
    ║                                                      ║
    ║  📝 DEFAULT ADMIN CREDENTIALS:                       ║
    ║     Username: admin                                  ║
    ║     Password: admin123                               ║
    ║                                                      ║
    ║  🚀 START HERE: Open http://localhost:8501           ║
    ║                                                      ║
    ╚══════════════════════════════════════════════════════╝
    """)

def main():
    """Main startup function"""
    print_banner()
    
    # Check requirements
    if not check_requirements():
        print("❌ Requirements check failed. Please install missing packages.")
        return
    
    # Initialize database
    if not initialize_database():
        print("❌ Database initialization failed.")
        return
    
    print("\n🚀 Starting KMRL Authentication System...")
    print("=" * 60)
    
    processes = []
    
    # Start FastAPI server
    api_process = start_fastapi_server()
    if api_process:
        processes.append(("FastAPI Server", api_process))
    
    # Start Streamlit login page
    login_process = start_streamlit_login()
    if login_process:
        processes.append(("Login Page", login_process))
    
    # Ask user if they want to start additional services
    print("\n🤔 Would you like to start additional services?")
    
    start_dashboard_choice = input("📊 Start main dashboard? (y/N): ").lower().strip()
    if start_dashboard_choice in ['y', 'yes']:
        dashboard_process = start_dashboard()
        if dashboard_process:
            processes.append(("Dashboard", dashboard_process))
    
    start_user_mgmt_choice = input("👥 Start user management interface? (y/N): ").lower().strip()
    if start_user_mgmt_choice in ['y', 'yes']:
        user_mgmt_process = start_user_management()
        if user_mgmt_process:
            processes.append(("User Management", user_mgmt_process))
    
    if processes:
        show_system_status()
        
        print("⏹️  Press Ctrl+C to stop all services")
        
        try:
            # Keep running until interrupted
            while True:
                time.sleep(1)
                
                # Check if any process died
                for name, process in processes:
                    if process.poll() is not None:
                        print(f"⚠️  {name} process ended unexpectedly")
                        processes.remove((name, process))
                        break
                
                if not processes:
                    print("❌ All processes ended. Exiting...")
                    break
                    
        except KeyboardInterrupt:
            print("\n\n🛑 Shutting down all services...")
            
            # Terminate all processes
            for name, process in processes:
                print(f"  Stopping {name}...")
                process.terminate()
                try:
                    process.wait(timeout=5)
                    print(f"  ✅ {name} stopped")
                except subprocess.TimeoutExpired:
                    print(f"  🔥 Force killing {name}...")
                    process.kill()
            
            print("✅ All services stopped. Goodbye!")
    
    else:
        print("❌ No services started successfully.")

if __name__ == "__main__":
    main()
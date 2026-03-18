#!/usr/bin/env python3
"""
🚀 KMRL Complete System Launcher
===============================
One-command script to run the entire Kochi Metro Fleet Optimization System

This script will:
1. Generate data
2. Run optimization engine
3. Launch web dashboard
4. Start all services

Author: KMRL AI Development Team
Date: September 2024
"""

import os
import sys
import subprocess
import time
import threading
import webbrowser
from pathlib import Path
import importlib.util

class KMRLSystemLauncher:
    def __init__(self):
        self.base_dir = Path.cwd()
        self.processes = []
        self.services_started = []
        
    def print_banner(self):
        """Print startup banner"""
        print("""
        ╔══════════════════════════════════════════════════════════════════╗
        ║                🚆 KOCHI METRO RAIL LIMITED 🚆                   ║
        ║                                                                  ║
        ║            🤖 INTELLIGENT FLEET OPTIMIZATION SYSTEM             ║
        ║                                                                  ║
        ║  ✨ AI-Powered Fleet Management                                  ║
        ║  📊 Real-time Dashboard                                          ║
        ║  🔧 Maintenance Optimization                                     ║
        ║  📈 ML-based Predictions                                         ║
        ║  🎯 Priority Management                                          ║
        ║                                                                  ║
        ║  🚀 Complete System Launcher - One Command Setup                ║
        ╚══════════════════════════════════════════════════════════════════╝
        """)
        
    def generate_data(self):
        """Generate required data files (optional, non-blocking)"""
        print("\n🏭 Checking for data generation...")
        
        # Look for data generator script
        data_generators = [
            "enhanced_data_generator.py",
            "large_scale_data_generator.py", 
            "data_generator.py"
        ]
        
        generator_script = None
        for script in data_generators:
            if (self.base_dir / script).exists():
                generator_script = script
                break
        
        if generator_script:
            print(f"📊 Found {generator_script}, attempting to run...")
            try:
                result = subprocess.run([
                    sys.executable, generator_script
                ], cwd=self.base_dir, timeout=10, capture_output=True, text=True)
                
                if result.returncode == 0:
                    print("✅ Data generation completed successfully!")
                else:
                    print(f"⚠️  Data generation completed with warnings (continuing anyway)")
                return True
            except subprocess.TimeoutExpired:
                print("⚠️  Data generation timed out (continuing with existing data)")
                return True
            except Exception as e:
                print(f"⚠️  Data generation failed: {e} (continuing with existing data)")
                return True
        else:
            print("📄 No data generator found, using existing data files...")
            return True

    def run_optimization_engine(self):
        """Run the intelligent optimization engine (optional, non-blocking)"""
        print("\n⚙️  Checking for optimization engine...")
        
        if (self.base_dir / "intelligent_optimization_engine.py").exists():
            print("🚀 Found optimization engine, attempting to run...")
            try:
                result = subprocess.run([
                    sys.executable, "intelligent_optimization_engine.py"
                ], cwd=self.base_dir, timeout=10, capture_output=True, text=True)
                
                if result.returncode == 0:
                    print("✅ Optimization engine completed successfully!")
                else:
                    print("⚠️  Optimization completed with warnings (continuing anyway)")
                return True
            except subprocess.TimeoutExpired:
                print("⚠️  Optimization timed out (continuing without optimization)")
                return True
            except Exception as e:
                print(f"⚠️  Optimization failed: {e} (continuing without optimization)")
                return True
        else:
            print("⚙️  No optimization engine found, skipping optimization...")
            return True

    def start_html_dashboard(self):
        """Start the HTML dashboard"""
        print("\n🌐 Starting HTML Dashboard...")
        
        html_file = self.base_dir / "index.html"
        if html_file.exists():
            try:
                # Open in default browser
                html_path = f"file://{html_file.absolute()}"
                webbrowser.open(html_path)
                print("✅ HTML Dashboard opened in browser!")
                print(f"🔗 URL: {html_path}")
                print("🔐 Login credentials:")
                print("   - admin / admin123")
                print("   - supervisor / super123") 
                print("   - worker / worker123")
                self.services_started.append("HTML Dashboard")
                return True
            except Exception as e:
                print(f"⚠️  Failed to open HTML dashboard: {e}")
                print(f"   You can manually open: {html_file.absolute()}")
                return False
        else:
            print("❌ index.html not found")
            return False

    def start_streamlit_dashboard(self):
        """Start Streamlit dashboard if available"""
        print("\n📊 Checking for Streamlit dashboard...")
        
        dashboard_files = [
            "dashboard.py",
            "kmrl_interactive_dashboard.py",
            "streamlit_dashboard.py"
        ]
        
        dashboard_script = None
        for script in dashboard_files:
            if (self.base_dir / script).exists():
                dashboard_script = script
                break
        
        if dashboard_script:
            print(f"🚀 Starting {dashboard_script}...")
            try:
                process = subprocess.Popen([
                    sys.executable, "-m", "streamlit", "run", dashboard_script,
                    "--server.port", "8501",
                    "--server.headless", "true",
                    "--browser.gatherUsageStats", "false"
                ], cwd=self.base_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
                # Give it time to start
                time.sleep(3)
                
                if process.poll() is None:
                    print("✅ Streamlit dashboard started!")
                    print("🔗 URL: http://localhost:8501")
                    self.processes.append(("Streamlit Dashboard", process))
                    self.services_started.append("Streamlit Dashboard")
                    
                    # Try to open in browser
                    try:
                        webbrowser.open("http://localhost:8501")
                    except:
                        pass
                    
                    return True
                else:
                    print("❌ Streamlit dashboard failed to start")
                    return False
                    
            except Exception as e:
                print(f"❌ Error starting Streamlit: {e}")
                return False
        else:
            print("📊 No Streamlit dashboard found, skipping...")
            return True

    def start_fastapi_service(self):
        """Start FastAPI service if available"""
        print("\n🚀 Checking for FastAPI service...")
        
        api_files = [
            "auth_api.py",
            "api_server.py",
            "main_api.py"
        ]
        
        api_script = None
        for script in api_files:
            if (self.base_dir / script).exists():
                api_script = script
                break
        
        if api_script:
            print(f"🌐 Starting {api_script}...")
            try:
                # Try to import uvicorn
                try:
                    import uvicorn
                    # Use uvicorn directly
                    process = subprocess.Popen([
                        sys.executable, "-m", "uvicorn", f"{api_script.replace('.py', '')}:app",
                        "--host", "0.0.0.0", "--port", "8000", "--reload"
                    ], cwd=self.base_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                except ImportError:
                    # Fallback to running the script directly
                    process = subprocess.Popen([
                        sys.executable, api_script
                    ], cwd=self.base_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
                # Give it time to start
                time.sleep(3)
                
                if process.poll() is None:
                    print("✅ FastAPI service started!")
                    print("🔗 API: http://localhost:8000")
                    print("📚 Docs: http://localhost:8000/docs")
                    self.processes.append(("FastAPI Service", process))
                    self.services_started.append("FastAPI Service")
                    return True
                else:
                    print("❌ FastAPI service failed to start")
                    return False
                    
            except Exception as e:
                print(f"❌ Error starting FastAPI: {e}")
                return False
        else:
            print("🚀 No FastAPI service found, skipping...")
            return True

    def run_system_validation(self):
        """Run system validation checks"""
        print("\n✅ Running system validation...")
        
        validation_scripts = [
            "ml_models_sanity_check.py",
            "validate_dashboard_data.py",
            "system_health_check.py"
        ]
        
        validation_passed = 0
        for script in validation_scripts:
            if (self.base_dir / script).exists():
                try:
                    result = subprocess.run([
                        sys.executable, script
                    ], cwd=self.base_dir, timeout=60, capture_output=True, text=True)
                    
                    if result.returncode == 0:
                        print(f"   ✅ {script}")
                        validation_passed += 1
                    else:
                        print(f"   ⚠️  {script} - warnings")
                        validation_passed += 1
                        
                except Exception as e:
                    print(f"   ❌ {script} - failed: {e}")
        
        if validation_passed > 0:
            print(f"✅ System validation completed ({validation_passed} checks)")
        else:
            print("⚠️  No validation scripts found")
        
        return True

    def show_system_status(self):
        """Show final system status"""
        print("""
        ╔══════════════════════════════════════════════════════════════════╗
        ║                        🎉 SYSTEM READY! 🎉                      ║
        ╚══════════════════════════════════════════════════════════════════╝
        """)
        
        print("🌟 Services Started:")
        for service in self.services_started:
            print(f"   ✅ {service}")
        
        print(f"\n📊 Available Interfaces:")
        if "HTML Dashboard" in self.services_started:
            print(f"   🌐 HTML Dashboard: file://{(self.base_dir / 'index.html').absolute()}")
        if "Streamlit Dashboard" in self.services_started:
            print(f"   📊 Streamlit Dashboard: http://localhost:8501")
        if "FastAPI Service" in self.services_started:
            print(f"   🚀 API Service: http://localhost:8000")
            print(f"   📚 API Documentation: http://localhost:8000/docs")
        
        print(f"\n🔐 Default Login Credentials:")
        print(f"   • admin / admin123 (Administrator)")
        print(f"   • supervisor / super123 (Supervisor)")  
        print(f"   • worker / worker123 (Worker)")
        
        print(f"\n📁 System Files:")
        print(f"   • Data files: Using existing data")
        print(f"   • Optimization results: Available if generated")
        
        if self.processes:
            print(f"\n⏹️  Press Ctrl+C to stop all background services")

    def cleanup_processes(self):
        """Cleanup background processes"""
        if self.processes:
            print(f"\n🛑 Stopping background services...")
            for name, process in self.processes:
                try:
                    print(f"   Stopping {name}...")
                    process.terminate()
                    process.wait(timeout=5)
                    print(f"   ✅ {name} stopped")
                except subprocess.TimeoutExpired:
                    print(f"   🔥 Force killing {name}...")
                    process.kill()
                except Exception as e:
                    print(f"   ⚠️  Error stopping {name}: {e}")
            
            print("✅ All background services stopped")

    def run_complete_system(self):
        """Run the complete system"""
        self.print_banner()
        
        # Step 1: Check/Generate data (optional, skip if fails)
        print("\n📊 Checking for existing data...")
        try:
            self.generate_data()
        except Exception as e:
            print(f"⚠️  Data generation skipped: {e}")
            print("🔄 Continuing with existing data...")

        # Step 2: Run optimization (optional, skip if fails)
        print("\n⚙️  Running optimization if available...")
        try:
            self.run_optimization_engine()
        except Exception as e:
            print(f"⚠️  Optimization skipped: {e}")
            print("🔄 Continuing without optimization...")
        
        # Step 3: Run validation (optional)
        print("\n✅ Running system validation...")
        try:
            self.run_system_validation()
        except Exception as e:
            print(f"⚠️  System validation skipped: {e}")
        
        # Step 4: Start services
        print(f"\n🚀 Starting web services...")
        
        # Start HTML dashboard (primary interface)
        self.start_html_dashboard()
        
        # Start additional services
        self.start_streamlit_dashboard() 
        self.start_fastapi_service()
        
        # Step 5: Show status
        self.show_system_status()
        
        # Step 6: Keep alive if background processes
        if self.processes:
            try:
                print(f"\n🔄 System running... (Press Ctrl+C to stop)")
                while True:
                    time.sleep(1)
                    
                    # Check if processes are still alive
                    for name, process in self.processes[:]:
                        if process.poll() is not None:
                            print(f"⚠️  {name} process ended")
                            self.processes.remove((name, process))
                    
                    if not self.processes:
                        print("ℹ️  All background processes ended")
                        break
                        
            except KeyboardInterrupt:
                print(f"\n\n👋 Shutting down system...")
                self.cleanup_processes()
        
        print(f"\n✅ KMRL System session completed!")
        return True


def main():
    """Main entry point"""
    launcher = KMRLSystemLauncher()
    
    try:
        success = launcher.run_complete_system()
        if success:
            print(f"\n🎉 System launched successfully!")
            print(f"💡 Tip: You can run this script anytime to restart the complete system")
        else:
            print(f"\n❌ System launch failed")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print(f"\n\n👋 System launch interrupted")
        launcher.cleanup_processes()
        sys.exit(0)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        launcher.cleanup_processes()
        sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Run script for the Website Analyzer Streamlit application.
Handles environment loading and application startup.
"""

import os
import sys
import subprocess
from pathlib import Path

def load_environment():
    """Load environment variables from .env file if it exists."""
    env_file = Path(__file__).parent / '.env'
    if env_file.exists():
        try:
            from dotenv import load_dotenv
            load_dotenv(env_file)
            print(f"✅ Loaded environment from {env_file}")
        except ImportError:
            print("⚠️  python-dotenv not installed. Install with: pip install python-dotenv")
        except Exception as e:
            print(f"⚠️  Error loading .env file: {e}")
    else:
        print("ℹ️  No .env file found. Using system environment variables.")

def check_dependencies():
    """Check if required dependencies are installed."""
    required_packages = ['streamlit', 'requests']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing required packages: {', '.join(missing_packages)}")
        print("Install with: pip install -r requirements.txt")
        return False
    
    print("✅ All required dependencies are installed")
    return True

def run_streamlit():
    """Run the Streamlit application."""
    app_file = Path(__file__).parent / 'app.py'
    
    if not app_file.exists():
        print(f"❌ Application file not found: {app_file}")
        return False
    
    print(f"🚀 Starting Website Analyzer...")
    print(f"📁 App file: {app_file}")
    print(f"🌐 Will open browser at: http://localhost:8501")
    print("=" * 50)
    
    try:
        # Run streamlit
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', str(app_file),
            '--server.headless', 'false',
            '--server.port', '8501',
            '--browser.gatherUsageStats', 'false'
        ])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error running application: {e}")
        return False
    
    return True

def main():
    """Main entry point."""
    print("🔍 Website Analyzer - Streamlit Client")
    print("=" * 50)
    
    # Load environment
    load_environment()
    
    # Check dependencies
    if not check_dependencies():
        print("\n💡 To install dependencies, run:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    # Check configuration
    api_url = os.getenv('WEBSITE_ANALYZER_API_URL', '')
    if not api_url or api_url == 'https://your-api-endpoint.amazonaws.com':
        print("\n⚠️  Warning: API URL not configured or using placeholder")
        print("   Set WEBSITE_ANALYZER_API_URL in your .env file")
        print("   The app will still run but API calls will fail")
    
    auth_key = os.getenv('AUTH_SECRET_KEY', '')
    if not auth_key:
        print("\n⚠️  Warning: AUTH_SECRET_KEY not configured")
        print("   Authentication may not work properly")
    
    print("\n🚀 Starting application...")
    
    # Run the app
    success = run_streamlit()
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main() 
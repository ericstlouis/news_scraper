import subprocess
import sys

def check_and_install_dependencies():
    """
    Check and install required packages if they're not already installed
    """
    # List of all required packages
    required_packages = [
        'requests',        # For making HTTP requests
        'beautifulsoup4', # For parsing HTML
        'lxml'           # For faster HTML parsing
    ]
    
    print("Checking and installing required packages...")
    
    for package in required_packages:
        try:
            __import__(package.replace('4', ''))  # Handle beautifulsoup4 -> beautifulsoup
            print(f"✓ {package} is already installed")
        except ImportError:
            print(f"Installing {package}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"✓ {package} has been installed successfully")
            except subprocess.CalledProcessError as e:
                print(f"❌ Error installing {package}: {e}")
                sys.exit(1)
    
    print("\nAll required packages are installed! You can now run the web scraper.")

if __name__ == "__main__":
    check_and_install_dependencies()

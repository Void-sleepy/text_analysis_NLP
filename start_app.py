import sys

def check_dependencies():
    required_packages = ['flask', 'textblob', 'nltk', 'textstat']
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    if missing_packages:
        print(f"Missing packages: {', '.join(missing_packages)}")
        return False
    return True

def download_nltk_data():
    try:
        import nltk
        nltk.download('punkt', quiet=True)
        return True
    except Exception as e:
        print(f"NLTK setup warning: {e}")
        return True

def main():
    print("Starting...........................")

    if not check_dependencies():
        print("Please install missing packages first.")
        sys.exit(1)

    download_nltk_data()

    try:
        from router import app
        print("✅ Backend loaded successfully!")
        print("   Visit: http://localhost:5000")
        print("⏹️ Press Ctrl+C to stop")
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"Failed to start: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
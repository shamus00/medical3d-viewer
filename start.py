#!/usr/bin/env python3
"""
Medical 3D Pipeline Starter
Choose how you want to run the pipeline
"""

import sys
import os

def main():
    print("🏥 Medical 3D Pipeline")
    print("======================")
    print()
    print("Choose how to run:")
    print("1. Test the pipeline")
    print("2. Start web API server")
    print("3. Interactive Python session")
    print("4. Exit")
    print()
    
    choice = input("Enter choice (1-4): ").strip()
    
    if choice == "1":
        print("\n🧪 Running pipeline test...")
        os.system("python test_pipeline.py")
        
    elif choice == "2":
        print("\n🌐 Starting web API server...")
        print("The server will start on http://localhost:5000")
        print("Press Ctrl+C to stop")
        # Note: API server file will be created separately
        print("❌ API server not yet created - run the full setup first")
        
    elif choice == "3":
        print("\n🐍 Starting interactive session...")
        print("Import the pipeline with: from med_pipeline import MedicalTo3D")
        os.system("python -i -c 'from med_pipeline import MedicalTo3D; print(\"Pipeline ready!\")'")
        
    elif choice == "4":
        print("👋 Goodbye!")
        
    else:
        print("❌ Invalid choice")
        main()

if __name__ == "__main__":
    main()

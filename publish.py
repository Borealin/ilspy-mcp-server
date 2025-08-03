#!/usr/bin/env python3
"""
Simple script to build and publish the package to PyPI.
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd: str) -> bool:
    """Run a command and return success status."""
    print(f"🔧 Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    return result.returncode == 0


def main():
    """Main function to build and publish package."""
    
    # Check if we're in the right directory
    if not Path("pyproject.toml").exists():
        print("❌ pyproject.toml not found. Run this script from the project root.")
        sys.exit(1)
    
    print("📦 Building and publishing ilspy-mcp-server...")
    
    # Clean previous builds
    print("\n1. Cleaning previous builds...")
    run_command("rm -rf dist/ build/")
    
    # Build the package
    print("\n2. Building package...")
    if not run_command("python -m build"):
        print("❌ Build failed!")
        sys.exit(1)
    
    # Check the package
    print("\n3. Checking package...")
    if not run_command("twine check dist/*"):
        print("❌ Package check failed!")
        sys.exit(1)
    
    # Ask for confirmation
    print("\n4. Ready to upload to PyPI")
    response = input("Do you want to upload to PyPI? (y/N): ")
    
    if response.lower() != 'y':
        print("Upload cancelled.")
        sys.exit(0)
    
    # Upload to PyPI
    print("\n5. Uploading to PyPI...")
    if not run_command("twine upload dist/*"):
        print("❌ Upload failed!")
        sys.exit(1)
    
    print("\n✅ Package successfully published to PyPI!")
    print("📦 Install with: pip install ilspy-mcp-server")


if __name__ == "__main__":
    main()
import os
import sys
from pathlib import Path


def setup_environment():
    """Initialize project directories and virtual environment."""

    project_root = Path(__file__).parent

    # Create required directories
    directories = [
        project_root / "models_pkl",
        project_root / "data",
        project_root / "data" / "uploads"
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"✓ Created directory: {directory}")

    print("\n✅ Environment setup complete!")
    print(f"\nProject structure ready at: {project_root}")
    print("\nNext steps:")
    print("1. pip install -r requirements.txt")
    print("2. Place your .pkl files in: models_pkl/")
    print("3. streamlit run app.py")


if __name__ == "__main__":
    setup_environment()

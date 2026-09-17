import os
import sys

# Define required libraries for the project
REQUIRED_PACKAGES = [
    'pandas',
    'numpy',
    'matplotlib',
    'seaborn',
    'sklearn',
    'statsmodels'
]

print("=== ENVIRONMENT VERIFICATION ===")
print(f"Python Executable: {sys.executable}")
print(f"Python Version: {sys.version.split()[0]}\n")

# Check library installations
all_passed = True
for package in REQUIRED_PACKAGES:
    try:
        __import__(package)
        print(f"[OK] Package '{package}' is installed.")
    except ImportError:
        print(f"[MISSING] Package '{package}' is NOT installed.")
        all_passed = False

# Check data file existence
raw_data_path = os.path.join('data', 'raw', 'online_retail_II.csv')
if os.path.exists(raw_data_path):
    print(f"\n[OK] Raw dataset found at '{raw_data_path}'.")
else:
    print(f"\n[WARNING] Dataset missing at '{raw_data_path}'. Check file location.")

if all_passed:
    print("\nEnvironment verification SUCCESSFUL. Ready for Phase 3.")
else:
    print("\nEnvironment verification FAILED. Please install missing packages.")
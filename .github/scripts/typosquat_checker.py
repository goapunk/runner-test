import json
import requests
import difflib
import sys

# Download top PyPI packages
TOP_URL = "https://hugovk.github.io/top-pypi-packages/top-pypi-packages-30-days.min.json"
resp = requests.get(TOP_URL)
data = resp.json()
top_packages = set(pkg["project"] for pkg in data["rows"])

# Load requirements.txt
with open("requirements.txt") as f:
    requirements = [
        line.strip().split("==")[0]
        for line in f
        if line.strip() and not line.startswith("#")
    ]

# Check for typosquatting
def check_typos(package_name, top_packages, cutoff=0.85):
    matches = difflib.get_close_matches(package_name, top_packages, n=5, cutoff=cutoff)
    return matches

# Report suspicious packages
suspicious = []
for req in requirements:
    similar = check_typos(req, top_packages)
    if similar and req not in top_packages:
        suspicious.append((req, similar))

if suspicious:
    print("❌ Possible typosquatting / suspicious package names detected:")
    for pkg, similar in suspicious:
        print(f"  {pkg}  -> similar to top packages: {similar}")
    sys.exit(1)  # FAIL CI
else:
    print("✅ No suspicious packages detected.")


import os
import re
import sys

def extract_value(header: str, body: str) -> str:
    """
    Find the value immediately after a markdown header like '### Company Name'
    Skips blank lines.
    """
    pattern = rf"### {re.escape(header)}\s*\n+([^\n]+)"
    match = re.search(pattern, body, re.IGNORECASE)
    return match.group(1).strip() if match else ""

if __name__ == "__main__":
    body = sys.stdin.read()

    company_name = extract_value("Company Name", body)
    company_code = extract_value("Company Code", body)
    location     = extract_value("Location", body)

    # Write to GitHub environment file so later steps can use them
    with open(os.environ["GITHUB_ENV"], "a") as f:
        f.write(f"company_name={company_name}\n")
        f.write(f"company_code={company_code}\n")
        f.write(f"location={location}\n")

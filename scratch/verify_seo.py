#!/usr/bin/env python3
import subprocess
import time
import urllib.request
import urllib.error
import re
import json
import sys

print("==================================================")
print("              Avelyn SEO Validator               ")
print("==================================================")

# 1. Start the Next.js production server in the background
print("Starting Next.js production server (npm run start)...")
proc = subprocess.Popen(
    ["npm", "run", "start"],
    cwd="/Users/vishwaksen/Desktop/projects/Avelyn/website",
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

# Wait for server to boot (port 3000)
time.sleep(3.5)

base_url = "http://localhost:3000"
routes = [
    "",
    "/about-avelyn",
    "/what-is-avelyn",
    "/avelyn-ai",
    "/avelyn-vs-chatgpt",
    "/avelyn-vs-grammarly"
]

all_passed = True
results = {}

def get_page(url):
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (SEO Validator)'}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            return response.status, response.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception as e:
        return 500, str(e)

try:
    # Validate Robots.txt
    print("\n[Robots.txt Verification]")
    status, robots_txt = get_page(f"{base_url}/robots.txt")
    print(f"URL: {base_url}/robots.txt -> Status: {status}")
    if status == 200:
        print("Content:")
        print("-" * 40)
        print(robots_txt.strip())
        print("-" * 40)
        if "sitemap.xml" not in robots_txt.lower():
            print("❌ Robots.txt is missing sitemap reference!")
            all_passed = False
    else:
        print("❌ Robots.txt is not accessible!")
        all_passed = False

    # Validate Sitemap.xml
    print("\n[Sitemap.xml Verification]")
    status, sitemap_xml = get_page(f"{base_url}/sitemap.xml")
    print(f"URL: {base_url}/sitemap.xml -> Status: {status}")
    if status == 200:
        print("Content:")
        print("-" * 40)
        print(sitemap_xml.strip())
        print("-" * 40)
        # Check routes inclusion
        for r in routes:
            expected_loc = f"https://avelyn.software{r}"
            if expected_loc not in sitemap_xml:
                print(f"❌ Sitemap is missing route: {expected_loc}")
                all_passed = False
    else:
        print("❌ Sitemap.xml is not accessible!")
        all_passed = False

    # Validate Pages
    print("\n[Routes & HTML Verification]")
    for r in routes:
        url = f"{base_url}{r}"
        status, html = get_page(url)
        print(f"Route: {r or '/'} -> HTTP Status: {status}")
        if status != 200:
            print(f"❌ Route {r} returned failure code!")
            all_passed = False
            continue

        # Check noindex
        if "noindex" in html.lower():
            print(f"❌ Route {r} contains 'noindex' meta tag!")
            all_passed = False

        # Check canonical URL
        canonical_match = re.search(r'<link[^>]*rel="canonical"[^>]*href="([^"]+)"', html)
        if canonical_match:
            canonical_url = canonical_match.group(1)
            expected_canonical = f"https://avelyn.software{r}"
            if canonical_url != expected_canonical:
                print(f"❌ Route {r} has incorrect canonical link: {canonical_url} (Expected: {expected_canonical})")
                all_passed = False
            else:
                print(f"  ✓ Canonical URL matches: {canonical_url}")
        else:
            print(f"❌ Route {r} is missing canonical link tag!")
            all_passed = False

        # Verify cross-linking (ensure all pages link to all other 5 pages)
        print("  Checking internal links:")
        for other in routes:
            if other == r:
                continue
            # Look for link tag pointing to other route
            # Check either absolute (https://avelyn.software/other) or relative (/other)
            pattern_rel = f'href="{other}"'
            pattern_abs = f'href="https://avelyn.software{other}"'
            if (pattern_rel in html) or (pattern_abs in html) or (other == "" and ('href="/"' in html or 'href="https://avelyn.software"' in html)):
                print(f"    ✓ Links to {other or '/'}")
            else:
                print(f"    ❌ MISSING LINK to {other or '/'}")
                all_passed = False

        # Extract and parse JSON-LD schemas
        print("  Checking JSON-LD Structured Data:")
        json_ld_blocks = re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', html, re.DOTALL)
        found_types = set()
        if json_ld_blocks:
            for block in json_ld_blocks:
                try:
                    schema_data = json.loads(block.strip())
                    schema_type = schema_data.get("@type", "Unknown")
                    found_types.add(schema_type)
                    print(f"    ✓ Valid JSON-LD found: type={schema_type}")
                except Exception as exc:
                    print(f"    ❌ Invalid JSON-LD schema payload: {exc}")
                    all_passed = False
        else:
            print("    ❌ No structured data JSON-LD scripts found!")
            all_passed = False

        # Verify required schemas
        required_global = {"Organization", "WebSite", "SoftwareApplication"}
        for req_t in required_global:
            if req_t not in found_types:
                print(f"    ❌ Missing required global schema: {req_t}")
                all_passed = False
        
        # If it is a sub-page, check BreadcrumbList
        if r != "":
            if "BreadcrumbList" not in found_types:
                print("    ❌ Missing subpage schema: BreadcrumbList")
                all_passed = False
        
        # If it is /what-is-avelyn, check FAQPage
        if r == "/what-is-avelyn":
            if "FAQPage" not in found_types:
                print("    ❌ Missing FAQ page schema: FAQPage")
                all_passed = False

        # Verify Brand usage "Avelyn"
        brand_count = len(re.findall(r'Avelyn', html))
        print(f"  ✓ Brand term 'Avelyn' occurrences: {brand_count}")

finally:
    # Clean terminate Next.js background process
    print("\nStopping Next.js server...")
    proc.terminate()
    proc.wait()
    print("Next.js server stopped.")

if all_passed:
    print("\n🎉 ALL SEO VERIFICATION CHECKS PASSED SUCCESSFULLY!")
    sys.exit(0)
else:
    print("\n❌ SOME SEO VERIFICATION CHECKS FAILED!")
    sys.exit(1)

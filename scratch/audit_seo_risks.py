#!/usr/bin/env python3
import subprocess
import time
import urllib.request
import urllib.error
import re
import json
import sys

print("==================================================")
print("             Avelyn SEO Risk Auditor              ")
print("==================================================")

# Start production server
print("Starting Next.js production server...")
proc = subprocess.Popen(
    ["npm", "run", "start"],
    cwd="/Users/vishwaksen/Desktop/projects/Avelyn/website",
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

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

def get_page(url):
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (SEO Auditor)'}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            return response.status, response.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception as e:
        return 500, str(e)

try:
    for r in routes:
        url = f"{base_url}{r}"
        status, html = get_page(url)
        if status != 200:
            print(f"❌ Failed to fetch route {r}: status {status}")
            continue
            
        # Clean HTML tags using regex
        # Remove head
        clean_html = re.sub(r'<head.*?>.*?</head>', ' ', html, flags=re.DOTALL|re.IGNORECASE)
        # Remove scripts
        clean_html = re.sub(r'<script.*?>.*?</script>', ' ', clean_html, flags=re.DOTALL|re.IGNORECASE)
        # Remove styles
        clean_html = re.sub(r'<style.*?>.*?</style>', ' ', clean_html, flags=re.DOTALL|re.IGNORECASE)
        # Remove comments
        clean_html = re.sub(r'<!--.*?-->', ' ', clean_html, flags=re.DOTALL)
        # Remove all other HTML tags
        clean_html = re.sub(r'<.*?>', ' ', clean_html, flags=re.DOTALL)
        
        # Clean up whitespace and entities
        clean_text = re.sub(r'\s+', ' ', clean_html).strip()
        # Decode some basic entities
        clean_text = clean_text.replace("&copy;", " ").replace("&nbsp;", " ")
        
        # Word count
        words = clean_text.split()
        word_count = len(words)
        
        # Brand count (exact match)
        brand_matches = re.findall(r'\bAvelyn\b', clean_text, re.IGNORECASE)
        brand_count = len(brand_matches)
        
        # Keyword density
        density = (brand_count / word_count * 100) if word_count > 0 else 0
        
        print(f"\nRoute: {r or '/'}")
        print(f"  - Clean Word Count: {word_count}")
        print(f"  - 'Avelyn' occurrences (visible text): {brand_count}")
        print(f"  - Keyword density: {density:.2f}%")
        
        if word_count < 800:
            print(f"  ⚠️  WARNING: Thin Content (< 800 words) detected!")
        if density > 5.0:
            print(f"  🚨 ALERT: Keyword Stuffing risk (> 5.0% density) detected!")

finally:
    print("\nStopping Next.js server...")
    proc.terminate()
    proc.wait()
    print("Server stopped.")

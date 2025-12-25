#!/usr/bin/env python3
"""
Diary Generator Script
Scans text files in the entries/ directory and generates HTML pages automatically.

Text file format:
- Filename: YYYY-MM-DD.txt
- First line: Full date (e.g., "December 25, 2025")
- Second line: Title (optional, if blank will use "Diary Entry")
- Rest: Content (can include blank lines for paragraphs)

Usage:
    python generate_diary.py
"""

import os
import re
from datetime import datetime
from pathlib import Path
from collections import defaultdict

# Paths
SCRIPT_DIR = Path(__file__).parent
ENTRIES_DIR = SCRIPT_DIR / "entries"
OUTPUT_DIR = SCRIPT_DIR

def parse_entry_file(filepath):
    """Parse a diary entry text file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    if len(lines) < 1:
        return None
    
    # First line is the date
    date_str = lines[0].strip()
    
    # Second line is the title (if exists and not empty)
    title = "Diary Entry"
    content_start = 1
    if len(lines) > 1 and lines[1].strip():
        title = lines[1].strip()
        content_start = 2
    
    # Rest is content
    content = ''.join(lines[content_start:]).strip()
    
    # Parse filename to get year, month, day
    filename = Path(filepath).stem  # Gets YYYY-MM-DD from YYYY-MM-DD.txt
    try:
        date_obj = datetime.strptime(filename, "%Y-%m-%d")
    except ValueError:
        print(f"Warning: Could not parse date from filename {filename}")
        return None
    
    return {
        'date_str': date_str,
        'title': title,
        'content': content,
        'year': date_obj.year,
        'month': date_obj.month,
        'month_name': date_obj.strftime("%B").lower(),
        'day': date_obj.day,
        'filename': filename,
        'date_obj': date_obj
    }

def format_content_to_html(content):
    """Convert plain text content to HTML paragraphs."""
    paragraphs = content.split('\n\n')
    html_parts = []
    for para in paragraphs:
        para = para.strip()
        if para:
            # Replace single newlines with <br /> within paragraphs
            para = para.replace('\n', '<br />\n')
            html_parts.append(f'<p>{para}</p>')
    return '\n\n'.join(html_parts)

def generate_entry_page(entry):
    """Generate HTML page for a single diary entry."""
    year = entry['year']
    month_name = entry['month_name']
    filename = entry['filename']
    
    # Create directory structure
    output_dir = OUTPUT_DIR / str(year) / month_name
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate HTML content
    content_html = format_content_to_html(entry['content'])
    
    html = f"""<!DOCTYPE HTML>
<html>
<head>
    <title>{entry['date_str']} - Vamsi Hemadri</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
    <link rel="stylesheet" href="../../../assets/css/main.css" />
    <noscript><link rel="stylesheet" href="../../../assets/css/noscript.css" /></noscript>
</head>
<body class="is-preload">

<div id="wrapper">
    <header id="header">
        <a href="../../../index.html" class="logo"><strong>Vamsi Hemadri</strong></a>
        <nav>
            <a href="#menu">Menu</a>
        </nav>
    </header>

    <nav id="menu">
        <ul class="links">
            <li><a href="../../../index.html">Home</a></li>
            <li><a href="../../../learnings/learningsLanding.html">Learnings</a></li>
            <li><a href="../../diaryLanding.html">Thoughts</a></li>
        </ul>
    </nav>

    <div id="main" class="alt">
        <section id="one">
            <div class="inner">
                <header class="major">
                    <h1>{entry['date_str']}</h1>
                </header>
                <p><a href="../{year}-index.html">← Back to {year}</a> | <a href="../../diaryLanding.html">← Diary Home</a></p>
                
                <h2>{entry['title']}</h2>
                {content_html}
                
            </div>
        </section>
    </div>

    <footer id="footer">
        <div class="inner">
            <ul class="copyright">
                <li>&copy; Vamsi Hemadri</li><li>Design: <a href="https://html5up.net">HTML5 UP</a></li>
            </ul>
        </div>
    </footer>
</div>

<script src="../../../assets/js/jquery.min.js"></script>
<script src="../../../assets/js/jquery.scrolly.min.js"></script>
<script src="../../../assets/js/jquery.scrollex.min.js"></script>
<script src="../../../assets/js/browser.min.js"></script>
<script src="../../../assets/js/breakpoints.min.js"></script>
<script src="../../../assets/js/util.js"></script>
<script src="../../../assets/js/main.js"></script>

</body>
</html>
"""
    
    # Write file
    output_file = output_dir / f"{filename}.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✓ Generated: {output_file.relative_to(OUTPUT_DIR)}")

def generate_year_index(year, entries):
    """Generate yearly index page."""
    # Group entries by month
    months = defaultdict(list)
    for entry in entries:
        months[entry['month']].append(entry)
    
    # Sort months in reverse order (December first)
    sorted_months = sorted(months.keys(), reverse=True)
    
    # Generate month sections
    month_sections = []
    for month_num in sorted_months:
        month_entries = sorted(months[month_num], key=lambda e: e['day'], reverse=True)
        month_name = month_entries[0]['month_name'].capitalize()
        
        entries_html = []
        for entry in month_entries:
            # Get first line of content as preview
            preview = entry['content'].split('\n')[0][:100]
            if len(entry['content']) > 100:
                preview += "..."
            
            entries_html.append(
                f'<li><a href="{entry["month_name"]}/{entry["filename"]}.html">{entry["date_str"]}</a> - {preview}</li>'
            )
        
        month_sections.append(f"""
                <h2>{month_name}</h2>
                <ul>
                    {''.join(entries_html)}
                </ul>
""")
    
    html = f"""<!DOCTYPE HTML>
<html>
<head>
    <title>{year} Diary - Vamsi Hemadri</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
    <link rel="stylesheet" href="../../assets/css/main.css" />
    <noscript><link rel="stylesheet" href="../../assets/css/noscript.css" /></noscript>
</head>
<body class="is-preload">

<div id="wrapper">
    <header id="header">
        <a href="../../index.html" class="logo"><strong>Vamsi Hemadri</strong></a>
        <nav>
            <a href="#menu">Menu</a>
        </nav>
    </header>

    <nav id="menu">
        <ul class="links">
            <li><a href="../../index.html">Home</a></li>
            <li><a href="../../learnings/learningsLanding.html">Learnings</a></li>
            <li><a href="../diaryLanding.html">Thoughts</a></li>
        </ul>
    </nav>

    <div id="main" class="alt">
        <section id="one">
            <div class="inner">
                <header class="major">
                    <h1>{year} Diary Entries</h1>
                </header>
                <p><a href="../diaryLanding.html">← Back to Diary Home</a></p>
                {''.join(month_sections)}
            </div>
        </section>
    </div>

    <footer id="footer">
        <div class="inner">
            <ul class="copyright">
                <li>&copy; Vamsi Hemadri</li><li>Design: <a href="https://html5up.net">HTML5 UP</a></li>
            </ul>
        </div>
    </footer>
</div>

<script src="../../assets/js/jquery.min.js"></script>
<script src="../../assets/js/jquery.scrolly.min.js"></script>
<script src="../../assets/js/jquery.scrollex.min.js"></script>
<script src="../../assets/js/browser.min.js"></script>
<script src="../../assets/js/breakpoints.min.js"></script>
<script src="../../assets/js/util.js"></script>
<script src="../../assets/js/main.js"></script>

</body>
</html>
"""
    
    output_file = OUTPUT_DIR / str(year) / f"{year}-index.html"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✓ Generated: {output_file.relative_to(OUTPUT_DIR)}")

def generate_landing_page(all_entries):
    """Generate main diary landing page."""
    # Group by year
    years = defaultdict(list)
    for entry in all_entries:
        years[entry['year']].append(entry)
    
    # Sort years in reverse order
    sorted_years = sorted(years.keys(), reverse=True)
    
    # Generate year sections
    year_sections = []
    for year in sorted_years:
        year_entries = sorted(years[year], key=lambda e: e['date_obj'], reverse=True)
        
        # Get top 3 recent entries for this year
        recent_entries = year_entries[:3]
        
        entries_html = []
        for entry in recent_entries:
            preview = entry['content'].split('\n')[0][:80]
            if len(entry['content']) > 80:
                preview += "..."
            
            entries_html.append(
                f'<li><a href="{year}/{entry["month_name"]}/{entry["filename"]}.html">{entry["date_str"]}</a> - {preview}</li>'
            )
        
        year_sections.append(f"""
                <h2>{year}</h2>
                <ul class="actions">
                    <li><a href="{year}/{year}-index.html" class="button">View All Entries</a></li>
                </ul>
                <h3>Recent Entries</h3>
                <ul>
                    {''.join(entries_html)}
                </ul>
                
                <hr style="margin: 3em 0;" />
""")
    
    # Remove last HR
    if year_sections:
        year_sections[-1] = year_sections[-1].replace('<hr style="margin: 3em 0;" />', '')
    
    html = f"""<!DOCTYPE HTML>
<!--
	Forty by HTML5 UP
	html5up.net | @ajlkn
	Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)
-->
<html>
<head>
    <title>My Diary - Vamsi Hemadri</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
    <link rel="stylesheet" href="../assets/css/main.css" />
    <noscript><link rel="stylesheet" href="../assets/css/noscript.css" /></noscript>
</head>
<body class="is-preload">

<!-- Wrapper -->
<div id="wrapper">

    <!-- Header -->
    <header id="header">
        <a href="../index.html" class="logo"><strong>Vamsi Hemadri</strong></a>
        <nav>
            <a href="#menu">Menu</a>
        </nav>
    </header>

    <!-- Menu -->
    <nav id="menu">
        <ul class="links">
            <li><a href="../index.html">Home</a></li>
            <li><a href="../learnings/learningsLanding.html">Learnings</a></li>
            <li><a href="diaryLanding.html">Thoughts</a></li>
        </ul>
    </nav>

    <!-- Main -->
    <div id="main" class="alt">

        <!-- One -->
        <section id="one">
            <div class="inner">
                <header class="major">
                    <h1>My Diary</h1>
                </header>
                <p>A personal space for thoughts, reflections, and daily observations. My journey captured in words, organized by time.</p>
            </div>
        </section>

        <!-- Two -->
        <section id="two">
            <div class="inner">
                {''.join(year_sections)}
            </div>
        </section>

    </div>

    <!-- Contact -->
    <section id="contact">
        <div class="inner">
            <section>
                <form method="post" action="#">
                    <div class="fields">
                        <div class="field half">
                            <label for="name">Name</label>
                            <input type="text" name="name" id="name" />
                        </div>
                        <div class="field half">
                            <label for="email">Email</label>
                            <input type="text" name="email" id="email" />
                        </div>
                        <div class="field">
                            <label for="message">Message</label>
                            <textarea name="message" id="message" rows="6"></textarea>
                        </div>
                    </div>
                    <ul class="actions">
                        <li><input type="submit" value="Send Message" class="primary" /></li>
                        <li><input type="reset" value="Clear" /></li>
                    </ul>
                </form>
            </section>
            <section class="split">
                <section>
                    <div class="contact-method">
                        <span class="icon solid alt fa-envelope"></span>
                        <h3>Email</h3>
                        <a href="#">13vamsihemadri@gmail.com</a>
                    </div>
                </section>
                <section>
                    <div class="contact-method">
                        <span class="icon solid alt fa-phone"></span>
                        <h3>Phone</h3>
                        <span>(+91) 789-688 0545</span>
                    </div>
                </section>
                <section>
                    <div class="contact-method">
                        <span class="icon solid alt fa-home"></span>
                        <h3>Address</h3>
                        <span>Bengaluru<br />
                        Bengaluru<br />
                        India</span>
                    </div>
                </section>
            </section>
        </div>
    </section>

    <!-- Footer -->
    <footer id="footer">
        <div class="inner">
            <ul class="icons">
                <li><a href="#" class="icon brands alt fa-twitter"><span class="label">Twitter</span></a></li>
                <li><a href="#" class="icon brands alt fa-facebook-f"><span class="label">Facebook</span></a></li>
                <li><a href="#" class="icon brands alt fa-instagram"><span class="label">Instagram</span></a></li>
                <li><a href="#" class="icon brands alt fa-github"><span class="label">GitHub</span></a></li>
                <li><a href="#" class="icon brands alt fa-linkedin-in"><span class="label">LinkedIn</span></a></li>
            </ul>
            <ul class="copyright">
                <li>&copy; Vamsi Hemadri</li><li>Design: <a href="https://html5up.net">HTML5 UP</a></li>
            </ul>
        </div>
    </footer>

</div>

<!-- Scripts -->
<script src="../assets/js/jquery.min.js"></script>
<script src="../assets/js/jquery.scrolly.min.js"></script>
<script src="../assets/js/jquery.scrollex.min.js"></script>
<script src="../assets/js/browser.min.js"></script>
<script src="../assets/js/breakpoints.min.js"></script>
<script src="../assets/js/util.js"></script>
<script src="../assets/js/main.js"></script>

</body>
</html>
"""
    
    output_file = OUTPUT_DIR / "diaryLanding.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✓ Generated: {output_file.relative_to(OUTPUT_DIR)}")

def main():
    """Main function to generate all diary pages."""
    print("🔍 Scanning for diary entries...")
    
    # Check if entries directory exists
    if not ENTRIES_DIR.exists():
        print(f"❌ Error: Entries directory not found at {ENTRIES_DIR}")
        print("   Please create it and add your .txt files")
        return
    
    # Find all .txt files
    txt_files = list(ENTRIES_DIR.glob("*.txt"))
    
    if not txt_files:
        print(f"❌ No .txt files found in {ENTRIES_DIR}")
        return
    
    print(f"📝 Found {len(txt_files)} entries")
    
    # Parse all entries
    all_entries = []
    for txt_file in txt_files:
        entry = parse_entry_file(txt_file)
        if entry:
            all_entries.append(entry)
    
    if not all_entries:
        print("❌ No valid entries found")
        return
    
    # Sort entries by date
    all_entries.sort(key=lambda e: e['date_obj'])
    
    print(f"\n🔨 Generating HTML pages...\n")
    
    # Generate individual entry pages
    for entry in all_entries:
        generate_entry_page(entry)
    
    # Group by year and generate yearly indexes
    years = defaultdict(list)
    for entry in all_entries:
        years[entry['year']].append(entry)
    
    for year, entries in years.items():
        generate_year_index(year, entries)
    
    # Generate landing page
    generate_landing_page(all_entries)
    
    print(f"\n✅ Done! Generated {len(all_entries)} entry pages, {len(years)} year indexes, and 1 landing page")
    print(f"\n💡 To add a new entry:")
    print(f"   1. Create a file: diary/entries/YYYY-MM-DD.txt")
    print(f"   2. First line: Full date (e.g., 'January 1, 2025')")
    print(f"   3. Second line: Title")
    print(f"   4. Rest: Your content")
    print(f"   5. Run: python diary/generate_diary.py")

if __name__ == "__main__":
    main()


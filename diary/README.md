# Diary System

A flexible, text-based diary system that automatically generates HTML pages from simple text files.

## 📁 Structure

```
diary/
├── entries/              # Put your .txt files here
│   ├── 2024-12-27.txt
│   └── 2025-12-25.txt
├── generate_diary.py     # The generator script
├── diaryLanding.html     # Auto-generated landing page
├── 2024/                 # Auto-generated year folders
│   ├── 2024-index.html
│   └── december/
│       └── 2024-12-27.html
└── 2025/
    ├── 2025-index.html
    └── december/
        └── 2025-12-25.html
```

## ✍️ How to Add a New Diary Entry

### Step 1: Create a Text File

In the `diary/entries/` folder, create a new file named: **`YYYY-MM-DD.txt`**

Example: `2025-12-26.txt`

### Step 2: Write Your Entry

Format:
```
[Line 1] Full date (e.g., "December 26, 2025")
[Line 2] Title (optional)
[Line 3+] Your content
```

Example (`2025-12-26.txt`):
```
December 26, 2025
Learning About Databases

Today I learned about database indexing and how B-trees work. 

It's fascinating how the data structure choices impact performance at scale. Query optimization is both an art and a science.
```

### Step 3: Generate HTML Pages

Run the generator script:
```bash
cd diary
python3 generate_diary.py
```

That's it! The script will:
- ✅ Create individual entry HTML pages
- ✅ Update yearly index pages
- ✅ Update the main diary landing page
- ✅ Organize everything by year and month

## 📝 Text File Format Details

### Filename
- **Must be**: `YYYY-MM-DD.txt` (e.g., `2025-01-15.txt`)
- Year: 4 digits
- Month: 2 digits (01-12)
- Day: 2 digits (01-31)

### Content
1. **Line 1**: Full date display (e.g., "January 15, 2025")
2. **Line 2**: Entry title (optional, defaults to "Diary Entry")
3. **Line 3+**: Your content
   - Use blank lines to separate paragraphs
   - Simple plain text (no HTML needed)

## 💡 Tips

### Quick Entry Creation
Create a simple bash alias in your `.zshrc` or `.bashrc`:

```bash
alias newdiary='cd ~/Documents/personal/site/vamsihemadri.github.io/diary/entries && vim $(date +%Y-%m-%d).txt'
```

Then just type `newdiary` to create and edit today's entry!

### After Writing
Don't forget to run the generator:
```bash
cd ~/Documents/personal/site/vamsihemadri.github.io/diary && python3 generate_diary.py
```

### Automation
You could even add to your alias:
```bash
alias newdiary='cd ~/Documents/personal/site/vamsihemadri.github.io/diary/entries && vim $(date +%Y-%m-%d).txt && cd .. && python3 generate_diary.py'
```

Now writing and publishing is just one command!

## 🎨 Customization

If you want to change the HTML styling, edit the templates inside `generate_diary.py`.

The script has three main template functions:
- `generate_entry_page()` - Individual entry pages
- `generate_year_index()` - Yearly index pages  
- `generate_landing_page()` - Main diary landing page

## 🔧 Requirements

- Python 3.6+
- No external dependencies (uses only standard library)

## 📊 What Gets Generated

For each entry, the script creates:
1. Individual HTML page at `YYYY/month/YYYY-MM-DD.html`
2. Updates/creates yearly index at `YYYY/YYYY-index.html`
3. Updates main landing page at `diaryLanding.html`

All pages maintain your site's design and navigation structure.


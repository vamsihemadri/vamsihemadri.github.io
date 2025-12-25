#!/bin/bash
# Quick script to create a new diary entry for today

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ENTRIES_DIR="$SCRIPT_DIR/entries"

# Get today's date
TODAY=$(date +%Y-%m-%d)
TODAY_DISPLAY=$(date "+%B %d, %Y")

FILENAME="$ENTRIES_DIR/$TODAY.txt"

# Check if entry already exists
if [ -f "$FILENAME" ]; then
    echo "📝 Entry for today already exists. Opening..."
    $EDITOR "$FILENAME"
else
    echo "✨ Creating new entry for $TODAY_DISPLAY..."
    
    # Create template
    cat > "$FILENAME" << EOF
$TODAY_DISPLAY
Entry Title

Write your thoughts here...

EOF
    
    echo "✅ Created: $FILENAME"
    
    # Open in editor (uses $EDITOR env var, falls back to vim)
    ${EDITOR:-vim} "$FILENAME"
fi

# Ask if they want to generate HTML
echo ""
read -p "🔨 Generate HTML pages? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    cd "$SCRIPT_DIR"
    python3 generate_diary.py
    echo ""
    echo "✅ Done! Your diary is updated."
fi


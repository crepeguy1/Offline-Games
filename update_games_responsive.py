#!/usr/bin/env python3
"""Update all game HTML files to be mobile-responsive."""

import os
import re
from pathlib import Path

GAMES_DIR = Path(r"c:\Users\crepe\OneDrive\Desktop\Gabb_GAmes\games")

RESPONSIVE_HEAD_CSS = '''  * {
    box-sizing: border-box;
  }
  body {
    background: #111;
    color: #eee;
    text-align: center;
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 10px;
    min-height: 100vh;
  }
  h1 {
    margin: 10px 0;
    font-size: clamp(1.5rem, 5vw, 2.5rem);
  }
  h2 {
    margin: 5px 0 20px;
    font-size: clamp(1rem, 4vw, 1.5rem);
  }
  button {
    min-height: 44px;
    min-width: 44px;
    cursor: pointer;
  }
  button:active {
    transform: scale(0.95);
  }
  canvas, #game {
    max-width: 100%;
    height: auto;
  }
  .controls {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 8px;
    margin-top: 20px;
  }
  .controls button {
    padding: clamp(10px, 2vw, 18px);
    font-size: clamp(1rem, 3vw, 1.5rem);
  }
  @media (max-width: 480px) {
    body { padding: 8px; }
  }
'''

def add_viewport_meta(html):
    """Add viewport meta tag if not present."""
    if '<meta name="viewport"' not in html:
        # Insert after charset meta
        html = re.sub(
            r'(<meta charset="[^"]+">)',
            r'\1\n<meta name="viewport" content="width=device-width, initial-scale=1.0">',
            html
        )
    return html

def update_body_styles(html):
    """Update body styles to be responsive."""
    body_style_pattern = r'<style>.*?body\s*\{.*?\}.*?</style>'
    
    if '<style>' in html:
        # Replace existing style block with responsive version
        # This is a simplified approach - for complex cases, manual review is needed
        html = re.sub(r'body\s*\{\s*[^}]+\}', f'body {{\n    background: #111;\n    color: #eee;\n    text-align: center;\n    font-family: Arial, sans-serif;\n    margin: 0;\n    padding: 10px;\n    min-height: 100vh;\n  }}', html, flags=re.DOTALL)
    
    return html

def process_all_games():
    """Process all game files."""
    game_files = list(GAMES_DIR.glob('*.html'))
    
    updated = 0
    skipped = []
    
    for game_file in game_files:
        # Skip files we already processed
        if game_file.name in ['2048.html', 'tetris.html']:
            print(f"✓ {game_file.name} (already updated)")
            continue
        
        try:
            # Try UTF-8 first, then fall back to latin-1
            try:
                content = game_file.read_text(encoding='utf-8')
            except UnicodeDecodeError:
                content = game_file.read_text(encoding='latin-1')
            
            original = content
            
            # Add viewport meta
            content = add_viewport_meta(content)
            
            # Check if already responsive
            if 'min-height' in content and 'clamp' in content:
                print(f"⊘ {game_file.name} (likely already responsive)")
                skipped.append(game_file.name)
                continue
            
            # Update if changed
            if content != original:
                try:
                    game_file.write_text(content, encoding='utf-8')
                except:
                    game_file.write_text(content, encoding='latin-1')
                updated += 1
                print(f"✓ {game_file.name} updated")
            else:
                print(f"- {game_file.name} (no changes needed)")
                
        except Exception as e:
            print(f"✗ {game_file.name}: {e}")
    
    print(f"\nSummary: {updated} files updated, {len(skipped)} skipped")

if __name__ == '__main__':
    process_all_games()

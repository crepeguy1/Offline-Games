#!/usr/bin/env python3
"""Enhance game files with full responsive CSS patterns."""

import os
import re
from pathlib import Path

GAMES_DIR = Path(r"c:\Users\crepe\OneDrive\Desktop\Gabb_GAmes\games")

# Already enhanced games
ENHANCED_GAMES = {
    '2048.html', 'tetris.html', 'breakout.html', 'pong.html',
    'space_invaders.html', 'flappy_bird.html', 'snake.html'
}

def add_responsive_css(html):
    """Add responsive CSS patterns to style blocks."""
    
    # First ensure viewport meta
    if '<meta name="viewport"' not in html:
        html = re.sub(
            r'(<meta charset="[^"]+">)',
            r'\1\n<meta name="viewport" content="width=device-width, initial-scale=1.0">',
            html
        )
    
    # Pattern to find existing style block
    style_pattern = r'<style>.*?</style>'
    match = re.search(style_pattern, html, re.DOTALL)
    
    if not match:
        return html
    
    style_block = match.group(0)
    
    # Add responsive patterns if not already present
    if 'clamp' in style_block or 'min-height: 44px' in style_block:
        return html  # Already enhanced
    
    # Extract existing CSS content
    css_content = style_block[7:-8]  # Remove <style> and </style>
    
    # Add universal box-sizing at top
    if 'box-sizing: border-box' not in css_content:
        css_content = '    * {\n      box-sizing: border-box;\n    }\n' + css_content
    
    # Enhance body with responsive padding and min-height
    css_content = re.sub(
        r'body\s*\{',
        'body {\n      margin: 0;\n      padding: 10px;\n      min-height: 100vh;',
        css_content
    )
    
    # Remove fixed height: 100vh and replace with min-height
    css_content = re.sub(r'height:\s*100vh', 'min-height: 100vh', css_content)
    
    # Enhance h1/h2 with clamp
    css_content = re.sub(
        r'h1\s*\{',
        'h1 {\n      font-size: clamp(1.5rem, 5vw, 2.5rem);',
        css_content
    )
    css_content = re.sub(
        r'h2\s*\{',
        'h2 {\n      font-size: clamp(1rem, 4vw, 1.5rem);',
        css_content
    )
    
    # Remove fixed font sizes from buttons and replace with clamp
    css_content = re.sub(
        r'(button[^\{]*\{[^}]*?)font-size:\s*\d+px',
        r'\1font-size: clamp(0.9rem, 3vw, 1.2rem)',
        css_content
    )
    
    # Add button touch targets and remove old padding
    css_content = re.sub(
        r'(button[^\{]*\{[^}]*?)padding:\s*\d+px\s*\d+px',
        r'\1padding: clamp(10px, 2vw, 18px)',
        css_content
    )
    
    # Add button min-height/width and cursor if not present
    if 'button' in css_content and 'min-height: 44px' not in css_content:
        button_pattern = r'(button[^\{]*\{[^}]*\n[^}]*)'
        css_content = re.sub(
            button_pattern,
            r'\1      min-height: 44px;\n      min-width: 44px;\n      cursor: pointer;',
            css_content,
            count=1
        )
    
    # Make canvas responsive
    css_content = re.sub(
        r'canvas\s*\{',
        'canvas {\n      max-width: 100%;\n      height: auto;',
        css_content
    )
    
    # Add mobile breakpoint at end if not present
    if '@media' not in css_content:
        css_content += '\n    @media (max-width: 480px) {\n      body { padding: 8px; }\n    }\n  '
    
    # Reconstruct style block
    new_style = f'<style>\n{css_content}\n</style>'
    new_html = html.replace(style_block, new_style)
    
    return new_html

def process_games():
    """Process all game files."""
    game_files = sorted(GAMES_DIR.glob('*.html'))
    
    enhanced = 0
    skipped = 0
    
    for game_file in game_files:
        if game_file.name in ENHANCED_GAMES:
            print(f"⊘ {game_file.name} (already manually enhanced)")
            continue
        
        try:
            # Read with encoding fallback
            try:
                content = game_file.read_text(encoding='utf-8')
            except UnicodeDecodeError:
                content = game_file.read_text(encoding='latin-1')
            
            original = content
            
            # Add responsive patterns
            new_content = add_responsive_css(content)
            
            if new_content == original:
                print(f"- {game_file.name} (no changes)")
                skipped += 1
            else:
                # Write back
                try:
                    game_file.write_text(new_content, encoding='utf-8')
                except:
                    game_file.write_text(new_content, encoding='latin-1')
                enhanced += 1
                print(f"✓ {game_file.name} enhanced")
                
        except Exception as e:
            print(f"✗ {game_file.name}: {e}")
    
    print(f"\nSummary: {enhanced} files enhanced, {skipped} skipped, {len(ENHANCED_GAMES)} already done")

if __name__ == '__main__':
    process_games()

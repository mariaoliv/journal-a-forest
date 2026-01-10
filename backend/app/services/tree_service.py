"""
Tree Service for generating trees based on entries.

Trees represent journal entries visually. Each entry unlocks a tree
with varying rarity based on entry characteristics.
"""

import random
import hashlib
from typing import Dict, Literal

TREE_TYPES = [
    "oak", "birch", "pine", "maple", "cherry", "willow", "cedar",
    "aspen", "elm", "fir", "spruce", "cypress", "redwood"
]

TREE_NAMES = {
    "oak": ["Ancient Oak", "Sturdy Oak", "Wisdom Oak"],
    "birch": ["Silver Birch", "Graceful Birch", "Morning Birch"],
    "pine": ["Evergreen Pine", "Resilient Pine", "Tall Pine"],
    "maple": ["Autumn Maple", "Crimson Maple", "Sweet Maple"],
    "cherry": ["Blossom Cherry", "Spring Cherry", "Delicate Cherry"],
    "willow": ["Weeping Willow", "Flowing Willow", "Reflective Willow"],
    "cedar": ["Sacred Cedar", "Ancient Cedar", "Strong Cedar"],
    "aspen": ["Quaking Aspen", "Golden Aspen", "Whispering Aspen"],
    "elm": ["Majestic Elm", "Shade Elm", "Noble Elm"],
    "fir": ["Balsam Fir", "Winter Fir", "Fragrant Fir"],
    "spruce": ["Blue Spruce", "Proud Spruce", "Tall Spruce"],
    "cypress": ["Mediterranean Cypress", "Elegant Cypress", "Timeless Cypress"],
    "redwood": ["Giant Redwood", "Ancient Redwood", "Towering Redwood"],
}

RARITY_WEIGHTS = {
    "common": 0.50,      # 50%
    "uncommon": 0.30,    # 30%
    "rare": 0.15,        # 15%
    "epic": 0.04,        # 4%
    "legendary": 0.01,   # 1%
}

def generate_tree(entry_text: str, entry_id: int, themes: list = None, emotions: list = None) -> Dict:
    """
    Generate a tree for a journal entry.
    
    Trees are deterministic based on entry content but appear random.
    Rarity is influenced by entry characteristics (length, themes, etc.).
    
    Args:
        entry_text: The journal entry text
        entry_id: Entry ID
        themes: List of themes from analysis
        emotions: List of emotions from analysis
    
    Returns:
        Dict with tree type, rarity, and display_name
    """
    # Deterministic seed based on entry content and ID
    content_hash = hashlib.md5(f"{entry_id}_{entry_text}".encode()).hexdigest()
    hash_int = int(content_hash[:12], 16)
    
    # Determine rarity (influenced by entry characteristics)
    entry_length = len(entry_text)
    num_themes = len(themes) if themes else 0
    num_emotions = len(emotions) if emotions else 0
    
    # Longer, more analyzed entries have better rarity chances
    rarity_bonus = min(0.2, (entry_length / 1000) + (num_themes * 0.03) + (num_emotions * 0.02))
    
    # Select rarity
    rand = (hash_int % 1000) / 1000.0 + rarity_bonus
    if rand >= 0.99:
        rarity = "legendary"
    elif rand >= 0.95:
        rarity = "epic"
    elif rand >= 0.80:
        rarity = "rare"
    elif rand >= 0.50:
        rarity = "uncommon"
    else:
        rarity = "common"
    
    # Select tree type (deterministic)
    tree_type = TREE_TYPES[hash_int % len(TREE_TYPES)]
    
    # Select display name (deterministic)
    names = TREE_NAMES.get(tree_type, ["Mystery Tree"])
    display_name = names[hash_int % len(names)]
    
    return {
        "type": tree_type,
        "rarity": rarity,
        "display_name": display_name,
    }


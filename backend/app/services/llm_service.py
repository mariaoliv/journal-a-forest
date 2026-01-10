"""
LLM Service for analyzing journal entries.

TODO: Integrate with OpenAI API or similar LLM service.
For now, returns deterministic mock responses based on entry content.
"""

import json
import hashlib
from typing import Dict, List

# TODO: Replace with actual LLM integration
# Example using OpenAI:
# import openai
# openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_entry(entry_text: str, prompt_id: str = None) -> Dict:
    """
    Analyze a journal entry and extract insights.
    
    TODO: Implement actual LLM analysis:
    1. Use OpenAI GPT-4 or similar model
    2. Prompt engineering for:
       - Memory summary (concise, factual)
       - Patterns reflection (observations, not advice)
       - Follow-up question (open-ended, thoughtful)
       - Themes extraction (keywords/concepts)
       - Emotions detection (sentiment analysis)
    3. Store embeddings in Chroma for retrieval
    4. Cache results for consistency
    
    Args:
        entry_text: The journal entry text
        prompt_id: Optional prompt ID that was used
    
    Returns:
        Dict with analysis results
    """
    # Mock implementation: deterministic based on content hash
    content_hash = hashlib.md5(entry_text.encode()).hexdigest()
    hash_int = int(content_hash[:8], 16)
    
    # Mock themes and emotions (deterministic but varied)
    mock_themes = ["reflection", "growth", "challenge"]
    mock_emotions = ["contemplative", "hopeful"]
    
    if hash_int % 3 == 0:
        mock_themes = ["relationships", "connection", "communication"]
        mock_emotions = ["grateful", "warm"]
    elif hash_int % 3 == 1:
        mock_themes = ["work", "productivity", "purpose"]
        mock_emotions = ["focused", "motivated"]
    
    return {
        "memory_summary": f"A thoughtful reflection on {', '.join(mock_themes[:2])}.",
        "patterns_reflection": (
            "I'm noticing you're exploring themes of personal growth and connection. "
            "There's a pattern of thoughtful reflection emerging in your entries."
        ),
        "follow_up_question": "What would it look like to deepen this exploration?",
        "themes": mock_themes,
        "emotions": mock_emotions,
        "unresolved": []
    }

def generate_prompts(entry_text: str, session_history: List[Dict] = None) -> List[Dict]:
    """
    Generate personalized prompts based on entry and history.
    
    TODO: Implement with LLM:
    1. Use conversation history to understand context
    2. Generate prompts that build on previous entries
    3. Vary prompt types (reflective, forward-looking, creative)
    4. Avoid repetition from recent prompts
    
    Args:
        entry_text: Recent entry text
        session_history: List of previous entries/analyses
    
    Returns:
        List of prompt dicts with 'id', 'text', 'category'
    """
    # Mock implementation: return starter prompts
    return [
        {"id": "p1", "text": "What's something you learned about yourself recently?", "category": "reflection"},
        {"id": "p2", "text": "Describe a moment that made you pause today.", "category": "mindfulness"},
        {"id": "p3", "text": "What conversation would you want to have with your future self?", "category": "future"},
        {"id": "p4", "text": "Write about a boundary you're learning to set.", "category": "growth"},
        {"id": "p5", "text": "What does rest look like for you right now?", "category": "wellness"},
        {"id": "p6", "text": "Describe a small moment of joy from this week.", "category": "gratitude"},
    ]

def analyze_brain_dump(brain_dump: str) -> Dict:
    """
    Analyze onboarding brain dump and extract initial insights.
    
    TODO: Implement with LLM to:
    1. Extract key themes, concerns, interests
    2. Generate starter prompts tailored to user
    3. Identify potential threads to explore
    4. Create welcoming, personalized initial tree
    
    Args:
        brain_dump: Initial onboarding text
    
    Returns:
        Dict with starter_prompts, threads, initial_tree
    """
    # Mock implementation
    content_hash = hashlib.md5(brain_dump.encode()).hexdigest()
    
    starter_prompts = [
        {"id": "sp1", "text": "What brings you to journaling right now?", "category": "intention"},
        {"id": "sp2", "text": "Write about what you're hoping to discover.", "category": "exploration"},
        {"id": "sp3", "text": "What's one thing you'd like to understand better about yourself?", "category": "curiosity"},
        {"id": "sp4", "text": "Describe a recent moment that stayed with you.", "category": "reflection"},
        {"id": "sp5", "text": "What feels important to you right now?", "category": "values"},
        {"id": "sp6", "text": "Write freely about whatever comes to mind.", "category": "freeform"},
    ]
    
    threads = []  # Empty for now, could extract from brain dump
    
    initial_tree = {
        "entry_id": 0,  # Special ID for initial tree
        "type": "oak",
        "rarity": "common",
        "display_name": "Seedling of Growth",
    }
    
    return {
        "starter_prompts": starter_prompts,
        "threads": threads,
        "initial_tree": initial_tree,
    }

def generate_weekly_insights(session_id: str, entries: List[Dict]) -> Dict:
    """
    Generate weekly reflection and pattern insights.
    
    TODO: Implement with LLM and Chroma:
    1. Retrieve all entries from past week using Chroma
    2. Use LLM to identify overarching patterns
    3. Generate reflection text (patterns, not advice)
    4. Aggregate themes and emotions
    5. Provide gentle observations about growth
    
    Args:
        session_id: User session
        entries: List of entry dicts with analysis
    
    Returns:
        Dict with patterns_reflection, themes, emotions_summary
    """
    # Mock implementation
    return {
        "patterns_reflection": (
            "This week, you've been exploring themes of growth and reflection. "
            "I notice a pattern of thoughtful engagement with your inner world. "
            "Your entries show increasing depth and self-awareness."
        ),
        "themes": ["growth", "reflection", "mindfulness"],
        "emotions_summary": {
            "contemplative": 3,
            "hopeful": 2,
            "grateful": 1,
        },
    }


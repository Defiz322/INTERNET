"""
Utility functions
"""
import random
import string
from datetime import datetime, timedelta


def generate_id(prefix: str = "") -> str:
    """Generate a unique ID"""
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
    if prefix:
        return f"{prefix}_{random_str}"
    return random_str


def generate_username() -> str:
    """Generate a random username"""
    prefixes = ["ghost", "shadow", "void", "net", "data", "cipher", "null", "echo",
                "photon", "byte", "glow", "dust", "static", "mirror", "lost"]
    suffixes = ["runner", "walker", "keeper", "seeker", "drifter", "haunt", "trace",
                "form", "zone", "node", "flux", "ghost", "mind", "eye", "void"]
    numbers = random.choice(["", "", str(random.randint(00, 999))])
    return f"{random.choice(prefixes)}{random.choice(suffixes)}{numbers}"


def generate_site_name() -> str:
    """Generate a random site name"""
    prefixes = ["archive", "void", "lost", "old", "dark", "ghost", "static", "net"]
    suffixes = ["forum", "log", "hub", "page", "zone", "net", "org", "net"]
    tld = random.choice([".net", ".org", ".tk", ".info", ""])
    return f"{random.choice(prefixes)}-{random.choice(suffixes)}{tld}"


def random_text(min_words: int = 5, max_words: int = 25) -> str:
    """Generate random text content"""
    words = [
        "the", "void", "data", "net", "lost", "old", "time", "user", "site",
        "page", "forum", "message", "ghost", "static", "echo", "memory", "archive",
        "shadow", "digital", "ancient", "forgotten", "hidden", "strange", "weird",
        "empty", "dead", "silent", "broken", "corrupted", "unknown", "mysterious"
    ]
    
    fragments = [
        "something is missing",
        "i remember when...",
        "does anyone else see this?",
        "the logs don't add up",
        "pages keep disappearing",
        "it's all connected",
        "we're not alone here",
        "time feels wrong",
        "i shouldn't be posting this",
        "they're watching"
    ]
    
    if random.random() < 0.3:
        return random.choice(fragments)
    
    length = random.randint(min_words, max_words)
    result = []
    for _ in range(length):
        if random.random() < 0.2:
            result.append(random.choice(fragments).split()[0] + "...")
        else:
            result.append(random.choice(words))
    
    return " ".join(result).capitalize() + "."


def random_time_ago(days_back: int = 365) -> str:
    """Generate a random timestamp string"""
    days = random.randint(1, days_back)
    hours = random.randint(0, 23)
    minutes = random.randint(0, 59)
    dt = datetime.now() - timedelta(days=days, hours=hours, minutes=minutes)
    return dt.strftime("%Y-%m-%d %H:%M:%S")

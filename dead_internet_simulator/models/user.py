"""
User model
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any
from datetime import datetime


@dataclass
class User:
    id: str
    username: str
    bio: str = ""
    trait: str = "curious"
    interests: List[str] = field(default_factory=list)
    reputation: int = 0
    activity_level: float = 0.5
    joined_date: str = ""
    last_active: str = ""
    is_online: bool = False
    is_player: bool = False
    communities: List[str] = field(default_factory=list)
    friends: List[str] = field(default_factory=list)
    enemies: List[str] = field(default_factory=list)
    post_count: int = 0
    mysterious: bool = False
    inactive_since: str = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "username": self.username,
            "bio": self.bio,
            "trait": self.trait,
            "interests": ",".join(self.interests),
            "reputation": self.reputation,
            "activity_level": self.activity_level,
            "joined_date": self.joined_date,
            "last_active": self.last_active,
            "is_online": self.is_online,
            "is_player": self.is_player,
            "communities": ",".join(self.communities),
            "friends": ",".join(self.friends),
            "enemies": ",".join(self.enemies),
            "post_count": self.post_count,
            "mysterious": self.mysterious,
            "inactive_since": self.inactive_since
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "User":
        def parse_list(s):
            if not s or s == "":
                return []
            return s.split(",")
        
        return cls(
            id=data["id"],
            username=data["username"],
            bio=data.get("bio", ""),
            trait=data.get("trait", "curious"),
            interests=parse_list(data.get("interests", "")),
            reputation=data.get("reputation", 0),
            activity_level=data.get("activity_level", 0.5),
            joined_date=data.get("joined_date", ""),
            last_active=data.get("last_active", ""),
            is_online=bool(data.get("is_online", 0)),
            is_player=bool(data.get("is_player", 0)),
            communities=parse_list(data.get("communities", "")),
            friends=parse_list(data.get("friends", "")),
            enemies=parse_list(data.get("enemies", "")),
            post_count=data.get("post_count", 0),
            mysterious=bool(data.get("mysterious", 0)),
            inactive_since=data.get("inactive_since")
        )

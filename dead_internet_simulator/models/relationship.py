"""
Relationship model
"""
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class Relationship:
    id: str
    user1_id: str
    user2_id: str
    type: str = "neutral"  # friend, enemy, neutral, suspicious
    strength: int = 0
    created_date: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "user1_id": self.user1_id,
            "user2_id": self.user2_id,
            "type": self.type,
            "strength": self.strength,
            "created_date": self.created_date
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Relationship":
        return cls(
            id=data["id"],
            user1_id=data["user1_id"],
            user2_id=data["user2_id"],
            type=data.get("type", "neutral"),
            strength=data.get("strength", 0),
            created_date=data.get("created_date", "")
        )

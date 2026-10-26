"""
Community model
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class Community:
    id: str
    name: str
    description: str = ""
    site_id: str = ""
    interests: List[str] = field(default_factory=list)
    members: List[str] = field(default_factory=list)
    created_date: str = ""
    activity: float = 0.5
    reputation: int = 0
    in_conflict: bool = False
    mysterious: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "site_id": self.site_id,
            "interests": ",".join(self.interests),
            "members": ",".join(self.members),
            "created_date": self.created_date,
            "activity": self.activity,
            "reputation": self.reputation,
            "in_conflict": self.in_conflict,
            "mysterious": self.mysterious
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Community":
        def parse_list(s):
            if not s or s == "":
                return []
            return s.split(",")
        
        return cls(
            id=data["id"],
            name=data["name"],
            description=data.get("description", ""),
            site_id=data.get("site_id", ""),
            interests=parse_list(data.get("interests", "")),
            members=parse_list(data.get("members", "")),
            created_date=data.get("created_date", ""),
            activity=data.get("activity", 0.5),
            reputation=data.get("reputation", 0),
            in_conflict=bool(data.get("in_conflict", 0)),
            mysterious=bool(data.get("mysterious", 0))
        )

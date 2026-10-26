"""
Event model
"""
from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class Event:
    id: str
    type: str
    title: str
    description: str
    created_date: str = ""
    affected_users: str = ""
    affected_communities: str = ""
    mysterious: bool = False
    resolved: bool = False
    hidden: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type,
            "title": self.title,
            "description": self.description,
            "created_date": self.created_date,
            "affected_users": self.affected_users,
            "affected_communities": self.affected_communities,
            "mysterious": self.mysterious,
            "resolved": self.resolved,
            "hidden": self.hidden
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Event":
        return cls(
            id=data["id"],
            type=data["type"],
            title=data["title"],
            description=data["description"],
            created_date=data.get("created_date", ""),
            affected_users=data.get("affected_users", ""),
            affected_communities=data.get("affected_communities", ""),
            mysterious=bool(data.get("mysterious", 0)),
            resolved=bool(data.get("resolved", 0)),
            hidden=bool(data.get("hidden", 0))
        )

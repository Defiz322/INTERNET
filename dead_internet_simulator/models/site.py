"""
Site model
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class Site:
    id: str
    name: str
    url: str
    type: str = "forum"
    description: str = ""
    created_date: str = ""
    abandoned: bool = False
    has_mystery: bool = False
    content: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        import json
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "type": self.type,
            "description": self.description,
            "created_date": self.created_date,
            "abandoned": self.abandoned,
            "has_mystery": self.has_mystery,
            "content": json.dumps(self.content)
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Site":
        import json
        content = {}
        if data.get("content"):
            try:
                content = json.loads(data["content"])
            except:
                content = {}
        
        return cls(
            id=data["id"],
            name=data["name"],
            url=data["url"],
            type=data.get("type", "forum"),
            description=data.get("description", ""),
            created_date=data.get("created_date", ""),
            abandoned=bool(data.get("abandoned", 0)),
            has_mystery=bool(data.get("has_mystery", 0)),
            content=content
        )

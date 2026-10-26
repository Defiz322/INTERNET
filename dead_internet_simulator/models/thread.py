"""
Thread model
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class Thread:
    id: str
    title: str
    community_id: str
    author_id: str
    site_id: str = ""
    created_date: str = ""
    last_reply: str = ""
    reply_count: int = 0
    views: int = 0
    sticky: bool = False
    locked: bool = False
    mysterious: bool = False
    deleted: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "community_id": self.community_id,
            "author_id": self.author_id,
            "site_id": self.site_id,
            "created_date": self.created_date,
            "last_reply": self.last_reply,
            "reply_count": self.reply_count,
            "views": self.views,
            "sticky": self.sticky,
            "locked": self.locked,
            "mysterious": self.mysterious,
            "deleted": self.deleted
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Thread":
        return cls(
            id=data["id"],
            title=data["title"],
            community_id=data["community_id"],
            author_id=data["author_id"],
            site_id=data.get("site_id", ""),
            created_date=data.get("created_date", ""),
            last_reply=data.get("last_reply", ""),
            reply_count=data.get("reply_count", 0),
            views=data.get("views", 0),
            sticky=bool(data.get("sticky", 0)),
            locked=bool(data.get("locked", 0)),
            mysterious=bool(data.get("mysterious", 0)),
            deleted=bool(data.get("deleted", 0))
        )

"""
Message model
"""
from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class Message:
    id: str
    thread_id: str
    author_id: str
    content: str
    created_date: str = ""
    reply_to: str = None
    edited: bool = False
    mysterious: bool = False
    deleted: bool = False
    has_hook: bool = False
    hook_data: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "thread_id": self.thread_id,
            "author_id": self.author_id,
            "content": self.content,
            "created_date": self.created_date,
            "reply_to": self.reply_to,
            "edited": self.edited,
            "mysterious": self.mysterious,
            "deleted": self.deleted,
            "has_hook": self.has_hook,
            "hook_data": self.hook_data
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Message":
        return cls(
            id=data["id"],
            thread_id=data["thread_id"],
            author_id=data["author_id"],
            content=data["content"],
            created_date=data.get("created_date", ""),
            reply_to=data.get("reply_to"),
            edited=bool(data.get("edited", 0)),
            mysterious=bool(data.get("mysterious", 0)),
            deleted=bool(data.get("deleted", 0)),
            has_hook=bool(data.get("has_hook", 0)),
            hook_data=data.get("hook_data", "")
        )

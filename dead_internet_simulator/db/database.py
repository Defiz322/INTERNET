"""
Database management for Dead Internet Simulator
"""
import sqlite3
import json
import threading
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

from ..core.config import DB_PATH


class Database:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self._local = threading.local()
        self._lock = threading.Lock()
        self.connect()
        self.create_tables()
    
    def connect(self):
        """Connect to database"""
        if not hasattr(self._local, 'conn') or self._local.conn is None:
            self._local.conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
            self._local.conn.row_factory = sqlite3.Row
            self._local.conn.execute("PRAGMA foreign_keys = ON")
        self.conn = self._local.conn
    
    def _get_conn(self):
        if not hasattr(self._local, 'conn') or self._local.conn is None:
            self._local.conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
            self._local.conn.row_factory = sqlite3.Row
            self._local.conn.execute("PRAGMA foreign_keys = ON")
        return self._local.conn
    
    def create_tables(self):
        """Create all tables"""
        conn = self._get_conn()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                bio TEXT,
                trait TEXT,
                interests TEXT,
                reputation INTEGER DEFAULT 0,
                activity_level REAL DEFAULT 0.5,
                joined_date TEXT,
                last_active TEXT,
                is_online INTEGER DEFAULT 0,
                is_player INTEGER DEFAULT 0,
                communities TEXT,
                friends TEXT,
                enemies TEXT,
                post_count INTEGER DEFAULT 0,
                mysterious INTEGER DEFAULT 0,
                inactive_since TEXT
            )
        """)
        
        # Sites table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sites (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                url TEXT UNIQUE NOT NULL,
                type TEXT,
                description TEXT,
                created_date TEXT,
                abandoned INTEGER DEFAULT 0,
                has_mystery INTEGER DEFAULT 0,
                content TEXT
            )
        """)
        
        # Communities table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS communities (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                site_id TEXT,
                interests TEXT,
                members TEXT,
                created_date TEXT,
                activity REAL DEFAULT 0.5,
                reputation INTEGER DEFAULT 0,
                in_conflict INTEGER DEFAULT 0,
                mysterious INTEGER DEFAULT 0,
                FOREIGN KEY (site_id) REFERENCES sites(id)
            )
        """)
        
        # Threads table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS threads (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                community_id TEXT,
                author_id TEXT,
                site_id TEXT,
                created_date TEXT,
                last_reply TEXT,
                reply_count INTEGER DEFAULT 0,
                views INTEGER DEFAULT 0,
                sticky INTEGER DEFAULT 0,
                locked INTEGER DEFAULT 0,
                mysterious INTEGER DEFAULT 0,
                deleted INTEGER DEFAULT 0,
                FOREIGN KEY (community_id) REFERENCES communities(id),
                FOREIGN KEY (author_id) REFERENCES users(id),
                FOREIGN KEY (site_id) REFERENCES sites(id)
            )
        """)
        
        # Messages table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id TEXT PRIMARY KEY,
                thread_id TEXT,
                author_id TEXT,
                content TEXT NOT NULL,
                created_date TEXT,
                reply_to TEXT,
                edited INTEGER DEFAULT 0,
                mysterious INTEGER DEFAULT 0,
                deleted INTEGER DEFAULT 0,
                has_hook INTEGER DEFAULT 0,
                hook_data TEXT,
                FOREIGN KEY (thread_id) REFERENCES threads(id),
                FOREIGN KEY (author_id) REFERENCES users(id)
            )
        """)
        
        # Events table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id TEXT PRIMARY KEY,
                type TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                created_date TEXT,
                affected_users TEXT,
                affected_communities TEXT,
                mysterious INTEGER DEFAULT 0,
                resolved INTEGER DEFAULT 0,
                hidden INTEGER DEFAULT 0
            )
        """)
        
        # Relationships table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS relationships (
                id TEXT PRIMARY KEY,
                user1_id TEXT,
                user2_id TEXT,
                type TEXT DEFAULT 'neutral',
                strength INTEGER DEFAULT 0,
                created_date TEXT,
                FOREIGN KEY (user1_id) REFERENCES users(id),
                FOREIGN KEY (user2_id) REFERENCES users(id)
            )
        """)
        
        # Plot hooks table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS plot_hooks (
                id TEXT PRIMARY KEY,
                type TEXT,
                description TEXT,
                discovered_by TEXT,
                revealed INTEGER DEFAULT 0,
                data TEXT,
                created_date TEXT
            )
        """)
        
        # Simulation state table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS simulation_state (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)
        
        conn.commit()
    
    def execute(self, query: str, params: tuple = ()):
        with self._lock:
            conn = self._get_conn()
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor
    
    def fetchone(self, query: str, params: tuple = ()):
        with self._lock:
            conn = self._get_conn()
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchone()
    
    def fetchall(self, query: str, params: tuple = ()):
        with self._lock:
            conn = self._get_conn()
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
    
    def save_user(self, user_dict: Dict[str, Any]):
        with self._lock:
            conn = self._get_conn()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO users VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                user_dict["id"], user_dict["username"], user_dict["bio"],
                user_dict["trait"], user_dict["interests"], user_dict["reputation"],
                user_dict["activity_level"], user_dict["joined_date"], user_dict["last_active"],
                user_dict["is_online"], user_dict["is_player"], user_dict["communities"],
                user_dict["friends"], user_dict["enemies"], user_dict["post_count"],
                user_dict["mysterious"], user_dict["inactive_since"]
            ))
            conn.commit()
    
    def save_site(self, site_dict: Dict[str, Any]):
        with self._lock:
            conn = self._get_conn()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO sites VALUES (?,?,?,?,?,?,?,?,?)
            """, (
                site_dict["id"], site_dict["name"], site_dict["url"],
                site_dict["type"], site_dict["description"], site_dict["created_date"],
                site_dict["abandoned"], site_dict["has_mystery"], site_dict["content"]
            ))
            conn.commit()
    
    def save_community(self, community_dict: Dict[str, Any]):
        with self._lock:
            conn = self._get_conn()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO communities VALUES (?,?,?,?,?,?,?,?,?,?,?)
            """, (
                community_dict["id"], community_dict["name"], community_dict["description"],
                community_dict["site_id"], community_dict["interests"], community_dict["members"],
                community_dict["created_date"], community_dict["activity"], community_dict["reputation"],
                community_dict["in_conflict"], community_dict["mysterious"]
            ))
            conn.commit()
    
    def save_thread(self, thread_dict: Dict[str, Any]):
        with self._lock:
            conn = self._get_conn()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO threads VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                thread_dict["id"], thread_dict["title"], thread_dict["community_id"],
                thread_dict["author_id"], thread_dict["site_id"], thread_dict["created_date"],
                thread_dict["last_reply"], thread_dict["reply_count"], thread_dict["views"],
                thread_dict["sticky"], thread_dict["locked"], thread_dict["mysterious"],
                thread_dict["deleted"]
            ))
            conn.commit()
    
    def save_message(self, message_dict: Dict[str, Any]):
        with self._lock:
            conn = self._get_conn()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO messages VALUES (?,?,?,?,?,?,?,?,?,?,?)
            """, (
                message_dict["id"], message_dict["thread_id"], message_dict["author_id"],
                message_dict["content"], message_dict["created_date"], message_dict["reply_to"],
                message_dict["edited"], message_dict["mysterious"], message_dict["deleted"],
                message_dict["has_hook"], message_dict["hook_data"]
            ))
            conn.commit()
    
    def save_event(self, event_dict: Dict[str, Any]):
        with self._lock:
            conn = self._get_conn()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO events VALUES (?,?,?,?,?,?,?,?,?,?)
            """, (
                event_dict["id"], event_dict["type"], event_dict["title"],
                event_dict["description"], event_dict["created_date"],
                event_dict["affected_users"], event_dict["affected_communities"],
                event_dict["mysterious"], event_dict["resolved"], event_dict["hidden"]
            ))
            conn.commit()
    
    def save_relationship(self, relationship_dict: Dict[str, Any]):
        with self._lock:
            conn = self._get_conn()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO relationships VALUES (?,?,?,?,?,?)
            """, (
                relationship_dict["id"], relationship_dict["user1_id"], relationship_dict["user2_id"],
                relationship_dict["type"], relationship_dict["strength"], relationship_dict["created_date"]
            ))
            conn.commit()
    
    def get_all_users(self):
        return self.fetchall("SELECT * FROM users")
    
    def get_all_sites(self):
        return self.fetchall("SELECT * FROM sites")
    
    def get_all_communities(self):
        return self.fetchall("SELECT * FROM communities")
    
    def get_all_threads(self):
        return self.fetchall("SELECT * FROM threads WHERE deleted = 0")
    
    def get_all_messages(self):
        return self.fetchall("SELECT * FROM messages WHERE deleted = 0")
    
    def get_all_events(self):
        return self.fetchall("SELECT * FROM events WHERE hidden = 0 ORDER BY created_date DESC")
    
    def get_sim_state(self, key: str) -> Optional[str]:
        row = self.fetchone("SELECT value FROM simulation_state WHERE key = ?", (key,))
        if row:
            return row[0]
        return None
    
    def set_sim_state(self, key: str, value: str):
        self.execute("INSERT OR REPLACE INTO simulation_state VALUES (?,?)", (key, value))
    
    def clear_all(self):
        """Clear all data for reset"""
        with self._lock:
            conn = self._get_conn()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM messages")
            cursor.execute("DELETE FROM threads")
            cursor.execute("DELETE FROM relationships")
            cursor.execute("DELETE FROM events")
            cursor.execute("DELETE FROM plot_hooks")
            cursor.execute("DELETE FROM communities")
            cursor.execute("DELETE FROM sites")
            cursor.execute("DELETE FROM users")
            cursor.execute("DELETE FROM simulation_state")
            conn.commit()
    
    def close(self):
        try:
            if hasattr(self._local, 'conn') and self._local.conn:
                self._local.conn.close()
                self._local.conn = None
        except:
            pass

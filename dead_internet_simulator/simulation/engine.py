"""
Simulation engine for autonomous behavior
"""
import random
from datetime import datetime
from ..core.utils import generate_id, random_text, random_time_ago
from ..core.config import TRAITS, INTERESTS


class SimulationEngine:
    def __init__(self, db):
        self.db = db
        self.running = False
        self.paused = False
        self.speed = 1.0
        self.tick_count = 0
    
    def start(self):
        self.running = True
        self.paused = False
    
    def pause(self):
        self.paused = True
    
    def resume(self):
        self.paused = False
    
    def set_speed(self, speed):
        self.speed = max(0.1, min(10.0, float(speed)))
    
    def tick(self):
        """Perform one simulation tick"""
        if not self.running or self.paused:
            return
        
        self.tick_count += 1
        
        # Get all users and communities
        try:
            users = self.db.get_all_users()
            communities = self.db.get_all_communities()
            threads = self.db.get_all_threads()
            
            if not users or not communities:
                return
            
            # Random chance for various events
            # User activity
            if random.random() < 0.4 * self.speed:
                self._simulate_user_activity(users, communities, threads)
            
            # Community events
            if random.random() < 0.3 * self.speed:
                self._simulate_community_events(communities)
            
            # Mysterious events
            if random.random() < 0.25 * self.speed:
                self._generate_mysterious_event(users, communities)
            
            # Update simulation time
            game_time = self.db.get_sim_state("game_time")
            if game_time:
                new_time = int(game_time) + int(self.speed)
                self.db.set_sim_state("game_time", str(new_time))
        except Exception as e:
            print(f"Tick error: {e}")
            pass
    
    def _simulate_user_activity(self, users, communities, threads):
        """Simulate a user performing an action"""
        try:
            active_users = [u for u in users if u[11] == 0]  # not player
            if not active_users:
                return
            
            user_row = random.choice(active_users)
            user_id = user_row[0]
            trait = user_row[3] if len(user_row) > 3 else 'curious'
            activity = user_row[6] if len(user_row) > 6 else 0.5
            
            if random.random() > float(activity):
                return
            
            action = self._choose_action(trait)
            
            if action == "create_thread" and communities:
                self._create_thread(user_id, communities)
            elif action == "reply" and threads:
                self._create_reply(user_id, threads)
            elif action == "spread_rumor":
                self._spread_rumor(user_id, users)
            elif action == "mysterious_post" and threads:
                self._create_mysterious_post(user_id, threads)
        except Exception as e:
            print(f"User activity error: {e}")
            pass
    
    def _choose_action(self, trait):
        """Choose action based on trait"""
        weights = {
            "create_thread": 0.2,
            "reply": 0.4,
            "spread_rumor": 0.1,
            "mysterious_post": 0.05,
            "support": 0.15,
            "argue": 0.1
        }
        
        # Adjust based on trait
        if trait == "outspoken":
            weights["create_thread"] += 0.1
            weights["argue"] += 0.1
        elif trait == "passive":
            weights["reply"] += 0.1
            weights["support"] += 0.1
        elif trait == "conspiratorial":
            weights["spread_rumor"] += 0.2
            weights["mysterious_post"] += 0.15
        elif trait == "secretive":
            weights["mysterious_post"] += 0.1
        
        actions = list(weights.keys())
        probs = list(weights.values())
        return random.choices(actions, weights=probs)[0]
    
    def _create_thread(self, user_id, communities):
        """Create a new thread"""
        try:
            if not communities:
                return
            community = random.choice(communities)
            comm_row = community
            comm_id = comm_row[0]
            site_id = comm_row[3] if len(comm_row) > 3 else ""
            
            titles = [
                "Something strange happened today",
                "Does this look familiar to anyone?",
                "I need to tell someone about this",
                "Warning about something I found",
                "New discovery in the archive",
                "Questions about an old page",
                "Am I going crazy or...",
                "Strange pattern noticed",
            ]
            
            thread_data = {
                "id": generate_id("thread"),
                "title": random.choice(titles),
                "community_id": comm_id,
                "author_id": user_id,
                "site_id": site_id,
                "created_date": random_time_ago(0),
                "last_reply": random_time_ago(0),
                "reply_count": 0,
                "views": 1,
                "sticky": 0,
                "locked": 0,
                "mysterious": 1 if random.random() < 0.3 else 0,
                "deleted": 0
            }
            self.db.save_thread(thread_data)
            
            # Create initial message
            msg_data = {
                "id": generate_id("msg"),
                "thread_id": thread_data["id"],
                "author_id": user_id,
                "content": random_text(10, 35),
                "created_date": random_time_ago(0),
                "reply_to": None,
                "edited": 0,
                "mysterious": thread_data["mysterious"],
                "deleted": 0,
                "has_hook": 1 if random.random() < 0.4 else 0,
                "hook_data": ""
            }
            self.db.save_message(msg_data)
        except Exception as e:
            print(f"Create thread error: {e}")
            pass
    
    def _create_reply(self, user_id, threads):
        """Create a reply to a thread"""
        try:
            if not threads:
                return
            thread = random.choice(threads)
            thread_id = thread[0]
            mysterious = thread[11] if len(thread) > 11 else 0
            
            msg_data = {
                "id": generate_id("msg"),
                "thread_id": thread_id,
                "author_id": user_id,
                "content": random_text(5, 25),
                "created_date": random_time_ago(0),
                "reply_to": None,
                "edited": 0,
                "mysterious": 1 if mysterious and random.random() < 0.3 else 0,
                "deleted": 0,
                "has_hook": 1 if random.random() < 0.2 else 0,
                "hook_data": ""
            }
            self.db.save_message(msg_data)
        except Exception as e:
            print(f"Create reply error: {e}")
            pass
    
    def _create_mysterious_post(self, user_id, threads):
        """Create a mysterious post"""
        try:
            if not threads:
                return
            thread = random.choice(threads)
            mysterious_contents = [
                "i shouldn't be telling you this but...",
                "they're deleting everything. look quickly.",
                "the pattern repeats every 7 days",
                "account [REDACTED] knows more than they say",
                "check the archive from 1997",
                "i can only post this once",
                "don't trust the timestamps"
            ]
            
            msg_data = {
                "id": generate_id("msg"),
                "thread_id": thread[0],
                "author_id": user_id,
                "content": random.choice(mysterious_contents),
                "created_date": random_time_ago(0),
                "reply_to": None,
                "edited": 0,
                "mysterious": 1,
                "deleted": 0,
                "has_hook": 1,
                "hook_data": "mystery"
            }
            self.db.save_message(msg_data)
        except Exception as e:
            print(f"Mysterious post error: {e}")
            pass
    
    def _spread_rumor(self, user_id, users):
        """Spread a rumor"""
        try:
            event_data = {
                "id": generate_id("event"),
                "type": "rumor",
                "title": "Whispers in the Void",
                "description": random.choice([
                    "A rumor is spreading about deleted pages returning.",
                    "Users whisper about accounts that post from the past.",
                    "Talk of a hidden section of the archive grows.",
                    "Speculation about who controls the void intensifies.",
                ]),
                "created_date": random_time_ago(0),
                "affected_users": user_id,
                "affected_communities": "",
                "mysterious": 1,
                "resolved": 0,
                "hidden": 0
            }
            self.db.save_event(event_data)
        except Exception as e:
            print(f"Spread rumor error: {e}")
            pass
    
    def _simulate_community_events(self, communities):
        """Simulate community-level events"""
        try:
            if not communities or len(communities) == 0:
                return
            
            community = random.choice(communities)
            event_data = {
                "id": generate_id("event"),
                "type": "community",
                "title": "Community Activity Shift",
                "description": random.choice([
                    "Activity in this community has increased mysteriously.",
                    "Tensions rise as old grudges resurface.",
                    "New members with no history appear.",
                    "The community seems to be fracturing.",
                ]),
                "created_date": random_time_ago(0),
                "affected_users": "",
                "affected_communities": community[0] if len(community) > 0 else "",
                "mysterious": 1 if random.random() < 0.5 else 0,
                "resolved": 0,
                "hidden": 0
            }
            self.db.save_event(event_data)
        except Exception as e:
            print(f"Community event error: {e}")
            pass
    
    def _generate_mysterious_event(self, users, communities):
        """Generate mysterious events"""
        try:
            event_types = [
                ("anomaly", "Temporal Anomaly", 
                 "Messages are appearing with timestamps from impossible dates."),
                ("disappearance", "Mass Silence", 
                 "Several users have gone completely silent at the same time."),
                ("mystery", "The Pattern", 
                 "A numerical pattern has appeared in posts across multiple communities."),
                ("haunting", "Digital Echoes", 
                 "Old deleted posts are being quoted as if they never disappeared."),
            ]
            
            etype, title, desc = random.choice(event_types)
            affected_users = ""
            affected_comms = ""
            try:
                if users and len(users) > 0:
                    max_c = min(3, len(users))
                    if max_c >= 1:
                        count = random.randint(1, max_c)
                        if count >= 1 and count <= len(users):
                            sampled = random.sample(list(users), count)
                            affected_users = ",".join([u[0] for u in sampled])
            except Exception as e:
                pass
            try:
                if communities and len(communities) > 0:
                    max_c = min(2, len(communities))
                    if max_c >= 1:
                        count = random.randint(1, max_c)
                        if count >= 1 and count <= len(communities):
                            sampled = random.sample(list(communities), count)
                            affected_comms = ",".join([c[0] for c in sampled])
            except Exception as e:
                pass
            
            event_data = {
                "id": generate_id("event"),
                "type": etype,
                "title": title,
                "description": desc,
                "created_date": random_time_ago(0),
                "affected_users": affected_users,
                "affected_communities": affected_comms,
                "mysterious": 1,
                "resolved": 0,
                "hidden": 0
            }
            self.db.save_event(event_data)
        except Exception as e:
            print(f"Mysterious event error: {e}")
            pass

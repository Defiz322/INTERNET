"""
World generation for initial setup
"""
import random
from datetime import datetime, timedelta
from ..core.utils import generate_id, generate_username, generate_site_name, random_text, random_time_ago
from ..core.config import TRAITS, INTERESTS, SITE_TYPES
from ..models import User, Site, Community, Thread, Message


class WorldGenerator:
    def __init__(self, db):
        self.db = db
    
    def is_first_run(self) -> bool:
        """Check if this is first run"""
        users = self.db.get_all_users()
        return len(users) == 0
    
    def generate_initial_world(self):
        """Generate initial world state"""
        print("Generating initial world...")
        
        # Create sites
        sites = self._generate_sites()
        for site in sites:
            self.db.save_site(site.to_dict())
        
        # Create users
        users = self._generate_users(25)
        for user in users:
            self.db.save_user(user.to_dict())
        
        # Create communities
        communities = self._generate_communities(sites, users)
        for community in communities:
            self.db.save_community(community.to_dict())
        
        # Create initial threads and messages
        threads = self._generate_threads(communities, users)
        for thread in threads:
            self.db.save_thread(thread.to_dict())
        
        messages = self._generate_messages(threads, users)
        for message in messages:
            self.db.save_message(message.to_dict())
        
        # Create initial events
        self._generate_initial_events(users, communities)
        
        # Set simulation state
        self.db.set_sim_state("initialized", "true")
        self.db.set_sim_state("game_time", str(random.randint(100, 500)))
        self.db.set_sim_state("sim_speed", "1.0")
        self.db.set_sim_state("paused", "false")
        
        print("World generation complete!")
    
    def _generate_sites(self):
        sites = []
        site_names = [
            ("lost-archive.net", "The Lost Archive", "forum", "An archive of forgotten web pages and discussions."),
            ("voidzone.org", "VoidZone", "imageboard", "A quiet imageboard where strange things are posted."),
            ("shadowlog.net", "ShadowLog", "blog", "Personal logs from those who remember the old internet."),
            ("necromancy.forum", "NetCrypt", "forum", "Discussions about digital archaeology and lost media."),
            ("staticvoid.tk", "Static Void", "cryptic page", "An empty page that shouldn't exist."),
            ("echochamber.org", "Echo Chamber", "forum", "Where echoes of old conversations linger."),
            ("dataremnant.net", "Data Remnant", "archive", "Fragments of data that refuse to be deleted."),
        ]
        
        for url, name, stype, desc in site_names:
            site = Site(
                id=generate_id("site"),
                name=name,
                url=url,
                type=stype,
                description=desc,
                created_date=random_time_ago(2000),
                abandoned=random.random() < 0.6,
                has_mystery=random.random() < 0.4,
                content={}
            )
            sites.append(site)
        return sites
    
    def _generate_users(self, count: int):
        users = []
        for i in range(count):
            username = generate_username()
            trait = random.choice(TRAITS)
            interests = random.sample(INTERESTS, min(random.randint(2, 4), len(INTERESTS)))
            bio_templates = [
                "I remember when the internet was different.",
                "Just a wanderer in the digital void.",
                "Searching for something lost.",
                "Logging the things that shouldn't be remembered.",
                "Here for the strange and forgotten.",
                "Collecting digital ghosts.",
                "I saw it before it was gone.",
                f"Interested in {interests[0]}.",
            ]
            
            user = User(
                id=generate_id("user"),
                username=username,
                bio=random.choice(bio_templates),
                trait=trait,
                interests=interests,
                reputation=random.randint(-10, 50),
                activity_level=random.uniform(0.2, 0.9),
                joined_date=random_time_ago(1500),
                last_active=random_time_ago(30),
                is_online=random.random() < 0.3,
                is_player=False,
                post_count=random.randint(0, 200),
                mysterious=random.random() < 0.15
            )
            users.append(user)
        return users
    
    def _generate_communities(self, sites, users):
        communities = []
        comm_names = [
            ("The Archivists", "Preserving lost data and forgotten pages."),
            ("Void Seekers", "Those who search the digital void for answers."),
            ("Net Ghosts", "Haunted by memories of the old web."),
            ("Static Collective", "Drawn to broken things and corrupted data."),
            ("Echo Group", "We hear things others don't."),
            ("Data Remnants", "What remains when everything is deleted."),
            ("Conspiracy Node", "Connecting the dots that shouldn't connect."),
        ]
        
        for name, desc in comm_names:
            site = random.choice(sites)
            member_count = min(random.randint(3, 10), len(users))
            members = random.sample([u.id for u in users], member_count) if users else []
            comm = Community(
                id=generate_id("comm"),
                name=name,
                description=desc,
                site_id=site.id,
                interests=random.sample(INTERESTS, min(random.randint(2, 3), len(INTERESTS))),
                members=members,
                created_date=random_time_ago(1000),
                activity=random.uniform(0.3, 0.8),
                reputation=random.randint(0, 100),
                in_conflict=random.random() < 0.2,
                mysterious=random.random() < 0.3
            )
            communities.append(comm)
        return communities
    
    def _generate_threads(self, communities, users):
        threads = []
        thread_titles = [
            "Does anyone remember this site?",
            "Something's wrong with the archive",
            "Strange messages appearing again",
            "The void is getting bigger",
            "Old accounts are coming back",
            "Pages from 2003 just vanished",
            "I found something I shouldn't have",
            "Are we being watched?",
            "The numbers don't make sense",
            "They keep deleting my posts",
            "What happened to user_ghost?",
            "Corrupted files in the backup",
            "I keep seeing the same image",
            "The timeline is broken",
            "Who else remembers Geocities?",
        ]
        
        for _ in range(30):
            community = random.choice(communities)
            author = random.choice([u for u in users if u.id in community.members])
            thread = Thread(
                id=generate_id("thread"),
                title=random.choice(thread_titles),
                community_id=community.id,
                author_id=author.id,
                site_id=community.site_id,
                created_date=random_time_ago(500),
                last_reply=random_time_ago(100),
                reply_count=random.randint(0, 25),
                views=random.randint(10, 500),
                sticky=random.random() < 0.1,
                locked=random.random() < 0.05,
                mysterious=random.random() < 0.25,
                deleted=False
            )
            threads.append(thread)
        return threads
    
    def _generate_messages(self, threads, users):
        messages = []
        for thread in threads:
            # Create original post
            author = next((u for u in users if u.id == thread.author_id), random.choice(users) if users else None)
            if not author:
                continue
            op_content = random_text(15, 40)
            if thread.mysterious or random.random() < 0.2:
                op_content = random.choice([
                    "i've been seeing this for years now. no one else ever mentions it.",
                    "the page exists only at 3 AM. i've tested this.",
                    "i shouldn't post this but someone needs to know.",
                    "every time i try to save it, the file becomes corrupted.",
                    "there's a pattern. connect the usernames."
                ])
            
            op = Message(
                id=generate_id("msg"),
                thread_id=thread.id,
                author_id=author.id,
                content=op_content,
                created_date=thread.created_date,
                mysterious=thread.mysterious,
                has_hook=random.random() < 0.3
            )
            messages.append(op)
            
            # Create replies
            reply_count = min(thread.reply_count, 10)  # Limit to avoid issues
            for i in range(reply_count):
                if not users:
                    break
                replier = random.choice(users)
                reply = Message(
                    id=generate_id("msg"),
                    thread_id=thread.id,
                    author_id=replier.id,
                    content=random_text(5, 30),
                    created_date=random_time_ago(50),
                    reply_to=op.id if random.random() < 0.3 else None,
                    mysterious=random.random() < 0.15,
                    has_hook=random.random() < 0.2
                )
                messages.append(reply)
        return messages
    
    def _generate_initial_events(self, users, communities):
        events = [
            ("mystery", "Old Account Resurfaces", 
             "An account that hasn't been seen in years suddenly posted in multiple forums."),
            ("anomaly", "Pages Vanishing", 
             "Several archived pages have disappeared from the Lost Archive overnight."),
            ("rumor", "The Pattern Spreads", 
             "Users in different communities are mentioning the same strange sequence of numbers."),
            ("disappearance", "User Goes Silent", 
             "A longtime member of Net Ghosts hasn't been seen in a week, unusual for them."),
        ]
        
        for etype, title, desc in events:
            affected_users = ""
            affected_comms = ""
            if users:
                try:
                    count = min(2, len(users))
                    affected_users = ",".join([u.id for u in random.sample(users, count)])
                except:
                    pass
            if communities:
                try:
                    count = min(1, len(communities))
                    affected_comms = ",".join([c.id for c in random.sample(communities, count)])
                except:
                    pass
            event_data = {
                "id": generate_id("event"),
                "type": etype,
                "title": title,
                "description": desc,
                "created_date": random_time_ago(20),
                "affected_users": affected_users,
                "affected_communities": affected_comms,
                "mysterious": 1,
                "resolved": 0,
                "hidden": 0
            }
            self.db.save_event(event_data)

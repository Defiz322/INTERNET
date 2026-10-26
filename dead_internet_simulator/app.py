"""
Main application class
"""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import threading
import time
import random
from datetime import datetime

from .core.config import COLORS, FONT_MONO, FONT_MONO_SMALL, FONT_MONO_LARGE, FONT_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT, MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT
from .db.database import Database
from .generators.world_gen import WorldGenerator
from .simulation.engine import SimulationEngine


class DeadInternetApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("DEAD INTERNET SIMULATOR")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.minsize(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)
        self.root.configure(bg=COLORS["bg_primary"])
        
        # Database and simulation
        self.db = Database()
        self.world_gen = WorldGenerator(self.db)
        self.sim_engine = SimulationEngine(self.db)
        
        # Player info
        self.player_id = None
        
        # Check if first run
        if self.world_gen.is_first_run():
            self.world_gen.generate_initial_world()
            self.sim_engine.start()
        else:
            self.sim_engine.start()
        
        # UI elements
        self.notebook = None
        self.status_bar = None
        self.game_time_label = None
        self.sim_speed_var = tk.StringVar(value="1.0")
        
        self.setup_ui()
        self.start_simulation_loop()
    
    def setup_ui(self):
        """Setup the main UI"""
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure styles
        style.configure("Dark.TFrame", background=COLORS["bg_primary"])
        style.configure("Dark.TNotebook", background=COLORS["bg_primary"], borderwidth=0)
        style.configure("Dark.TNotebook.Tab", 
                       background=COLORS["bg_secondary"],
                       foreground=COLORS["text_primary"],
                       padding=[20, 8],
                       font=FONT_MONO)
        style.map("Dark.TNotebook.Tab",
                 background=[("selected", COLORS["bg_tertiary"])],
                 foreground=[("selected", COLORS["text_accent"])])
        
        style.configure("Dark.TLabel", 
                       background=COLORS["bg_primary"],
                       foreground=COLORS["text_primary"],
                       font=FONT_MONO)
        style.configure("Title.TLabel",
                       background=COLORS["bg_primary"],
                       foreground=COLORS["text_accent"],
                       font=FONT_TITLE)
        style.configure("Subtitle.TLabel",
                       background=COLORS["bg_primary"],
                       foreground=COLORS["text_secondary"],
                       font=FONT_MONO)
        
        # Main container
        main_frame = ttk.Frame(self.root, style="Dark.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Title
        title_frame = ttk.Frame(main_frame, style="Dark.TFrame")
        title_frame.pack(fill=tk.X, pady=(0, 5))
        title_label = ttk.Label(title_frame, text=">> DEAD INTERNET SIMULATOR <<", style="Title.TLabel")
        title_label.pack()
        subtitle_label = ttk.Label(title_frame, text="[ABANDONED NETWORK - LIVING IN THE VOID]", style="Subtitle.TLabel")
        subtitle_label.pack()
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(main_frame, style="Dark.TNotebook")
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.create_home_tab()
        self.create_browser_tab()
        self.create_forums_tab()
        self.create_users_tab()
        self.create_communities_tab()
        self.create_archive_tab()
        self.create_events_tab()
        self.create_settings_tab()
        
        # Status bar
        self.status_bar = tk.Frame(main_frame, bg=COLORS["bg_secondary"], height=25)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        self.status_bar.pack_propagate(False)
        
        self.game_time_label = tk.Label(self.status_bar, 
                                       text="TIME: 0000", 
                                       bg=COLORS["bg_secondary"],
                                       fg=COLORS["text_accent"],
                                       font=FONT_MONO_SMALL)
        self.game_time_label.pack(side=tk.LEFT, padx=10)
        
        status_label = tk.Label(self.status_bar,
                               text="| SIMULATION ACTIVE |",
                               bg=COLORS["bg_secondary"],
                               fg=COLORS["text_secondary"],
                               font=FONT_MONO_SMALL)
        status_label.pack(side=tk.LEFT)
        
        # Player button
        player_btn = tk.Button(self.status_bar,
                              text="[CREATE/VIEW PLAYER]",
                              bg=COLORS["bg_tertiary"],
                              fg=COLORS["text_link"],
                              font=FONT_MONO_SMALL,
                              borderwidth=1,
                              relief=tk.FLAT,
                              command=self.create_or_view_player)
        player_btn.pack(side=tk.RIGHT, padx=10)
    
    def create_home_tab(self):
        frame = ttk.Frame(self.notebook, style="Dark.TFrame")
        self.notebook.add(frame, text="HOME")
        
        # Main content
        content = tk.Frame(frame, bg=COLORS["bg_primary"])
        content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Summary section
        summary_frame = tk.LabelFrame(content, 
                                     text="INTERNET STATUS",
                                     bg=COLORS["bg_primary"],
                                     fg=COLORS["text_accent"],
                                     font=FONT_MONO,
                                     bd=1,
                                     relief=tk.SOLID)
        summary_frame.pack(fill=tk.X, pady=(0, 10))
        
        summary_text = tk.Text(summary_frame,
                              height=6,
                              bg=COLORS["bg_secondary"],
                              fg=COLORS["text_primary"],
                              font=FONT_MONO_SMALL,
                              wrap=tk.WORD,
                              bd=0)
        summary_text.pack(fill=tk.X, padx=5, pady=5)
        summary_text.insert(tk.END, 
            ">> NETWORK SCAN COMPLETE\n"
            ">> STATUS: ABANDONED BUT ACTIVE\n"
            ">> LIFEFORMS DETECTED: UNKNOWN\n"
            ">> MYSTERY LEVEL: ELEVATED\n"
            ">> TIME FLOW: IRREGULAR\n"
            ">> SUGGESTION: EXPLORE CAREFULLY\n")
        summary_text.config(state=tk.DISABLED)
        
        # Recent events
        events_frame = tk.LabelFrame(content,
                                   text="RECENT EVENTS",
                                   bg=COLORS["bg_primary"],
                                   fg=COLORS["text_accent"],
                                   font=FONT_MONO,
                                   bd=1,
                                   relief=tk.SOLID)
        events_frame.pack(fill=tk.BOTH, expand=True)
        
        self.home_events_list = tk.Listbox(events_frame,
                                          bg=COLORS["bg_secondary"],
                                          fg=COLORS["text_primary"],
                                          font=FONT_MONO_SMALL,
                                          selectbackground=COLORS["bg_hover"],
                                          selectforeground=COLORS["text_accent"],
                                          bd=0,
                                          height=15)
        self.home_events_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.refresh_home_events()
        
        btn_frame = tk.Frame(events_frame, bg=COLORS["bg_primary"])
        btn_frame.pack(fill=tk.X, padx=5, pady=(0, 5))
        refresh_btn = tk.Button(btn_frame,
                               text="[REFRESH]",
                               bg=COLORS["bg_tertiary"],
                               fg=COLORS["text_primary"],
                               font=FONT_MONO_SMALL,
                               borderwidth=1,
                               relief=tk.FLAT,
                               command=self.refresh_home_events)
        refresh_btn.pack(side=tk.RIGHT)
    
    def refresh_home_events(self):
        self.home_events_list.delete(0, tk.END)
        events = self.db.get_all_events()
        for event in events[:10]:
            self.home_events_list.insert(tk.END, f"[{event[1].upper()}] {event[2]}")
    
    def create_browser_tab(self):
        frame = ttk.Frame(self.notebook, style="Dark.TFrame")
        self.notebook.add(frame, text="BROWSER")
        
        content = tk.Frame(frame, bg=COLORS["bg_primary"])
        content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Sites list
        sites_frame = tk.LabelFrame(content,
                                  text="DISCOVERED SITES",
                                  bg=COLORS["bg_primary"],
                                  fg=COLORS["text_accent"],
                                  font=FONT_MONO,
                                  bd=1,
                                  relief=tk.SOLID)
        sites_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview for sites
        columns = ("name", "url", "type", "status")
        self.sites_tree = ttk.Treeview(sites_frame, columns=columns, show="headings", height=15)
        
        self.sites_tree.heading("name", text="SITE NAME")
        self.sites_tree.heading("url", text="ADDRESS")
        self.sites_tree.heading("type", text="TYPE")
        self.sites_tree.heading("status", text="STATUS")
        
        self.sites_tree.column("name", width=200)
        self.sites_tree.column("url", width=200)
        self.sites_tree.column("type", width=100)
        self.sites_tree.column("status", width=100)
        
        style = ttk.Style()
        style.configure("Treeview",
                       background=COLORS["bg_secondary"],
                       foreground=COLORS["text_primary"],
                       fieldbackground=COLORS["bg_secondary"],
                       font=FONT_MONO_SMALL)
        style.configure("Treeview.Heading",
                       background=COLORS["bg_tertiary"],
                       foreground=COLORS["text_accent"],
                       font=FONT_MONO_SMALL)
        style.map('Treeview', background=[('selected', COLORS["bg_hover"])])
        
        self.sites_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.refresh_sites()
        
        btn_frame = tk.Frame(sites_frame, bg=COLORS["bg_primary"])
        btn_frame.pack(fill=tk.X, padx=5, pady=(0, 5))
        
        open_btn = tk.Button(btn_frame,
                            text="[OPEN SITE]",
                            bg=COLORS["bg_tertiary"],
                            fg=COLORS["text_primary"],
                            font=FONT_MONO_SMALL,
                            borderwidth=1,
                            relief=tk.FLAT,
                            command=self.open_site)
        open_btn.pack(side=tk.LEFT)
        
        refresh_btn = tk.Button(btn_frame,
                               text="[REFRESH]",
                               bg=COLORS["bg_tertiary"],
                               fg=COLORS["text_primary"],
                               font=FONT_MONO_SMALL,
                               borderwidth=1,
                               relief=tk.FLAT,
                               command=self.refresh_sites)
        refresh_btn.pack(side=tk.LEFT, padx=5)
    
    def refresh_sites(self):
        for item in self.sites_tree.get_children():
            self.sites_tree.delete(item)
        sites = self.db.get_all_sites()
        for site in sites:
            status = "ABANDONED" if site[6] else "ACTIVE"
            if site[7]:
                status += " [MYSTERY]"
            self.sites_tree.insert("", tk.END, values=(site[1], site[2], site[3], status))
    
    def open_site(self):
        selection = self.sites_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Select a site to open.")
            return
        item = self.sites_tree.item(selection[0])
        values = item['values']
        messagebox.showinfo("Site Viewer", f"Opening {values[0]} ({values[1]})\n\nType: {values[2]}\nStatus: {values[3]}\n\n[Site content would be displayed here in a full implementation]")
    
    def create_forums_tab(self):
        frame = ttk.Frame(self.notebook, style="Dark.TFrame")
        self.notebook.add(frame, text="FORUMS")
        
        content = tk.Frame(frame, bg=COLORS["bg_primary"])
        content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Threads list
        threads_frame = tk.LabelFrame(content,
                                    text="DISCUSSION THREADS",
                                    bg=COLORS["bg_primary"],
                                    fg=COLORS["text_accent"],
                                    font=FONT_MONO,
                                    bd=1,
                                    relief=tk.SOLID)
        threads_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("title", "replies", "mystery")
        self.threads_tree = ttk.Treeview(threads_frame, columns=columns, show="headings", height=15)
        
        self.threads_tree.heading("title", text="THREAD TITLE")
        self.threads_tree.heading("replies", text="REPLIES")
        self.threads_tree.heading("mystery", text="STATUS")
        
        self.threads_tree.column("title", width=400)
        self.threads_tree.column("replies", width=100)
        self.threads_tree.column("mystery", width=100)
        
        self.threads_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.refresh_threads()
        
        btn_frame = tk.Frame(threads_frame, bg=COLORS["bg_primary"])
        btn_frame.pack(fill=tk.X, padx=5, pady=(0, 5))
        
        view_btn = tk.Button(btn_frame,
                            text="[VIEW THREAD]",
                            bg=COLORS["bg_tertiary"],
                            fg=COLORS["text_primary"],
                            font=FONT_MONO_SMALL,
                            borderwidth=1,
                            relief=tk.FLAT,
                            command=self.view_thread)
        view_btn.pack(side=tk.LEFT)
        
        new_btn = tk.Button(btn_frame,
                           text="[NEW THREAD]",
                           bg=COLORS["bg_tertiary"],
                           fg=COLORS["text_primary"],
                           font=FONT_MONO_SMALL,
                           borderwidth=1,
                           relief=tk.FLAT,
                           command=self.new_thread)
        new_btn.pack(side=tk.LEFT, padx=5)
        
        refresh_btn = tk.Button(btn_frame,
                               text="[REFRESH]",
                               bg=COLORS["bg_tertiary"],
                               fg=COLORS["text_primary"],
                               font=FONT_MONO_SMALL,
                               borderwidth=1,
                               relief=tk.FLAT,
                               command=self.refresh_threads)
        refresh_btn.pack(side=tk.LEFT)
    
    def refresh_threads(self):
        for item in self.threads_tree.get_children():
            self.threads_tree.delete(item)
        threads = self.db.get_all_threads()
        for thread in threads:
            mystery = "MYSTERIOUS" if thread[11] else "NORMAL"
            self.threads_tree.insert("", tk.END, values=(thread[1], thread[7], mystery))
    
    def view_thread(self):
        selection = self.threads_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Select a thread to view.")
            return
        threads = self.db.get_all_threads()
        idx = self.threads_tree.index(selection[0])
        if idx >= len(threads):
            return
        thread = threads[idx]
        thread_id = thread[0]
        title = thread[1]
        
        # Get messages
        messages = []
        for msg in self.db.get_all_messages():
            if msg[1] == thread_id:
                messages.append(msg)
        
        # Create window
        win = tk.Toplevel(self.root)
        win.title(f"Thread: {title}")
        win.geometry("700x500")
        win.configure(bg=COLORS["bg_primary"])
        
        title_label = tk.Label(win, text=f">> {title}", bg=COLORS["bg_primary"], fg=COLORS["text_accent"], font=FONT_TITLE, wraplength=650)
        title_label.pack(padx=10, pady=10)
        
        # Messages frame
        msg_frame = tk.Frame(win, bg=COLORS["bg_secondary"])
        msg_frame.pack(fill=tk.BOTH, expand=True, padx=10)
        
        text = tk.Text(msg_frame, bg=COLORS["bg_secondary"], fg=COLORS["text_primary"], font=FONT_MONO_SMALL, wrap=tk.WORD, bd=0)
        scrollbar = tk.Scrollbar(msg_frame, command=text.yview)
        text.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        for msg in messages:
            author_id = msg[2]
            # Get author name
            author_name = "unknown"
            for user in self.db.get_all_users():
                if user[0] == author_id:
                    author_name = user[1]
                    break
            text.insert(tk.END, f"[{author_name}] {msg[4]}\n")
            if msg[9]:  # mysterious
                text.insert(tk.END, f"{msg[3]}\n\n", "mystery")
            else:
                text.insert(tk.END, f"{msg[3]}\n\n")
        
        text.tag_config("mystery", foreground=COLORS["text_warning"])
        text.config(state=tk.DISABLED)
        
        # Reply section
        if self.player_id:
            reply_frame = tk.Frame(win, bg=COLORS["bg_primary"])
            reply_frame.pack(fill=tk.X, padx=10, pady=10)
            reply_entry = tk.Entry(reply_frame, bg=COLORS["bg_secondary"], fg=COLORS["text_primary"], font=FONT_MONO_SMALL, insertbackground=COLORS["text_accent"])
            reply_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            def post_reply():
                content = reply_entry.get()
                if content:
                    from .core.utils import generate_id
                    msg_data = {
                        "id": generate_id("msg"),
                        "thread_id": thread_id,
                        "author_id": self.player_id,
                        "content": content,
                        "created_date": __import__('datetime').datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "reply_to": None,
                        "edited": 0,
                        "mysterious": 0,
                        "deleted": 0,
                        "has_hook": 0,
                        "hook_data": ""
                    }
                    self.db.save_message(msg_data)
                    messagebox.showinfo("Reply", "Reply posted.", parent=win)
                    win.destroy()
                    self.view_thread()
            reply_btn = tk.Button(reply_frame, text="[POST]", bg=COLORS["bg_tertiary"], fg=COLORS["text_primary"], font=FONT_MONO_SMALL, command=post_reply)
            reply_btn.pack(side=tk.LEFT, padx=5)
    
    def new_thread(self):
        if not self.player_id:
            messagebox.showwarning("No Player", "Create a player account first (see status bar).")
            return
        communities = self.db.get_all_communities()
        if not communities:
            messagebox.showwarning("No Communities", "No communities available.")
            return
        title = simpledialog.askstring("New Thread", "Enter thread title:", parent=self.root)
        if not title:
            return
        content = simpledialog.askstring("Thread Content", "Enter first post:", parent=self.root)
        if not content:
            content = "..."
        community = random.choice(communities)
        from .core.utils import generate_id
        from datetime import datetime
        thread_data = {
            "id": generate_id("thread"),
            "title": title,
            "community_id": community[0],
            "author_id": self.player_id,
            "site_id": community[3],
            "created_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "last_reply": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "reply_count": 0,
            "views": 1,
            "sticky": 0,
            "locked": 0,
            "mysterious": 0,
            "deleted": 0
        }
        self.db.save_thread(thread_data)
        msg_data = {
            "id": generate_id("msg"),
            "thread_id": thread_data["id"],
            "author_id": self.player_id,
            "content": content,
            "created_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "reply_to": None,
            "edited": 0,
            "mysterious": 0,
            "deleted": 0,
            "has_hook": 0,
            "hook_data": ""
        }
        self.db.save_message(msg_data)
        messagebox.showinfo("Thread Created", f"Thread '{title}' created.")
        self.refresh_threads()
        self.refresh_all()
    
    def create_users_tab(self):
        frame = ttk.Frame(self.notebook, style="Dark.TFrame")
        self.notebook.add(frame, text="USERS")
        
        content = tk.Frame(frame, bg=COLORS["bg_primary"])
        content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        users_frame = tk.LabelFrame(content,
                                   text="NETWORK USERS",
                                   bg=COLORS["bg_primary"],
                                   fg=COLORS["text_accent"],
                                   font=FONT_MONO,
                                   bd=1,
                                   relief=tk.SOLID)
        users_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("username", "trait", "reputation", "posts")
        self.users_tree = ttk.Treeview(users_frame, columns=columns, show="headings", height=15)
        
        self.users_tree.heading("username", text="USERNAME")
        self.users_tree.heading("trait", text="TRAIT")
        self.users_tree.heading("reputation", text="REP")
        self.users_tree.heading("posts", text="POSTS")
        
        self.users_tree.column("username", width=200)
        self.users_tree.column("trait", width=150)
        self.users_tree.column("reputation", width=80)
        self.users_tree.column("posts", width=80)
        
        self.users_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.refresh_users()
        
        btn_frame = tk.Frame(users_frame, bg=COLORS["bg_primary"])
        btn_frame.pack(fill=tk.X, padx=5, pady=(0, 5))
        
        view_btn = tk.Button(btn_frame,
                            text="[VIEW PROFILE]",
                            bg=COLORS["bg_tertiary"],
                            fg=COLORS["text_primary"],
                            font=FONT_MONO_SMALL,
                            borderwidth=1,
                            relief=tk.FLAT,
                            command=self.view_user)
        view_btn.pack(side=tk.LEFT)
        
        refresh_btn = tk.Button(btn_frame,
                               text="[REFRESH]",
                               bg=COLORS["bg_tertiary"],
                               fg=COLORS["text_primary"],
                               font=FONT_MONO_SMALL,
                               borderwidth=1,
                               relief=tk.FLAT,
                               command=self.refresh_users)
        refresh_btn.pack(side=tk.LEFT, padx=5)
    
    def refresh_users(self):
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)
        users = self.db.get_all_users()
        for user in users:
            if user[10]:  # is_player
                username = f"{user[1]} [PLAYER]"
            else:
                username = user[1]
            self.users_tree.insert("", tk.END, values=(username, user[3], user[5], user[15]))
    
    def view_user(self):
        selection = self.users_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Select a user to view.")
            return
        users = self.db.get_all_users()
        idx = self.users_tree.index(selection[0])
        if idx >= len(users):
            return
        user = users[idx]
        
        win = tk.Toplevel(self.root)
        win.title(f"Profile: {user[1]}")
        win.geometry("500x400")
        win.configure(bg=COLORS["bg_primary"])
        
        info = tk.Text(win, bg=COLORS["bg_secondary"], fg=COLORS["text_primary"], font=FONT_MONO_SMALL, wrap=tk.WORD, bd=0)
        info.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        info.insert(tk.END, f">> USER PROFILE\n\n")
        info.insert(tk.END, f"Username: {user[1]}\n")
        info.insert(tk.END, f"Bio: {user[2]}\n\n")
        info.insert(tk.END, f"Trait: {user[3]}\n")
        info.insert(tk.END, f"Interests: {user[4]}\n")
        info.insert(tk.END, f"Reputation: {user[5]}\n")
        info.insert(tk.END, f"Activity Level: {user[6]:.2f}\n")
        info.insert(tk.END, f"Joined: {user[7]}\n")
        info.insert(tk.END, f"Last Active: {user[8]}\n")
        info.insert(tk.END, f"Posts: {user[15]}\n")
        if user[16]:
            info.insert(tk.END, f"\n[STATUS: MYSTERIOUS]\n")
        if user[10]:
            info.insert(tk.END, f"\n[TYPE: PLAYER]\n")
        info.config(state=tk.DISABLED)
    
    def create_communities_tab(self):
        frame = ttk.Frame(self.notebook, style="Dark.TFrame")
        self.notebook.add(frame, text="COMMUNITIES")
        
        content = tk.Frame(frame, bg=COLORS["bg_primary"])
        content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        comm_frame = tk.LabelFrame(content,
                                  text="COMMUNITIES",
                                  bg=COLORS["bg_primary"],
                                  fg=COLORS["text_accent"],
                                  font=FONT_MONO,
                                  bd=1,
                                  relief=tk.SOLID)
        comm_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("name", "members", "activity", "conflict")
        self.comm_tree = ttk.Treeview(comm_frame, columns=columns, show="headings", height=15)
        
        self.comm_tree.heading("name", text="COMMUNITY")
        self.comm_tree.heading("members", text="MEMBERS")
        self.comm_tree.heading("activity", text="ACTIVITY")
        self.comm_tree.heading("conflict", text="STATUS")
        
        self.comm_tree.column("name", width=250)
        self.comm_tree.column("members", width=100)
        self.comm_tree.column("activity", width=100)
        self.comm_tree.column("conflict", width=120)
        
        self.comm_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.refresh_communities()
        
        btn_frame = tk.Frame(comm_frame, bg=COLORS["bg_primary"])
        btn_frame.pack(fill=tk.X, padx=5, pady=(0, 5))
        
        view_btn = tk.Button(btn_frame,
                            text="[VIEW COMMUNITY]",
                            bg=COLORS["bg_tertiary"],
                            fg=COLORS["text_primary"],
                            font=FONT_MONO_SMALL,
                            borderwidth=1,
                            relief=tk.FLAT,
                            command=self.view_community)
        view_btn.pack(side=tk.LEFT)
        
        create_btn = tk.Button(btn_frame,
                              text="[CREATE COMMUNITY]",
                              bg=COLORS["bg_tertiary"],
                              fg=COLORS["text_primary"],
                              font=FONT_MONO_SMALL,
                              borderwidth=1,
                              relief=tk.FLAT,
                              command=self.create_community)
        create_btn.pack(side=tk.LEFT, padx=5)
        
        refresh_btn = tk.Button(btn_frame,
                               text="[REFRESH]",
                               bg=COLORS["bg_tertiary"],
                               fg=COLORS["text_primary"],
                               font=FONT_MONO_SMALL,
                               borderwidth=1,
                               relief=tk.FLAT,
                               command=self.refresh_communities)
        refresh_btn.pack(side=tk.LEFT)
    
    def refresh_communities(self):
        for item in self.comm_tree.get_children():
            self.comm_tree.delete(item)
        communities = self.db.get_all_communities()
        for comm in communities:
            members = comm[5].split(',') if comm[5] else []
            activity = f"{comm[7]:.1f}"
            status = "IN CONFLICT" if comm[9] else "NORMAL"
            if comm[10]:
                status += " [MYSTERY]"
            self.comm_tree.insert("", tk.END, values=(comm[1], len(members), activity, status))
    
    def view_community(self):
        selection = self.comm_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Select a community to view.")
            return
        communities = self.db.get_all_communities()
        idx = self.comm_tree.index(selection[0])
        if idx >= len(communities):
            return
        comm = communities[idx]
        
        win = tk.Toplevel(self.root)
        win.title(f"Community: {comm[1]}")
        win.geometry("500x400")
        win.configure(bg=COLORS["bg_primary"])
        
        info = tk.Text(win, bg=COLORS["bg_secondary"], fg=COLORS["text_primary"], font=FONT_MONO_SMALL, wrap=tk.WORD, bd=0)
        info.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        info.insert(tk.END, f">> {comm[1]}\n\n")
        info.insert(tk.END, f"{comm[2]}\n\n")
        info.insert(tk.END, f"Interests: {comm[4]}\n")
        members = comm[5].split(',') if comm[5] else []
        info.insert(tk.END, f"Members: {len(members)}\n")
        info.insert(tk.END, f"Activity: {comm[7]:.2f}\n")
        info.insert(tk.END, f"Reputation: {comm[8]}\n")
        info.insert(tk.END, f"Created: {comm[6]}\n\n")
        if comm[9]:
            info.insert(tk.END, "[STATUS: IN CONFLICT]\n")
        if comm[10]:
            info.insert(tk.END, "[STATUS: MYSTERIOUS]\n")
        info.config(state=tk.DISABLED)
    
    def create_community(self):
        if not self.player_id:
            messagebox.showwarning("No Player", "Create a player account first.")
            return
        name = simpledialog.askstring("New Community", "Enter community name:", parent=self.root)
        if not name:
            return
        desc = simpledialog.askstring("Description", "Enter description:", parent=self.root) or ""
        sites = self.db.get_all_sites()
        if not sites:
            messagebox.showwarning("No Sites", "No sites available.")
            return
        from .core.utils import generate_id
        from datetime import datetime
        from .core.config import INTERESTS
        comm_data = {
            "id": generate_id("comm"),
            "name": name,
            "description": desc,
            "site_id": random.choice(sites)[0],
            "interests": ",".join(random.sample(INTERESTS, min(2, len(INTERESTS)))),
            "members": self.player_id,
            "created_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "activity": 0.5,
            "reputation": 0,
            "in_conflict": 0,
            "mysterious": 0
        }
        self.db.save_community(comm_data)
        messagebox.showinfo("Community Created", f"Community '{name}' created.")
        self.refresh_communities()
        self.refresh_all()
    
    def create_archive_tab(self):
        frame = ttk.Frame(self.notebook, style="Dark.TFrame")
        self.notebook.add(frame, text="ARCHIVE")
        
        content = tk.Frame(frame, bg=COLORS["bg_primary"])
        content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        archive_frame = tk.LabelFrame(content,
                                     text="ARCHIVED CONTENT",
                                     bg=COLORS["bg_primary"],
                                     fg=COLORS["text_accent"],
                                     font=FONT_MONO,
                                     bd=1,
                                     relief=tk.SOLID)
        archive_frame.pack(fill=tk.BOTH, expand=True)
        
        archive_text = tk.Text(archive_frame,
                              bg=COLORS["bg_secondary"],
                              fg=COLORS["text_primary"],
                              font=FONT_MONO_SMALL,
                              wrap=tk.WORD,
                              bd=0)
        archive_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        archive_text.insert(tk.END,
            ">> ARCHIVE ACCESS\n\n"
            "This section contains old messages, deleted threads,\n"
            "and historical events from the early days of this network.\n\n"
            "Many files are corrupted or partially recovered.\n"
            "Some entries contradict others - this appears intentional.\n\n"
            "[ARCHIVE INDEX]\n"
            "- recovered_posts.dat [PARTIAL]\n"
            "- deleted_threads.log [CORRUPTED]\n"
            "- timeline_mismatch.txt [ENCRYPTED]\n"
            "- user_disappearances.db [FRAGMENTED]\n\n"
            ">> MORE DATA MAY BE DISCOVERED AS SIMULATION PROGRESSES\n")
        archive_text.config(state=tk.DISABLED)
    
    def create_events_tab(self):
        frame = ttk.Frame(self.notebook, style="Dark.TFrame")
        self.notebook.add(frame, text="EVENTS")
        
        content = tk.Frame(frame, bg=COLORS["bg_primary"])
        content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        events_frame = tk.LabelFrame(content,
                                    text="INCIDENT LOG",
                                    bg=COLORS["bg_primary"],
                                    fg=COLORS["text_accent"],
                                    font=FONT_MONO,
                                    bd=1,
                                    relief=tk.SOLID)
        events_frame.pack(fill=tk.BOTH, expand=True)
        
        self.events_listbox = tk.Listbox(events_frame,
                                        bg=COLORS["bg_secondary"],
                                        fg=COLORS["text_primary"],
                                        font=FONT_MONO_SMALL,
                                        selectbackground=COLORS["bg_hover"],
                                        selectforeground=COLORS["text_accent"],
                                        bd=0)
        self.events_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.refresh_events()
        
        btn_frame = tk.Frame(events_frame, bg=COLORS["bg_primary"])
        btn_frame.pack(fill=tk.X, padx=5, pady=(0, 5))
        
        view_btn = tk.Button(btn_frame,
                            text="[VIEW DETAILS]",
                            bg=COLORS["bg_tertiary"],
                            fg=COLORS["text_primary"],
                            font=FONT_MONO_SMALL,
                            borderwidth=1,
                            relief=tk.FLAT,
                            command=self.view_event)
        view_btn.pack(side=tk.LEFT)
        
        refresh_btn = tk.Button(btn_frame,
                               text="[REFRESH]",
                               bg=COLORS["bg_tertiary"],
                               fg=COLORS["text_primary"],
                               font=FONT_MONO_SMALL,
                               borderwidth=1,
                               relief=tk.FLAT,
                               command=self.refresh_events)
        refresh_btn.pack(side=tk.LEFT, padx=5)
    
    def refresh_events(self):
        self.events_listbox.delete(0, tk.END)
        events = self.db.get_all_events()
        for event in events:
            self.events_listbox.insert(tk.END, f"[{event[1].upper()}] {event[2]} - {event[4][:10]}")
    
    def view_event(self):
        selection = self.events_listbox.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Select an event to view.")
            return
        events = self.db.get_all_events()
        idx = selection[0]
        if idx < len(events):
            event = events[idx]
            messagebox.showinfo("Event Details", 
                f"Type: {event[1]}\n"
                f"Title: {event[2]}\n"
                f"Date: {event[4]}\n\n"
                f"{event[3]}\n\n"
                f"Mysterious: {'Yes' if event[7] else 'No'}")
    
    def create_settings_tab(self):
        frame = ttk.Frame(self.notebook, style="Dark.TFrame")
        self.notebook.add(frame, text="SETTINGS")
        
        content = tk.Frame(frame, bg=COLORS["bg_primary"])
        content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Simulation settings
        sim_frame = tk.LabelFrame(content,
                                 text="SIMULATION",
                                 bg=COLORS["bg_primary"],
                                 fg=COLORS["text_accent"],
                                 font=FONT_MONO,
                                 bd=1,
                                 relief=tk.SOLID)
        sim_frame.pack(fill=tk.X, pady=(0, 10))
        
        sim_inner = tk.Frame(sim_frame, bg=COLORS["bg_primary"])
        sim_inner.pack(fill=tk.X, padx=10, pady=10)
        
        # Speed control
        speed_frame = tk.Frame(sim_inner, bg=COLORS["bg_primary"])
        speed_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(speed_frame, 
                text="Simulation Speed:", 
                bg=COLORS["bg_primary"],
                fg=COLORS["text_primary"],
                font=FONT_MONO).pack(side=tk.LEFT)
        
        speed_scale = tk.Scale(speed_frame,
                              from_=0.1,
                              to=10.0,
                              resolution=0.1,
                              orient=tk.HORIZONTAL,
                              bg=COLORS["bg_secondary"],
                              fg=COLORS["text_primary"],
                              highlightthickness=0,
                              troughcolor=COLORS["bg_tertiary"],
                              command=self.change_speed)
        speed_scale.set(1.0)
        speed_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        
        # Control buttons
        ctrl_frame = tk.Frame(sim_inner, bg=COLORS["bg_primary"])
        ctrl_frame.pack(fill=tk.X, pady=5)
        
        pause_btn = tk.Button(ctrl_frame,
                             text="[PAUSE/RESUME]",
                             bg=COLORS["bg_tertiary"],
                             fg=COLORS["text_primary"],
                             font=FONT_MONO_SMALL,
                             borderwidth=1,
                             relief=tk.FLAT,
                             command=self.toggle_pause)
        pause_btn.pack(side=tk.LEFT)
        
        # Data settings
        data_frame = tk.LabelFrame(content,
                                  text="DATA MANAGEMENT",
                                  bg=COLORS["bg_primary"],
                                  fg=COLORS["text_accent"],
                                  font=FONT_MONO,
                                  bd=1,
                                  relief=tk.SOLID)
        data_frame.pack(fill=tk.X)
        
        data_inner = tk.Frame(data_frame, bg=COLORS["bg_primary"])
        data_inner.pack(fill=tk.X, padx=10, pady=10)
        
        reset_btn = tk.Button(data_inner,
                             text="[RESET WORLD]",
                             bg=COLORS["bg_tertiary"],
                             fg=COLORS["text_danger"],
                             font=FONT_MONO_SMALL,
                             borderwidth=1,
                             relief=tk.FLAT,
                             command=self.reset_world)
        reset_btn.pack(side=tk.LEFT)
        
        save_info = tk.Label(data_inner,
                            text="| World auto-saves between sessions",
                            bg=COLORS["bg_primary"],
                            fg=COLORS["text_secondary"],
                            font=FONT_MONO_SMALL)
        save_info.pack(side=tk.LEFT, padx=10)
    
    def change_speed(self, val):
        speed = float(val)
        self.sim_engine.set_speed(speed)
    
    def toggle_pause(self):
        if self.sim_engine.paused:
            self.sim_engine.resume()
            messagebox.showinfo("Simulation", "Simulation resumed.")
        else:
            self.sim_engine.pause()
            messagebox.showinfo("Simulation", "Simulation paused.")
    
    def reset_world(self):
        result = messagebox.askyesno("Reset World", 
                                    "This will delete all current data and generate a new world.\n\nAre you sure?",
                                    icon='warning')
        if result:
            self.db.clear_all()
            self.world_gen.generate_initial_world()
            self.sim_engine.start()
            self.refresh_all()
            messagebox.showinfo("Reset Complete", "New world has been generated.")
    
    def create_or_view_player(self):
        if self.player_id:
            # View player
            users = self.db.get_all_users()
            for user in users:
                if user[0] == self.player_id:
                    win = tk.Toplevel(self.root)
                    win.title(f"Player: {user[1]}")
                    win.geometry("450x350")
                    win.configure(bg=COLORS["bg_primary"])
                    info = tk.Text(win, bg=COLORS["bg_secondary"], fg=COLORS["text_primary"], font=FONT_MONO_SMALL, wrap=tk.WORD, bd=0)
                    info.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
                    info.insert(tk.END, f">> PLAYER PROFILE\n\n")
                    info.insert(tk.END, f"Username: {user[1]}\n")
                    info.insert(tk.END, f"Bio: {user[2]}\n")
                    info.insert(tk.END, f"Trait: {user[3]}\n")
                    info.insert(tk.END, f"Interests: {user[4]}\n")
                    info.insert(tk.END, f"Reputation: {user[5]}\n")
                    info.insert(tk.END, f"Posts: {user[15]}\n")
                    info.insert(tk.END, f"Joined: {user[7]}\n")
                    info.config(state=tk.DISABLED)
                    return
        else:
            # Create player
            username = simpledialog.askstring("Create Player", "Enter your username:", parent=self.root)
            if username:
                from .core.utils import generate_id
                from .core.config import TRAITS, INTERESTS
                player_data = {
                    "id": generate_id("player"),
                    "username": username,
                    "bio": "A wanderer in the dead internet.",
                    "trait": random.choice(TRAITS),
                    "interests": ",".join(random.sample(INTERESTS, min(3, len(INTERESTS)))),
                    "reputation": 0,
                    "activity_level": 0.7,
                    "joined_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "last_active": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "is_online": 1,
                    "is_player": 1,
                    "communities": "",
                    "friends": "",
                    "enemies": "",
                    "post_count": 0,
                    "mysterious": 0,
                    "inactive_since": None
                }
                self.db.save_user(player_data)
                self.player_id = player_data["id"]
                messagebox.showinfo("Player Created", f"Welcome, {username}!\n\nYou now exist in the dead internet.")
                self.refresh_users()
                self.refresh_all()
    
    def refresh_all(self):
        self.refresh_home_events()
        self.refresh_sites()
        self.refresh_threads()
        self.refresh_users()
        self.refresh_communities()
        self.refresh_events()
    
    def start_simulation_loop(self):
        def sim_loop():
            while True:
                try:
                    if hasattr(self, 'sim_engine') and hasattr(self, 'db'):
                        self.sim_engine.tick()
                    # Update UI from main thread
                    if hasattr(self, 'root'):
                        self.root.after(0, self.update_ui)
                    time.sleep(2.0 / max(0.1, getattr(self.sim_engine, 'speed', 1.0)))
                except Exception as e:
                    print(f"Simulation error: {e}")
                    time.sleep(5)
        
        thread = threading.Thread(target=sim_loop, daemon=True)
        thread.start()
    
    def update_ui(self):
        # Update game time
        try:
            game_time = self.db.get_sim_state("game_time")
            if game_time and self.game_time_label:
                self.game_time_label.config(text=f"TIME: {game_time.zfill(4)}")
            # Refresh home events occasionally
            if hasattr(self, 'home_events_list') and random.randint(0, 10) == 0:
                self.refresh_home_events()
            if hasattr(self, 'events_listbox') and random.randint(0, 15) == 0:
                self.refresh_events()
        except:
            pass
    
    def run(self):
        self.root.mainloop()
    
    def __del__(self):
        if hasattr(self, 'db'):
            self.db.close()

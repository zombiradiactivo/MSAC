import os
import json
import ctypes
import zipfile
import requests
import threading
import subprocess
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
from tkinter import messagebox

## https://developer.valvesoftware.com/wiki/Dedicated_Servers_List
## https://developer.valvesoftware.com/wiki/Dedicated_Server_Name_Enumeration

class SteamCMDApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('SteamCMD GUI')
        self.geometry('800x250')
        self.minsize(800, 250)
        self.maxsize(800, 400)
        
        self.create_tabs()
        self.create_update_install_tab()
        self.create_run_server_tab()
        self.create_console_tab()


        

    def create_tabs(self):
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill='both', expand=True)
        self.update_install_tab = self.tabview.add("Update/Install")
        self.run_server_tab = self.tabview.add("Run Server")
        self.console_tab = self.tabview.add("Console")


    def create_update_install_tab(self):
                # Lista de servidores dedicados
        self.servers = [
            {"name": "7 Days to Die Dedicated Server", "appid": 294420, "anonymous": True},
            {"name": "Age of Chivalry Dedicated Server", "appid": 17515, "anonymous": True},
            {"name": "Alien Swarm Dedicated Server", "appid": 635, "anonymous": False},
            {"name": "Alien Swarm: Reactive Drop Dedicated Server", "appid": 582400, "anonymous": True},
            {"name": "Aliens vs Predator Dedicated Server", "appid": 34120, "anonymous": False},
            {"name": "America's Army 3 Dedicated Server", "appid": 13180, "anonymous": False},
            {"name": "America's Army: Proving Grounds Dedicated Server", "appid": 203300, "anonymous": False},
            {"name": "ARK: Survival Evolved Dedicated Server", "appid": 376030, "anonymous": True},
            {"name": "ARK: Survival of the Fittest Dedicated Server ", "appid": 445400, "anonymous": False},
            {"name": "Arma 3 Dedicated Server", "appid": 233780, "anonymous": False},
            {"name": "Assetto Corsa Dedicated Server", "appid": 302550, "anonymous": False},
            {"name": "ASTRONEER Dedicated Server", "appid": 728470, "anonymous": True},
            {"name": "Black Mesa: Deathmatch Dedicated Server ", "appid": 346680, "anonymous": True},
            {"name": "Blade Symphony Dedicated Server", "appid": 228780, "anonymous": False},
            {"name": "BlazeRush Dedicated Server ", "appid": 332850, "anonymous": True},
            {"name": "BrainBread 2 Dedicated Server", "appid": 475370, "anonymous": False},
            {"name": "Breach Dedicated Server", "appid": 72310, "anonymous": False},
            {"name": "Brink Dedicated Server", "appid": 72780, "anonymous": False},
            {"name": "Call of Duty: Modern Warfare 3 Dedicated Server| ", "appid": 42750, "anonymous": False},
            {"name": "Capsa Dedicated Server ", "appid": 667230, "anonymous": False},
            {"name": "Chivalry: Deadliest Warrior Dedicated server ", "appid": 258680, "anonymous": False},
            {"name": "Chivalry: Medieval Warfare Dedicated Server ", "appid": 220070, "anonymous": False},
            {"name": "Conan Exiles Dedicated Server ", "appid": 443030, "anonymous": True},
            {"name": "Contagion Dedicated Server ", "appid": 238430, "anonymous": False},
            {"name": "Counter-Strike 1.6 Dedicated Server ", "appid": 90, "anonymous": True},
            {"name": "Counter-Strike Global Offensive Dedicated Server", "appid": 740, "anonymous": True},
            {"name": "Counter-Strike: Condition Zero Dedicated Server ", "appid": 90, "anonymous": True, "extra_option":"90 mod czero"},
            {"name": "Counter-Strike: Source Dedicated Server ", "appid": 232330, "anonymous": True},
            {"name": "D.I.P.R.I.P. Dedicated Server ", "appid": 17535, "anonymous": True},
            {"name": "Dark Messiah of Might & Magic Dedicated Server ", "appid": 2145, "anonymous": False},
            {"name": "Darkest Hour Dedicated Server ", "appid": 1290, "anonymous": False},
            {"name": "Day of Defeat Dedicated Server ", "appid": 90, "anonymous": True, "extra_option":"90 mod dod"},
            {"name": "Day of Defeat: Source Dedicated Server", "appid": 232290, "anonymous": True},
            {"name": "Day of Infamy Dedicated Server ", "appid": 462310, "anonymous": True},
            {"name": "Dayz Dedicated Server ", "appid": 223350, "anonymous": False},
            {"name": "Deathmatch Classic Dedicated Server ", "appid": 90, "anonymous": True, "extra_option":"90 mod dmc"},
            {"name": "Dino D-Day Dedicated Server ", "appid": 70010, "anonymous": False},
            {"name": "Double Action Dedicated Server", "appid": 317800, "anonymous": True},
            {"name": "Dystopia Dedicated Server ", "appid": 17585, "anonymous": True},
            {"name": "E.Y.E - Dedicated Server ", "appid": 91720, "anonymous": False},
            {"name": "Eden Star Dedicated Server ", "appid": 419790, "anonymous": True},
            {"name": "Empires Dedicated Server ", "appid": 460040, "anonymous": True},
            {"name": "Eternal Silence Dedicated Server ", "appid": 17555, "anonymous": True},
            {"name": "Fistful of Frags Server ", "appid": 295230, "anonymous": True},
            {"name": "Fortress Forever Dedicated Server ", "appid": 329710, "anonymous": True},
            {"name": "Garry's Mod Dedicated Server ", "appid": 4020, "anonymous": True},
            {"name": "GTR Evolution Demo Dedicated Server ", "appid": 8730, "anonymous": False},
            {"name": "Half-Life 2: Deathmatch Dedicated Server ", "appid": 232370, "anonymous": True},
            {"name": "Half-Life Deathmatch: Source Dedicated server ", "appid": 255470, "anonymous": True},
            {"name": "Half-Life Dedicated Server ", "appid": 90, "anonymous": True},
            {"name": "Half-Life: Opposing Force Dedicated Server ", "appid": 90, "anonymous": True, "extra_option":"90 mod gearbox"},
            {"name": "Homefront Dedicated Server ", "appid": 55280, "anonymous": False},
            {"name": "Hurtworld dedicated server Bat file ", "appid": 405100, "anonymous": True},
            {"name": "Insurgency Dedicated Server", "appid": 237410, "anonymous": True},
            {"name": "Insurgency: Modern Infantry Combat Dedicated Server ", "appid": 17705, "anonymous": True},
            {"name": "Insurgency: Sandstorm Dedicated Server ", "appid": 581330, "anonymous": True},
            {"name": "JBMod Dedicated Server ", "appid": 2181210, "anonymous": True},
            {"name": "Just Cause 2: Multiplayer Dedicated Server ", "appid": 261140, "anonymous": True},
            {"name": "Killing Floor 2 Dedicated Server Windows", "appid": 232130, "anonymous": True},
            {"name": "Killing Floor Beta Dedicated Server", "appid": 1273, "anonymous": False},
            {"name": "Killing Floor Dedicated Server Windows", "appid": 215350, "anonymous": False},
            {"name": "Kingdoms Rise Dedicated Server ", "appid": 265360, "anonymous": True},
            {"name": "Lambda Wars Dedicated Server ", "appid": 319060, "anonymous": False},
            {"name": "Left 4 Dead 2 Dedicated Server", "appid": 222860, "anonymous": True},
            {"name": "Left 4 Dead Dedicated Server ", "appid": 222840, "anonymous": True},
            {"name": "Life is Feudal: Your Own Dedicated Server ", "appid": 320850, "anonymous": True},
            {"name": "Mod and Play Dedicated Server ", "appid": 1301040, "anonymous": True},
            {"name": "Monday Night Combat Dedicated Server ", "appid": 63220, "anonymous": False},
            {"name": "Natural Selection 2 Dedicated Server", "appid": 4940, "anonymous": False},
            {"name": "NEOTOKYO Dedicated Server ", "appid": 313600, "anonymous": True},
            {"name": "Nexuiz Dedicated Server ", "appid": 96810, "anonymous": False},
            {"name": "No More Room in Hell Dedicated Server", "appid": 317670, "anonymous": False},
            {"name": "NS2: Combat Dedicated Server", "appid": 313900, "anonymous": True},
            {"name": "Nuclear Dawn Dedicated Server ", "appid": 111710, "anonymous": True},
            {"name": "Out of Reach Dedicated Server", "appid": 406800, "anonymous": True},
            {"name": "Painkiller Hell & Damnation Dedicated Server ", "appid": 230030, "anonymous": False},
            {"name": "Palworld Dedicated Server ", "appid": 2394010, "anonymous": True},
            {"name": "Pirates, Vikings, and Knights II Dedicated Server ", "appid": 17575, "anonymous": True},
            {"name": "Primal Carnage Dedicated Server ", "appid": 224620, "anonymous": False},
            {"name": "Project Zomboid Dedicated Server", "appid": 108600, "anonymous": False},
            {"name": "RACE 07 Dedicated Server ", "appid": 8610, "anonymous": False},
            {"name": "RACE 07 Demo - Crowne Plaza Edition Dedicated Server ", "appid": 8680, "anonymous": False},
            {"name": "RACE 07 Demo Dedicated Server ", "appid": 4270, "anonymous": False},
            {"name": "RACE On - Demo: Dedicated Server ", "appid": 8770, "anonymous": False},
            {"name": "Ravaged Dedicated Server ", "appid": 223160, "anonymous": False},
            {"name": "Red Orchestra 2 Dedicated Server ", "appid": 212542, "anonymous": False},
            {"name": "Red Orchestra Windows Dedicated Server  ", "appid": 212542, "anonymous": False},
            {"name": "Reflex Dedicated Server ", "appid": 223240, "anonymous": True},
            {"name": "Reign Of Kings Dedicated Server ", "appid": 381690, "anonymous": False},
            {"name": "Ricochet Dedicated Server  ", "appid": 90, "anonymous": True, "extra_option":"90 mod ricochet"},
            {"name": "Rust Dedicated Server", "appid": 258550, "anonymous": True},
            {"name": "Satisfactory Dedicated Server", "appid": 1690800, "anonymous": True},
            {"name": "Serious Sam 3 Dedicated Server ", "appid": 41080, "anonymous": False},
            {"name": "Serious Sam Classics: Revolution Dedicated Server ", "appid": 41005, "anonymous": False},
            {"name": "Serious Sam HD Dedicated Server ", "appid": 41005, "anonymous": False},
            {"name": "Serious Sam HD: The Second Encounter Dedicated Server ", "appid": 41015, "anonymous": True},
            {"name": "Sniper Elite 3 Dedicated Server ", "appid": 266910, "anonymous": False},
            {"name": "Sniper Elite V2 Dedicated Server ", "appid": 208050, "anonymous": False},
            {"name": "Sons Of The Forest Dedicated Server ", "appid": 2465200, "anonymous": True},
            {"name": "Source 2007 Dedicated Server ", "appid": 310, "anonymous": True},
            {"name": "Source Dedicated Server ", "appid": 205, "anonymous": True},
            {"name": "Source SDK Base 2006 MP Dedicated Server ", "appid": 205, "anonymous": True},
            {"name": "Source SDK Base 2013 Dedicated Server ", "appid": 244310, "anonymous": True},
            {"name": "Space Engineers Dedicated Server", "appid": 298740, "anonymous": True},
            {"name": "Squad Dedicated Server", "appid": 403240, "anonymous": True},
            {"name": "Starbound Dedicated server", "appid": 211820, "anonymous": False},
            {"name": "Starvoid Dedicated Server ", "appid": 210370, "anonymous": False},
            {"name": "STCC - The Game Demo Dedicated Server ", "appid": 8710, "anonymous": False},
            {"name": "Sven Co-op Dedicated Server ", "appid": 276060, "anonymous": True},
            {"name": "Synergy Dedicated Server ", "appid": 17525, "anonymous": True},
            {"name": "Takedown: Red Sabre Dedicated Server ", "appid": 261020, "anonymous": True},
            {"name": "Team Fortress 2 Dedicated Server ", "appid": 232250, "anonymous": True},
            {"name": "Team Fortress Classic dedicated server ", "appid": 90, "anonymous": True, "extra_option":"90 mod tfc"},
            {"name": "The Forest Dedicated Server ", "appid": 556450, "anonymous": True},
            {"name": "The Haunted: Hells Reach Dedicated Server ", "appid": 43210, "anonymous": False},
            {"name": "The Ship Dedicated Server ", "appid": 2403, "anonymous": False},
            {"name": "Tower Unite Dedicated server", "appid": 439660, "anonymous": True},
            {"name": "Zombie Grinder Dedicated Server ", "appid": 374980, "anonymous": False},
            {"name": "Zombie Panic Source Dedicated Server ", "appid": 17505, "anonymous": True},

        ]

        # SteamCMD Configuration
        steamcmd_frame = ctk.CTkFrame(self.update_install_tab, fg_color="transparent")
        steamcmd_frame.pack(fill='x', padx=10, pady=5)
        
        steamcmd_download = ctk.CTkButton(steamcmd_frame, text="Download SteamCMD", command=self.descargar_steamcmd)
        steamcmd_download.pack(side='left', padx=5)
        
        steamcmd_label = ctk.CTkLabel(steamcmd_frame, text="SteamCMD path")
        steamcmd_label.pack(side='left', padx=5)
        
        self.steamcmd_entry = ctk.CTkEntry(steamcmd_frame)
        self.steamcmd_entry.pack(side='left', fill='x', expand=True, padx=5)
        
        steamcmd_browse_button = ctk.CTkButton(steamcmd_frame, text="Browse", command=self.browse_steamcmd)
        steamcmd_browse_button.pack(side='left', padx=5)
        
        # Server Configuration
        server_frame = ctk.CTkFrame(self.update_install_tab, fg_color="transparent")
        server_frame.pack(fill='x', padx=10, pady=5)
        
        game_label = ctk.CTkLabel(server_frame, text="Game")
        game_label.pack(side='left', padx=5)
        
        self.game_combobox = ctk.CTkComboBox(server_frame, values=[server['name'] for server in self.servers])
        self.game_combobox.pack(side='left', padx=5)
        self.game_combobox.bind("<<ComboboxSelected>>", self.on_game_selected)
        
        
        # Login Configuration
        login_frame = ctk.CTkFrame(self.update_install_tab, fg_color="transparent")
        login_frame.pack(fill='x', padx=10, pady=5)
        
        login_label = ctk.CTkLabel(login_frame, text="Username/Password")
        login_label.pack(side='left', padx=5)
        
        self.login_entry = ctk.CTkEntry(login_frame)
        self.login_entry.pack(side='left', fill='x', expand=True, padx=5)

        self.password_entry = ctk.CTkEntry(login_frame)
        self.password_entry.pack(side='left', fill='x', expand=True, padx=5)

        self.anonymous_checkbox = ctk.CTkCheckBox(login_frame, text="Login as Anonymous")
        self.anonymous_checkbox.pack(side='left', padx=5)
        
        # Server Path
        path_frame = ctk.CTkFrame(self.update_install_tab, fg_color="transparent")
        path_frame.pack(fill='x', padx=10, pady=5)
        
        server_path_label = ctk.CTkLabel(path_frame, text="Server Path")
        server_path_label.pack(side='left', padx=5)
        
        self.server_path_entry = ctk.CTkEntry(path_frame)
        self.server_path_entry.pack(side='left', fill='x', expand=True, padx=5)
        
        server_path_browse_button = ctk.CTkButton(path_frame, text="Browse", command=self.browse_server_path)
        server_path_browse_button.pack(side='left', padx=5)
        
        self.validate_checkbox = ctk.CTkCheckBox(path_frame, text="Validate Files")
        self.validate_checkbox.pack(side='left', padx=5)
        
        self.console_checkbox = ctk.CTkCheckBox(path_frame, text="Use the Console")
        self.console_checkbox.pack(side='left', padx=5)
        
        update_install_button = ctk.CTkButton(path_frame, text="Update/Install", command=self.update_install)
        update_install_button.pack(side='left', padx=5)

    def create_run_server_tab(self):
        # Srcds Configuration
        srcds_frame = ctk.CTkFrame(self.run_server_tab, fg_color="transparent")
        srcds_frame.pack(fill='x', padx=10, pady=5)
        
        srcds_label = ctk.CTkLabel(srcds_frame, text="Srcds path")
        srcds_label.pack(side='left', padx=5)
        
        self.srcds_entry = ctk.CTkEntry(srcds_frame)
        self.srcds_entry.pack(side='left', fill='x', expand=True, padx=5)
        
        srcds_browse_button = ctk.CTkButton(srcds_frame, text="Browse", command=self.browse_srcds)
        srcds_browse_button.pack(side='left', padx=5)
        
        # Game Configuration
        game_frame = ctk.CTkFrame(self.run_server_tab, fg_color="transparent")
        game_frame.pack(fill='x', padx=10, pady=5)
        
        game_label = ctk.CTkLabel(game_frame, text="Game")
        game_label.pack(side='left', padx=5)

        
        self.game_combobox1 = ctk.CTkComboBox(game_frame, values=[server['name'] for server in self.servers])
        self.game_combobox1.pack(side='left', padx=5)
        self.game_combobox1.bind("<<ComboboxSelected>>", self.on_game_selected)

        
        self.custom_mod_checkbox = ctk.CTkCheckBox(game_frame, text="Custom Mod")
        self.custom_mod_checkbox.pack(side='left', padx=5)
        
        # Server Name
        server_name_label = ctk.CTkLabel(game_frame, text="Server Name")
        server_name_label.pack(side='left', padx=5)
        
        self.server_name_entry = ctk.CTkEntry(game_frame)
        self.server_name_entry.pack(side='left', fill='x', expand=True, padx=5)
        
        # Map
        map_label = ctk.CTkLabel(game_frame, text="Map")
        map_label.pack(side='left', padx=5)
        
        self.map_entry = ctk.CTkEntry(game_frame)
        self.map_entry.pack(side='left', fill='x', expand=True, padx=5)
        
        # Network Configuration
        network_frame = ctk.CTkFrame(self.run_server_tab, fg_color="transparent")
        network_frame.pack(fill='x', padx=10, pady=5)
        
        network_label = ctk.CTkLabel(network_frame, text="Network")
        network_label.pack(side='left', padx=5)
        
        self.network_combobox = ctk.CTkComboBox(network_frame, values=["Internet", "Lan"])
        self.network_combobox.pack(side='left', padx=5)
        
        max_players_label = ctk.CTkLabel(network_frame, text="Max Players")
        max_players_label.pack(side='left', padx=5)
        
        self.max_players_spinbox = ctk.CTkEntry(network_frame)
        self.max_players_spinbox.pack(side='left', padx=5)
        
        # UDP Port
        udp_port_label = ctk.CTkLabel(network_frame, text="UDP Port")
        udp_port_label.pack(side='left', padx=5)
        
        self.udp_port_entry = ctk.CTkEntry(network_frame)
        self.udp_port_entry.pack(side='left', fill='x', expand=True, padx=5)
        
        # RCON
        rcon_label = ctk.CTkLabel(network_frame, text="RCON")
        rcon_label.pack(side='left', padx=5)
        
        self.rcon_entry = ctk.CTkEntry(network_frame)
        self.rcon_entry.pack(side='left', fill='x', expand=True, padx=5)
        
        # Checkboxes 
        options_frame = ctk.CTkFrame(self.run_server_tab, fg_color="transparent")
        options_frame.pack(fill='x', padx=10, pady=5)
        
        self.debug_mode_checkbox = ctk.CTkCheckBox(options_frame, text="Debug Mode")
        self.debug_mode_checkbox.pack(side='left', padx=5)
        
        self.sourcetv_checkbox = ctk.CTkCheckBox(options_frame, text="SourceTV")
        self.sourcetv_checkbox.pack(side='left', padx=5)
        
        self.console_mode_checkbox = ctk.CTkCheckBox(options_frame, text="Console Mode")
        self.console_mode_checkbox.pack(side='left', padx=5)
        
        self.insecure_checkbox = ctk.CTkCheckBox(options_frame, text="Insecure")
        self.insecure_checkbox.pack(side='left', padx=5)
        
        self.disable_bots_checkbox = ctk.CTkCheckBox(options_frame, text="Disable Bots")
        self.disable_bots_checkbox.pack(side='left', padx=5)
        
        self.dev_messages_checkbox = ctk.CTkCheckBox(options_frame, text="Dev Messages")
        self.dev_messages_checkbox.pack(side='left', padx=5)
        # Save and Run Button
        launch_frame = ctk.CTkFrame(self.run_server_tab, fg_color="transparent")
        launch_frame.place(relx=0.4, rely=0.8, relwidth=0.6, relheight=0.15)

        steam_profiles = self.load_profiles()
        self.profile_combobox = ctk.CTkComboBox(launch_frame, values=[f"{profile['game']} - {profile['name']}" for profile in steam_profiles])
        self.profile_combobox.pack(side='left', expand=True, padx=5)
        self.profile_combobox.bind("<<ComboboxSelected>>", self.on_profile_selected)
        
        self.update_combobox(self.profile_combobox, steam_profiles)

        profile_save = ctk.CTkButton(launch_frame, text="Save", command=self.save_profile)
        profile_save.pack(side='left', expand=True,padx=5)

        run_button = ctk.CTkButton(launch_frame, text="Run", command=self.run_server)
        run_button.pack(side='left', expand=True, padx=5)
    
    def create_console_tab(self):
        self.console_text = ctk.CTkTextbox(self.console_tab, width=50, height=20)
        self.console_text.pack(fill='both', expand=True, padx=5, pady=5)

        self.console_entry = ctk.CTkEntry(self.console_tab)
        self.console_entry.pack(side='left', fill='x', expand=True, padx=5)


    def browse_steamcmd(self):
        path = filedialog.askopenfilename(filetypes=[("Executable files", "*.exe")])
        if path:
            self.steamcmd_entry.insert(0, path)
    
    def browse_server_path(self):
        path = filedialog.askdirectory()
        if path:
            self.server_path_entry.insert(0, path)
    
    def browse_srcds(self):
        path = filedialog.askopenfilename(filetypes=[("Executable files", "*.exe")])
        if path:
            self.srcds_entry.insert(0, path)
    
    def add_custom_game(self):
        custom_game = ctk.CTkInputDialog(text="Enter Custom Game Name", title="Add Custom Game")
        game_name = custom_game.get_input()
        if game_name:
            self.game_combobox.set(game_name)
            self.game_combobox.configure(values=self.game_combobox.cget("values") + [game_name])

    def on_game_selected(self, event):
        selected_game = self.game_combobox.get()
        for server in self.servers:
            if server['name'] == selected_game:
                self.anonymous_checkbox.set(server['anonymous'])
                self.login_entry.configure(state="disabled" if server['anonymous'] else "normal")
                self.password_entry.configure(state="disabled" if server['anonymous'] else "normal")
                break


    def update_install(self):
        steamcmd_path = self.steamcmd_entry.get()
        game = self.game_combobox.get()
        username = self.login_entry.get() if not self.anonymous_checkbox.get() else "anonymous"
        password = self.password_entry.get() if not self.anonymous_checkbox.get() else ""
        server_path = self.server_path_entry.get()
        validate_files = self.validate_checkbox.get()

        if not steamcmd_path or not game or not server_path:
            messagebox.showerror("Error", "Please fill in all required fields.")
            return

        appid = None
        extra_option = None

        for server in self.servers:
            if server['name'] == game:
                appid = server['appid']
                extra_option = server.get('extra_option', None)
                break

        if appid is None:
            messagebox.showerror("Error", "Game not found in the server list.")
            return

        validate_flag = "validate" if validate_files else ""
        if extra_option:
            command = f'"{steamcmd_path}" +force_install_dir "{server_path}" +login {username} {password} +app_set_config {extra_option} +app_update {appid} {validate_flag} +quit'
            print(command)
        else:
            command = f'"{steamcmd_path}" +force_install_dir "{server_path}" +login {username} {password} +app_update {appid} {validate_flag} +quit'
            print(command)

        self.console_text.insert('end', f"Running command: {command}")

        threading.Thread(target=self.run_steamcmd, args=(command,)).start()        

    def get_network_value(self):
        network = self.network_combobox.get()
        return 0 if network == "Internet" else 1

    def run_server(self):
        srcds_path = self.srcds_entry.get()
        game = self.game_combobox1.get()
        server_name = self.server_name_entry.get()
        map_name = self.map_entry.get()
        network = self.get_network_value()
        max_players = self.max_players_spinbox.get()
        udp_port = self.udp_port_entry.get()
        rcon_password = self.rcon_entry.get()
        
        if not srcds_path or not game or not server_name or not map_name or not udp_port:
            messagebox.showerror("Error", "Please fill in all required fields.")
            return
        
        debug_mode = "-debug" if self.debug_mode_checkbox.get() else ""
        sourcetv = "-sourcetv" if self.sourcetv_checkbox.get() else ""
        console_mode = "-console" if self.console_mode_checkbox.get() else ""
        insecure = "-insecure" if self.insecure_checkbox.get() else ""
        disable_bots = "+mp_autoteambalance 0 +mp_limitteams 0" if self.disable_bots_checkbox.get() else ""
        dev_messages = "-dev" if self.dev_messages_checkbox.get() else ""
        
        command = f'"{srcds_path}" -game {game} -console +hostname "{server_name}" +map {map_name} +maxplayers {max_players} +sv_lan {network} -port {udp_port} +rcon_password "{rcon_password}" {debug_mode} {sourcetv} {console_mode} {insecure} {disable_bots} {dev_messages}'
        
        self.console_text.insert(ctk.END, f"Running command: {command}")
        threading.Thread(target=self.run_command, args=(command,)).start()    



    def run_command(self, command):
        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
            stdout, stderr = process.communicate()
            self.console_text.insert('end', f"{stdout}\n{stderr}\n")
            print(f"{stdout}\n{stderr}\n")

        except Exception as e:
            self.console_text.insert('end', f"Error: {str(e)}\n")
            print(f"Error: {str(e)}\n")


    def run_steamcmd(self, command):
        shell32 = ctypes.windll.shell32
        cmd_command = f'cmd.exe /c "{command}"'
        result = shell32.ShellExecuteW(None, "open", "cmd.exe", f'/c {cmd_command}', None, 1)
        print(result)

        if result > 32:
            self.console_text.insert('end', "SteamCMD se abrió correctamente.\n")
        else:
            self.console_text.insert('end', "Error al abrir SteamCMD.\n")


    def load_profiles(self):
        try:
            with open("steam_profiles.json", "r") as file:
                steam_profiles = json.load(file)
        except FileNotFoundError:
            steam_profiles = []
        return steam_profiles

    def update_combobox(self, combobox, steam_profiles):
        # Actualizar los valores del combobox con los perfiles cargados
        combobox_values = [f"{profile['srcds']} - {profile['game']} - {profile['name']} - {profile['map']} - {profile['netword']} - {profile['max_players']} - {profile['udp_port']} - {profile['rcon']} - {profile['is_custom']} - {profile['has_debug']} - {profile['has_sourcetv']} - {profile['has_console']} - {profile['is_insecure']} - {profile['has_disable_bots']} - {profile['has_dev_messages']}" for profile in steam_profiles]
        combobox['values'] = combobox_values
        
    def on_profile_selected(self, event):
        # Obtener el perfil seleccionado del combobox
        selected_profile = self.profile_combobox.get()
        srcds, game, name, map, netword, max_players, udp_port, rcon, is_custom, has_debug, has_sourcetv, has_console, is_insecure, has_disable_bots, has_dev_messages  = selected_profile.split(' - ')
        # Actualizar los campos de entrada con los valores del perfil seleccionado
        self.srcds_entry.delete(0, ctk.END)
        self.srcds_entry.insert(0, srcds)
        self.game_combobox1.set(game)
        self.server_name_entry.delete(0, ctk.END)
        self.server_name_entry.insert(0, name)
        self.map_entry.delete(0, ctk.END)
        self.map_entry.insert(0, map)
        self.network_combobox.set(netword)
        self.max_players_spinbox.delete(0, ctk.END)
        self.max_players_spinbox.insert(0, max_players)
        self.udp_port_entry.delete(0, ctk.END)
        self.udp_port_entry.insert(0, udp_port)
        self.rcon_entry.delete(0, ctk.END)
        self.rcon_entry.insert(0, rcon)
        if is_custom == "1":
            self.custom_mod_checkbox.select()
        else:
            self.custom_mod_checkbox.deselect() 
        if has_debug == "1":
            self.debug_mode_checkbox.select()
        else:
            self.debug_mode_checkbox.deselect() 
        if has_sourcetv == "1":
            self.sourcetv_checkbox.select()
        else:
            self.sourcetv_checkbox.deselect() 
        if has_console == "1":
            self.console_mode_checkbox.select()
        else:
            self.console_mode_checkbox.deselect() 
        if is_insecure == "1":
            self.insecure_checkbox.select()
        else:
            self.insecure_checkbox.deselect() 
        if has_disable_bots == "1":
            self.disable_bots_checkbox.select()
        else:
            self.disable_bots_checkbox.deselect() 
        if has_dev_messages == "1":
            self.dev_messages_checkbox.select()
        else:
            self.dev_messages_checkbox.deselect() 

    def save_profile(self):
        # Obtener los valores de entrada del usuario y la versión seleccionada
        srcds = self.srcds_entry.get()
        game = self.game_combobox1.get()
        name = self.server_name_entry.get()
        map = self.map_entry.get()
        netword = self.network_combobox.get()
        max_players = self.max_players_spinbox.get()
        udp_port = self.udp_port_entry.get()
        rcon = self.rcon_entry.get()
        is_custom = self.custom_mod_checkbox.get()
        has_debug = self.debug_mode_checkbox.get()
        has_sourcetv = self.sourcetv_checkbox.get()
        has_console = self.console_mode_checkbox.get()
        is_insecure = self.insecure_checkbox.get()
        has_disable_bots = self.disable_bots_checkbox.get()
        has_dev_messages = self.dev_messages_checkbox.get()

        # Crear un nuevo perfil
        new_profile = {
            "srcds": srcds,
            "game": game,
            "name": name,
            "map": map,
            "netword": netword,
            "max_players": max_players,
            "udp_port": udp_port,
            "rcon": rcon,
            "is_custom": is_custom,
            "has_debug": has_debug,
            "has_sourcetv": has_sourcetv,
            "has_console": has_console,
            "is_insecure": is_insecure,
            "has_disable_bots": has_disable_bots,
            "has_dev_messages": has_dev_messages
        }

        # Intentar cargar perfiles existentes, si el archivo no existe, inicializar una lista vacía
        try:
            with open("steam_profiles.json", "r") as file:
                steam_profiles = json.load(file)
        except FileNotFoundError:
            steam_profiles = []

        # Agregar el nuevo perfil a la lista
        steam_profiles.append(new_profile)

        # Guardar la lista actualizada de perfiles en el archivo JSON
        with open("steam_profiles.json", "w") as file:
            json.dump(steam_profiles, file, indent=4)
            
    def descargar_steamcmd(self):
        url = "https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip"
        nombre_archivo = "steamcmd.zip"
        carpeta = "Steam Servers/SteamCMD"
        ruta_zip = os.path.join(carpeta, nombre_archivo)
        try:
            if not os.path.exists(carpeta):
                os.makedirs(carpeta)

            ruta_completa = os.path.join(carpeta, nombre_archivo)

            if not os.path.exists(ruta_completa):
                with requests.get(url, stream=True) as respuesta:
                    total_size = int(respuesta.headers.get('content-length', 0))
                    chunk_size = 8192  # Tamaño del chunk
                    received_bytes = 0

                    download_progress_bar = ctk.CTkProgressBar(self, mode='determinate')
                    download_progress_bar.place(relx=0, rely=1, relwidth=1, anchor='sw')

                    with open(ruta_completa, 'wb') as archivo:
                        for data in respuesta.iter_content(chunk_size=chunk_size):
                            received_bytes += len(data)
                            archivo.write(data)
                            percent_complete = round((received_bytes / total_size)* 100, 1)
                            percent_complete_bar = round(((received_bytes / total_size)), 3)
                            print(f"{percent_complete_bar} bar")
                            print(f"{percent_complete} no")
                            if percent_complete % 1 == 0:
                                download_progress_bar.set(percent_complete_bar)                            

                            
                print(f"Descarga de '{nombre_archivo}' completada en '{carpeta}'")
                # Destruir la barra de progreso al finalizar la descarga
                download_progress_bar.destroy()           
                with zipfile.ZipFile(ruta_zip, 'r') as zip_ref:
                    zip_ref.extractall(carpeta)
                print(f"Descarga de '{nombre_archivo}' completada en '{carpeta}'")
            else:
                print(f"'{nombre_archivo}' ya existe en '{carpeta}', no es necesario descargarlo nuevamente.")
        except requests.RequestException as e:
            print(f"Error de conexión: {e}")


app = SteamCMDApp()
app.mainloop()

import customtkinter as ctk
from PIL import Image
import os
import json
import tkinter.messagebox as messagebox
import threading
import webbrowser

# === CONFIG ===
SETTINGS_FILE = "settings.json"
LOGO_IMAGE = "rust_logo.png"  # Must be in the same folder

# === DISCORD OAUTH ===
DISCORD_CLIENT_ID = "1362601040603643954"
# NOTE: This redirect URI is for real OAuth2 but requires a live server running at this address
DISCORD_REDIRECT_URI = "https://cf79-2601-483-4500-2650-6df-26cb-44e-5572.ngrok-free.app/callback"

# This URL just opens the bot invite link with permissions, no OAuth callback required
DISCORD_BOT_INVITE_URL = (
    f"https://discord.com/api/oauth2/authorize?"
    f"client_id={DISCORD_CLIENT_ID}"
    f"&permissions=268437504"  # example permissions for your bot
    f"&scope=bot"
)

# === SETUP ===
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.title("Rust Raid Alarm")
app.geometry("600x600")
app.configure(bg="#1e1e1e")
app.resizable(False, False)

# === LOAD SETTINGS ===
if os.path.exists(SETTINGS_FILE):
    with open(SETTINGS_FILE, "r") as f:
        settings = json.load(f)
else:
    settings = {
        "phone_number": "",
        "server_id": "",
        "wol": False,
        "auto_join": False,
        "discord_linked": False,
        "start_minimized": False,
        "start_on_boot": False
    }

# === FUNCTIONS ===
def save_settings():
    settings["phone_number"] = phone_entry.get()
    settings["server_id"] = server_entry.get()
    settings["wol"] = wol_var.get()
    settings["auto_join"] = auto_join_var.get()
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f)
    save_button.configure(text="Settings Saved!")
    threading.Timer(3.0, lambda: save_button.configure(text="Save Settings")).start()

def link_discord():
    if settings.get("discord_linked"):
        messagebox.showinfo("Info", "Discord is already linked!")
        return
    # Open Discord bot invite URL (no OAuth callback needed)
    webbrowser.open(DISCORD_BOT_INVITE_URL)
    # We *assume* the user will link the bot manually in Discord
    settings["discord_linked"] = True
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f)
    discord_button.configure(text="Discord Linked!", fg_color="#5865F2")

def unlink_discord():
    confirm = messagebox.askokcancel(
        "Unlink Discord",
        "Unlinking Discord will remove saved credentials from this app, "
        "but the bot will remain in your Discord server.\n\n"
        "To remove the bot fully, go to your Discord server settings > Integrations > "
        "and remove the bot manually."
    )
    if confirm:
        settings["discord_linked"] = False
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f)
        discord_button.configure(text="Link Discord", fg_color="#5865F2")
        messagebox.showinfo("Unlinked", "Discord has been unlinked.")

def open_settings_page():
    main_frame.pack_forget()
    settings_frame.pack(pady=40)

def go_back():
    settings_frame.pack_forget()
    main_frame.pack(pady=40)

def toggle_startup():
    settings["start_on_boot"] = start_on_boot_var.get()

def toggle_minimized():
    settings["start_minimized"] = start_minimized_var.get()

# === MAIN FRAME ===
main_frame = ctk.CTkFrame(app, fg_color="transparent")
main_frame.pack(pady=40)

# === LOGO ===
if os.path.exists(LOGO_IMAGE):
    logo_img = ctk.CTkImage(light_image=Image.open(LOGO_IMAGE).convert("RGBA"), size=(350, 160))
    logo_label = ctk.CTkLabel(main_frame, image=logo_img, text="")
    logo_label.pack(pady=(0, 10))

# === SERVER ENTRY ===
server_entry = ctk.CTkEntry(main_frame, placeholder_text="Rust Server ID", width=300)
if settings["server_id"]:
    server_entry.insert(0, settings["server_id"])
server_entry.pack(pady=10)

# === PHONE ENTRY ===
phone_entry = ctk.CTkEntry(main_frame, placeholder_text="Phone Number", width=300)
if settings["phone_number"]:
    phone_entry.insert(0, settings["phone_number"])
phone_entry.pack(pady=10)

# === TOGGLES ===
orange_color = "#e95420"

wol_var = ctk.BooleanVar(value=settings["wol"])
wol_checkbox = ctk.CTkCheckBox(main_frame, text="Enable Wake-on-LAN", variable=wol_var, fg_color=orange_color, hover_color="#cc471d")
wol_checkbox.pack(pady=5)

auto_join_var = ctk.BooleanVar(value=settings["auto_join"])
auto_join_checkbox = ctk.CTkCheckBox(main_frame, text="Auto-Join Rust Server", variable=auto_join_var, fg_color=orange_color, hover_color="#cc471d")
auto_join_checkbox.pack(pady=5)

# === BUTTONS ===
discord_button = ctk.CTkButton(
    main_frame,
    text="Discord Linked!" if settings.get("discord_linked") else "Link Discord",
    command=link_discord,
    fg_color="#5865F2",
    corner_radius=30,
    width=200
)
discord_button.pack(pady=20)

save_button = ctk.CTkButton(
    main_frame,
    text="Save Settings",
    command=save_settings,
    fg_color=orange_color,
    hover_color="#d84315",
    corner_radius=30,
    width=200
)
save_button.pack()

settings_button = ctk.CTkButton(
    main_frame,
    text="Settings ⚙️",
    command=open_settings_page,
    fg_color="white",
    text_color="black",
    height=40,
    corner_radius=30,
    width=100
)
settings_button.pack(pady=10)

# === SETTINGS FRAME ===
settings_frame = ctk.CTkFrame(app, fg_color="transparent")

back_button = ctk.CTkButton(
    settings_frame,
    text="⬅ Back",
    command=go_back,
    fg_color="#c1460f",
    hover_color="#9c380c"
)
back_button.pack(pady=10)

unlink_button = ctk.CTkButton(
    settings_frame,
    text="Unlink Discord",
    command=unlink_discord,
    fg_color="#5865F2",
    corner_radius=30,
    width=200
)
unlink_button.pack(pady=10)

start_on_boot_var = ctk.BooleanVar(value=settings.get("start_on_boot", False))
startup_checkbox = ctk.CTkCheckBox(settings_frame, text="Start on Windows Startup", variable=start_on_boot_var, command=toggle_startup, fg_color=orange_color, hover_color="#cc471d")
startup_checkbox.pack(pady=10)

start_minimized_var = ctk.BooleanVar(value=settings.get("start_minimized", False))
minimize_checkbox = ctk.CTkCheckBox(settings_frame, text="Run Minimized", variable=start_minimized_var, command=toggle_minimized, fg_color=orange_color, hover_color="#cc471d")
minimize_checkbox.pack(pady=10)

# === START APP ===
app.mainloop()

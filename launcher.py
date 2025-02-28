import tkinter as tk
from tkinter import ttk, messagebox

def get_settings(username_var, mode_var, ip_var, port_var, port_host_var, host_join_var):
    """Gets user settings and returns them as a dictionary. Shows errors without closing the window."""
    username = username_var.get().strip()
    mode = mode_var.get()
    ip = ip_var.get().strip() if mode == "Join" else "NULL"
    port = port_var.get().strip() if mode == "Join" else port_host_var.get().strip()

    # Validate input
    if mode != "Host" or host_join_var.get():
        if not username:
            messagebox.showerror("Error", "Username is required!")
            return None
    
    if mode == "Join" and (not ip or not port):
        messagebox.showerror("Error", "IP and Port are required to Join!")
        return None
    
    if mode == "Host" and not port:
        messagebox.showerror("Error", "Port is required to Host!")
        return None

    if mode == "Host" and host_join_var.get():
        mode = "all"  # Host & Join mode

    # Store settings in a dictionary
    settings = {
        "username": username,
        "mode": mode.lower(),
        "ip": ip,
        "port": port
    }

    return settings

def update_ui(mode_var, join_frame, host_frame, port_var, port_host_var, username_entry, host_join_var):
    """Updates the UI based on the selected mode (Join or Host)."""
    if mode_var.get() == "Join":
        join_frame.pack(pady=10)
        host_frame.pack_forget()
        port_var.set(port_host_var.get())  # Sync port field
        username_entry.pack()  # Show username entry
    else:
        host_frame.pack(pady=10)
        join_frame.pack_forget()
        port_host_var.set(port_var.get())  # Sync port field
        if host_join_var.get():
            username_entry.pack()  # Show username entry if "Also Join" is checked
        else:
            username_entry.pack_forget()  # Hide username entry if only hosting

def main():
    """Initializes and runs the Tkinter launcher and returns user settings."""
    root = tk.Tk()
    root.title("Game Launcher")
    root.geometry("350x300")

    # Variables
    username_var = tk.StringVar()
    mode_var = tk.StringVar(value="Join")
    ip_var = tk.StringVar()
    port_var = tk.StringVar()
    port_host_var = tk.StringVar()
    host_join_var = tk.IntVar()

    # Username
    tk.Label(root, text="Username:").pack(pady=5)
    username_entry = tk.Entry(root, textvariable=username_var)
    username_entry.pack()

    # Join or Host selection
    tk.Label(root, text="Choose Mode:").pack(pady=5)
    mode_frame = tk.Frame(root)
    mode_frame.pack()

    join_radio = ttk.Radiobutton(mode_frame, text="Join", variable=mode_var, value="Join")
    join_radio.grid(row=0, column=0, padx=10)

    host_radio = ttk.Radiobutton(mode_frame, text="Host", variable=mode_var, value="Host")
    host_radio.grid(row=0, column=1, padx=10)

    # Join options (IP & Port)
    join_frame = tk.Frame(root)
    tk.Label(join_frame, text="IP Address:").pack()
    ip_entry = tk.Entry(join_frame, textvariable=ip_var)
    ip_entry.pack()

    tk.Label(join_frame, text="Port:").pack()
    port_entry = tk.Entry(join_frame, textvariable=port_var)
    port_entry.pack()

    # Host options (Port & Host+Join checkbox)
    host_frame = tk.Frame(root)
    tk.Label(host_frame, text="Port:").pack()
    port_host_entry = tk.Entry(host_frame, textvariable=port_host_var)
    port_host_entry.pack()

    host_join_check = tk.Checkbutton(host_frame, text="Also Join", variable=host_join_var, command=lambda: update_ui(mode_var, join_frame, host_frame, port_var, port_host_var, username_entry, host_join_var))
    host_join_check.pack()

    # Bind mode change to update UI
    mode_var.trace_add("write", lambda *args: update_ui(mode_var, join_frame, host_frame, port_var, port_host_var, username_entry, host_join_var))

    # Start button
    def on_start():
        settings = get_settings(username_var, mode_var, ip_var, port_var, port_host_var, host_join_var)
        if settings:
            root.quit()  # Only quit if settings are valid

    start_button = tk.Button(root, text="Start Game", command=on_start)
    start_button.pack(pady=20)

    # Initialize UI
    update_ui(mode_var, join_frame, host_frame, port_var, port_host_var, username_entry, host_join_var)

    # Run Tkinter main loop
    root.mainloop()

    return get_settings(username_var, mode_var, ip_var, port_var, port_host_var, host_join_var)

if __name__ == "__main__":
    settings = main()
    print(settings)  # Print settings for debugging
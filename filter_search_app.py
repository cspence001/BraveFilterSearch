import tkinter as tk
from tkinter import ttk, messagebox
import requests
import os
import sys
import signal

# Directory to store local content
LOCAL_CONTENT_DIR = "local_content"

# Fetch JSON data from a URL
def fetch_json_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching JSON data: {e}")
        return []

# Fetch the content from a URL and save it locally
def fetch_and_save_url_content(url, filename):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        content_type = response.headers.get('Content-Type', '')
        if 'text' not in content_type:
            print(f"Skipping non-text content from {url}")
            return None
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(response.text)
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

# Load the content from a local file
def load_local_content(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return None

# Search for the keyword in the content
def search_in_content(content, keyword):
    if not content:
        return []

    lines = content.splitlines()
    filtered_lines = [line for line in lines if keyword.lower() in line.lower() and not line.strip().startswith('!')]
    return filtered_lines

# Update the results based on selected checkboxes and keyword
def update_results():
    keyword = keyword_var.get()
    selected_uuids = [uuid for uuid, var in check_vars.items() if var.get()]

    result_text.delete(1.0, tk.END)

    if not selected_uuids:
        result_text.insert(tk.END, "Please select at least one filter.")
        return

    # Dictionary to keep track of which URLs correspond to which titles
    url_title_mapping = {}

    for uuid in selected_uuids:
        for item in data:
            if item['uuid'] == uuid:
                list_title = item.get('title', 'No Title')
                result_text.insert(tk.END, f"\n\n--- List Title: {list_title} ---\n\n", "list_title")

                for source in item.get('sources', []):
                    url = source.get('url')
                    title = source.get('title', 'No Title')  # Provide a default title if missing
                    if url:
                        url_title_mapping[url] = title
                        filename = os.path.join(LOCAL_CONTENT_DIR, f"{uuid}_{title}.txt")
                        if not os.path.exists(filename):
                            content = fetch_and_save_url_content(url, filename)
                        else:
                            content = load_local_content(filename)

                        if content is None:
                            result_text.insert(tk.END, f"\n\n--- Failed to load content from {url} ({title}) ---\n\n", "url")
                            continue

                        filtered_lines = search_in_content(content, keyword)

                        if filtered_lines:
                            result_text.insert(tk.END, f"\n\n--- Content from {url} ({title}) ---\n\n", "url")
                            result_text.insert(tk.END, f"--- Filter: {title} ---\n\n", "uuid_title")  # Use the title from the source
                            for line in filtered_lines:
                                result_text.insert(tk.END, line + "\n")

    if result_text.get(1.0, tk.END).strip() == "":
        result_text.insert(tk.END, "No results found.")

# Function to handle checkbox state change
def on_checkbox_change(*args):
    update_results()

# Function to handle keyword entry change
def on_keyword_change(*args):
    update_results()

# Function to clean up local files
def cleanup_local_content():
    if os.path.exists(LOCAL_CONTENT_DIR):
        for filename in os.listdir(LOCAL_CONTENT_DIR):
            file_path = os.path.join(LOCAL_CONTENT_DIR, filename)
            os.remove(file_path)
        os.rmdir(LOCAL_CONTENT_DIR)

def exit_program():
    cleanup_local_content()
    root.destroy()

def signal_handler(signal, frame):
    print("\nSignal received, cleaning up...")
    cleanup_local_content()
    sys.exit(0)

def build_gui():
    global check_vars, keyword_var, result_text, data, root

    root = tk.Tk()
    root.title("Filter Search App")

    # Create local content directory if it doesn't exist
    if not os.path.exists(LOCAL_CONTENT_DIR):
        os.makedirs(LOCAL_CONTENT_DIR)

    # Fetch JSON data from URL
    url = "https://raw.githubusercontent.com/brave/adblock-resources/master/filter_lists/list_catalog.json"
    global data
    data = fetch_json_data(url)

    if not data:
        messagebox.showerror("Error", "Failed to load data.")
        root.destroy()
        return

    # Create a frame for the checkboxes and result area
    left_frame = ttk.Frame(root, padding="10")
    left_frame.grid(row=0, column=0, sticky="nsew")

    right_frame = ttk.Frame(root, padding="10")
    right_frame.grid(row=0, column=1, sticky="nsew")

    # Create canvas and scrollbar for checkboxes
    canvas = tk.Canvas(left_frame)
    scrollbar = tk.Scrollbar(left_frame, orient="vertical", command=canvas.yview)
    checkbox_frame = ttk.Frame(canvas)

    # Add a window to the canvas for the checkbox frame
    canvas.create_window((0, 0), window=checkbox_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")

    # Add checkboxes to the checkbox frame
    check_vars = {}
    for item in data:
        uuid = item['uuid']
        title = item.get('title', 'No Title')  # Provide a default title if missing
        var = tk.IntVar()
        check_vars[uuid] = var
        cb = ttk.Checkbutton(checkbox_frame, text=title, variable=var, command=on_checkbox_change)
        cb.pack(anchor="w", padx=5, pady=2)

    # Update the scroll region of the canvas when the frame is resized
    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    checkbox_frame.bind("<Configure>", on_frame_configure)

    # Entry for keyword
    ttk.Label(right_frame, text="Keyword:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    keyword_var = tk.StringVar()
    keyword_var.trace_add("write", on_keyword_change)
    keyword_entry = ttk.Entry(right_frame, textvariable=keyword_var, width=50)
    keyword_entry.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

    # Create a frame for the result text and scrollbar
    result_frame = ttk.Frame(right_frame)
    result_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

    # Create the text widget for results
    result_text = tk.Text(result_frame, wrap=tk.WORD, width=80, height=20)
    result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Create and place the scrollbar
    result_scrollbar = tk.Scrollbar(result_frame, orient="vertical", command=result_text.yview)
    result_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Link the scrollbar with the text widget
    result_text.configure(yscrollcommand=result_scrollbar.set)

    # Configure tags for result_text
    result_text.tag_configure("url", foreground="blue")
    result_text.tag_configure("uuid_title", foreground="yellow")
    result_text.tag_configure("list_title", foreground="orange")

    # Adjust grid weights to make sure the widgets expand properly
    root.grid_rowconfigure(0, weight=1)  # Main row
    root.grid_columnconfigure(0, weight=1)  # Left column (checkboxes)
    root.grid_columnconfigure(1, weight=2)  # Right column (results)

    left_frame.grid_rowconfigure(0, weight=1)
    left_frame.grid_columnconfigure(0, weight=1)

    right_frame.grid_rowconfigure(2, weight=1)
    right_frame.grid_columnconfigure(0, weight=1)

    # Set the close event to clean up local content
    root.protocol("WM_DELETE_WINDOW", exit_program)

    # Set up signal handler for interrupts
    signal.signal(signal.SIGINT, signal_handler)

    # Start the main loop
    root.mainloop()

if __name__ == "__main__":
    build_gui()

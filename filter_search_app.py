import tkinter as tk
from tkinter import ttk, messagebox
import requests
import os
import sys
import signal
import json

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

# Load the active filters
def load_active_filters():
    input_file_path = os.path.expanduser('~/Library/Application Support/BraveSoftware/Brave-Browser/Local State')
    try:
        with open(input_file_path, 'r') as file:
            raw_content = file.read()
        json_start_index = raw_content.find('{')
        json_string = raw_content[json_start_index:]
        data = json.loads(json_string)
        active_filters = [
            uuid for uuid, details in data['brave']['ad_block']['regional_filters'].items()
            if details.get('enabled')
        ]
        return active_filters
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading active filters: {e}")
        return []

# Function to toggle active filters
def toggle_active_filters(var):
    if var.get():
        active_filters = load_active_filters()
        for uuid in check_vars:
            check_vars[uuid].set(1 if uuid in active_filters else 0)
    else:
        for uuid in check_vars:
            check_vars[uuid].set(0)
    update_results()  # Call to update the results after toggling filters

# Load custom filters
def load_custom_filters():
    input_file_path = os.path.expanduser('~/Library/Application Support/BraveSoftware/Brave-Browser/Local State')
    try:
        with open(input_file_path, 'r') as file:
            raw_content = file.read()
        json_start_index = raw_content.find('{')
        json_string = raw_content[json_start_index:]
        data = json.loads(json_string)
        custom_filters = data['brave']['ad_block'].get('custom_filters', '').strip().splitlines()
        return [filter for filter in custom_filters if filter]
    except Exception as e:
        print(f"Error loading custom filters: {e}")
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
    global current_filters  # Make current_filters accessible globally
    keyword = keyword_var.get()
    selected_uuids = [uuid for uuid, var in check_vars.items() if var.get()]
    custom_filters_enabled = custom_filters_var.get() == 1

    result_text.delete(1.0, tk.END)
    current_filters = []

    if not selected_uuids and not custom_filters_enabled:
        result_text.insert(tk.END, "Please select at least one filter or enable custom filters.")
        return

    # If custom filters are enabled, add them to the results
    if custom_filters_enabled:
        custom_filters = load_custom_filters()
        # If there's no keyword, show all custom filters
        if keyword:
            filtered_custom_filters = search_in_content("\n".join(custom_filters), keyword)
        else:
            filtered_custom_filters = custom_filters  # Show all if no keyword

        if filtered_custom_filters:
            result_text.insert(tk.END, "\n\n--- Custom Filters ---\n\n")
            for filter in filtered_custom_filters:
                result_text.insert(tk.END, filter + "\n")
                current_filters.append(filter)  # Keep track of custom filters

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
                                current_filters.append(line)  # Add filtered lines to current filters

    if not current_filters:
        result_text.insert(tk.END, "No results found.")

def compare_filters(new_filter_text):

    new_filters = new_filter_text.strip().splitlines()

    # Ensure both filters are enabled
    if active_filters_var.get() == 0:
        active_filters_var.set(1)  # Enable "Show My Active Filters"
        toggle_active_filters(active_filters_var)  # Load active filters

    if custom_filters_var.get() == 0:
        custom_filters_var.set(1)  # Enable "My Custom Filters"
        # Load custom filters if not already loaded
        update_results()  # This will also load custom filters into results

    # Clear previous results
    compare_results_text.delete(1.0, tk.END)

    if not new_filters:
        messagebox.showinfo("Info", "Please enter filters to compare.")
        return

    # Now both filters are guaranteed to be enabled
    for new_filter in new_filters:
        if new_filter in current_filters:
            # Highlight duplicate filters in red
            compare_results_text.insert(tk.END, f"{new_filter}\n", "duplicate_filter")
        else:
            # Highlight new filters in green
            compare_results_text.insert(tk.END, f"{new_filter}\n", "new_filter")

    # Configure tags for highlighting
    compare_results_text.tag_configure("new_filter", foreground="green")
    compare_results_text.tag_configure("duplicate_filter", foreground="red")


def add_new_filters(new_filters):
    input_file_path = os.path.expanduser('~/Library/Application Support/BraveSoftware/Brave-Browser/Local State')

    try:
        with open(input_file_path, 'r') as file:
            raw_content = file.read()

        json_start_index = raw_content.find('{')
        json_string = raw_content[json_start_index:]
        data = json.loads(json_string)

        # Get existing custom filters
        existing_custom_filters = data['brave']['ad_block'].get('custom_filters', '').strip().splitlines()

        # Create a set for fast lookup of existing filters
        existing_filter_set = set(existing_custom_filters)

        # Keep track of whether we have added any new filters
        new_filters_added = False

        # Append new filters while avoiding duplicates
        for new_filter in new_filters:
            if new_filter and new_filter not in existing_filter_set:
                existing_custom_filters.append(new_filter)
                new_filters_added = True  # Mark that a new filter was added

        if not new_filters_added:
            messagebox.showinfo("Info", "No new Filters to Add.")
            return

        # Update the custom filters in the data
        data['brave']['ad_block']['custom_filters'] = "\n".join(existing_custom_filters)

        # Save the updated data back to the file
        with open(input_file_path, 'w') as file:
            file.write(json.dumps(data, indent=4))

        messagebox.showinfo("Success", "New filters added successfully!")

    except Exception as e:
        print(f"Error adding new filters: {e}")
        messagebox.showerror("Error", "Failed to add new filters.")


def create_filter_comparison_frame(right_frame):
    global filter_comparison_frame, filter_text, compare_results_text, filter_button

    filter_comparison_frame = ttk.Frame(right_frame)
    filter_comparison_frame.grid(row=3, column=1, padx=10, pady=5, sticky="nsew")

    # Button to toggle visibility of the filter comparison section
    filter_button = ttk.Button(filter_comparison_frame, text="Load Custom Filters", command=toggle_filter_frame)
    filter_button.pack(pady=5)

    # Create a frame for the additional filters
    comparison_content_frame = ttk.LabelFrame(filter_comparison_frame, text="Add Custom Filters", padding="10")
    comparison_content_frame.pack(padx=5, pady=5, fill="both", expand=True)

    # Text area for user to paste additional filters
    filter_text = tk.Text(comparison_content_frame, height=20, width=50)
    filter_text.pack(padx=5, pady=5)

    # Button to compare filters
    compare_button = ttk.Button(comparison_content_frame, text="Compare Filters", command=lambda: compare_filters(filter_text.get("1.0", tk.END)))
    compare_button.pack(pady=5)

    # New results box for comparison results
    compare_results_text = tk.Text(comparison_content_frame, height=20, width=50, wrap=tk.WORD)
    compare_results_text.pack(padx=5, pady=5)

    # Add the note
    note_label = ttk.Label(comparison_content_frame, text="Ensure Brave Browser Application is closed before Adding new Filters", foreground="red")
    note_label.pack(pady=5)

    # Button to add new filters
    add_filters_button = ttk.Button(comparison_content_frame, text="Add New Filters", command=lambda: add_new_filters(filter_text.get("1.0", tk.END).strip().splitlines()))
    add_filters_button.pack(pady=5)

    # Initially hide the comparison frame
    comparison_content_frame.pack_forget()


def toggle_filter_frame():
    if filter_button['text'] == "Load Custom Filters":
        filter_button['text'] = "Hide Custom Filters"
        filter_comparison_frame.children['!labelframe'].pack(padx=5, pady=5, fill="both", expand=True)
    else:
        filter_button['text'] = "Load Custom Filters"
        filter_comparison_frame.children['!labelframe'].pack_forget()

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
    global check_vars, keyword_var, result_text, data, root, custom_filters_var, current_filters, active_filters_var, custom_filters_var
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
    left_frame.pack(side="left", fill="both", expand=True)

    right_frame = ttk.Frame(root, padding="10")
    right_frame.pack(side="right", fill="both", expand=True)

    # Add the filter comparison frame
    create_filter_comparison_frame(right_frame)

    # Create a frame for the active filters checkbox
    active_filters_frame = ttk.Frame(right_frame)
    active_filters_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

    # Create a frame for the active filters checkbox
    active_filters_var = tk.IntVar()
    active_filters_checkbox = ttk.Checkbutton(active_filters_frame, text="Show My Active Filters", variable=active_filters_var, command=lambda: toggle_active_filters(active_filters_var))
    active_filters_checkbox.grid(row=0, column=0, sticky="w")

    # Add the checkbox
    custom_filters_var = tk.IntVar()
    custom_filters_checkbox = ttk.Checkbutton(active_filters_frame, text="My Custom Filters", variable=custom_filters_var, command=on_checkbox_change)
    custom_filters_checkbox.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    # Create canvas and scrollbar for checkboxes
    canvas = tk.Canvas(left_frame)
    scrollbar = tk.Scrollbar(left_frame, orient="vertical", command=canvas.yview)
    checkbox_frame = ttk.Frame(canvas)

    # Add a window to the canvas for the checkbox frame
    canvas.create_window((0, 0), window=checkbox_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

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
    ttk.Label(right_frame, text="Keyword:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    keyword_var = tk.StringVar()
    keyword_var.trace_add("write", on_keyword_change)
    keyword_entry = ttk.Entry(right_frame, textvariable=keyword_var, width=50)
    keyword_entry.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

    # Create a frame for the result text and scrollbar
    result_frame = ttk.Frame(right_frame)
    result_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

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

    right_frame.grid_rowconfigure(3, weight=1)
    right_frame.grid_columnconfigure(0, weight=1)

    # Set the close event to clean up local content
    root.protocol("WM_DELETE_WINDOW", exit_program)

    # Set up signal handler for interrupts
    signal.signal(signal.SIGINT, signal_handler)

    # Start the main loop
    root.mainloop()

if __name__ == "__main__":
    build_gui()

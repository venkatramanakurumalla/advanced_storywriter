import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import json
import random
import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
from tkinter import ttk  # For progress bar

# Load the tokenizer and model
tokenizer = GPT2Tokenizer.from_pretrained("distilgpt2")
model = GPT2LMHeadModel.from_pretrained("distilgpt2")

# Ensure pad_token_id is set
if tokenizer.pad_token_id is None:
    tokenizer.pad_token_id = tokenizer.eos_token_id

# Function to load story elements data
def load_story_data(file_path='story.json'):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        messagebox.showerror("Error", "The JSON file is empty or not properly formatted.")
        return {"settings": [], "characters": [], "plot_twists": []}
    except FileNotFoundError:
        messagebox.showerror("Error", "The JSON file was not found.")
        return {"settings": [], "characters": [], "plot_twists": []}

# Load initial story elements
story_data = load_story_data()

# Function to retrieve elements from the dataset
def retrieve_story_elements():
    setting = random.choice(story_data['settings']) if story_data['settings'] else ""
    character = random.choice(story_data['characters']) if story_data['characters'] else ""
    plot_twist = random.choice(story_data['plot_twists']) if story_data['plot_twists'] else ""
    return setting, character, plot_twist

# Function to generate story text with RAG
def generate_story(prompt, base_story, max_length=100, num_iterations=10, temperature=0.7, top_k=50, top_p=0.9):
    try:
        setting, character, plot_twist = retrieve_story_elements()
        story = f"{prompt} {base_story} {setting} with {character} who {plot_twist}. "
        input_ids = tokenizer.encode(story, return_tensors='pt')

        for _ in range(num_iterations):
            attention_mask = (input_ids != tokenizer.pad_token_id).long()

            output = model.generate(
                input_ids,
                attention_mask=attention_mask,
                max_length=len(input_ids[0]) + max_length,
                pad_token_id=tokenizer.eos_token_id,
                do_sample=True,
                top_k=top_k,
                top_p=top_p,
                temperature=temperature,
                no_repeat_ngram_size=2,
                early_stopping=True
            )

            output_text = tokenizer.decode(output[0], skip_special_tokens=True)
            story = output_text
            input_ids = tokenizer.encode(story, return_tensors='pt')

        return story
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during story generation: {e}")
        return ""

# Function to handle story generation when the button is clicked
def generate_and_display_story():
    try:
        prompt = prompt_entry.get()
        max_length = int(length_entry.get())
        temperature = float(temp_entry.get())
        top_k = int(top_k_entry.get())
        top_p = float(top_p_entry.get())
        base_story = base_story_entry.get(1.0, tk.END).strip()

        # Validate inputs
        if not prompt:
            messagebox.showwarning("Input Error", "Please enter a story prompt.")
            return
        if not (0 < max_length <= 1024):
            messagebox.showwarning("Input Error", "Max length should be between 1 and 1024.")
            return
        if not (0.0 < temperature <= 1.0):
            messagebox.showwarning("Input Error", "Temperature should be between 0.1 and 1.0.")
            return
        if not (0 <= top_k <= 1000):
            messagebox.showwarning("Input Error", "Top-k should be between 0 and 1000.")
            return
        if not (0.0 <= top_p <= 1.0):
            messagebox.showwarning("Input Error", "Top-p should be between 0.0 and 1.0.")
            return

        # Show progress bar
        progress_bar.start()

        story = generate_story(prompt, base_story, max_length=max_length, temperature=temperature, top_k=top_k, top_p=top_p)

        # Hide progress bar
        progress_bar.stop()

        if story:
            output_textbox.delete(1.0, tk.END)
            output_textbox.insert(tk.END, story)
            # Save to story history
            story_history.insert(tk.END, f"{story}\n{'-'*40}\n")
        else:
            messagebox.showwarning("Generation Error", "No story was generated.")
    except ValueError:
        messagebox.showwarning("Input Error", "Please check your input values.")

# Function to load custom story data
def load_custom_story():
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
    if file_path:
        global story_data
        story_data = load_story_data(file_path)
        messagebox.showinfo("Success", "Custom story data loaded successfully.")

# Function to save the generated story to a file
def save_story():
    story = output_textbox.get(1.0, tk.END)
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'w') as file:
            file.write(story)

# Set up the main application window
app = tk.Tk()
app.title("Creative Story Writer")

# Create the prompt entry
prompt_label = tk.Label(app, text="Enter your story prompt:")
prompt_label.pack(pady=5)
prompt_entry = tk.Entry(app, width=50)
prompt_entry.pack(pady=5)

# Create the base story text area
base_story_label = tk.Label(app, text="Enter your base story (optional):")
base_story_label.pack(pady=5)
base_story_entry = scrolledtext.ScrolledText(app, wrap=tk.WORD, width=50, height=5)
base_story_entry.pack(pady=5)

# Create fields for advanced settings
length_label = tk.Label(app, text="Max Length:")
length_label.pack(pady=5)
length_entry = tk.Entry(app, width=10)
length_entry.pack(pady=5)
length_entry.insert(tk.END, '100')

temp_label = tk.Label(app, text="Temperature:")
temp_label.pack(pady=5)
temp_entry = tk.Entry(app, width=10)
temp_entry.pack(pady=5)
temp_entry.insert(tk.END, '0.7')

top_k_label = tk.Label(app, text="Top-k:")
top_k_label.pack(pady=5)
top_k_entry = tk.Entry(app, width=10)
top_k_entry.pack(pady=5)
top_k_entry.insert(tk.END, '50')

top_p_label = tk.Label(app, text="Top-p:")
top_p_label.pack(pady=5)
top_p_entry = tk.Entry(app, width=10)
top_p_entry.pack(pady=5)
top_p_entry.insert(tk.END, '0.9')

# Create the button to generate the story
generate_button = tk.Button(app, text="Generate Story", command=generate_and_display_story)
generate_button.pack(pady=10)

# Create the button to load custom story data
load_button = tk.Button(app, text="Load Custom Story Data", command=load_custom_story)
load_button.pack(pady=10)

# Create the button to save the story
save_button = tk.Button(app, text="Save Story", command=save_story)
save_button.pack(pady=10)

# Create the text area to display the generated story
output_textbox = scrolledtext.ScrolledText(app, wrap=tk.WORD, width=70, height=20)
output_textbox.pack(pady=20)

# Create the story history area
history_label = tk.Label(app, text="Story History (Current Session):")
history_label.pack(pady=5)
story_history = scrolledtext.ScrolledText(app, wrap=tk.WORD, width=70, height=10)
story_history.pack(pady=10)

# Add a progress bar
progress_bar = ttk.Progressbar(app, mode='indeterminate')
progress_bar.pack(pady=5)

# Run the application
app.mainloop()

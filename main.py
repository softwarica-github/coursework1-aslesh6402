import tkinter as tk
from tkinter import scrolledtext, messagebox, Checkbutton, IntVar, Entry, Label, Frame, Button, filedialog, simpledialog
from bs4 import BeautifulSoup
import requests
import csv
import json
import re

def scrape():
    url = url_entry.get()
    content = ""
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Scrape according to selected options
        if headline_var.get():
            content += "Headlines:\n" + '\n'.join([headline.text for headline in soup.find_all(['h1', 'h2', 'h3'])]) + "\n\n"
        
        if paragraph_var.get():
            content += "Paragraphs:\n" + '\n\n'.join([p.text for p in soup.find_all('p')]) + "\n\n"
        
        if link_var.get():
            content += "Links:\n" + '\n'.join([a['href'] for a in soup.find_all('a', href=True)]) + "\n\n"
        
        if image_var.get():
            content += "Images:\n" + '\n'.join([img['src'] for img in soup.find_all('img', src=True)]) + "\n\n"
        
        # Custom Tag/Element Extraction
        custom_tag = custom_tag_entry.get()
        if custom_tag:
            elements = soup.find_all(custom_tag)
            custom_content = '\n\n'.join([str(element) for element in elements])
            content += f"Custom {custom_tag} Elements:\n" + custom_content + "\n\n"
        
        result_area.delete(1.0, tk.END)
        result_area.insert(tk.INSERT, content)

    except Exception as e:
        messagebox.showerror("Error", "Failed to scrape the URL. Error: " + str(e))

def save_data():
    file_type = file_type_var.get()
    data = result_area.get(1.0, tk.END)
    if not data.strip():
        messagebox.showwarning("Warning", "No data to save!")
        return
    
    file_name = filedialog.asksaveasfilename(defaultextension=f".{file_type}",
                                             filetypes=[(f"{file_type.upper()} files", f"*.{file_type}")])
    
    if not file_name:
        return  # User cancelled save
    
    try:
        if file_type == 'csv':
            with open(file_name, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Content'])
                writer.writerow([data])

        elif file_type == 'json':
            with open(file_name, 'w', encoding='utf-8') as file:
                json.dump({"content": data}, file, ensure_ascii=False, indent=4)
        elif file_type == 'txt':
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(data)
        messagebox.showinfo("Success", f"Data successfully saved as {file_name}!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save file. Error: {e}")

# GUI setup
root = tk.Tk()
root.title("Advanced Web Scraper GUI")

frame = Frame(root)
frame.pack(padx=10, pady=10)

url_label = Label(frame, text="URL:")
url_label.pack(side=tk.LEFT)
url_entry = Entry(frame, width=50)
url_entry.pack(side=tk.LEFT)

scrape_button = Button(frame, text="Scrape", command=scrape)
scrape_button.pack(side=tk.LEFT, padx=5)

options_frame = Frame(root)
options_frame.pack(padx=10, pady=5)

headline_var = IntVar()
paragraph_var = IntVar()
link_var = IntVar()
image_var = IntVar()
Checkbutton(options_frame, text="Headlines", variable=headline_var).pack(side=tk.LEFT)
Checkbutton(options_frame, text="Paragraphs", variable=paragraph_var).pack(side=tk.LEFT)
Checkbutton(options_frame, text="Links", variable=link_var).pack(side=tk.LEFT)
Checkbutton(options_frame, text="Images", variable=image_var).pack(side=tk.LEFT)

custom_tag_frame = Frame(root)
custom_tag_frame.pack(padx=10, pady=5)
custom_tag_label = Label(custom_tag_frame, text="Custom Tag:")
custom_tag_label.pack(side=tk.LEFT)
custom_tag_entry = Entry(custom_tag_frame, width=20)
custom_tag_entry.pack(side=tk.LEFT)

save_frame = Frame(root)
save_frame.pack(padx=10, pady=5)

file_type_var = tk.StringVar(value='txt')
Button(save_frame, text="CSV", command=lambda: file_type_var.set('csv')).pack(side=tk.LEFT)
Button(save_frame, text="JSON", command=lambda: file_type_var.set('json')).pack(side=tk.LEFT)
Button(save_frame, text="TXT", command=lambda: file_type_var.set('txt')).pack(side=tk.LEFT)

save_button = Button(save_frame, text="Save Data", command=save_data)
save_button.pack(side=tk.RIGHT, padx=5)

result_area = scrolledtext.ScrolledText(root, width=60, height=20)
result_area.pack(padx=10, pady=5)

root.mainloop()

import tkinter as tk
import tkinter.font as font
import json

MAX_PEOPLE = 10  # Maximum number of people

# Function to set the font size for labels
def set_font_size(label, size):
    label['font'] = font.Font(size=size)


def calculate_shared_miles():
    try:
        miles_per_trip = float(trip_miles_entry.get())
        names_on_trip = name_entry.get().split(",")
        num_people_on_trip = len(names_on_trip)

        if num_people_on_trip > 0:
            shared_miles = miles_per_trip / num_people_on_trip
            for name in names_on_trip:
                name = name.strip().lower()  # Convert to lowercase
                if name in names:
                    person_idx = names.index(name)
                    total_miles[person_idx] += shared_miles
                else:
                    names.append(name)
                    total_miles.append(shared_miles)

            update_shared_miles_text()
            undo_actions.append(names_on_trip)
            undo_miles.append(shared_miles)
            save_data()
    except ValueError:
        pass

def calculate_gas_cost():
    try:
        total_gas_cost = float(total_cost_entry.get())
        total_miles_driven = float(total_miles_driven_entry.get())  # New entry for total miles driven
        cost_per_mile = total_gas_cost / total_miles_driven  # Calculate cost per mile
        cost_per_person = [round(cost_per_mile * miles, 2) for miles in total_miles]  # Calculate cost per person
        show_cost_per_person(cost_per_person)
    except ValueError:
        pass

def undo_action():
    if undo_actions and undo_miles:
        last_names = undo_actions.pop()
        last_miles = undo_miles.pop()
        for name in last_names:
            name = name.strip().lower()  # Convert to lowercase
            if name in names:
                person_idx = names.index(name)
                total_miles[person_idx] -= last_miles
        update_shared_miles_text()
        save_data()

def clear_all_miles():
    global total_miles, names
    total_miles = [0] * len(names)
    update_shared_miles_text()
    cost_per_person_text.config(text="Cost Per Person:")
    total_cost_entry.delete(0, tk.END)
    names = []  # Clear the names list
    save_data()

def clear_gas_cost():
    total_cost_entry.delete(0, tk.END)
    cost_per_person_text.config(text="Cost Per Person:")

def update_shared_miles_text():
    shared_miles_text.config(text="Shared Miles:")
    for name, miles in zip(names, total_miles):
        shared_miles_text.config(text=f"{shared_miles_text.cget('text')}\n{name}: {miles:.2f}")

def save_data():
    data = {'names': names, 'total_miles': total_miles}
    with open('shared_miles_data.json', 'w') as file:
        json.dump(data, file)

def load_data():
    try:
        with open('shared_miles_data.json', 'r') as file:
            data = json.load(file)
            return data['names'], data['total_miles']
    except FileNotFoundError:
        return [], []

def show_cost_per_person(cost_per_person):
    cost_per_person_text.config(text="Cost Per Person:")
    for name, cost in zip(names, cost_per_person):
        cost_per_person_text.config(text=f"{cost_per_person_text.cget('text')}\n{name}: ${cost:.2f}")

# Create the main window
root = tk.Tk()
root.title("Shared Miles Calculator")

# Initialize names list and total miles list
names, total_miles = load_data()
if not names:
    names = []
    total_miles = []

undo_actions = []
undo_miles = []

# Input fields for shared miles
name_label = tk.Label(root, text="Names on Trip (comma-separated):")
name_label.pack()
name_entry = tk.Entry(root)
name_entry.pack()
name_entry.config(width=30)  # Widen the entry box

trip_miles_label = tk.Label(root, text="Miles Driven on Trip:")
trip_miles_label.pack()
trip_miles_entry = tk.Entry(root)
trip_miles_entry.pack()
trip_miles_entry.config(width=30)  # Widen the entry box

calculate_button = tk.Button(root, text="Calculate Shared Miles", command=calculate_shared_miles)
calculate_button.pack(pady=10)  # Add spacing

undo_button = tk.Button(root, text="Undo", command=undo_action)
undo_button.pack(pady=10)  # Add spacing

clear_miles_button = tk.Button(root, text="Clear All Miles", command=clear_all_miles)
clear_miles_button.pack(pady=10)  # Add spacing

shared_miles_text = tk.Label(root, text="Shared Miles:")
shared_miles_text.pack()
set_font_size(shared_miles_text, 16)  # Set font size to 16

# Input fields for gas cost
total_cost_label = tk.Label(root, text="Total Gas Cost:")
total_cost_label.pack()
total_cost_entry = tk.Entry(root)
total_cost_entry.pack()
total_cost_entry.config(width=30)  # Widen the entry box

total_miles_driven_label = tk.Label(root, text="Total Miles Driven in Trip:")
total_miles_driven_label.pack()
total_miles_driven_entry = tk.Entry(root)
total_miles_driven_entry.pack()
total_miles_driven_entry.config(width=30)  # Widen the entry box

calculate_cost_button = tk.Button(root, text="Calculate Gas Cost", command=calculate_gas_cost)
calculate_cost_button.pack(pady=10)  # Add spacing

clear_gas_cost_button = tk.Button(root, text="Clear Gas Cost", command=clear_gas_cost)
clear_gas_cost_button.pack(pady=10)  # Add spacing

cost_per_person_text = tk.Label(root, text="Cost Per Person:")
cost_per_person_text.pack()
set_font_size(cost_per_person_text, 16)  # Set font size to 16

# Update the shared miles and cost per mile texts
update_shared_miles_text()
show_cost_per_person([])

# Start the main loop
root.mainloop()
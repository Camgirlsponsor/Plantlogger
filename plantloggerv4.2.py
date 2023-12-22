import tkinter as tk
from tkinter import ttk, filedialog
from datetime import datetime

class PlantLogger:
    def __init__(self, root):
        self.root = root
        self.root.title("Plant Logger V4.2 by CRP9")

        # Variables to store plant information
        self.plant_name_var = tk.StringVar()
        self.start_date_var = tk.StringVar()
        self.watering_date_var = tk.StringVar()
        self.nutrient_date_var = tk.StringVar()
        self.flower_date_var = tk.StringVar()
        self.custom_date_var = tk.StringVar()
        self.custom_action_var = tk.StringVar()
        self.log_text = tk.Text(root, height=20, width=60, state="disabled")
        self.log_text.grid(row=0, column=4, rowspan=9, padx=10, pady=5)

        # Create and pack labels
        ttk.Label(root, text="Plant Name:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        ttk.Label(root, text="Plant Start Date:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        ttk.Label(root, text="Last Watering Date:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        ttk.Label(root, text="Last Nutrient Date:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        ttk.Label(root, text="Switched to Flower Date:").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        ttk.Label(root, text="Custom Date and Time:").grid(row=5, column=0, sticky="w", padx=10, pady=5)
        ttk.Label(root, text="Custom Action:").grid(row=6, column=0, sticky="w", padx=10, pady=5)

        # Create and pack entry widgets
        ttk.Entry(root, textvariable=self.plant_name_var).grid(row=0, column=1, padx=10, pady=5)
        ttk.Entry(root, textvariable=self.start_date_var, state="readonly").grid(row=1, column=1, padx=10, pady=5)
        ttk.Entry(root, textvariable=self.watering_date_var, state="readonly").grid(row=2, column=1, padx=10, pady=5)
        ttk.Entry(root, textvariable=self.nutrient_date_var, state="readonly").grid(row=3, column=1, padx=10, pady=5)
        ttk.Entry(root, textvariable=self.flower_date_var, state="readonly").grid(row=4, column=1, padx=10, pady=5)
        ttk.Entry(root, textvariable=self.custom_date_var).grid(row=5, column=1, padx=10, pady=5)

        # Create and pack dropdown box for custom actions
        custom_actions = ["Watering", "Nutrients", "Other", "Plant Start Date"]
        ttk.Combobox(root, textvariable=self.custom_action_var, values=custom_actions).grid(row=6, column=1, padx=10, pady=5)

        # Create and pack buttons
        ttk.Button(root, text="Set Start Date", command=self.set_start_date).grid(row=1, column=2, padx=10, pady=5)
        ttk.Button(root, text="Log Watering", command=self.log_watering).grid(row=2, column=2, padx=10, pady=5)
        ttk.Button(root, text="Log Nutrient", command=self.log_nutrient).grid(row=3, column=2, padx=10, pady=5)
        ttk.Button(root, text="Log Flower Date", command=self.log_flower_date).grid(row=4, column=2, padx=10, pady=5)
        ttk.Button(root, text="Log Custom Date", command=self.log_custom_date).grid(row=5, column=2, padx=10, pady=5)

        # Create and pack buttons for saving and loading
        ttk.Button(root, text="Save Logs", command=self.save_logs).grid(row=7, column=0, padx=10, pady=5, sticky="w")
        ttk.Button(root, text="Load Logs", command=self.load_logs).grid(row=7, column=1, padx=10, pady=5, sticky="w")

        # Load logs on startup
        self.load_logs()

    def set_start_date(self):
        start_date = self.get_current_date()
        self.start_date_var.set(start_date)
        self.log_action("Set Start Date")

    def log_watering(self):
        watering_date = self.get_current_date()
        self.watering_date_var.set(watering_date)
        self.log_action("Log Watering")

    def log_nutrient(self):
        nutrient_date = self.get_current_date()
        self.nutrient_date_var.set(nutrient_date)
        self.log_action("Log Nutrient")

    def log_flower_date(self):
        flower_date = self.get_current_date()
        self.flower_date_var.set(flower_date)
        self.log_action("Log Flower Date")

    def log_custom_date(self):
        custom_date_str = self.custom_date_var.get()
        custom_action = self.custom_action_var.get()
        if custom_action:
            try:
                custom_date = datetime.strptime(custom_date_str, "%Y-%m-%d %H:%M:%S")
                log_message = f"{self.get_plant_name()} - Log {custom_action}: {custom_date.strftime('%Y-%m-%d %H:%M:%S')}\n"
                self.log_text.configure(state="normal")
                self.log_text.insert(tk.END, log_message)
                self.log_text.configure(state="disabled")
            except ValueError:
                tk.messagebox.showerror("Error", "Invalid date and time format. Please use 'YYYY-MM-DD HH:mm:SS'.")
        else:
            tk.messagebox.showwarning("Warning", "Please select a custom action.")

    def get_current_date(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_plant_name(self):
        plant_name = self.plant_name_var.get()
        return plant_name if plant_name else "Unnamed Plant"

    def log_action(self, action):
        plant_name = self.get_plant_name()
        log_message = f"{plant_name} - {action}: {self.get_current_date()}\n"
        self.log_text.configure(state="normal")
        self.log_text.insert(tk.END, log_message)
        self.log_text.configure(state="disabled")

    def save_logs(self):
        try:
            filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
            if filename:
                with open(filename, "w") as file:
                    file.write(self.log_text.get("1.0", tk.END))
                tk.messagebox.showinfo("Success", "Logs saved successfully.")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Error saving logs: {e}")

    def load_logs(self):
        try:
            filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
            if filename:
                with open(filename, "r") as file:
                    logs = file.read()
                    self.log_text.configure(state="normal")
                    self.log_text.delete("1.0", tk.END)
                    self.log_text.insert(tk.END, logs)
                    self.log_text.configure(state="disabled")
                tk.messagebox.showinfo("Success", "Logs loaded successfully.")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Error loading logs: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PlantLogger(root)
    root.mainloop()

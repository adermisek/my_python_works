import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from file_handler import FileHandler
from data_processor import DataProcessor

class ExcelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Excel Data Viewer")
        self.root.geometry("700x600")

        self.create_widgets()
        self.df = None
        self.filepath = ""

    def create_widgets(self):
        """Kreira sve GUI elemente"""
        self.frame_top = ttk.Frame(self.root, padding=10)
        self.frame_top.pack(fill=tk.X)

        self.load_button = ttk.Button(self.frame_top, text="Load Excel File", command=self.load_file)
        self.load_button.pack(side=tk.LEFT, padx=5)

        self.process_button = ttk.Button(self.frame_top, text="Filter & Save", command=self.process_data, state=tk.DISABLED)
        self.process_button.pack(side=tk.LEFT, padx=5)

        self.chart_button = ttk.Button(self.frame_top, text="Prikaži graf", command=self.show_salary_chart, state=tk.DISABLED)
        self.chart_button.pack(side=tk.LEFT, padx=5)

        self.label_path = ttk.Label(self.frame_top, text="No file loaded", foreground="red")
        self.label_path.pack(side=tk.LEFT, padx=10)

        self.frame_bottom = ttk.LabelFrame(self.root, text="Sheets", padding=10)
        self.frame_bottom.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.sheet_list = tk.Listbox(self.frame_bottom, height=5)
        self.sheet_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.status_label = ttk.Label(self.root, text="", foreground="blue", font=("Arial",12,"bold"))
        self.status_label.pack(pady=5)

    def load_file(self):
        """Učitava Excel fajl i prikazuje sheetove"""
        self.df, self.filepath = FileHandler.load_excel_file(self)
        if self.df is not None:
            self.display_message("File učitan! Klikni 'Filter & Save' ili 'Prikaži graf'")
            self.process_button.config(state=tk.NORMAL)
            self.chart_button.config(state=tk.NORMAL)

    def process_data(self):
        """Manipulira podacima i sprema isfiltrirani file"""
        if self.df is not None:
            df_filtered, grouped, grouped_dep, df_neto = DataProcessor.manipulate(self.df)
            output_path = DataProcessor.save_to_excel(df_filtered, grouped, grouped_dep, df_neto)
            self.display_message(f"File spremljen: {output_path}")

    def show_salary_chart(self):
        """Prikazuje grafikon za 10 najvećih novih plaća sa starim plaćama"""
        if self.df is not None:
            df_top10 = self.df.nlargest(10, "New_Salary")  # Uzmi top 10 po novoj plaći
            
            names = df_top10["Full_Name"]  # Imena zaposlenika
            old_salaries = df_top10["Salary"]
            new_salaries = df_top10["New_Salary"]

            fig, ax = plt.subplots(figsize=(8, 5))
            bar_width = 0.4  # Širina stupaca

            indices = range(len(names))  # Indeksi za X-os
            ax.bar(indices, old_salaries, bar_width, label="Stara Plaća", color="red", alpha=0.6)
            ax.bar([i + bar_width for i in indices], new_salaries, bar_width, label="Nova Plaća", color="green", alpha=0.6)

            ax.set_xticks([i + bar_width / 2 for i in indices])  
            ax.set_xticklabels(names, rotation=45, ha="right")  

            ax.set_xlabel("Zaposlenici")
            ax.set_ylabel("Plaća")
            ax.set_title("Top 10 najvećih novih plaća vs. Stare plaće")
            ax.legend()

            # Prikaz grafike unutar Tkinter GUI-a
            if hasattr(self, 'canvas'):
                self.canvas.get_tk_widget().destroy()  # Ukloni prethodni graf ako postoji

            self.canvas = FigureCanvasTkAgg(fig, master=self.root)
            self.canvas.get_tk_widget().pack()
            self.canvas.draw()

    def update_sheets(self, sheet_names, filepath):
        """Ažurira listu sheetova u GUI-ju"""
        self.label_path.config(text=filepath.split("/")[-1], foreground = "black", font=("Arial",10))
        self.sheet_list.delete(0, tk.END)
        for sheet in sheet_names:
            self.sheet_list.insert(tk.END, sheet)

    def display_message(self, message):
        """Prikazuje status poruku"""
        self.status_label.config(text=message)

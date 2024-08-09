import customtkinter as ctk
import os
from pdf_to_audiobook import pdf_to_audiobook
import threading

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class PDFToAudiobookApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("PDF to Audiobook Converter")
        self.geometry("700x600")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(self.main_frame, text="PDF to Audiobook Converter", 
                                        font=ctk.CTkFont(size=28, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 30), sticky="ew")

        # File selection frame
        self.file_frame = ctk.CTkFrame(self.main_frame)
        self.file_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.file_frame.grid_columnconfigure(1, weight=1)

        self.pdf_label = ctk.CTkLabel(self.file_frame, text="Input PDF:", anchor="w")
        self.pdf_label.grid(row=0, column=0, padx=(20, 10), pady=10, sticky="w")
        self.pdf_entry = ctk.CTkEntry(self.file_frame, placeholder_text="Select PDF File")
        self.pdf_entry.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="ew")
        self.pdf_button = ctk.CTkButton(self.file_frame, text="Browse", command=self.browse_pdf, width=100)
        self.pdf_button.grid(row=0, column=2, padx=(0, 20), pady=10)

        self.output_label = ctk.CTkLabel(self.file_frame, text="Output MP3:", anchor="w")
        self.output_label.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="w")
        self.output_entry = ctk.CTkEntry(self.file_frame, placeholder_text="Select Output File")
        self.output_entry.grid(row=1, column=1, padx=(0, 10), pady=10, sticky="ew")
        self.output_button = ctk.CTkButton(self.file_frame, text="Save As", command=self.save_output, width=100)
        self.output_button.grid(row=1, column=2, padx=(0, 20), pady=10)

        # Settings frame
        self.settings_frame = ctk.CTkFrame(self.main_frame)
        self.settings_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.settings_frame.grid_columnconfigure(1, weight=1)

        self.lang_label = ctk.CTkLabel(self.settings_frame, text="Language:", anchor="w")
        self.lang_label.grid(row=0, column=0, padx=(20, 10), pady=10, sticky="w")
        self.lang_combobox = ctk.CTkComboBox(self.settings_frame, 
                                             values=["English", "Spanish", "French", "German", "Italian", "Portuguese", "Chinese", "Japanese"])
        self.lang_combobox.grid(row=0, column=1, padx=(0, 20), pady=10, sticky="ew")

        self.chunk_label = ctk.CTkLabel(self.settings_frame, text="Chunk Size:", anchor="w")
        self.chunk_label.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="w")
        self.chunk_slider = ctk.CTkSlider(self.settings_frame, from_=100, to=1000, number_of_steps=18)
        self.chunk_slider.grid(row=1, column=1, padx=(0, 20), pady=10, sticky="ew")
        self.chunk_slider.set(500)
        self.chunk_value_label = ctk.CTkLabel(self.settings_frame, text="500")
        self.chunk_value_label.grid(row=1, column=2, padx=(0, 20), pady=10)
        self.chunk_slider.configure(command=self.update_chunk_value)

        # Convert button
        self.convert_button = ctk.CTkButton(self.main_frame, text="Convert to Audiobook", 
                                            command=self.start_conversion, height=40,
                                            font=ctk.CTkFont(size=16, weight="bold"))
        self.convert_button.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="ew")

        # Progress and status
        self.progress_bar = ctk.CTkProgressBar(self.main_frame)
        self.progress_bar.grid(row=4, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.progress_bar.set(0)

        self.status_label = ctk.CTkLabel(self.main_frame, text="Ready to convert", height=40,
                                         fg_color=("gray85", "gray25"), corner_radius=6)
        self.status_label.grid(row=5, column=0, padx=20, pady=(0, 20), sticky="ew")

    def update_chunk_value(self, value):
        self.chunk_value_label.configure(text=f"{int(value)}")

    def browse_pdf(self):
        filename = ctk.filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if filename:
            self.pdf_entry.delete(0, ctk.END)
            self.pdf_entry.insert(0, filename)

    def save_output(self):
        filename = ctk.filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 Files", "*.mp3")])
        if filename:
            self.output_entry.delete(0, ctk.END)
            self.output_entry.insert(0, filename)

    def start_conversion(self):
        pdf_path = self.pdf_entry.get()
        output_path = self.output_entry.get()
        lang = self.lang_combobox.get().lower()[:2]
        chunk_size = int(self.chunk_slider.get())

        if not pdf_path or not output_path:
            self.status_label.configure(text="Please select both input PDF and output MP3 file.")
            return

        self.convert_button.configure(state="disabled")
        self.progress_bar.set(0)
        self.status_label.configure(text="Converting... Please wait.")

        thread = threading.Thread(target=self.run_conversion, args=(pdf_path, output_path, lang, chunk_size))
        thread.start()

    def run_conversion(self, pdf_path, output_path, lang, chunk_size):
        try:
            pdf_to_audiobook(pdf_path, output_path, lang, chunk_size)
            self.after(0, self.conversion_complete)
        except Exception as e:
            self.after(0, self.conversion_error, str(e))

    def conversion_complete(self):
        self.progress_bar.set(1)
        self.status_label.configure(text="Conversion Complete! Your audiobook is ready.")
        self.convert_button.configure(state="normal")

    def conversion_error(self, error_message):
        self.status_label.configure(text=f"Error: {error_message}")
        self.convert_button.configure(state="normal")

if __name__ == "__main__":
    app = PDFToAudiobookApp()
    app.mainloop()
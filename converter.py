from PIL import Image
from pathlib import Path
from pillow_heif import register_heif_opener
from tqdm import tqdm
from argparse import ArgumentParser
import customtkinter
from tkinter import filedialog

register_heif_opener()

class HEICConverterApp(customtkinter.CTk):
    def __init__(self, delete_default=False):
        super().__init__()
        self.title("HEIC to JPEG Converter")
        self.geometry("800x250")

        # Configure layout: one column, stretch vertically
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)

        # Info label
        self.info_label = customtkinter.CTkLabel(
            self,
            text="Select the folder containing the HEIC files"
        )
        self.info_label.grid(row=0, column=0, pady=(15, 5), sticky="n")

        # Folder selector frame (centered layout)
        self.folder_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.folder_frame.grid(row=1, column=0, pady=5)

        self.folder_path_label = customtkinter.CTkLabel(self.folder_frame, text="No folder selected")
        self.folder_path_label.pack(side="left", padx=10)

        self.folder_button = customtkinter.CTkButton(
            self.folder_frame,
            text="Browse",
            command=self.select_folder
        )
        self.folder_button.pack(side="left", padx=10)

        # Convert button
        self.convert_button = customtkinter.CTkButton(
            self,
            text="Press to Convert",
            command=self.convert_heic
        )
        self.convert_button.grid(row=2, column=0, pady=5)

        # Delete checkbox
        self.delete_var = customtkinter.BooleanVar(value=delete_default)
        self.delete_checkbox = customtkinter.CTkCheckBox(
            self,
            text="Delete HEIC files after conversion",
            variable=self.delete_var
        )
        self.delete_checkbox.grid(row=3, column=0, pady=5)

        # Output labels
        self.start_output_label = customtkinter.CTkLabel(self, text="")
        self.start_output_label.grid(row=4, column=0, pady=5)

        self.end_output_label = customtkinter.CTkLabel(self, text="")
        self.end_output_label.grid(row=5, column=0, pady=5)

        # Store selected folder
        self.folder_path = None

    def select_folder(self):
        folder = filedialog.askdirectory(title="Select Folder")
        if folder:
            self.folder_path = folder
            self.folder_path_label.configure(text=folder)

    def convert_heic(self):
        if not self.folder_path:
            self.end_output_label.configure(text="No folder selected")
            return

        self.start_output_label.configure(text="Converting HEIC files to JPG...")
        self.update()  # Force GUI refresh

        files = list(Path(self.folder_path).glob("*.heic")) + list(Path(self.folder_path).glob("*.HEIC"))

        if not files:
            self.end_output_label.configure(text="No HEIC files found")
            return

        for f in tqdm(files):
            image = Image.open(str(f))
            image.convert('RGB').save(str(f.with_suffix('.jpg')))
            if self.delete_var.get():
                f.unlink()

        self.end_output_label.configure(text="Conversion complete!")

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-d", "--delete", action="store_true", help="Delete the file after conversion")
    params = parser.parse_args()

    # CustomTkinter appearance
    customtkinter.set_appearance_mode("System")
    customtkinter.set_default_color_theme("blue")

    # Run app
    app = HEICConverterApp(delete_default=params.delete)
    app.mainloop()

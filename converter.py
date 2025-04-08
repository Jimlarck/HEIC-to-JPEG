from PIL import Image
from pathlib import Path
from pillow_heif import register_heif_opener
from tqdm import tqdm
from argparse import ArgumentParser
import dearpygui.dearpygui as dpg

register_heif_opener()

# Create window
dpg.create_context()

def main(params):
    # Add GUI Components 
    with dpg.window(tag="Primary Window"): 
        dpg.add_text(tag="info", default_value="Place all HEIC files in the same folder as this program")
        dpg.add_button(label="Press to Convert", tag="convertbtn", callback=convertHEIC)
        dpg.add_checkbox(tag="delete_checkbox", label="Delete HEIC files after conversion", default_value=params.delete)
        dpg.add_text(tag="startoutput", default_value="")
        dpg.add_text(tag="endoutput", default_value="")

# Define conversion function here. 
def convertHEIC():
    dpg.set_value(item="startoutput", value="Converting HEIC files to JPG")
    files = list(Path(".").glob("*.heic")) + list(Path(".").glob("*.HEIC"))
    # Check that we have files to convert
    if len(files) == 0:
        dpg.set_value(item="endoutput", value="No HEIC files found")
        return
    else:
        dpg.set_value(item="endoutput", value="Completed!")
    # Convert
    for f in tqdm(files):
        image = Image.open(str(f))
        image.convert('RGB').save(str(f.with_suffix('.jpg')))
        if dpg.get_value("delete_checkbox"):
            f.unlink()

if __name__ == "__main__":
    parser = ArgumentParser()
    # delete option, default false
    parser.add_argument("-d", "--delete", action="store_true", help="Delete the file after conversion")
    params = parser.parse_args()
    main(params)

# Init dearpygui as a 600x200 window. 
dpg.create_viewport(title='HEIC to JPEG Converter', width=600, height=200)
dpg.setup_dearpygui()
dpg.show_viewport()
# Enable and set primary window to disable nested windows.
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()

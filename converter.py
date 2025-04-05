from PIL import Image
from pathlib import Path
from pillow_heif import register_heif_opener
from tqdm import tqdm
from argparse import ArgumentParser
import dearpygui.dearpygui as dpg
register_heif_opener()
# Create window viewport Converter
dpg.create_context()
dpg.create_viewport(title='Converter', width=600, height=400)
# Add GUI Components
def main(params):
    with dpg.window(label="Convert HEIC to JPEG", width=600, height=400):
        dpg.add_text(tag="info", default_value="Place all HEIC files in the same folder as this program")
        dpg.add_button(label="Press to Convert", tag="convertbtn",callback=convertHEIC)
        dpg.add_text(tag="startProcess", default_value="")
        dpg.add_text(tag="endProcess", default_value="")


def convertHEIC():
    dpg.set_value(item="startProcess", value="Converting HEIC files to JPG")
    files = list(Path(".").glob("*.heic")) + list(Path(".").glob("*.HEIC"))

    if len(files) == 0:
        dpg.set_value(item="endProcess", value="No HEIC files found")
        return
    else:
        dpg.set_value(item="endProcess",value="Completed!")

    for f in tqdm(files):
        image = Image.open(str(f))
        image.convert('RGB').save(str(f.with_suffix('.jpg')))
        if params.delete:
            f.unlink()


if __name__ == "__main__":
    parser = ArgumentParser()
    # delete option, default false
    parser.add_argument("-d", "--delete", action="store_true", help="Delete the file after conversion")
    params = parser.parse_args()
    main(params)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()


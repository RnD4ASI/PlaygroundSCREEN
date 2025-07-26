import time
import mss
import numpy as np
from PIL import Image
import os
import argparse
from datetime import datetime
import tkinter as tk

def get_imagehash(image):
    """
    Calculates the perceptual hash of an image.
    """
    # Convert to grayscale and resize
    image = image.convert("L").resize((16, 16), Image.LANCZOS)
    # Convert image to numpy array
    data = np.array(image.getdata()).reshape(16, 16)
    # Calculate the mean hash
    mean = data.mean()
    # Create the hash
    return (data > mean).flatten()

def select_area():
    """
    Allows the user to select a screen area using a GUI.
    """
    root = tk.Tk()
    root.attributes("-alpha", 0.3)
    root.attributes("-fullscreen", True)

    x, y, w, h = 0, 0, 0, 0
    area = {}

    def on_mouse_down(event):
        nonlocal x, y
        x, y = event.x, event.y
        canvas.create_rectangle(x, y, x, y, outline="red", width=2, tags="rect")

    def on_mouse_move(event):
        nonlocal w, h
        w, h = event.x - x, event.y - y
        canvas.coords("rect", x, y, x + w, y + h)

    def on_mouse_up(event):
        nonlocal area
        area = {"top": y, "left": x, "width": w, "height": h}
        root.quit()

    canvas = tk.Canvas(root, cursor="cross")
    canvas.pack(fill="both", expand=True)

    canvas.bind("<ButtonPress-1>", on_mouse_down)
    canvas.bind("<B1-Motion>", on_mouse_move)
    canvas.bind("<ButtonRelease-1>", on_mouse_up)

    root.mainloop()
    root.destroy()

    return area

def capture_and_save(area, output_folder):
    """
    Captures the screen area and saves it if the content has changed.
    """
    last_hash = None
    with mss.mss() as sct:
        while True:
            sct_img = sct.grab(area)
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")

            current_hash = get_imagehash(img)

            if current_hash != last_hash:
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
                filename = os.path.join(output_folder, f"{timestamp}.png")
                img.save(filename)
                print(f"Saved screenshot: {filename}")
                last_hash = current_hash

            time.sleep(0.1) # Adjust the interval as needed

def main():
    """
    Main function to run the screen capture program.
    """
    parser = argparse.ArgumentParser(description="Continuously capture a selected screen area.")
    parser.add_argument("output_folder", help="The folder to save the screenshots.")
    args = parser.parse_args()

    if not os.path.exists(args.output_folder):
        os.makedirs(args.output_folder)

    area = select_area()
    if area:
        capture_and_save(area, args.output_folder)

if __name__ == "__main__":
    main()

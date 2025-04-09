from PIL import Image, ImageTk
import os

def resize_image(size, image_url):
    """
    Resize image to the given size and return a Tk-compatible image.
    Args:
        size (tuple): (width, height)
        image_url (str): Relative path to image from project root
    Returns:
        ImageTk.PhotoImage or None if loading fails
    """
    try:
        # Get absolute path to the image
        base_path = os.path.dirname(os.path.abspath(__file__))
        abs_path = os.path.join(base_path, image_url)

        # Load and resize
        original_image = Image.open(abs_path)
        resized_image = original_image.resize(size, Image.LANCZOS)
        tk_image = ImageTk.PhotoImage(resized_image)
        return tk_image

    except Exception as e:
        print(f"[Image Error] Could not load '{image_url}' → {e}")
        return None


def centre_window(arg):
    pass  # You can fill this in later

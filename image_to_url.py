import base64

def load_png_as_base64(file):
    image_data = file.read()
    encoded_string = base64.b64encode(image_data)
    return encoded_string.decode("utf-8")
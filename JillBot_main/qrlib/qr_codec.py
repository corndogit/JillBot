import qrcode
from pyzbar.pyzbar import decode
from PIL import Image


def make_qr_code(data: str):
    """
    Turns string object into a QR code in PNG format.
    :param data string to encode
    :returns PilImage
    """
    image = qrcode.make(data)
    return image


def decode_qr_code(data):
    """| Finds QR code in image and decodes it using pyzbar library"""
    decode_qr = decode(Image.open(data))  # PIL.PngImagePlugin.PngImageFile
    try:
        return decode_qr[0].data.decode('utf-8')
    except IndexError:
        raise FileNotFoundError

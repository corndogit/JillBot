import qrcode
from pyzbar.pyzbar import decode
from PIL import Image


def make_qr_code(data: str):
    """
    Turns string object into a QR code in PNG format.

    :param data string to encode
    :returns: PilImage
    """
    image = qrcode.make(data)
    return image


def decode_qr_code(data):
    """
    Finds QR code in image and decodes it using pyzbar library

    :param data Image bytes
    :returns: String of the decoded bytes encoded in UTF-8
    """
    decode_qr = decode(Image.open(data))
    try:
        return decode_qr[0].data.decode('utf-8')
    except IndexError:
        raise FileNotFoundError

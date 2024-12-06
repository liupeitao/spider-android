import base64
import re
from pathlib import Path

import pytesseract
from PIL import Image

LOGIN_PATTERN = re.compile(r"Login code: (\d+)")
LOGIN_TIME = re.compile(r"(\d+:\d+\s?[PA]M).*Login code")
WEB_LOGIN_CODE = re.compile(r"login code: (\w+)")
WEB_LOGIN_CODE1 = re.compile(r"your login code:\s+(\w+)")
WEB_LOGIN_TIME = re.compile(r"(\d+:\d+\s?[PA]M) Web login code")

# Path to the image file
# image_path =Path( '/home/liupeitao/projects/lamda/partial.png')


def extract_varifycation(img: Path):
    # Open the image file
    image = Image.open(img)

    # Use pytesseract to do OCR on the image
    text = pytesseract.image_to_string(image, lang="eng")
    text = re.sub(r"\s+", " ", text)
    web_varify_date = None
    varify_date = None
    try:
        web_varify = WEB_LOGIN_CODE.search(text).group(1)
    except Exception:
        web_varify = None
    if web_varify is None:
        try:        
            web_varify = WEB_LOGIN_CODE1.search(text).group(1)
        except Exception:
            web_varify = None
    try:
        web_varify_date = WEB_LOGIN_TIME.search(text).group(1)
    except Exception:
        web_varify_date = None
    try:
        varify = LOGIN_PATTERN.search(text).group(1)
    except Exception:
        varify = None
    try:
        varify_date = LOGIN_TIME.search(text).group(1)
    except Exception:
        varify = None
    return {
        "varify": {"code": varify, "time": varify_date},
        "web_varify": {"code": web_varify, "time": web_varify_date},
        "raw": text,
        "img": base64.encodebytes(image.tobytes()).decode(),
    }


# image_path = Path("/home/liupeitao/projects/lamda/partial.png")
# res = extract_varifycation(img=image_path)
# print(res["varify"], res["web_varify"])

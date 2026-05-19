import pytesseract
from PIL import Image


def extract_text(image_path):

    image = Image.open(image_path)

    text = pytesseract.image_to_string(image)

    return text


if __name__ == "__main__":

    text = extract_text("../uploads/report.png")

    print(text)
import logging
import easyocr
from PIL import Image, ImageDraw, ImageFont
import numpy as np


# All possible stat rolls
possible_values = {
    "element damage dealt": [9.54, 10.94, 12.34, 13.75, 15.15, 16.55, 17.95, 19.35, 20.75, 22.15, 23.56, 24.96, 26.36, 27.76, 29.16],
    "max ammunition capacity": [27.84, 31.95, 36.06, 40.17, 44.28, 48.39, 52.50, 56.60, 60.71, 64.82, 68.93, 73.04, 77.15, 81.26, 85.37],
    "critical damage": [6.64, 7.62, 8.60, 9.58, 10.56, 11.54, 12.52, 13.50, 14.48, 15.46, 16.44, 17.42, 18.40, 19.38, 20.36],
    "critical rate": [2.30, 2.64, 2.98, 3.32, 3.66, 4.00, 4.35, 4.69, 5.03, 5.37, 5.71, 6.05, 6.39, 6.73, 7.07],
    "charge damage": [4.77, 5.47, 6.18, 6.88, 7.59, 8.29, 9.00, 9.70, 10.40, 11.11, 11.81, 12.52, 13.22, 13.93, 14.63],
    "charge speed": [1.98, 2.28, 2.57, 2.86, 3.16, 3.45, 3.75, 4.04, 4.33, 4.63, 4.92, 5.21, 5.51, 5.80, 6.09],
    "hit rate": [4.77, 5.47, 6.18, 6.88, 7.59, 8.29, 9.00, 9.70, 10.40, 11.11, 11.81, 12.52, 13.22, 13.93, 14.63],
    "atk": [4.77, 5.47, 6.18, 6.88, 7.59, 8.29, 9.00, 9.70, 10.40, 11.11, 11.81, 12.52, 13.22, 13.93, 14.63],
    "def": [4.77, 5.47, 6.18, 6.88, 7.59, 8.29, 9.00, 9.70, 10.40, 11.11, 11.81, 12.52, 13.22, 13.93, 14.63],
}

class StatReader():
    logger = None
    ocr = None
    totals = None
    img_count = 0

    def __init__(self):
        self.logger = logging.getLogger("StatReader")
        self.ocr = easyocr.Reader(["en"])
        self.images = []
        self.totals = {}
        for k in possible_values.keys():
            self.totals[k] = 0.0


    def DebugDraw(self, result, img: Image):
        # Convert the image back to RGB for drawing
        img = img.convert("RGB")
        draw = ImageDraw.Draw(img)

        # Font for text (optional, ensure ttf is available on the system)
        try:
            font = ImageFont.truetype("arial.ttf", size=15)
        except IOError:
            font = ImageFont.load_default()

        # Overlay bounding boxes, text, and probabilities
        for bbox, text, prob in result:
            flattened_bbox = [coord for point in bbox for coord in point]
            # Draw bounding box
            draw.polygon(flattened_bbox, outline="red", width=2)

            # Add text and probability
            x, y = bbox[0]  # Top-left corner of the bounding box
            draw.text((x, y - 15), f"{text} ({prob:.2f})", fill="blue", font=font)

        # Save to a temporary output image
        temp_output_path = f"{self.img_count} temp_output_image.png"
        self.img_count += 1
        img.save(temp_output_path)

        return img


    def ReadImage(self, img: Image):
        img = img.convert("L") # Convert the image to grayscale
        img = img.resize((1920, 1080), Image.Resampling.LANCZOS)
        img = img.crop((737, 727, 737+417, 727+120))
        prev_totals = self.totals.copy()
        npimg = np.array(img)

        result = self.ocr.readtext(npimg)

        self.DebugDraw(result, img)
        # TODO(Richy): this should be moved to a stat parser class or something
        for i in range(0, len(result)):
            _, text, _  = result[i]
            text = text.lower()
            text = text.replace("increase", "")
            text = text.strip()

            def gotHit():
                if i >= len(result):
                    self.logger.warning(f"bad bounds {i}[{text}]")
                    return False

                _, value, _ = result[i+1]
                value = value.replace("%", "")
                value = value.replace(",", ".")
                value = value.strip()
                try:
                    value = float(value)
                except:
                    self.logger.warning(f"bad parse {i}[{text}: {value}]")
                    return False

                # for when the OCR fails to read the decimal, because all stat roll values are < 100%
                if value >= 100:
                    value = value / 100.0
                if value >= 100:
                    value = value / 100.0

                if value in possible_values[text]:
                    # got a value hit
                    self.totals[text] += value
                else:
                    self.logger.warning(f"bad value {i}[{text}: {value}]")
                    return False
                return True

            if text == "":
                continue
            if "%" in text:
                continue
            if text == "effect not obtained":
                continue
            if text in possible_values:
                if gotHit():
                    i += 1 # skip next
                continue
            else:
                if i >= len(result) - 1:
                    self.logger.warning(f"bad bounds {i}[{text}]")
                    continue
                # try a forward look
                _, text2, _ = result[i+1]
                text2 = text2.lower()
                text2 = text2.strip()
                if f"{text} {text2}" in possible_values:
                    text = f"{text} {text2}"
                    i += 1 # skip to text2
                    if gotHit():
                        i += 1 # skip next
                    continue
                self.logger.warning(f"bad text {i}[{text}]")
                continue
        for totals in self.totals:
            prev_totals[totals] = self.totals[totals] - prev_totals[totals]
        return prev_totals


    def ReadFileImage(self, filepath):
        img = Image.open(filepath)
        prev_totals = self.ReadImage(img)
        return prev_totals
    
    def ResetTotals(self):
        for k in possible_values.keys():
            self.totals[k] = 0.0
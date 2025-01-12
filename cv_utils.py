import cv2

def draw_text_bottom_right(image, text, font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=1, color=(255, 255, 255), thickness=2, margin=10):
    (h, w) = image.shape[:2]

    (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)

    x = w - text_width - margin
    y = h - baseline - margin

    cv2.putText(image, text, (x, y), font, font_scale, color, thickness)

    return image

import cv2

def draw_text_top_right(image, text, font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=1, color=(255, 255, 255), thickness=2, margin=10):
    """
    Zeichnet Text in der oberen rechten Ecke eines Bildes.

    :param image: Das Bild, auf dem der Text gezeichnet wird (numpy array).
    :param text: Der Text, der gezeichnet werden soll.
    :param font: Die Schriftart (default: cv2.FONT_HERSHEY_SIMPLEX).
    :param font_scale: Die Skalierung des Textes (default: 1).
    :param color: Die Farbe des Textes in BGR (default: weiß (255, 255, 255)).
    :param thickness: Die Dicke der Linien des Textes (default: 2).
    :param margin: Abstand in Pixeln vom Rand (default: 10).
    :return: Das Bild mit dem gezeichneten Text.
    """
    # Bilddimensionen
    (h, w) = image.shape[:2]

    # Textgröße berechnen
    (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)

    # Position berechnen
    x = w - text_width - margin  # Abstand vom rechten Rand
    y = text_height + margin     # Abstand vom oberen Rand (Texthöhe berücksichtigen)

    # Text zeichnen
    cv2.putText(image, text, (x, y), font, font_scale, color, thickness)

    return image

def draw_text_top_left(image, text, font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=1, color=(255, 255, 255), thickness=2, margin=10):
    """
    Zeichnet Text in der oberen linken Ecke eines Bildes.

    :param image: Das Bild, auf dem der Text gezeichnet wird (numpy array).
    :param text: Der Text, der gezeichnet werden soll.
    :param font: Die Schriftart (default: cv2.FONT_HERSHEY_SIMPLEX).
    :param font_scale: Die Skalierung des Textes (default: 1).
    :param color: Die Farbe des Textes in BGR (default: weiß (255, 255, 255)).
    :param thickness: Die Dicke der Linien des Textes (default: 2).
    :param margin: Abstand in Pixeln vom Rand (default: 10).
    :return: Das Bild mit dem gezeichneten Text.
    """
    # Textgröße berechnen
    (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)

    # Position berechnen
    x = margin  # Abstand vom linken Rand
    y = text_height + margin  # Abstand vom oberen Rand (Texthöhe berücksichtigen)

    # Text zeichnen
    cv2.putText(image, text, (x, y), font, font_scale, color, thickness)

    return image
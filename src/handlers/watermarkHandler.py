import base64
import io
import math
from datetime import datetime

from PIL import Image, ImageDraw, ImageFont
from werkzeug.datastructures import FileStorage
from werkzeug.formparser import parse_form_data
from werkzeug.wrappers import Request


def add_watermark(image, watermark_text="Your Watermark", font_size=48, font_color=(255, 0, 0)):
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("resources/arial.ttf", font_size)
    print(f'font: {font}')
    angle = math.atan2(image.height, image.width)

    text_width, _ = draw.textsize(watermark_text, font=font)
    step = (text_width * 0.5) / math.cos(angle)
    d = 0.0
    diagonal_length = math.sqrt(image.width ** 2 + image.height ** 2)

    while d < diagonal_length:
        x = d * math.cos(angle)
        y = image.height - d * math.sin(angle)
        draw.text((x, y), watermark_text, font=font, fill=font_color)
        d += step


def hex_to_rgb(hex_color):
    try:
        hex_color = hex_color.lstrip('#')

        rgb_tuple = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        print(f'rgb_tuple: {rgb_tuple}')
        if all(0 <= value <= 255 for value in rgb_tuple):
            return rgb_tuple
        else:
            return None
    except Exception as e:
        print(f'Invalid hex color: {e}')
        pass

    return None


def handler(event, context):
    try:
        print(f'Event: {event}')
        print(f'Context: {context}')

        headers = event.get('headers', {})
        content_type = headers.get('Content-Type') or headers.get('content-type')

        if content_type is None:
            print("Content-Type not provided in headers")
            return {
                'statusCode': 400,
                'body': 'Content-Type not provided in headers'
            }
        
        print(f'Content-Type: {content_type}')

        body_encoded = event.get('body', b'')
        if body_encoded is None:
            print("Body not provided in the event")
            return {
                'statusCode': 400,
                'body': 'Body not provided in the event'
            }
        body = base64.b64decode(body_encoded) if event.get('isBase64Encoded', False) else body_encoded
        print(f'Body: {body}')

        environ = {
            'REQUEST_METHOD': 'POST',
            'CONTENT_TYPE': content_type,
            'wsgi.input': io.BytesIO(body),
            'CONTENT_LENGTH': str(len(body))
        }

        _, form, files = parse_form_data(environ)

        print(f'form: {form}')

        watermark_text = form.get('watermarkText', 'Your Watermark')
        fontSizeValue = form.get('fontSize', 48)
        fontSizeValue = form.get('fontSize', 48)
        if isinstance(fontSizeValue, str):
            font_size = int(fontSizeValue) if fontSizeValue.isdigit() else 48
        elif isinstance(fontSizeValue, int):
            font_size = fontSizeValue
        else:
            font_size = 48

        font_color = form.get('fontColor', (255, 0, 0))

        fontColorValue = form.get('fontColor', '#FF0000')
        font_color = hex_to_rgb(fontColorValue) if fontColorValue.startswith("#") else (255, 0, 0)
        
        print(f'Watermark Text: {watermark_text}')
        print(f'Font Size: {font_size}')
        print(f'Font Color: {font_color}')

        image_file: FileStorage = files.get('image')
        print(f'Image File: {image_file}')
        if image_file:
            image = Image.open(image_file)
        else:
            print('No image provided, using sample image')
            image = Image.open('resources/sample.jpg')

        add_watermark(image, watermark_text, font_size, font_color)

        image.save('watermarked_image.png')

        output_buffer = io.BytesIO()
        image.save(output_buffer, format='PNG')
        watermarked_image = base64.b64encode(output_buffer.getvalue()).decode()

        print(f'Watermarked Image Length: {len(watermarked_image)}')

        return {
            'statusCode': 200,
            'body': watermarked_image,
            'headers': {
                'Content-Type': 'image/png',
                'Content-Disposition': f'attachment; filename="watermarked_image_{datetime.now().strftime("%Y%m%d%H%M%S")}.png"'
            },
            'isBase64Encoded': True
        }
    except Exception as e:
        print(f'UNHANDLED EXCEPTION, CRITICAL!!!: {e}')
        return {
            'statusCode': 500,
            'body': 'Что-то пошло не так, критическая ошибка'
        }
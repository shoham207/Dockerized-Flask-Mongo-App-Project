from PIL import Image, ImageDraw, ImageFont
import random
import os
import numpy as np
import requests
from PIL import Image
import io
import PIL

class MemeImageModule:
    """
    A service for creating meme images with text overlays.
    """

    image_size = None

    def __init__(self, font_path=None, image_size=(800, 600),
                 default_font_size=50, text_color=(255, 255, 255)):
        """
        Initialize the MemeImageService.

        Args:
            font_path (str): Path to a TTF font file. If None, uses default
            image_size (tuple): Default size for generated images (width, height)
            default_font_size (int): Default font size for text
            text_color (tuple): RGB color tuple for text
        """
        self.image_size = image_size
        self.text_color = text_color
        self.default_font_size = default_font_size

        # Try to use Arial or fall back to default
        try:
            if font_path:
                self.font = ImageFont.truetype(font_path, size=default_font_size)
            else:
                # Try to find a system font
                system_fonts = [
                    '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',  # Linux
                    '/System/Library/Fonts/Arial.ttf',  # MacOS
                    'C:\\Windows\\Fonts\\Arial.ttf'  # Windows
                ]
                for font_path in system_fonts:
                    if os.path.exists(font_path):
                        self.font = ImageFont.truetype(font_path, size=default_font_size)
                        break
                else:
                    self.font = ImageFont.load_default()
        except Exception:
            self.font = ImageFont.load_default()

    def _wrap_text(self, text: str, max_width: int) -> list:
        """
        Wrap text to fit within a given width.
        """
        words = text.split()
        lines = []
        current_line = []

        for word in words:
            current_line.append(word)
            # Check if current line width exceeds max_width
            line = ' '.join(current_line)
            bbox = self.font.getbbox(line)
            if bbox[2] > max_width:
                if len(current_line) == 1:
                    lines.append(line)
                    current_line = []
                else:
                    current_line.pop()
                    lines.append(' '.join(current_line))
                    current_line = [word]

        if current_line:
            lines.append(' '.join(current_line))

        return lines

    def _add_text_to_image(self, image: Image.Image, text: str) -> Image.Image:
        """
        Add text to an image with proper wrapping and positioning.
        """
        draw = ImageDraw.Draw(image)

        # Calculate maximum width for text
        max_width = int(image.width * 0.7)  # 90% of image width

        # Wrap text
        lines = self._wrap_text(text, max_width)

        # Calculate total text height
        line_spacing = self.default_font_size * 1.2
        total_text_height = len(lines) * line_spacing

        # Calculate starting Y position to center text vertically
        current_y = (image.height - total_text_height) / 2

        # Draw each line
        for line in lines:
            # Get line width for centering
            bbox = self.font.getbbox(line)
            text_width = bbox[2] - bbox[0]
            x = (image.width - text_width) / 2

            # Add subtle text shadow for better readability
            shadow_offset = 3
            draw.text((x + shadow_offset, current_y + shadow_offset),
                      line, font=self.font, fill=(0, 0, 0))

            # Draw main text
            draw.text((x, current_y), line, font=self.font, fill=self.text_color)
            current_y += line_spacing

        return image.resize((800, 600), PIL.Image.Resampling.LANCZOS)

    def create_meme_with_solid_background(self, text: str, background_color=None) -> Image.Image:
        """
        Create a meme with solid background color.

        Args:
            text (str): The text to put on the image
            background_color (tuple): RGB color tuple. If None, generates random color

        Returns:
            PIL.Image: The generated meme image
        """
        if background_color is None:
            background_color = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255)
            )

        # Create image with background color
        image = Image.new('RGB', self.image_size, background_color)
        return MemeImageModule._add_text_to_image(self,image, text)

    def create_meme_with_downloaded_image(self, text: str, image_url: str) -> Image.Image:
        response = requests.get(image_url)
        response.raise_for_status()

        with Image.open(io.BytesIO(response.content)) as img:
            # Use LANCZOS (best for downscaling) or specific size
            resized_img = img.resize(
                (self.image_size[0], self.image_size[1]),
                Image.Resampling.LANCZOS
            )

            # Add text to the image
            resized_img = MemeImageModule._add_text_to_image(self, resized_img, text)

        return resized_img

    def create_gradient_background(self) -> Image.Image:
        """
        Create a background with a gradient effect.
        """
        # Create gradient colors
        color1 = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        color2 = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        # Create gradient array
        width, height = self.image_size
        image_array = np.zeros((height, width, 3), dtype=np.uint8)

        for y in range(height):
            ratio = y / height
            for x in range(width):
                for i in range(3):
                    image_array[y, x, i] = int(color1[i] * (1 - ratio) + color2[i] * ratio)

        return Image.fromarray(image_array)

    def create_meme_with_gradient(self, text: str) -> Image.Image:
        """
        Create a meme with gradient background.

        Args:
            text (str): The text to put on the image

        Returns:
            PIL.Image: The generated meme image
        """
        image = MemeImageModule.create_gradient_background(self)
        return MemeImageModule._add_text_to_image(self, image, text)


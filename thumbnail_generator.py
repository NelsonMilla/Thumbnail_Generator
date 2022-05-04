from math import ceil
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import pyfiglet



class ThumbnailGenerator:


    def main(self):
        print(pyfiglet.figlet_format('Thumbnail Generator v1.0'))
        nombre_taller = input('Enter text to print: ')
        nombre_tallerista = input('Enter image to apply: (saved on talleristas folder) ')
        x_text_coord = 500
        y_text_coord = 226
        with Image.open('fondos/fondo_1.png').convert("RGB") as img:
            draw = ImageDraw.Draw(img)

            # Create container for the text

            # Write the workshop name
            font = ImageFont.truetype('fonts/Arvo-Bold.ttf', size=60) # You can store your own font on the fonts folder
            lines = self.text_wrap(nombre_taller, font, img.size[0]-x_text_coord-20) # Separate the text in lines to fit in the image
            calculated = y_text_coord + (len(lines) * font.getsize(lines[0])[1]) # Calculates ending position of text to draw rectangle first
            # Draw a rectangle around the text
            SPACING = 80
            draw.rounded_rectangle(((x_text_coord-SPACING, y_text_coord-SPACING-50+20), (font.getsize(lines[0])[0] + SPACING + x_text_coord + 20, calculated + SPACING + 70)), fill='#c93d62', radius=20, outline="black", width=5)
            draw.rounded_rectangle(((x_text_coord-SPACING, y_text_coord-SPACING-50), (font.getsize(lines[0])[0] + SPACING + x_text_coord, calculated + SPACING + 50)), fill='white', outline='black', radius=20, width=5)
            # Draw the text
            for line in lines:
                draw.text((x_text_coord, y_text_coord), line, fill='black', font=font)
                y_text_coord += font.getsize(line)[1]

            # Put the workshopist image
            try:
                with Image.open(f'talleristas/{nombre_tallerista}.png').convert("RGB") as img_tallerista:
                    RESIZE_VALUE = 500
                    aspect_ratio = img_tallerista.size[1] / img_tallerista.size[0]
                    img_tallerista = img_tallerista.resize((RESIZE_VALUE, ceil(RESIZE_VALUE * aspect_ratio)), Image.ANTIALIAS)
                    img_tallerista = Image.fromarray(self.crop_image_into_circle(img_tallerista))
                    img.paste(img_tallerista, (0, img.size[1] - img_tallerista.size[1]), img_tallerista)
            except Exception as e:
                raise(e)

            # Save image to drive
            img.save(f'output/thumbnail_{nombre_taller}_{nombre_tallerista}.png')


    def text_wrap(self, text, font, max_width):
            """
            Wrap text base on specified width.
            This is to enable text of width more than the image width to be display
            nicely.
            @params:
                text: str
                    text to wrap
                font: obj
                    font of the text
                max_width: int
                    width to split the text with
            @return
                lines: list[str]
                    list of sub-strings
            """
            lines = []
            # If the text width is smaller than the image width, then no need to split
            # just add it to the line list and return
            if font.getsize(text)[0]  <= max_width:
                lines.append(text)
            else:
                #split the line by spaces to get words
                words = text.split(' ')
                i = 0
                # append every word to a line while its width is shorter than the image width
                while i < len(words):
                    line = ''
                    while i < len(words) and font.getsize(line + words[i])[0] <= max_width:
                        line = line + words[i]+ " "
                        i += 1
                    if not line:
                        line = words[i]
                        i += 1
                    lines.append(line)
            return lines

    def crop_image_into_circle(self, img):
        # First crop into square
        h,w = img.size[0], img.size[1]
        m = min(h,w)
        img = img.crop(((w-m)//2, (h-m)//2, m+(w-m)//2, m+(h-m)//2))
        h,w = m,m
        print(f'Image size is {img.size}')
        # creating luminous image
        lum_img = Image.new('L',[h,w] ,0)
        draw = ImageDraw.Draw(lum_img)
        draw.pieslice([(0,0),(h,w)],0,360,fill=255)
        img_arr = np.array(img)
        lum_img_arr = np.array(lum_img)
        return np.dstack((img_arr, lum_img_arr))

ThumbnailGenerator().main()
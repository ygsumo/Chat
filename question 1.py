from PIL import Image, ImageDraw, ImageFont


class AddNumToAvatar():

    def __init__(self):
        self.my_font = None
        self.image = None

    def open_avatar(self, url):
        self.image = Image.open(url)

    def get_size(self, image):
        return self.image.size

    def draw_font(self, str, ttf, color):
        width, height = self.get_size(self.image)
        fontSize = min(width, height)//11
        self.my_font = ImageFont.truetype(ttf, fontSize)
        draw = ImageDraw.Draw(self.image)
        position = (0.9 * width, 0.1 * height - fontSize)
        draw.text(position, str, font=self.my_font, fill=color)
        self.image.show()
        self.image.save("haha.png")



if __name__ == '__main__':
    ava = AddNumToAvatar()
    image = ava.open_avatar("avatar.jpg")
    ava.draw_font("5", "Arial.ttf", "#ff0000")
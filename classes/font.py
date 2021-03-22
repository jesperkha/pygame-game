# Font class

from pygame import image, Rect, transform

# LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,:!?"
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class Font:
    def __init__(self, filename) -> None:
        self.filename = filename
        self.chars = {}

    
    @staticmethod
    def clip_surface(surf, x, y, w, h) -> object:
        temp_surf = surf.copy()
        clip_rect = Rect(x, y, w, h)
        temp_surf.set_clip(clip_rect)
        new_image = surf.subsurface(temp_surf.get_clip())
        return new_image.copy()
    

    def load(self):
        self.font_image = image.load(self.filename).convert_alpha()

        current_width = 0
        current_char = 0
        for x in range(self.font_image.get_width()):
            
            if self.font_image.get_at((x, 0)) == (255, 0, 0):
                self.chars[LETTERS[current_char]] = Font.clip_surface(self.font_image, x - current_width, 0, current_width, self.font_image.get_height())
                current_width = 0
                current_char += 1

            else:
                current_width += 1

    
    def render(self, win: object, pos: tuple, text: str, letter_spacing: int = 1, scale: int = 1) -> tuple:
        space = 0 # acts as string width
        height = 0
        x = pos[0]
        y = pos[1]

        for letter in text:
            pre_char = self.chars[letter]
            char = transform.scale(pre_char, (pre_char.get_width() * scale, pre_char.get_height() * scale))
            win.blit(char, (pos[0] + space, pos[1]))
            space += char.get_width() + letter_spacing * scale
            height = char.get_height()

        # returns size of string
        return (x, y, space, height)
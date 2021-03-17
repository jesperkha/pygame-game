# Font class

from pygame import image, Rect

# LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,:!?"
LETTERS = "ABC"

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
        self.font_image = image.load(self.filename).convert()

        current_width = 0
        current_char = 0
        for x in range(self.font_image.get_width()):
            
            if self.font_image.get_at((x, 0)) == (255, 0, 0):
                self.chars[LETTERS[current_char]] = Font.clip_surface(self.font_image, x - current_width, 0, current_width, self.font_image.get_height())
                current_width = 0
                current_char += 1

            else:
                current_width += 1

    
    def render(self, win: object, pos: tuple, text: str, letter_spacing: int = 1):
        space = 0
        for letter in text:
            win.blit(self.chars[letter], (pos[0] + space, pos[1]))
            space += self.chars[letter].get_width() + letter_spacing




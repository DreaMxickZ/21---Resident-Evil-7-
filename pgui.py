import pygame
from pygame import mixer

class Label:
    def __init__(self, text, font:str=None, font_size:int=30, text_color:str|tuple='#FFFFFF', x:int=0, y:int=0):
        self.surface = pygame.display.get_surface()
        self.text = text
        self.font = font
        self.text_color = text_color
        self.pos_x = x
        self.pos_y = y
        
        self.pressed = False
        
        self.font_size = font_size
        if font == None:
            self.font = pygame.font.SysFont('Arial', 30)
        else:
            self.font = pygame.font.Font(font, font_size)
    
    def rect(self):
        textobj = self.font.render(self.text, 1, self.text_color)
        textrect = textobj.get_rect()
        textrect.topleft = (self.pos_x, self.pos_y)
        return textobj, textrect
    
    def draw(self):
        textobj, textrect = self.rect()
        self.surface.blit(textobj, textrect)
    
    def is_collided(self):
        textobj, textrect = self.rect()
        if textrect.collidepoint(pygame.mouse.get_pos()):
            return True
        
    def clicked(self) -> bool:
        if self.is_collided() and pygame.mouse.get_pressed()[0] and not self.pressed:
            self.pressed = True
        else:
            self.pressed = False
        return self.pressed

class BlackJackCard(Label):
    def __init__(self, text, font: str = None, font_size: int = 120, text_color: str | tuple = '#FFFFFF', background_color: str | tuple = '#000000', x: int = 0, y: int = 0):
        super().__init__(text, font, font_size, text_color, x, y)
        self.background_color = background_color
        
        self.font_size = font_size
        if font == None:
            self.font = pygame.font.SysFont('Arial', font_size)
        else:
            self.font = pygame.font.Font(font, font_size)
    
    def rect(self):
        textobj = self.font.render(self.text, 1, self.text_color)
        textrect = textobj.get_rect()
        textrect.topleft = (self.pos_x, self.pos_y)
        return textobj, textrect

    def draw(self): #draw with background color
        textobj, textrect = self.rect()
        pygame.draw.rect(self.surface, self.background_color, textrect)
        self.surface.blit(textobj, textrect)

class Button():
    def __init__(self, text, font:str=None, font_size:int=30, width:int=250, height:int=50, x:int=0, y:int=0,  border: int=12):
        mixer.init()
        
        self.surface = pygame.display.get_surface()
        
        self.collide_sound_played = False

        self.rect = pygame.Rect(x, y, width, height)
        self.top_rect = self.rect.copy()
        self.bottom_rect = self.rect.copy()
        
        self.border = border
        self.elevation = 0
        self.dynamic_elevation = 0
        
        self.top_color = '#475F77'
        self.top_color_hover = '#D74B4B'
        self.t_color_state = self.top_color
        self.bottom_color = '#354B5E'
        
        self.text = text
        self.text_color = "#FFFFFF"
        self.font_size = font_size
        if font == None:
            self.font = pygame.font.SysFont('Arial', 30)
        else:
            self.font = pygame.font.Font(font, font_size)
        self.text_surf = self.font.render(text, True, self.text_color)
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)
    
    def draw(self):
        self.top_rect.y = self.rect.y - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center
        
        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation
        
        pygame.draw.rect(self.surface, self.bottom_color, self.bottom_rect, border_radius=self.border)
        pygame.draw.rect(self.surface, self.t_color_state, self.top_rect, border_radius=self.border)
        
        self.surface.blit(self.text_surf, self.text_rect)
    
    def is_collided(self) -> bool:
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return True
        else:
            return False

    def clicked(self) -> bool:
        mouse_press = pygame.mouse.get_pressed()[0]
        pressed = False
        if self.is_collided() and mouse_press and not pressed:
            pressed = True
        else:
            pressed = False
        return pressed  
    
    def set_hover(self, color: str | tuple = '#D74B4B'):
        self.top_color_hover = color
        if self.is_collided():
            self.t_color_state = self.top_color_hover
        else:
            self.t_color_state = self.top_color

    def set_elevate(self, elevation: int = 5):
        self.elevation = elevation
        if self.clicked():
            self.dynamic_elevation = 0
        else:
            self.dynamic_elevation = self.elevation

print("\nThis is a library for pygame gui")
print("pgui library from https://github.com/saveffer1")

if __name__ == "__main__":
    raise RuntimeError("This module is not meant to run on its own!")
import pygame
from pygame.constants import KEYDOWN


# button class
class Button:
    def __init__(self, x, y, image, scale, select_image:pygame.Surface=None):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

        self.select_image = select_image
        self.overlay_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        self.overlay_surface.fill((255, 255, 255, 20))

    def draw(self, surface):
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
            if pygame.mouse.get_pressed()[0] == 0 and self.clicked:
                self.clicked = False
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        
        # draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))
        # check mouseover 
        if self.rect.collidepoint(pos):
            # draw overlay
            if self.select_image:
                surface.blit(self.select_image, (self.rect.x, self.rect.bottom - 30))
            #pygame.draw.rect(surface, (255, 255, 255, 20), self.rect, 5)
            surface.blit(self.overlay_surface, (self.rect.x, self.rect.y))

       
        return action

class TextBox:
    def __init__(self, x, y, default_text='', background_image=None):
        width = 300
        height = 100
        self.rect = pygame.rect.Rect(x, y, width, height)
        self.rect.topleft = (x, y)
        self.clicked = False
        self.text = default_text

        self.color_active = pygame.Color('lightskyblue3') 
        self.color_passive = pygame.Color('chartreuse4') 
        self.color = self.color_passive 

        self.background_image = background_image


    def draw(self, surface, font):
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()
        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
                self.color = self.color_active
        else:
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == True:
                self.clicked = False
                self.color = self.color_passive
        

        # draw rectangle and argument passed which should 
        # be on screen 
        if self.background_image:
            surface.blit(self.background_image, (self.rect.x, self.rect.y + 20))
        #pygame.draw.rect(surface, self.color, self.rect) 
    
        text_surface = font.render(self.text, True, (255, 255, 255)) 
        
        # render at position stated in arguments 
        surface.blit(text_surface, (self.rect.x+5, self.rect.y+5)) 
        
        # set width of textfield so that text cannot get 
        # outside of user's text input 
        self.w = max(100, text_surface.get_width()+10) 

        return action
    
    def text_update(self, event):

        if event.type == pygame.KEYDOWN: 
  
            # Check for backspace 
            if event.key == pygame.K_BACKSPACE: 
  
                # get text input from 0 to -1 i.e. end. 
                self.text = self.text[:-1] 

            elif event.key == pygame.K_RETURN:
                return True
            # Unicode standard is used for string 
            # formation 
        
            else:
                self.text += event.unicode                


class key(Button):
    def __init__(self, x, y, image, scale, letter: str, font: str, image_pressed, select_image:pygame.Surface=None):
        super().__init__(x, y, image, scale)
        self.image_unpressed = self.image
        self.image_pressed = pygame.transform.scale(image_pressed, (int(image_pressed.get_width() * scale), int(image_pressed.get_height() * scale)))
        self.letter = letter
        self.select_image = select_image
        font_ = pygame.font.Font(font, 90)
        self.text = font_.render(letter, False, (255, 255, 255))

        self.pressed = False

    
    def draw(self, surface: pygame.Surface):
        action = super().draw(surface)
        if action:
            pass
        if pygame.key.get_pressed()[ord(self.letter)]:
            action = True
        if self.pressed:
            self.image = self.image_pressed
        else:
            self.image = self.image_unpressed
        surface.blit(self.text, (self.rect.centerx - self.text.get_width() // 2, \
                                  self.rect.centery - self.text.get_height() // 2 - 15 + self.pressed * 10))
        return action
        
        

        
        

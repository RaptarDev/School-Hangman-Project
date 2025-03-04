from typing import Text
import pygame
from pygame.constants import KEYDOWN
from button import *
from utils import loadImage, randomWordFromFile
import numpy as np

class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()

        # Loads The fonts
        self.font = pygame.font.SysFont('arial', 30)

        self.running = True

        self.points = 100

        self.assets = {
            'playButton': loadImage('buttons/play.png', 6),
            'quitButton': loadImage('buttons/quit.png', 6),
            'menuButton': loadImage('buttons/menu.png', 4.5),
        }

        # Button classes for menu
        self.playButton = Button((self.screen.get_width() - 180) / 2, 250, self.assets['playButton'], 1)
        self.quitButton = Button((self.screen.get_width() - 180) / 2, 550, self.assets['quitButton'], 1)
        self.menuButton = Button((self.screen.get_width() - 180) / 2, 600, self.assets['menuButton'], 1)
        
    def menu(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False


            # Draws the backgound object
            self.screen.fill('white')

            # Draws the buttons
            
            self.playButton.draw(self.screen)
            self.quitButton.draw(self.screen)

            if self.playButton.clicked:
                self.difficultyMenu()
            if self.quitButton.clicked:
                self.running = False
            
            pygame.display.update()

            

            # Caps Frames to 60
            self.clock.tick(60)

    def difficultyMenu(self):
        select_diff_text = self.font.render("Select Difficulty", True, "black")

        easyButton = Button((self.screen.get_width() - 180) / 2, 300, self.assets['playButton'], 1)
        mediumButton = Button((self.screen.get_width() - 180) / 2, 450, self.assets['playButton'], 1)
        hardButton = Button((self.screen.get_width() - 180) / 2, 600, self.assets['playButton'], 1)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False


            # Draws the backgound object
            self.screen.fill('white')

            # Draws the buttons
            self.screen.blit(select_diff_text, ((self.screen.get_width() - 180)/2, 10))
            easyButton.draw(self.screen)
            mediumButton.draw(self.screen)
            hardButton.draw(self.screen)
            
            if easyButton.clicked:
                self.mainGameLoop("easy")
            elif mediumButton.clicked:
                self.mainGameLoop("medium")
            elif hardButton.clicked:
                self.mainGameLoop("hard")
            
            pygame.display.update()

            

            # Caps Frames to 60
            self.clock.tick(60)

    def mainGameLoop(self, difficulty):

        enter = False

        text_box = TextBox(500, 300)

        difficulty_text = self.font.render(difficulty, True, "black")
        word = randomWordFromFile("data/word_lists/" + difficulty + "_words.txt")[0].replace("\n", "")
        word_text = self.font.render(word, True, "black")
        letters = list(word)
        guessed_letters = []
        for i in letters:
            guessed_letters.append("_")


        guessed_word_text = self.font.render("".join(guessed_letters), True, "black")


        you_win_text = self.font.render("You Win!", True, (0, 0, 0))
        you_lose_text = self.font.render("You Lose!", True, (0, 0, 0))

        win_state = ""

        points_text = self.font.render(str(self.points), True, (0,0,0))

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type is pygame.KEYDOWN:
                    print(event.key)

                enter = text_box.text_update(event)

            guessed_word_text = self.font.render("".join(guessed_letters), True, "black")

            length = len(text_box.text)
            if enter and length > 0 and not win_state == "win":
                if length == 1 and text_box.text in letters:
                    
                    print(list(filter(lambda i: letters[i] == text_box.text, range(len(letters)))))
                    for i in list(filter(lambda i: letters[i] == text_box.text, range(len(letters)))):
                        guessed_letters[i] = text_box.text
                        print(guessed_letters)
                    if guessed_letters == letters:
                        print("you min")
                        win_state = "win"
                        self.points += 100
                    text_box.text = ""
                    
                elif length > 1 and text_box.text == word: 
                    print('win')
                    win_state = "win"
                    self.points += 100
                else:
                    text_box.text = ""
                    self.points -= 10
                
            if self.points <= 0:
                win_state = "lose"
            
            points_text = self.font.render(str(self.points), True, (0,0,0))

            # Draws the backgound object
            self.screen.fill('white')

            self.screen.blit(difficulty_text, (500, 20))
            #self.screen.blit(word_text, (500, 40))
            self.screen.blit(guessed_word_text, (500, 200))
            text_box.draw(self.screen, self.font)
            self.screen.blit(points_text, (200, 200))

            if win_state == "win":
                self.screen.blit(you_win_text, (500, 300))
                
                
            elif win_state == "lose":
                self.screen.blit(you_lose_text, (500, 300))
            

            pygame.display.update()

            # Caps Frames to 60
            self.clock.tick(60)



game = Game()
game.menu()



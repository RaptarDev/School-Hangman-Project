import time
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
            'key': loadImage('buttons/key.png', 5),
            'key_pressed': loadImage('buttons/key_clicked.png', 5)
        }

        self.font = pygame.font.Font('data/font/PixelOperator-Bold.ttf', 120)

        # Button classes for menu
        self.playButton = Button((self.screen.get_width() - 180) / 2, 250, self.assets['playButton'], 1)
        self.quitButton = Button((self.screen.get_width() - 180) / 2, 550, self.assets['quitButton'], 1)
        self.menuButton = Button((self.screen.get_width() - 180) / 2, 600, self.assets['menuButton'], 1)


    def checkLetter(self, length, text, letters, guessed_letters, word):
        win_state = ""
        if length == 1 and text in letters:
            print(list(filter(lambda i: letters[i] == text, range(len(letters)))))
            for i in list(filter(lambda i: letters[i] == text, range(len(letters)))):
                guessed_letters[i] = text
                print(guessed_letters)
            if guessed_letters == letters:
                print("you min")
                win_state = "win"
                self.points += 100
                text = ""
                    
        elif length > 1 and text == word: 
                print('win')
                win_state = "win"
                self.points += 100
        else:
                text = ""
                self.points -= 10
        
        return guessed_letters, win_state
        

    def menu(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False


            # Draws the backgound object
            self.screen.fill('black')

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
        select_diff_text = self.font.render("Select Difficulty", True, "white")

        easyButton = Button((self.screen.get_width() - self.assets['playButton'].get_width()) / 2, 300, self.assets['playButton'], 1)
        mediumButton = Button((self.screen.get_width() - self.assets['playButton'].get_width()) / 2, 450, self.assets['playButton'], 1)
        hardButton = Button((self.screen.get_width() - self.assets['playButton'].get_width()) / 2, 600, self.assets['playButton'], 1)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Draws the backgound object
            self.screen.fill('black')

            # Draws the buttons
            self.screen.blit(select_diff_text, ((self.screen.get_width() - select_diff_text.get_width())/2, 10))
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

        text_box = TextBox((self.screen.get_width() - 300) / 2, 250)
        text_box.clicked = False

        difficulty_text = self.font.render(difficulty, True, "white")
        word = randomWordFromFile("data/word_lists/" + difficulty + "_words.txt")[0].replace("\n", "")

        letters = list(word)
        guessed_letters = []
        for i in letters:
            guessed_letters.append("")
        
        word_length = len(word)
        empty_text = self.font.render("_", False, "white")

        guess_letters_texts = []

        attempted_guesses = []
       
        you_win_text = self.font.render("You Win!", True, (255, 255, 255))
        you_lose_text = self.font.render("You Lose!", True, (255, 255, 255))

        win_state = ""

        points_text = self.font.render(str(self.points), True, (255,255,255))
        
        # Define the keys for each row
        row1 = "qwertyuiop"
        row2 = "asdfghjkl"
        row3 = "zxcvbnm"
        
        # Create the keyboard with keys in three rows
        keyboard = {}
        for i, k in enumerate(row1):
            keyboard[k] = key(100 + i * 110, 380, self.assets['key'], 1, k, 'data/font/PixelOperator-Bold.ttf', self.assets['key_pressed'])
        for i, k in enumerate(row2):
            keyboard[k] = key(130 + i * 110, 490, self.assets['key'], 1, k, 'data/font/PixelOperator-Bold.ttf', self.assets['key_pressed'])
        for i, k in enumerate(row3):
            keyboard[k] = key(160 + i * 110, 600, self.assets['key'], 1, k, 'data/font/PixelOperator-Bold.ttf', self.assets['key_pressed'])

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if text_box.clicked:
                    enter = text_box.text_update(event)

            length = len(text_box.text)
            if enter and length > 0 and not win_state == "win":
               guessed_letters, win_state = self.checkLetter(length, text_box.text, letters, guessed_letters, word)
               if text_box.text in keyboard.keys():
                   keyboard[text_box.text].pressed = True
               text_box.text = ""
                
            if self.points <= 0:
                win_state = "lose"
            
            points_text = self.font.render(str(self.points), True, (255,255,255))

            guess_letters_texts = [self.font.render(i, True, "white") for i in guessed_letters]

            # Draws the backgound object
            self.screen.fill('black')

            self.screen.blit(difficulty_text, ((self.screen.get_width() - difficulty_text.get_width()) / 2 , 20))

            for i in range(word_length):
                self.screen.blit(empty_text, ((self.screen.get_width() - (empty_text.get_width() + 17) * word_length ) / 2 + i * 60, 100))
                self.screen.blit(guess_letters_texts[i], ((self.screen.get_width() - (empty_text.get_width() + 19) * word_length) / 2 + i * 60, 100))

            text_box.draw(self.screen, self.font)
            self.screen.blit(points_text, (20, 20))
            for i in keyboard.values():
                if i.draw(self.screen) and not i.pressed and not text_box.clicked:
                    i.pressed = True
                    guessed_letters, win_state = self.checkLetter(1, i.letter, letters, guessed_letters, word)

            if win_state == "win":
                self.screen.blit(you_win_text, (500, 300))
                self.points += 100
                time.sleep(1)
                self.mainGameLoop(difficulty)
    
            elif win_state == "lose":
                self.screen.blit(you_lose_text, (500, 300))
                time.sleep(1)
                self.points = 100
                self.menu()

            pygame.display.update()

            # Caps Frames to 60
            self.clock.tick(60)
    
    def loseScreen(self):
        pass


game = Game()
game.menu()


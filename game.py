import time
from typing import Text
import pygame
from pygame.constants import KEYDOWN
from button import *
from utils import *
import numpy as np


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((1280, 720))
        self.screen.set_colorkey((0, 0, 0))
        pygame.display.set_caption("Hangman")   
        self.clock = pygame.time.Clock()

        # Loads The fonts
        self.title_font = pygame.font.Font('data/font/Anarchaos.otf', 120)
        self.small_font = pygame.font.Font('data/font/Anarchaos.otf', 80)
        self.underline_font = pygame.font.Font('data/font/Storm Gust.ttf', 120)

        # Checks if the game is running
        self.running = True

        self.points = 100

        # Loads the assets
        self.assets = {
            'playButton': loadImage('buttons/play.png', 1),
            'quitButton': loadImage('buttons/quit.png', 1),
            'menuButton': loadImage('buttons/menu.png', 1),
            'backButton': loadImage('buttons/back.png', 1),
            'rulesButton': loadImage('buttons/rules.png', 1),
            'highscoreButton': loadImage('buttons/highscores.png', 1),

            'easyButton': loadImage('buttons/easy.png', 1),
            'mediumButton': loadImage('buttons/medium.png', 1),
            'hardButton': loadImage('buttons/hard.png', 1),

            'key': loadImage('buttons/key.png', 1),
            'key_pressed': loadImage('buttons/key_clicked.png', 1),
            'select': loadImage('buttons/select.png', 1),
            'select_big': loadImage('buttons/select-big.png', 1),

            'text_box': loadImage('buttons/text_box.png', 1),

            "hangman": loadImages('hangman', 1),

        }
        for i in self.assets.values():
            if type(i) == list:
                continue
            i.set_colorkey((0, 0, 0))
        
        self.sounds = {
            'background_music': pygame.mixer.Sound("data/sounds/gameovermachinehead.mp3"),
            'button_click': pygame.mixer.Sound("data/sounds/click.wav"),
            'key_click': [pygame.mixer.Sound("data/sounds/key_click-01.wav"),
                          pygame.mixer.Sound("data/sounds/key_click-02.wav"),
                          pygame.mixer.Sound("data/sounds/key_click-03.wav"),
                          pygame.mixer.Sound("data/sounds/key_click-04.wav"),
                        ]
        }

        # Loads the save data
        self.data = {
            "highscore_easy": [],
            "highscore_medium": [],
            "highscore_hard": [],
        }
           
        self.data = loadSave("data/save.json", self.data)

        self.name = ""


    def checkLetter(self, length, text, letters, guessed_letters, word):
        win_state = ""
        # Checks if the letter is in the word
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
        # Checks if the word is the same as the guessed word
        elif length > 1 and text == word: 
                print('win')
                win_state = "win"
                self.points += 100
        # if the letter is not in the word
        else:
                text = ""
                self.points -= 10
        
        return guessed_letters, win_state
        

    def menu(self):
        title = self.title_font.render("HAngman", True, "white")

        # Sets up the buttons
        playButton = Button((self.screen.get_width() - 180) / 2, 250, self.assets['playButton'], 1, self.assets['select_big'], sound=self.sounds['button_click'])
        quitButton = Button((self.screen.get_width() - 180) / 2, 550, self.assets['quitButton'], 1, self.assets['select_big'], sound=self.sounds['button_click'])
        menuButton = Button((self.screen.get_width() - 180) / 2, 600, self.assets['menuButton'], 1, self.assets['select_big'], sound=self.sounds['button_click'])
        highscoreButton = Button((self.screen.get_width() - 180) / 2 - 100, 400, self.assets['highscoreButton'], 1, self.assets['select_big'], sound=self.sounds['button_click'])
        rulesButton = Button((self.screen.get_width() - 180) / 2 + 100, 400, self.assets['rulesButton'], 1, self.assets['select_big'], sound=self.sounds['button_click'])

        # Set up music 
        self.sounds['background_music'].play(-1)
        self.sounds['background_music'].set_volume(0.1)


        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Draws the backgound 
            self.screen.fill('black')

            # Draws the title
            self.screen.blit(title, ((self.screen.get_width() - title.get_width()) / 2, 20))

            # Draws the buttons
            playButton.draw(self.screen)
            highscoreButton.draw(self.screen)
            rulesButton.draw(self.screen)
            quitButton.draw(self.screen)

            # Checks if the buttons are clicked
            if playButton.clicked:
                self.inputName()
            elif highscoreButton.clicked:
                self.highscoreMenu()
            elif rulesButton.clicked:
                self.rulesMenu()
            if quitButton.clicked:
                self.running = False
            
            pygame.display.update()
            
            # Caps Frames to 60
            self.clock.tick(60)

    def rulesMenu(self):
        # Sets up the text
        backButton = Button(30, 600, self.assets['backButton'], 1, self.assets['select_big'], sound=self.sounds['button_click'])

        # Sets up the text
        rules_text = self.title_font.render("Rules", True, "white")
        
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Draws the backgound object
            self.screen.fill('black')

            # Draws the buttons
            backButton.draw(self.screen)

            # Draws the text
            self.screen.blit(rules_text, ((self.screen.get_width() - rules_text.get_width()) / 2, 20))

            # Draws the rules
            rules = [
                "1. You have 100 points to start with",
                "2. For every correct letter you get 10 points",
                "3. For every wrong letter you lose 10 points",
                "4. If you lose all your points you lose",
                "5. If you guess the word you win",
                "6. You can guess the word by typing it in the text box",
                "7. You can guess a letter by clicking the keyboard",
            ]
            for i, rule in enumerate(rules):
                rule_text = self.small_font.render(rule, True, "white")
                rule_text = pygame.transform.scale_by(rule_text, 0.5)
                self.screen.blit(rule_text, (20, 150 + i * 60))

            # Checks if the buttons are clicked
            if backButton.clicked:
                self.menu()

            pygame.display.update()

            # Caps Frames to 60
            self.clock.tick(60)


    def highscoreMenu(self):
        # Sets up the buttons
        backButton = Button(30, 600, self.assets['backButton'], 1, self.assets['select_big'], sound=self.sounds['button_click'])
        
        # Render Highscores Title texts 
        highscore_text = self.title_font.render("Highscore", True, "white")
        easy_text = self.title_font.render("Easy", True, "white")
        medium_text = self.title_font.render("Medium", True, "white")
        hard_text = self.title_font.render("Hard", True, "white")

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Draws the backgound object
            self.screen.fill('black')

            # Draws the buttons
            backButton.draw(self.screen)

            # Draws the Title text
            self.screen.blit(highscore_text, ((self.screen.get_width() - highscore_text.get_width()) / 2, 20))

            # Calculate the horizontal positions for the texts
            spacing = self.screen.get_width() // 4
            easy_x = spacing - easy_text.get_width() // 2 - 100
            medium_x = 2 * spacing - medium_text.get_width() // 2
            hard_x = 3 * spacing - hard_text.get_width() // 2 + 100

            # Draw the texts at the calculated positions
            self.screen.blit(easy_text, (easy_x, 150))
            self.screen.blit(medium_text, (medium_x, 150))
            self.screen.blit(hard_text, (hard_x, 150))

            # Draws the highscores
            # easy 
            for i, score in enumerate(self.data['highscore_easy']):
                score_text = self.small_font.render(f"{score['name']} - {score['score']}", True, "white")
                self.screen.blit(score_text, (easy_x, 250 + i * 80))
            # medium
            for i, score in enumerate(self.data['highscore_medium']):
                score_text = self.small_font.render(f"{score['name']} - {score['score']}", True, "white")
                self.screen.blit(score_text, (medium_x, 250 + i * 80))
            # hard      
            for i, score in enumerate(self.data['highscore_hard']):
                score_text = self.small_font.render(f"{score['name']} - {score['score']}", True, "white")
                self.screen.blit(score_text, (hard_x, 250 + i * 80))

            # Checks if the buttons are clicked
            if backButton.clicked:
                self.menu()

            pygame.display.update()

            # Caps Frames to 60
            self.clock.tick(60)


    def inputName(self):
        # Sets up the text
        NameTitle = self.title_font.render("Enter Your Name", True, "white")

        # Sets up the text box
        nameBox = TextBox((self.screen.get_width() - 300) / 2, 250, '', self.assets['text_box'], sound=self.sounds['button_click'])
        nameBox.clicked = True
        enter = False


        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # Checks if the text box is clicked
                if nameBox.clicked:
                    enter = nameBox.text_update(event)

            # Checks if the enter key is pressed
            if enter:
                self.name = nameBox.text
                self.difficultyMenu()
            
            # Draws the backgound object
            self.screen.fill('black')

            # Draws the text box
            nameBox.draw(self.screen, self.title_font)

            # Draws the text
            self.screen.blit(NameTitle, ((self.screen.get_width() - NameTitle.get_width()) / 2, 20))

            pygame.display.update()

            # Caps Frames to 60
            self.clock.tick(60)


    def difficultyMenu(self):
        time.sleep(0.1)
        # Sets up the text
        select_diff_text = self.title_font.render("Select Difficulty", True, "white")

        # Sets up the buttons
        easyButton = Button((self.screen.get_width() - self.assets['easyButton'].get_width()) / 2, 300, self.assets['easyButton'], 1, self.assets['select_big'], sound=self.sounds['button_click'])
        mediumButton = Button((self.screen.get_width() - self.assets['mediumButton'].get_width()) / 2, 450, self.assets['mediumButton'], 1, self.assets['select_big'], sound=self.sounds['button_click'])
        hardButton = Button((self.screen.get_width() - self.assets['hardButton'].get_width()) / 2, 600, self.assets['hardButton'], 1, self.assets['select_big'], sound=self.sounds['button_click'])

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
            
            # Checks if the buttons are clicked and then starts the game loop
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

        # Sets up the text box
        text_box = TextBox((self.screen.get_width() - 300) / 2, 250, '', self.assets['text_box'], sound=self.sounds['button_click'])

        difficulty_text = self.title_font.render(difficulty, True, "white")

        # Selects a random word from the word list then 
        word = randomWordFromFile("data/word_lists/" + difficulty + "_words.txt")[0].replace("\n", "")
        letters = list(word)
        guessed_letters = []
        for i in letters:
            guessed_letters.append("")
        
        # Sets up the base for where the letters will be displayed
        word_length = len(word)
        empty_text = self.underline_font.render("_", False, "white")
        guess_letters_texts = []

        # Sets up the wrong guesses
        wrong_guesses = 0

        # Sets up the win state
        win_state = ""

        # Sets up the points text
        points_text = self.title_font.render(str(self.points), True, (255,255,255))
        
       # Create the keyboard with keys in three rows
        row1 = "qwertyuiop"
        row2 = "asdfghjkl"
        row3 = "zxcvbnm"
        keyboard = {}
        for i, k in enumerate(row1):
            keyboard[k] = key(100 + i * 110, 380, self.assets['key'], 1, k, 'data/font/Anarchaos.otf', self.assets['key_pressed'], self.assets['select'], sound=self.sounds['key_click'][random.randint(0, 3)])
        for i, k in enumerate(row2):
            keyboard[k] = key(130 + i * 110, 490, self.assets['key'], 1, k, 'data/font/Anarchaos.otf', self.assets['key_pressed'], self.assets['select'], sound=self.sounds['key_click'][random.randint(0, 3)])
        for i, k in enumerate(row3):
            keyboard[k] = key(160 + i * 110, 600, self.assets['key'], 1, k, 'data/font/Anarchaos.otf', self.assets['key_pressed'], self.assets['select'], sound=self.sounds['key_click'][random.randint(0, 3)])

        # Create a new surface for the empty_texts
        empty_text_surface = pygame.Surface((80 * word_length, 200), pygame.SRCALPHA)

        # Main game loop
        while self.running:
            # Checks if the events and if to close the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if text_box.clicked:
                    enter = text_box.text_update(event)

            # Checks if the text box is clicked and if the enter key is pressed to check the letter is in the word
            length = len(text_box.text)
            if enter and length > 0 and not win_state == "win":
               guessed_letters, win_state = self.checkLetter(length, text_box.text, letters, guessed_letters, word)
               if text_box.text in keyboard.keys():
                    keyboard[text_box.text].pressed = True
               if not text_box.text in letters:
                    wrong_guesses += 1 # Increment the wrong guesses
               text_box.text = ""
                
            # Checks if the player has won or lost
            if self.points <= 0:
                win_state = "lose"
            
            # Render the text
            points_text = self.title_font.render(str(self.points), True, (255,255,255))

            guess_letters_texts = [self.title_font.render(i, True, "white") for i in guessed_letters]

            # Draws the backgound object
            self.screen.fill('black')

            # Draws the text
            self.screen.blit(difficulty_text, ((self.screen.get_width() - difficulty_text.get_width()) / 2 , 20))

            # Draws the word
            empty_text_surface.fill((0, 0, 0, 0))  # Clear the surface
            for i in range(word_length):
                empty_text_surface.blit(empty_text, (i * 80, 0))
                self.screen.blit(guess_letters_texts[i], ((self.screen.get_width() - (empty_text.get_width()) * word_length) / 2 + i * 80, 100))
            self.screen.blit(empty_text_surface, ((self.screen.get_width() - empty_text_surface.get_width()) / 2, 90))
            
            # Draws the text box
            text_box.draw(self.screen, self.title_font)

            self.screen.blit(points_text, (20, 20))

            # Draws the hangman stages
            
            if wrong_guesses >= 8:
                win_state = "lose"
            elif wrong_guesses > 0:
                hangman_image = self.assets[f'hangman'][wrong_guesses - 1]
                hangman_image.set_colorkey((0, 0, 0))
                self.screen.blit(hangman_image, (200, 120))

            # Draws the keyboard
            for i in keyboard.values():
                if i.draw(self.screen) and not i.pressed and not text_box.clicked:
                    i.pressed = True
                    guessed_letters, win_state = self.checkLetter(1, i.letter, letters, guessed_letters, word)
                    if not i.letter in letters:
                        wrong_guesses += 1

            # Checks the winstate
            if win_state == "win":
                self.points += 100
                self.mainGameLoop(difficulty)
            elif win_state == "lose":

                self.loseScreen(self.points, word, difficulty)
            
            pygame.display.update()

            # Caps Frames to 60
            self.clock.tick(60)
    

    def loseScreen(self, points, word, diff):
        # Adds the highscore to the save file
        self.data['highscore_' + diff].append({"score":  points, "name": self.name})
        
        # Sorts the list by score in descending order and then takes the top 5
        self.data['highscore_' + diff] = sorted(
            self.data['highscore_' + diff], key=lambda x: x['score'], reverse=True)[:5]
        
        # Saves the data to the save.json file
        json.dump(self.data, open("data/save.json", 'w'))

        # Resets the points
        self.points = 100

        # Sets up the text
        you_lose_text = self.title_font.render("Game Over!", True, (255, 255, 255))
        word_text = self.small_font.render(f"The word was {word}!!", True, (255, 255, 255))
        highscore_text = self.small_font.render(f"Highscore: {self.data['highscore_' + diff][0]['score']}", True, (255, 255, 255))
        points_text = self.small_font.render(f"Score: {points}", True, (255, 255, 255))

        # Create a semi-transparent overlay
        surface = pygame.Surface((1280, 720), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 128))
        # Sets up the background
        overlay = self.screen.copy()
        overlay.set_alpha(128)  # Set transparency level (0-255)

        # Sets up the buttons
        playButton = Button((self.screen.get_width() - 180) / 2, 320, self.assets['playButton'], 1, self.assets['select_big'], sound=self.sounds['button_click'])
        menuButton = Button((self.screen.get_width() - 180) / 2, 440, self.assets['menuButton'], 1, self.assets['select_big'], sound=self.sounds['button_click'])
        quitButton = Button((self.screen.get_width() - 180) / 2, 550, self.assets['quitButton'], 1, self.assets['select_big'], sound=self.sounds['button_click'])

        # Main loop
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Blit the overlay onto the screen
            self.screen.blit(overlay, (0, 0))
            self.screen.blit(surface, (0, 0))

            # Draw the lose screen text
            self.screen.blit(you_lose_text, ((self.screen.get_width() - you_lose_text.get_width()) / 2, 20))
            self.screen.blit(word_text, (265, 120))
            self.screen.blit(highscore_text, (265, 180))
            self.screen.blit(points_text, (265, 240))


            # Draws the buttons
            playButton.draw(self.screen)
            menuButton.draw(self.screen)
            quitButton.draw(self.screen)

            # Draw Hangman
            hangman_image = pygame.transform.scale_by(self.assets['hangman'][7], 1.5)
            hangman_image.set_colorkey((0, 0, 0))            
            self.screen.blit(hangman_image, (200, 300))

            # Checks if the buttons are clicked
            if playButton.clicked:
                self.difficultyMenu()
            if menuButton.clicked:
                self.menu()
            if quitButton.clicked:
                self.running = False

            pygame.display.update()

            # Caps Frames to 60
            self.clock.tick(60)



game = Game()
game.menu()


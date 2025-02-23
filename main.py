import pygame
import english_words
import random

web2lowerset = english_words.get_english_words_set(['web2'], lower=True)

word = random.sample(sorted(web2lowerset), 1)[0]
print(word)
chosen_word = ""


letters = ""
for i in range(len(word)):
    letters += "_ "
    chosen_word += " "

points = 100

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

arial = pygame.font.SysFont("arial", 20)
score_text = arial.render(f"Score: {points}", True, "black")

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    # RENDER YOUR GAME HERE
    score_text = arial.render(f"Score: {points}", True, "black")
    screen.blit(score_text, (100, 200))
    

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()

print(letters)
while chosen_word != word and points > 0:
    x = input("pick a word or letter?")
    if x == "word":
        print
        if input("word: ") == word:
            
            chosen_word = word
        else: 
            points -= 10
    elif x == "letter":
        y = input("letter: ")
        
        if y in list(word):
            print('s')
            
            for i in get_indices(word, y):
                print
                lst_chosen_word = list(chosen_word)
                lst_letters = list(letters)

                lst_chosen_word[i] = y
                lst_letters[2*i] = y
                print('sf')
            
                chosen_word = ''.join(lst_chosen_word)
                letters = ''.join(lst_letters)
        else: 
            points -= 10
                
    
    print(letters)

if points > 0:
    print(f"WIN YOU!! \n You scored {points} points")
else: 
    print("You lose :(")

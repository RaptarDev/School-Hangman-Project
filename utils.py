import os
import pygame
import random
import json

BASE_IMG_PATH = 'data/images/'

def loadImage(path, scale = 1):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((255, 255, 255))
    img = pygame.transform.scale_by(img, scale)
    return img.convert()

def loadImages(path, scale = 1):
    images = []
    for img_name in os.listdir(BASE_IMG_PATH + path):
        images.append(loadImage(path + '/' + img_name, scale))
    print(images)
    return images

class Animation:
    def __init__(self, images, imgDur=5, loop=True, scale = 1):
        self.images = images
        self.loop = loop
        self.imgDuration = imgDur
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images, self.imgDuration, self.loop)

    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.imgDuration * len(self.images))
        else:
            self.frame = min(self.frame, self.imgDuration * len(self.images) - 1)
            if self.frame >= self.imgDuration * len(self.images) - 1:
                self.done = True


    def img(self):
        return self.images[int(self.frame / self.imgDuration)]

def randomWordFromFile(file_path):
    f = open(file_path, "r")
    lines = f.readlines()
    return random.sample(lines, 1)

def loadSave(saveFile, base_data):
    try:
        f = open(saveFile, 'r')
        return json.load(f)
    except:
        json.dump(base_data, open(saveFile, 'w'))
        return base_data
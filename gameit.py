#!/usr/bin/python3
import pygame

pygame.init()
pygame.event.set_allowed((pygame.KEYDOWN, pygame.QUIT))
pygame.display.set_caption('gameit.py')
pygame.display.init()
screen = pygame.display.set_mode((1024, 768))

while 1:
    for evt in pygame.event.get():
        print(f"event! {evt}, {evt.type}")
        if evt.type == pygame.KEYDOWN:
            ko = evt.key
            if 0:  # not ko:
                continue
            print(f"<{ko}>")

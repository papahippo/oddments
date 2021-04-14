#!/usr/bin/python3
import pygame


def main():
    pygame.init()
    song = pygame.mixer.Sound('/usr/share/sounds/KDE-Im-Phone-Ring.ogg')
    clock = pygame.time.Clock()
    song.play()
    while True:
        clock.tick(60)
    pygame.quit()



if __name__ == "__main__":
    main()

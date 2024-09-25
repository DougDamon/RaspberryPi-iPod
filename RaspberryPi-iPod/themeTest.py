import pygame
import pygame_gui
import os


print(os.getcwd())
themefile = 'test_theme.json'
pygame.init()
pygame.display.set_caption('Test')
window_surface = pygame.display.set_mode((320,240))
background = pygame.Surface((320,240))
background.fill(pygame.Color('aquamarine1'))
manager = pygame_gui.UIManager((320,240), themefile) 

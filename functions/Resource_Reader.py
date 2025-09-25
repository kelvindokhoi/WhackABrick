import pygame,sys,os
def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores files in sys._MEIPASS/resource
        base_path = os.path.join(sys._MEIPASS, "resource") #type:ignore
    except AttributeError:
        # In development, use the resource directory
        base_path = os.path.abspath(".\\resource")
    return os.path.join(base_path, relative_path)

def image_loader(image_path, dimension, alpha=True):
    if alpha:
        return pygame.transform.scale(pygame.image.load(resource_path(image_path)).convert_alpha(),dimension)
    else:
        return pygame.transform.scale(pygame.image.load(resource_path(image_path)).convert(),dimension)
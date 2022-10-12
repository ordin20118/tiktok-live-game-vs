import pygame


stone_tile = pygame.transform.scale(pygame.image.load('game/res/tile/stone_texture_1.png'), (10,10))

soldier_images_right = []
def import_soldier_right(size):
    soldier_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Run_1.png'), size), True, False))
    soldier_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Run_2.png'), size), True, False))
    soldier_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Run_3.png'), size), True, False))
    soldier_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Run_4.png'), size), True, False))
    soldier_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Run_5.png'), size), True, False))
    soldier_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Run_6.png'), size), True, False))
    soldier_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Run_7.png'), size), True, False))
    soldier_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Run_8.png'), size), True, False))
    soldier_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Run_9.png'), size), True, False))
    soldier_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Run_10.png'), size), True, False))
    soldier_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Attack_1.png'), size), True, False))
    soldier_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Attack_2.png'), size), True, False))
    soldier_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Attack_3.png'), size), True, False))
    soldier_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Attack_4.png'), size), True, False))
    soldier_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Attack_5.png'), size), True, False))
    soldier_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Attack_6.png'), size), True, False))
    soldier_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Attack_7.png'), size), True, False))
    soldier_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Attack_8.png'), size), True, False))
    soldier_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Attack_9.png'), size), True, False))
    soldier_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Attack_10.png'), size), True, False))


            
solider_images_left = []
def import_soldier_left(size):
    solider_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Run_1.png'), size))
    solider_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Run_2.png'), size))
    solider_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Run_3.png'), size))
    solider_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Run_4.png'), size))
    solider_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Run_5.png'), size))
    solider_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Run_6.png'), size))
    solider_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Run_7.png'), size))
    solider_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Run_8.png'), size))
    solider_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Run_9.png'), size))
    solider_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Run_10.png'), size))
    solider_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Attack_1.png'), size))
    solider_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Attack_2.png'), size))
    solider_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Attack_3.png'), size))
    solider_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Attack_4.png'), size))
    solider_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Attack_5.png'), size))
    solider_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Attack_6.png'), size))
    solider_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Attack_7.png'), size))
    solider_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Attack_8.png'), size))
    solider_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Attack_9.png'), size))
    solider_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Attack_10.png'), size))



castle_images_right = []
def import_castle_right(size):  
    castle_images_right.append(pygame.transform.scale(pygame.image.load('game/res/castle/png/castle_1.png'), size))
    castle_images_right.append(pygame.transform.scale(pygame.image.load('game/res/castle/png/castle_2.png'), size))
    castle_images_right.append(pygame.transform.scale(pygame.image.load('game/res/castle/png/castle_3.png'), size))
            
castle_images_left = []
def import_castle_left(size):
    castle_images_left.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/castle/png/castle_1.png'), size), True, False))
    castle_images_left.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/castle/png/castle_2.png'), size), True, False))
    castle_images_left.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/castle/png/castle_3.png'), size), True, False))

stone_tile_images = []
stone_tile = pygame.transform.scale(pygame.image.load('game/res/tile/stone_texture_1.png'), (50,50))
stone_tile_images.append(stone_tile)


ground_tile_images = []
def import_ground_images(size):
    ground_tile_images.append(pygame.transform.scale(pygame.image.load('game/res/tile/ground_1.png'), size))
    ground_tile_images.append(pygame.transform.scale(pygame.image.load('game/res/tile/ground_2.png'), size))
    ground_tile_images.append(pygame.transform.scale(pygame.image.load('game/res/tile/ground_3.png'), size))
    ground_tile_images.append(pygame.transform.scale(pygame.image.load('game/res/tile/ground_4.png'), size))


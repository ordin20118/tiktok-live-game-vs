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
    soldier_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Dead_1.png'), (size[0] * 1.5, size[1] * 1.2)), True, False))
    soldier_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Dead_2.png'), (size[0] * 1.5, size[1] * 1.2)), True, False))
    soldier_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Dead_3.png'), (size[0] * 1.5, size[1] * 1.2)), True, False))
    soldier_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Dead_4.png'), (size[0] * 1.5, size[1] * 1.2)), True, False))
    soldier_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Dead_5.png'), (size[0] * 1.5, size[1] * 1.2)), True, False))
    soldier_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Dead_6.png'), (size[0] * 1.5, size[1] * 1.2)), True, False))
    soldier_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Dead_7.png'), (size[0] * 1.5, size[1] * 1.2)), True, False))
    soldier_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Dead_8.png'), (size[0] * 1.5, size[1] * 1.2)), True, False))
    soldier_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Dead_9.png'), (size[0] * 1.5, size[1] * 1.2)), True, False))
    soldier_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Dead_10.png'), (size[0] * 1.5, size[1] * 1.2)), True, False))    

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
    solider_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Dead_1.png'), (size[0] * 1.5, size[1] * 1.2)))
    solider_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Dead_2.png'), (size[0] * 1.5, size[1] * 1.2)))
    solider_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Dead_3.png'), (size[0] * 1.5, size[1] * 1.2)))
    solider_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Dead_4.png'), (size[0] * 1.5, size[1] * 1.2)))
    solider_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Dead_5.png'), (size[0] * 1.5, size[1] * 1.2)))
    solider_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Dead_6.png'), (size[0] * 1.5, size[1] * 1.2)))
    solider_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Dead_7.png'), (size[0] * 1.5, size[1] * 1.2)))
    solider_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Dead_8.png'), (size[0] * 1.5, size[1] * 1.2)))
    solider_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Dead_9.png'), (size[0] * 1.5, size[1] * 1.2)))
    solider_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Dead_10.png'), (size[0] * 1.5, size[1] * 1.2)))

knight_images_right = []
def import_knight_right(size):
    knight_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight_gold/knight_run_01.png'), size), True, False))
    knight_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight_gold/knight_run_02.png'), size), True, False))
    knight_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight_gold/knight_run_03.png'), size), True, False))
    knight_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight_gold/knight_run_04.png'), size), True, False))
    knight_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight_gold/knight_run_05.png'), size), True, False))
    knight_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight_gold/knight_run_06.png'), size), True, False))
    knight_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight_gold/knight_run_07.png'), size), True, False))
    knight_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight_gold/knight_run_08.png'), size), True, False))
    knight_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight_gold/knight_run_09.png'), size), True, False))
    knight_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight_gold/knight_run_10.png'), size), True, False))
    knight_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight_gold/knight_attack_01.png'), size), True, False))
    knight_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight_gold/knight_attack_02.png'), size), True, False))
    knight_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight_gold/knight_attack_03.png'), size), True, False))
    knight_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight_gold/knight_attack_04.png'), size), True, False))
    knight_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight_gold/knight_attack_05.png'), size), True, False))
    knight_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight_gold/knight_attack_06.png'), size), True, False))
    knight_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight_gold/knight_attack_07.png'), size), True, False))
    knight_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight_gold/knight_attack_08.png'), size), True, False))
    knight_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight_gold/knight_attack_09.png'), size), True, False))
    knight_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight_gold/knight_attack_10.png'), size), True, False))
    

knight_images_left = []
def import_knight_left(size):
    knight_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight_gold/knight_run_01.png'), size))
    knight_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight_gold/knight_run_02.png'), size))
    knight_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight_gold/knight_run_03.png'), size))
    knight_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight_gold/knight_run_04.png'), size))
    knight_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight_gold/knight_run_05.png'), size))
    knight_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight_gold/knight_run_06.png'), size))
    knight_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight_gold/knight_run_07.png'), size))
    knight_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight_gold/knight_run_08.png'), size))
    knight_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight_gold/knight_run_09.png'), size))
    knight_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight_gold/knight_run_10.png'), size))
    knight_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight_gold/knight_attack_01.png'), size))
    knight_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight_gold/knight_attack_02.png'), size))
    knight_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight_gold/knight_attack_03.png'), size))
    knight_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight_gold/knight_attack_04.png'), size))
    knight_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight_gold/knight_attack_05.png'), size))
    knight_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight_gold/knight_attack_06.png'), size))
    knight_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight_gold/knight_attack_07.png'), size))
    knight_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight_gold/knight_attack_08.png'), size))
    knight_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight_gold/knight_attack_09.png'), size))
    knight_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight_gold/knight_attack_10.png'), size))



lightning_images = []
def import_lightning_images(size):
    lightning_images.append(pygame.transform.scale(pygame.image.load('game/res/skill/lightning/lightning_1.png'), size))
    lightning_images.append(pygame.transform.scale(pygame.image.load('game/res/skill/lightning/lightning_2.png'), size))
    lightning_images.append(pygame.transform.scale(pygame.image.load('game/res/skill/lightning/lightning_3.png'), size))
    lightning_images.append(pygame.transform.scale(pygame.image.load('game/res/skill/lightning/lightning_4.png'), size))
    lightning_images.append(pygame.transform.scale(pygame.image.load('game/res/skill/lightning/lightning_5.png'), size))
    lightning_images.append(pygame.transform.scale(pygame.image.load('game/res/skill/lightning/lightning_6.png'), size))
    lightning_images.append(pygame.transform.scale(pygame.image.load('game/res/skill/lightning/lightning_7.png'), size))


devil_images = []
def import_devil_images(size):
    devil_images.append(pygame.transform.scale(pygame.image.load('game/res/skill/devil/devil_1.png'), size))
    devil_images.append(pygame.transform.scale(pygame.image.load('game/res/skill/devil/devil_2.png'), size))
    devil_images.append(pygame.transform.scale(pygame.image.load('game/res/skill/devil/devil_3.png'), size))
    devil_images.append(pygame.transform.scale(pygame.image.load('game/res/skill/devil/devil_4.png'), size))



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

menu_images = []
def import_menu_images(size, skills):
    for skill in skills:
        print(skill['image'])
        menu_images.append(pygame.transform.scale(pygame.image.load(skill['image']), size))


def import_sound():
    sound_map = {}
    devil_sound = pygame.mixer.Sound("game/res/sound/devil_boss_laugh.mp3")
    devil_sound.set_volume(0.2)
    sound_map['devil'] = devil_sound
    donation_sound = pygame.mixer.Sound("game/res/sound/donation.mp3")
    donation_sound.set_volume(0.7)
    sound_map['donation'] = donation_sound
    thunder_sound = pygame.mixer.Sound("game/res/sound/thunder_3.mp3")
    thunder_sound.set_volume(0.1)
    sound_map['thunder'] = thunder_sound
    stage_clear_sound = pygame.mixer.Sound("game/res/sound/stage_clear.mp3")
    stage_clear_sound.set_volume(0.7)
    sound_map['stage_clear'] = stage_clear_sound
    sword_attack_sound = pygame.mixer.Sound("game/res/sound/sword_attack.mp3")
    sword_attack_sound.set_volume(0.1)
    sound_map['sword_attack'] = sword_attack_sound
    return sound_map
    
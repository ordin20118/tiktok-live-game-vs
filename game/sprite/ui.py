import pygame
     
class SkillMenuSprite(pygame.sprite.Sprite):

    # state
    # 0: none
    # 1: can't use
    def __init__(self, size, position, group, name, coin, images, game):

        super(SkillMenuSprite, self).__init__()

        self.game = game
        self.name = name
        self.coin = coin
        self.state = 0
        self.group = group
        self.images = images        
        self.rect = pygame.Rect(position, size)
        self.img_index = 0
        self.img_index_start = 0
        self.img_index_end = 0
        self.image = self.images[self.img_index]          
        self.animation_time = 1

        # mt와 결합하여 animation_time을 계산할 시간 초기화
        self.current_time = 0

    def draw(self):
        #print("메뉴 DRAW")
        name_text = self.game.main_font_15.render(self.name, True, self.game.COLOR_WHITE)            
        name_text_rect = name_text.get_rect()        
        name_text_size = name_text_rect.size
        name_text_rect.centerx = self.rect.centerx
        self.game.SCREEN.blit(name_text, (name_text_rect.x, self.rect.y + self.rect.size[1] + 10))
        
        coin_text = self.game.main_font_11.render('%d Coin' % self.coin, True, self.game.COLOR_YELLOW)            
        coin_text_rect = coin_text.get_rect()        
        name_text_size = coin_text_rect.size
        coin_text_rect.centerx = self.rect.centerx
        self.game.SCREEN.blit(coin_text, (coin_text_rect.x, self.rect.y + self.rect.size[1] + name_text_rect.size[1] + 10))

    def draw_back(self):
        pass
        #pygame.draw.rect(self.game.SCREEN, (131, 133, 131), [self.rect.x, self.rect.y, self.rect.size[0], self.rect.size[1]], border_radius=5)
        
                

    def update(self, mt, game):
        pass

class DonationSprite(pygame.sprite.Sprite):

    # state
    # 0: none
    # 1: can't use
    def __init__(self, size, position, group, name, coin, images, sound, game):

        super(DonationSprite, self).__init__()

        self.game = game
        self.name = name
        self.coin = coin
        self.state = 0
        self.group = group
        self.images = images        
        self.rect = pygame.Rect(position, size)
        self.img_index = 0
        self.img_index_start = 0
        self.img_index_end = 0
        self.image = self.images[self.img_index]          
        self.animation_time = 2
        self.sound = sound
        self.sound.play()

        # mt와 결합하여 animation_time을 계산할 시간 초기화
        self.current_time = 0

    def draw(self):
        #print("메뉴 DRAW")
        name_text = self.game.main_font_15.render(self.name, True, self.game.COLOR_WHITE)            
        name_text_rect = name_text.get_rect()        
        name_text_size = name_text_rect.size
        
        name_text_rect.centerx = self.rect.centerx
        self.game.SCREEN.blit(name_text, (name_text_rect.x, self.rect.y + self.rect.size[1] + 10))
        
        coin_text = self.game.main_font_11.render('%d Coin' % self.coin, True, self.game.COLOR_YELLOW)            
        coin_text_rect = coin_text.get_rect()        
        name_text_size = coin_text_rect.size
        coin_text_rect.centerx = self.rect.centerx
        self.game.SCREEN.blit(coin_text, (coin_text_rect.x, self.rect.y + self.rect.size[1] + name_text_rect.size[1] + 10))

    def draw_back(self):
        pass
        #pygame.draw.rect(self.game.SCREEN, (131, 133, 131), [self.rect.x, self.rect.y, self.rect.size[0], self.rect.size[1]], border_radius=5)

    def update(self, mt, game):
        # TODO: 일정 시간(1.3초) 후 사라짐
        self.current_time += mt
        if self.current_time >= self.animation_time:
            self.current_time = 0
           
            self.img_index += 1
            if self.img_index >= self.img_index_end:                
                self.img_index = self.img_index_start
                self.game.donation_state = True
                self.kill()    
                return
        
        

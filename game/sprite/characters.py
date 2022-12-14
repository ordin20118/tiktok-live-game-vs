import pygame
import random

# 기본 오브젝트 클래스
class BaseObject:
    def __init__(self, size, position, movement, group, hp, power, name, profile, images, game):
        self.game = game
        self.name = name
        self.profile = profile
        self.state = 1
        self.hp = hp
        self.hp_max = hp
        self.power = power
        self.movement = movement
        self.now_movement = movement
        self.group = group
        self.type = 1
        self.images = images
    
    def move(self):
        dx, dy = self.now_movement
        self.rect.x += dx
        self.rect.y += dy

    def update(self, mt, game):
        pass

    def draw(self, mt):
        pass
    
    def draw_back(self):
        pass

    def damaged(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.destroy_self()

    def destroy_self(self):
        self.kill()

class SoldierSprite(pygame.sprite.Sprite, BaseObject):

    # state
    # 0: idle
    # 1: move
    # 2: attack
    # 3: die
    # type
    # 1: character
    # 2: structure(castle)
    # 3: skill
    def __init__(self, size, position, movement, state, group, hp, power, name, profile, images, game):

        super(SoldierSprite, self).__init__()

        self.game = game
        self.name = name        
        self.profile = profile
        self.state = state
        self.hp = hp
        self.hp_max = hp
        self.power = power
        self.movement = movement
        self.now_movement = movement
        self.group = group
        self.type = 1
        self.chat = None    # 사용자 채팅        

        # 이미지를 Rect안에 넣기 위해 Rect의 크기 지정
        # 이미지의 크기와 같게 하거나, 크기를 다르게 한다면 pygame.transform.scale을 사용하여 rect 안에
        # 이미지를 맞추도록 한다.
        #size = (60, 60)

        self.images = images
    
        
        # Rect 크기와 Image 크기 맞추기. pygame.transform.scale
        #self.images = [pygame.transform.scale(image, size) for image in images]         

        # rect 만들기
        self.rect = pygame.Rect(position, size)

        # 캐릭터의 첫번째 이미지
        
        if self.state == 0:
            self.img_index_start = 0
            self.img_index_end = 9
        elif self.state == 1:
            self.img_index_start = 0
            self.img_index_end = 9
        elif self.state == 2:
            self.img_index_start = 10
            self.img_index_end = 19
        elif self.state == 3:
            self.img_index_start = 20
            self.img_index_end = 29

        self.img_index = self.img_index_start
        self.image = self.images[self.img_index]  # 'image' is the current image of the animation.

        # 1초에 보여줄 1장의 이미지 시간을 계산, 소수점 3자리까지 반올림
        #self.animation_time = round(100 / len(self.images * 100), 2)
        img_len = self.img_index_end - self.img_index_start + 1
        self.animation_time = round(100 / (img_len * 150), 2)
        self.chat_animation_time = 3
        self.chat_animation_now = 0

        # mt와 결합하여 animation_time을 계산할 시간 초기화
        self.current_time = 0
        self.current_attack_time = 0

    def update(self, mt, game):
        
        self.move()
        
        if self.group == 'left':
            self.collide_enemy(mt, game.right_group, game)
        else:
            self.collide_enemy(mt, game.left_group, game)

        if self.state == 0:
            self.img_index_start = 0
            self.img_index_end = 9
        elif self.state == 1:
            self.img_index_start = 0
            self.img_index_end = 9
        elif self.state == 2:
            self.img_index_start = 10
            self.img_index_end = 19
        elif self.state == 3:
            self.img_index_start = 20
            self.img_index_end = 29

        # loop 시간 더하기
        self.current_time += mt

        # loop time 경과가 animation_time을 넘어서면 새로운 이미지 출력 
        if self.current_time >= self.animation_time:
            self.current_time = 0
           
            self.img_index += 1
            if self.img_index >= self.img_index_end:
                self.img_index = self.img_index_start
                if self.state == 3: # 죽은 상태 애니메이션의 경우 완료 후 self 제거
                    self.kill()
                    return

            self.image = self.images[self.img_index]

    def draw(self, mt):
        # 채팅 출력
        if self.chat != None:

            msg = self.chat
            if len(msg) >= 25:
                msg = msg[0:25] + '...'
            chat = self.game.main_font_15.render(msg, True, self.game.COLOR_BLACK)
            chat_rect = chat.get_rect()
            chat_size = chat_rect.size
            # 채팅창
            chat_back_rect = pygame.draw.rect(self.game.SCREEN, self.game.COLOR_WHITE, [self.rect.x, self.rect.y - 30, chat_size[0] + 20, chat_size[1] + 10])
            chat_rect.centerx = chat_back_rect.centerx
            # 채팅 메시지
            self.game.SCREEN.blit(chat, (self.rect.x + 10, chat_back_rect.y + 3))
            self.chat_animation_now += mt
            if self.chat_animation_now >= self.chat_animation_time:
                self.chat = None
                self.chat_animation_now = 0
        
        # 닉네임 출력        
        if self.name != 'left_soldier' and self.name != 'right_soldier' and self.name != 'dead_soldier':
            name = self.name
            if len(self.name) > 10:
                name = self.name[0:10]

            nickname_text = self.game.main_font_13.render(name, True, self.game.COLOR_BLACK)
            nickname_text_rect = nickname_text.get_rect()
            nickname_text_size = nickname_text_rect.size            
            nickname_text_rect.centerx = self.rect.centerx            
            self_size_y = self.rect.size[1]
            nick_xy = (nickname_text_rect.x, self.rect.y + self_size_y + 2)
            self.game.SCREEN.blit(nickname_text, nick_xy)
        
            # 프로필 출력
            if self.profile != None:
                self.game.SCREEN.blit(self.profile, (nickname_text_rect.x - self.game.profile_size[0] - 5, nick_xy[1] - (self.game.profile_size[1] * 0.2)))

        # 체력바 그리기
        if self.hp < self.hp_max:
            pygame.draw.rect(self.game.SCREEN, (131, 133, 131), [self.rect.x - 1, self.rect.y - 5 , 50, 10])
            pygame.draw.rect(self.game.SCREEN, (189, 76, 49), [self.rect.x - 1, self.rect.y - 5, 50 * self.hp / self.hp_max, 10])


    def collide_enemy(self, mt, enemy_group, game):
        
        if self.state == 3:
            return

        collide = pygame.sprite.pygame.sprite.spritecollide(self, enemy_group, False)

        if collide:
            # 정상적으로 작동하는지 확인하기 위해 부딪혔을 때 collide라는 문자열이 나오게 한다.
            #print("%s detect collide" % self.group)
            
            if(self.state == 2):

                self.current_attack_time += mt

                #print("attack_time:[%s] / animation_time[%s]" % (mt ,self.animation_time))

                # attack loop time 경과가 animation_time을 넘어서면 새로운 이미지 출력 
                if self.current_attack_time >= self.animation_time * 10:
                    self.current_attack_time = 0                    
                    
                    # 20% 확률로 출력
                    rnum = random.randint(0, 4)
                    if rnum == 1:
                        self.game.sound_map['sword_attack'].play()

                    for enemy in collide:
                        if enemy.type == 1:
                            enemy.damaged(self.power)
                        elif enemy.type == 2:
                            enemy.damaged(self.power)

            else:
                self.state = 2
                self.img_index = 10
                self.now_movement = (0, 0)
            
            
        else:
            #print("%s is no collide" % self.group)
            self.state = 1
            if self.group == 'left':
                self.now_movement = (1, 0)
            else:
                self.now_movement = (-1, 0)
    
    def destroy_self(self):
        # 죽음 상태의 솔져 생성
        if self.group == 'left':
            interval_x = (self.rect.size[0] * 1.5) - self.rect.size[0]
            sp_xy = (self.rect.x - interval_x, self.rect.y)
            sp_size = (self.rect.size[0] * 1.2, self.rect.size[1])
            dead_player = SoldierSprite(size=sp_size, position=sp_xy, movement=(0,0), state=3, group='left', 
                                                    hp=100, power=0, name='dead_soldier', profile=None, images=self.images, game=self.game)
            self.game.sprite_group.add(dead_player)
        else:
            sp_xy = (self.rect.x, self.rect.y)
            sp_size = (self.rect.size[0] * 1.2, self.rect.size[1])
            dead_player = SoldierSprite(size=sp_size, position=sp_xy, movement=(0,0), state=3, group='right', 
                                                    hp=100, power=0, name='dead_soldier', profile=None, images=self.images, game=self.game)
            self.game.sprite_group.add(dead_player)
        self.kill()


class KnightSprite(pygame.sprite.Sprite, BaseObject):

    # state
    # 0: idle
    # 1: move
    # 2: attack
    # 3: die
    def __init__(self, size, position, movement, group, hp, power, name, profile, images, game):

        super(KnightSprite, self).__init__()

        self.game = game
        self.name = name          
        self.profile = profile
        self.state = 1
        self.hp = hp
        self.hp_max = hp
        self.power = power
        self.movement = movement
        self.now_movement = movement
        self.group = group
        self.type = 1
        self.chat = None    # 사용자 채팅     

        # 이미지를 Rect안에 넣기 위해 Rect의 크기 지정
        # 이미지의 크기와 같게 하거나, 크기를 다르게 한다면 pygame.transform.scale을 사용하여 rect 안에
        # 이미지를 맞추도록 한다.
        #size = (60, 60)

        self.images = images
    
        
        # Rect 크기와 Image 크기 맞추기. pygame.transform.scale
        #self.images = [pygame.transform.scale(image, size) for image in images]         

        # rect 만들기
        self.rect = pygame.Rect(position, size)

        # 캐릭터의 첫번째 이미지
        self.img_index = 0
        self.img_index_start = 0
        self.img_index_end = 9
        self.image = self.images[self.img_index]  # 'image' is the current image of the animation.

        # 1초에 보여줄 1장의 이미지 시간을 계산, 소수점 3자리까지 반올림
        #self.animation_time = round(100 / len(self.images * 100), 2)
        img_len = self.img_index_end - self.img_index_start + 1
        self.animation_time = round(100 / (img_len * 150), 2)

        self.chat_animation_time = 3
        self.chat_animation_now = 0

        # mt와 결합하여 animation_time을 계산할 시간 초기화
        self.current_time = 0
        self.current_attack_time = 0

    def update(self, mt, game):
        # update를 통해 캐릭터의 이미지가 계속 반복해서 나타나도록 한다.
        
        self.move()
        
        if self.group == 'left':
            self.collide_enemy(mt, game.right_group, game)
        else:
            self.collide_enemy(mt, game.left_group, game)

        if self.state == 0:
            self.img_index_start = 0
            self.img_index_end = 9
        elif self.state == 1:
            self.img_index_start = 0
            self.img_index_end = 9
        elif self.state == 2:
            self.img_index_start = 10
            self.img_index_end = 19
        elif self.state == 3:
            self.img_index_start = 20
            self.img_index_end = 29

        # loop 시간 더하기
        self.current_time += mt

        # loop time 경과가 animation_time을 넘어서면 새로운 이미지 출력 
        if self.current_time >= self.animation_time:
            self.current_time = 0
           
            self.img_index += 1
            if self.img_index >= self.img_index_end:
                self.img_index = self.img_index_start

            self.image = self.images[self.img_index]

    def draw(self, mt):
        # 채팅 출력
        if self.chat != None:

            msg = self.chat
            if len(msg) >= 25:
                msg = msg[0:25] + '...'
            chat = self.game.main_font_15.render(msg, True, self.game.COLOR_BLACK)
            chat_rect = chat.get_rect()
            chat_size = chat_rect.size
            # 채팅창
            chat_back_rect = pygame.draw.rect(self.game.SCREEN, self.game.COLOR_WHITE, [self.rect.x, self.rect.y - 30, chat_size[0] + 20, chat_size[1] + 10])
            chat_rect.centerx = chat_back_rect.centerx
            # 채팅 메시지
            self.game.SCREEN.blit(chat, (self.rect.x + 10, chat_back_rect.y + 3))
            self.chat_animation_now += mt
            if self.chat_animation_now >= self.chat_animation_time:
                self.chat = None
                self.chat_animation_now = 0
        
        # 닉네임 출력        
        if self.name != 'left_knight' and self.name != 'right_knight' and self.name != 'dead_knight':
            nickname_text = self.game.main_font_13.render(self.name, True, self.game.COLOR_BLACK)
            nickname_text_rect = nickname_text.get_rect()
            nickname_text_size = nickname_text_rect.size            
            nickname_text_rect.centerx = self.rect.centerx            
            self_size_y = self.rect.size[1]
            nick_xy = (nickname_text_rect.x, self.rect.y + self_size_y + 2)
            self.game.SCREEN.blit(nickname_text, nick_xy)

            # 프로필 출력
            if self.profile != None:
                self.game.SCREEN.blit(self.profile, (nickname_text_rect.x - self.game.profile_size[0] - 5, nick_xy[1] - (self.game.profile_size[1] * 0.2)))

        # 체력바 그리기
        if self.hp < self.hp_max:
            pygame.draw.rect(self.game.SCREEN, (131, 133, 131), [self.rect.x - 1, self.rect.y - 5 , 50, 10])
            pygame.draw.rect(self.game.SCREEN, (189, 76, 49), [self.rect.x - 1, self.rect.y - 5, 50 * self.hp / self.hp_max, 10])


    def collide_enemy(self, mt, enemy_group, game):
        
        collide = pygame.sprite.pygame.sprite.spritecollide(self, enemy_group, False)

        if collide:
            # 정상적으로 작동하는지 확인하기 위해 부딪혔을 때 collide라는 문자열이 나오게 한다.
            #print("%s detect collide" % self.group)
            
            if(self.state == 2):

                self.current_attack_time += mt

                #print("attack_time:[%s] / animation_time[%s]" % (mt ,self.animation_time))

                # attack loop time 경과가 animation_time을 넘어서면 새로운 이미지 출력 
                if self.current_attack_time >= self.animation_time * 10:
                    self.current_attack_time = 0
                    for enemy in collide:
                        if enemy.type == 1:
                            enemy.damaged(self.power)
                        elif enemy.type == 2:
                            enemy.damaged(self.power)

            else:
                self.state = 2
                self.img_index = 10
                self.now_movement = (0, 0)
            
            
        else:
            #print("%s is no collide" % self.group)
            self.state = 1
            self.now_movement = self.movement
        
class CastleSprite(pygame.sprite.Sprite, BaseObject):

    # state
    # 0: idle
    # 1: move
    # 2: attack
    # 3: die
    def __init__(self, size, position, movement, group, hp, power, name, images, game):

        super(CastleSprite, self).__init__()

        self.game = game
        self.name = name
        self.state = 0
        self.hp = hp
        self.hp_max = hp
        self.power = power
        self.movement = movement
        self.group = group
        self.type = 2

        # 이미지를 Rect안에 넣기 위해 Rect의 크기 지정
        # 이미지의 크기와 같게 하거나, 크기를 다르게 한다면 pygame.transform.scale을 사용하여 rect 안에
        # 이미지를 맞추도록 한다.
        #size = (60, 60)

        self.images = images
        
        # rect 만들기
        self.rect = pygame.Rect(position, size)

        # 캐릭터의 첫번째 이미지
        self.img_index = 0
        self.img_index_start = 0
        self.img_index_end = 9
        self.image = self.images[self.img_index]  # 'image' is the current image of the animation.

        # 1초에 보여줄 1장의 이미지 시간을 계산, 소수점 3자리까지 반올림
        #self.animation_time = round(100 / len(self.images * 100), 2)
        img_len = self.img_index_end - self.img_index_start + 1
        self.animation_time = round(100 / (img_len * 150), 2)

        # mt와 결합하여 animation_time을 계산할 시간 초기화
        self.current_time = 0
        self.current_attack_time = 0

    def move(self):
        dx, dy = self.movement
        self.rect.x += dx
        self.rect.y += dy

    def update(self, mt, game):
                
        if self.group == 'left':
            self.collide_enemy(mt, game.right_group, game)
        else:
            self.collide_enemy(mt, game.left_group, game)

        
        if self.hp >= self.hp_max * 0.5:
            self.img_index_start = 0
            self.img_index_end = 0
        elif self.hp >= self.hp_max * 0.25:
            if self.img_index_start == 0:
                self.game.sound_map['collapse'].play()
            self.img_index_start = 1
            self.img_index_end = 1
        elif self.hp <= self.hp_max * 0.1:
            if self.img_index_start == 1:
                self.game.sound_map['collapse'].play()
            self.img_index_start = 2
            self.img_index_end = 2

        # loop 시간 더하기
        self.current_time += mt

        # loop time 경과가 animation_time을 넘어서면 새로운 이미지 출력 
        if self.current_time >= self.animation_time:
            self.current_time = 0
           
            self.img_index += 1
            if self.img_index >= self.img_index_end:
                self.img_index = self.img_index_start

            self.image = self.images[self.img_index]

    def draw(self, mt):
        
        # 체력바 그리기
        if self.group == 'left':
            pygame.draw.rect(self.game.SCREEN, (131, 133, 131), [self.rect.x + 20, self.rect.y - 45 , 160, 20])
            pygame.draw.rect(self.game.SCREEN, (189, 76, 49), [self.rect.x + 20, self.rect.y - 45, 160 * self.hp / self.hp_max, 20])
        else:
            grow_rect = pygame.draw.rect(self.game.SCREEN, (131, 133, 131), [(self.rect.x + self.rect.size[0]) - 178, self.rect.y - 45 , 160, 20])

            now_hp_rect = pygame.Rect(0, 0, 160 * (self.hp / self.hp_max), 20)
            now_hp_rect.topright = grow_rect.topright

            pygame.draw.rect(self.game.SCREEN, (189, 76, 49), now_hp_rect)
            #pygame.draw.rect(self.game.SCREEN, (189, 76, 49), [(self.rect.x + self.rect.size[0]) - (178 * (self.hp / self.hp_max)), self.rect.y - 45, 160 * (self.hp / self.hp_max), 20])
        
        # 그룹명 그리기 - 이름 길이만큼 길어져야한다.        
        if self.group == 'left':            
            # 텍스트 설정
            text = self.game.main_font_20.render(self.name, True, self.game.COLOR_BLACK)            
            text_rect = text.get_rect()
            text_size = text_rect.size
            #text_rect.centerx = background_rect.centerx            
            
            # 텍스트보다 가로 +20, 세로 +10
            background_rect = pygame.draw.rect(self.game.SCREEN, (255, 255, 255), [self.rect.x + 40, self.rect.y - 80, text_size[0] + 20, text_size[1] + 10])
            self.game.SCREEN.blit(text, (self.rect.x + 40 + 10, self.rect.y - 80 + 5))

        else:            
            text = self.game.main_font_20.render(self.name, True, self.game.COLOR_BLACK)
            text_rect = text.get_rect()
            text_size = text_rect.size
            pygame.draw.rect(self.game.SCREEN, (255, 255, 255), [self.game.SCREEN.get_width() - text_size[0] - 30 - 10 - 2, self.rect.y - 80 , text_size[0] + 20, text_size[1] + 10])
            self.game.SCREEN.blit(text, (self.game.SCREEN.get_width() - text_size[0] - 30 - 2, self.rect.y - 80 + 5))


    def collide_enemy(self, mt, enemy_group, game):
        
        collide = pygame.sprite.pygame.sprite.spritecollide(self, enemy_group, False)

        if collide:            
            if(self.state == 2):
                self.current_attack_time += mt

                # attack loop time 경과가 animation_time을 넘어서면 새로운 이미지 출력                 
                if self.current_attack_time >= self.animation_time:
                    self.current_attack_time = 0
                    for enemy in collide:
                        enemy.hp -= self.power
                        if enemy.hp <= 0:
                            enemy_name = enemy.name
                            game.sprite_group.remove(enemy)
                            if enemy.group == 'left':
                                game.left_group.remove(enemy)
                            else:
                                game.right_group.remove(enemy)
                            
                            del(enemy)
                            return
            else:
                self.state = 2
                self.img_index = 10
                self.movement = (0, 0)
        else:
            self.state = 1
            if self.group == 'left':
                self.movement = (1, 0)
            else:
                self.movement = (-1, 0)
    
    def damaged(self, damage):
        if self.hp > 0:
            self.hp -= damage
            if self.hp <= 0:
                self.destroy_self()

    def destroy_self(self):
        if self.game.destroyed_castle == None:
            self.game.destroyed_castle = self.group
        self.kill()


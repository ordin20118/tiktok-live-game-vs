import pygame

# 기본 오브젝트 클래스
class BaseObject:
    def __init__(self, spr, coord, kinds, game):
        self.kinds = kinds
        self.spr = spr
        self.spr_index = 0
        self.game = game
        self.width = spr[0].get_width()
        self.height = spr[0].get_height()
        self.direction = True
        self.vspeed = 0
        self.gravity = 0.2
        self.movement = [0, 0]
        self.collision = {'top' : False, 'bottom' : False, 'right' : False, 'left' : False}
        self.rect = pygame.rect.Rect(coord[0], coord[1], self.width, self.height)
        self.frameSpeed = 0
        self.frameTimer = 0
        self.destroy = False

    def physics(self):
        self.movement[0] = 0
        self.movement[1] = 0

        if self.gravity != 0:
            self.movement[1] += self.vspeed

            self.vspeed += self.gravity
            if self.vspeed > 3:
                self.vspeed = 3

    def physics_after(self):
        self.rect, self.collision = move(self.rect, self.movement)

        if self.collision['bottom']:
            self.vspeed = 0

        if self.rect.y > 400 or self.rect.y  > 400 or self.rect.y  > 400:
            self.destroy = True
    
    def draw(self):
        self.game.screen_scaled.blit(pygame.transform.flip(self.spr[self.spr_index], self.direction, False)
                    , (self.rect.x - self.game.camera_scroll[0], self.rect.y - self.game.camera_scroll[1]))

        if self.kinds == 'enemy' and self.hp < self.hpm:
            pygame.draw.rect(self.game.screen_scaled, (131, 133, 131)
            , [self.rect.x - 1 - self.game.camera_scroll[0], self.rect.y - 5 - self.game.camera_scroll[1], 10, 2])
            pygame.draw.rect(self.game.screen_scaled, (189, 76, 49)
            , [self.rect.x - 1 - self.game.camera_scroll[0], self.rect.y - 5 - self.game.camera_scroll[1], 10 * self.hp / self.hpm, 2])

    def animation(self, mode):
        if mode == 'loop':
            self.frameTimer += 1

            if self.frameTimer >= self.frameSpeed:
                self.frameTimer = 0
                if self.spr_index < len(self.spr) - 1:
                    self.spr_index += 1
                else:
                    self.spr_index = 0

    def destroy_self(self):
        if self.kinds == 'enemy':
            enemys.remove(self)

        objects.remove(self)
        del(self)

class AnimatedSprite(pygame.sprite.Sprite, BaseObject):

    # state
    # 0: idle
    # 1: move
    # 2: attack
    # 3: die

    def __init__(self, position, movement, group, hp, power, name):

        super(AnimatedSprite, self).__init__()

        self.name = name
        self.state = 1
        self.hp = hp
        self.hp_max = hp
        self.power = power
        self.movement = movement
        self.group = group

        # 이미지를 Rect안에 넣기 위해 Rect의 크기 지정
        # 이미지의 크기와 같게 하거나, 크기를 다르게 한다면 pygame.transform.scale을 사용하여 rect 안에
        # 이미지를 맞추도록 한다.
        size = (60, 60)

        # 여러장의 이미지를 리스트로 저장한다. 이미지 경로는 자신들의 경로를 사용한다.
        self.images = []
        if group == 'right':
            self.images.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Run_1.png'), size), True, False))
            self.images.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Run_2.png'), size), True, False))
            self.images.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Run_3.png'), size), True, False))
            self.images.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Run_4.png'), size), True, False))
            self.images.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Run_5.png'), size), True, False))
            self.images.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Run_6.png'), size), True, False))
            self.images.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Run_7.png'), size), True, False))
            self.images.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Run_8.png'), size), True, False))
            self.images.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Run_9.png'), size), True, False))
            self.images.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Run_10.png'), size), True, False))
            self.images.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Attack_1.png'), size), True, False))
            self.images.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Attack_2.png'), size), True, False))
            self.images.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Attack_3.png'), size), True, False))
            self.images.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Attack_4.png'), size), True, False))
            self.images.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Attack_5.png'), size), True, False))
            self.images.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Attack_6.png'), size), True, False))
            self.images.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Attack_7.png'), size), True, False))
            self.images.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Attack_8.png'), size), True, False))
            self.images.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Attack_9.png'), size), True, False))
            self.images.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Attack_10.png'), size), True, False))
        else:
            self.images.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Run_1.png'), size))
            self.images.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Run_2.png'), size))
            self.images.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Run_3.png'), size))
            self.images.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Run_4.png'), size))
            self.images.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Run_5.png'), size))
            self.images.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Run_6.png'), size))
            self.images.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Run_7.png'), size))
            self.images.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Run_8.png'), size))
            self.images.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Run_9.png'), size))
            self.images.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Run_10.png'), size))
            self.images.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Attack_1.png'), size))
            self.images.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Attack_2.png'), size))
            self.images.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Attack_3.png'), size))
            self.images.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Attack_4.png'), size))
            self.images.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Attack_5.png'), size))
            self.images.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Attack_6.png'), size))
            self.images.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Attack_7.png'), size))
            self.images.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Attack_8.png'), size))
            self.images.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Attack_9.png'), size))
            self.images.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Attack_10.png'), size))

        
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

        # mt와 결합하여 animation_time을 계산할 시간 초기화
        self.current_time = 0

    def move(self):
        dx, dy = self.movement
        self.rect.x += dx
        self.rect.y += dy

    def update(self, mt, game):
        # update를 통해 캐릭터의 이미지가 계속 반복해서 나타나도록 한다.
        
        self.move()
        
        if self.group == 'left':
            self.collide_enemy(game.right_group, game)
        else:
            self.collide_enemy(game.left_group, game)

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

    def collide_enemy(self, enemy_group, game):
        
        collide = pygame.sprite.pygame.sprite.spritecollide(self, enemy_group, False)

        if collide:
            # 정상적으로 작동하는지 확인하기 위해 부딪혔을 때 collide라는 문자열이 나오게 한다.
            #print("%s detect collide" % self.group)
            
            if(self.state == 2):
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
                        print('%s is dead' % enemy_name)
                        return
            else:
                self.state = 2
                self.img_index = 10
                self.movement = (0, 0)
            
            
        else:
            #print("%s is no collide" % self.group)
            self.state = 1
            if self.group == 'left':
                self.movement = (1, 0)
            else:
                self.movement = (-1, 0)
        

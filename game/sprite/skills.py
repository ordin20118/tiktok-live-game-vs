import pygame

class SkillSprite:

    # state
    # 0: idle
    # 1: move
    # 2: attack
    # 3: die
    # type
    # 1: character
    # 2: structure(castle)
    # 3: skill
    # skill_type
    # 1: 단일 공격
    # 2: 범위 공격 또는 스플래시
    def __init__(self, size, position, movement, group, hp, power, name, skill_type, images, animation_count, sound, game):

        super(SkillSprite, self).__init__()

        self.game = game
        self.name = name
        self.state = 2
        self.hp = hp
        self.hp_max = hp
        self.power = power
        self.movement = movement
        self.group = group
        self.type = 3
        self.skill_type = skill_type

        self.use_collide = True         # 충돌 감지 사용 여부

        self.images = images
        self.now_animation_count = 0
        self.animation_count = animation_count
        self.sound = sound
        self.rect = pygame.Rect(position, size)

        self.img_index = 0
        self.img_index_start = 0
        self.img_index_end = len(images) - 1
        self.image = self.images[self.img_index] 

        img_len = self.img_index_end - self.img_index_start + 1
        self.animation_time = round(100 / (img_len * 150), 2)

        # mt와 결합하여 animation_time을 계산할 시간 초기화
        self.current_time = 0
        self.current_attack_time = 0

        self.sound.play()

    def move(self):
        dx, dy = self.movement
        self.rect.x += dx
        self.rect.y += dy

    def update(self, mt, game):
        super().update()
        # update를 통해 캐릭터의 이미지가 계속 반복해서 나타나도록 한다.
        print("skill update")
        
        if self.group == 'left':
            self.collide_enemy(mt, game.right_group, game)
        else:
            self.collide_enemy(mt, game.left_group, game)

        

        # loop 시간 더하기
        self.current_time += mt

        # loop time 경과가 animation_time을 넘어서면 새로운 이미지 출력 
        if self.current_time >= self.animation_time:
            self.current_time = 0
           
            self.img_index += 1
            if self.img_index >= self.img_index_end:                
                self.img_index = self.img_index_start
                self.now_animation_count += 1
                if self.now_animation_count == self.animation_count:
                    # game.sprite_group.remove(self)
                    # game.left_group.remove(self)
                    # del(self)
                    self.kill()
                return

            self.image = self.images[self.img_index]

    def draw(self):
        pass

    def draw_back(self):
        pass


    def collide_enemy(self, mt, enemy_group, game):        
        collide = pygame.sprite.pygame.sprite.spritecollide(self, enemy_group, False)

        if collide and self.use_collide:
          
            for enemy in collide:
                if enemy.type == 1:
                    enemy.kill()

            # 스킬 데미지에 대해 지연 시간을 가지고 싶다면
            # self.current_attack_time += mt
            # if self.current_attack_time >= self.animation_time * 10:
            #     self.current_attack_time = 0
                
       
class LightningSprite(pygame.sprite.Sprite, SkillSprite):

    # state
    # 0: idle
    # 1: move
    # 2: attack
    # 3: die
    # type
    # 1: character
    # 2: structure(castle)
    # 3: skill
    # skill_type
    # 1: 단일 공격
    # 2: 범위 공격 또는 스플래시
    def __init__(self, size, position, movement, group, hp, power, name, skill_type, images, animation_count, sound, game):
        #SkillSprite.__init__(self, size, position, movement, group, hp, power, name, skill_type, images, animation_count, sound, game)
        super(LightningSprite, self).__init__()
        self.game = game
        self.name = name
        self.state = 2
        self.hp = hp
        self.hp_max = hp
        self.power = power
        self.movement = movement
        self.group = group
        self.type = 3
        self.skill_type = skill_type

        self.use_collide = True         # 충돌 감지 사용 여부

        self.images = images
        self.now_animation_count = 0
        self.animation_count = animation_count
        self.sound = sound
        self.rect = pygame.Rect(position, size)

        self.img_index = 0
        self.img_index_start = 0
        self.img_index_end = len(images) - 1
        self.image = self.images[self.img_index] 

        img_len = self.img_index_end - self.img_index_start + 1
        self.animation_time = round(100 / (img_len * 150), 2)

        # mt와 결합하여 animation_time을 계산할 시간 초기화
        self.current_time = 0
        self.current_attack_time = 0

        self.sound.play()
        
    def update(self, mt, game):

        if self.group == 'left':
            self.collide_enemy(mt, game.right_group, game)
        else:
            self.collide_enemy(mt, game.left_group, game)

        # loop 시간 더하기
        self.current_time += mt

        # loop time 경과가 animation_time을 넘어서면 새로운 이미지 출력 
        if self.current_time >= self.animation_time:
            self.current_time = 0
           
            self.img_index += 1
            if self.img_index >= self.img_index_end:                
                self.img_index = self.img_index_start
                self.now_animation_count += 1
                if self.now_animation_count == self.animation_count:
                    # game.sprite_group.remove(self)
                    # game.left_group.remove(self)
                    # del(self)
                    self.kill()
                return

            self.image = self.images[self.img_index]

    def draw(self):
        pass

    def draw_back(self):
        pass

    def collide_enemy(self, mt, enemy_group, game):        
        collide = pygame.sprite.pygame.sprite.spritecollide(self, enemy_group, False)

        if collide and self.use_collide:
          
            for enemy in collide:
                if enemy.type == 1:
                    enemy.damaged(self.power)
                    self.use_collide = False
                    break

            # 스킬 데미지에 대해 지연 시간을 가지고 싶다면
            # self.current_attack_time += mt
            # if self.current_attack_time >= self.animation_time * 10:
            #     self.current_attack_time = 0


class DevilSprite(pygame.sprite.Sprite, SkillSprite):

    # state
    # 0: idle
    # 1: move
    # 2: attack
    # 3: die
    # type
    # 1: character
    # 2: structure(castle)
    # 3: skill
    # skill_type
    # 1: 단일 공격
    # 2: 범위 공격 또는 스플래시
    def __init__(self, size, position, movement, group, hp, power, name, skill_type, images, animation_count, sound, game):
        #SkillSprite.__init__(self, size, position, movement, group, hp, power, name, skill_type, images, animation_count, sound, game)
        super(DevilSprite, self).__init__()
        self.game = game
        self.name = name
        self.state = 2
        self.hp = hp
        self.hp_max = hp
        self.power = power
        self.movement = movement
        self.group = group
        self.type = 3
        self.skill_type = skill_type

        self.use_collide = True         # 충돌 감지 사용 여부

        self.images = images
        self.now_animation_count = 0
        self.animation_count = animation_count
        self.sound = sound
        self.rect = pygame.Rect(position, size)

        self.img_index = 0
        self.img_index_start = 0
        self.img_index_end = len(images) - 1
        self.image = self.images[self.img_index] 

        img_len = self.img_index_end - self.img_index_start + 1
        self.animation_time = round(100 / (img_len * 150), 2)

        # mt와 결합하여 animation_time을 계산할 시간 초기화
        self.current_time = 0
        self.current_attack_time = 0

        self.sound.play()
        
    def update(self, mt, game):

        if self.group == 'left':
            self.collide_enemy(mt, game.right_group, game)
        else:
            self.collide_enemy(mt, game.left_group, game)

        # loop 시간 더하기
        self.current_time += mt

        # loop time 경과가 animation_time을 넘어서면 새로운 이미지 출력 
        if self.current_time >= self.animation_time:
            self.current_time = 0
           
            self.img_index += 1
            if self.img_index >= self.img_index_end:                
                self.img_index = self.img_index_start
                self.now_animation_count += 1
                if self.now_animation_count == self.animation_count:
                    self.kill()
                return

            self.image = self.images[self.img_index]


    def collide_enemy(self, mt, enemy_group, game):        
        if self.use_collide:
            for enemy in enemy_group:
                if enemy.type == 1:
                    enemy.damaged(self.power) 
            self.use_collide = False
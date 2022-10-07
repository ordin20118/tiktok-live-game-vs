import pygame


class AnimatedSprite(pygame.sprite.Sprite):

    def __init__(self, position):

        super(AnimatedSprite, self).__init__()

        # 이미지를 Rect안에 넣기 위해 Rect의 크기 지정
        # 이미지의 크기와 같게 하거나, 크기를 다르게 한다면 pygame.transform.scale을 사용하여 rect 안에
        # 이미지를 맞추도록 한다.
        size = (53, 53)


        # 여러장의 이미지를 리스트로 저장한다. 이미지 경로는 자신들의 경로를 사용한다.
        images = []
        images.append(pygame.image.load('res/character/knight/png/Run_1.png'))
        images.append(pygame.image.load('res/character/knight/png/Run_2.png'))
        images.append(pygame.image.load('res/character/knight/png/Run_3.png'))
        images.append(pygame.image.load('res/character/knight/png/Run_4.png'))
        images.append(pygame.image.load('res/character/knight/png/Run_5.png'))
        images.append(pygame.image.load('res/character/knight/png/Run_6.png'))
        images.append(pygame.image.load('res/character/knight/png/Run_7.png'))
        images.append(pygame.image.load('res/character/knight/png/Run_8.png'))
        images.append(pygame.image.load('res/character/knight/png/Run_9.png'))
        images.append(pygame.image.load('res/character/knight/png/Run_10.png'))
         

        # rect 만들기
        self.rect = pygame.Rect(position, size)


        # Rect 크기와 Image 크기 맞추기. pygame.transform.scale
        self.images = [pygame.transform.scale(image, size) for image in images]
 

        # 캐릭터의 첫번째 이미지
        self.index = 0
        self.image = images[self.index]  # 'image' is the current image of the animation.


    def update(self):
        # update를 통해 캐릭터의 이미지가 계속 반복해서 나타나도록 한다.
        self.index += 1

        if self.index >= len(self.images):
            self.index = 0

        self.image = self.images[self.index]
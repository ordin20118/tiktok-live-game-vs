import pygame
from game.sprite import characters

# 스크린 전체 크기 지정
SCREEN_WIDTH = 475
SCREEN_HEIGHT = 844


pygame.init() #파이 게임 초기화
pygame.display.set_caption("WAR GAME")
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #화면 크기 설정
clock = pygame.time.Clock() 
FPS = 60

# 전역 변수
BLUE = (0, 0, 255)

def main():

    # player 생성
    player = characters.AnimatedSprite(position=(100, 527.5))
    # 생성된 player를 그룹에 넣기
    all_sprites = pygame.sprite.Group(player)  

    is_running = True
    while is_running: #게임 루프
        

        # 변수 업데이트

        #30 FPS (초당 프레임 수) 를 위한 딜레이 추가, 딜레이 시간이 아닌 목표로 하는 FPS 값
        mt = clock.tick(FPS) / 1000 # 1000dmf 나누어줘서 초단위로 변경하여 반환

        #print(mt)

        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # 화면 그리기
        
        # all_sprites 그룹안에 든 모든 Sprite update
        all_sprites.update(mt)

        # 배경색
        SCREEN.fill(BLUE) 

        # 모든 sprite 화면에 그려주기
        all_sprites.draw(SCREEN)
        pygame.display.update() #모든 화면 그리기 업데이트
        




if __name__ == '__main__':
    main()
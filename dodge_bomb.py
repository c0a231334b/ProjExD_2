import os
import random
import sys
import pygame as pg
import time


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, 5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (5, 0), 
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def game_over(screen: pg.Surface) -> None:
    go_bg = pg.Surface((1100, 650))
    pg.draw.rect(go_bg, (0, 0, 0), [0, 0, 1100, 650])
    go_bg.set_alpha(210)
    screen.blit(go_bg, [0, 0])      # blit: 画面に描画する
    fonto = pg.font.Font(None, 80)
    txt = fonto.render("Game Over", True, (255, 255, 255))
    go_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    screen.blit(go_img, [340, 290]) # こうかとんの左側の画像を表示
    screen.blit(go_img, [720, 290]) # こうかとんの右側の画像を表示
    screen.blit(txt, [400, 300])    # Game Overの文字を表示
    pg.display.update()             # 画面更新
    time.sleep(5)

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """爆弾の画像リストと加速度リストを初期化する"""
    bb_img = []
    bb_accs = [1 + 0.2 * i for i in range(10)] # 爆弾の加速度リスト
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r), pg.SRCALPHA)
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.append(bb_img)
    return bb_img, bb_accs

    # accs = [a for a in range(1, 11)]


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数で与えられたRectが画面内にあるかどうかを判定する
    引数:こうかとんRect or 爆弾Rect
    戻り値：真理値タプル（横, 縦）/画面内:True, 画面外:False
    """
    yoko, tate = True, True # 初期化してる。True: 画面内, False: 画面外
    if rct.left < 0 or WIDTH < rct.right: #横方向判定
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom: #縦方向判定
        tate = False
    return yoko, tate

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20)) # 爆弾用の空urface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10) # 爆弾円を描画
    bb_img.set_colorkey((0, 0, 0)) # 爆弾の黒色を透明化
    bb_rct = bb_img.get_rect() # 爆弾rectの抽出
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT) # 横用の乱数と縦用の乱数を生成
    vx, vy = 5, 5 # 爆弾速度ベクトル
    clock = pg.time.Clock()
    tmr = 0

    # stage = min(tmr//500, 9) # 爆弾の大きさを0~9の範囲に収める
    # bb_img = bb_img[stage]
    # spped_multiplier = bb_accs[stage]
    # vx, vy = vx * spped_multiplier, vy * spped_multiplier
    # bb_rct.move_ip(vx, vy) # 爆弾を動かす
    # vx, vy = vx / spped_multiplier, vy / spped_multiplier


    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            game_over(screen)
            print("Game Over!!")
            return # ゲーム―オーバー
        
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]

        # 時間に応じて爆弾を拡大＆加速
        
        
        kk_rct.move_ip(sum_mv)
        # こうかとんが画面外なら、元の場所に戻す
        if check_bound(kk_rct) != (True, True): # どこかしら画面からはみ出てたら
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy) #爆弾を動かす
        yoko, tate = check_bound(bb_rct)
        if not yoko: # 横にはみ出てる
            vx *= -1
        if not tate: # 縦にはみ出てる
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()

        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
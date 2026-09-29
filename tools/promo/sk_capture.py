# -*- coding: utf-8 -*-
"""프레임 캡처 — 게임마다 세션을 열고, 고정 dt 로 물리를 돌린 뒤 한 장씩 찍는다.
자체 rAF 루프는 멈춘다(__CAP.stop). 이미 있는 프레임은 건너뛰어 재개 가능."""
import os, sys, time
S = r"C:/Users/ADMIN/AppData/Local/Temp/claude/c--Users-ADMIN-Antigravity/3fa05fad-ad53-453e-9e14-6af59210b93d/scratchpad"
sys.path.insert(0, S)
from sk import Sess
from sk_story import SHOTS, TOTAL, FPS

SEED = 42
RAW = os.path.join(S,'sk_raw'); os.makedirs(RAW, exist_ok=True)
PHONE = os.path.join(S,'sk_phone'); os.makedirs(PHONE, exist_ok=True)
fp = lambda d,i: os.path.join(d, 'f%05d.png' % i)

# 프레임 진행: 서브스텝 10회 + 그리기 1회. play=False 면 화면만 그린다.
STEP_PLAY = "__CAP.frame(1/24, 10)"
STEP_IDLE = "__CAP.draw()"

def run_shot(shot, lo, port, tag, outdir, game_key='game', frag_key='frag', w=1920, h=1080,
             dpr=1, mobile=False):
    need = [i for i in range(lo, lo+shot['n']) if not os.path.exists(fp(outdir,i))]
    if not need:
        print('  건너뜀 (완료)'); return
    s = Sess(port=port, w=w, h=h, dpr=dpr, mobile=mobile, tag=tag)
    try:
        s.goto(shot[game_key], shot.get(frag_key,''))
        if not s.js('!!window.__CAP'): raise RuntimeError('__CAP 없음: '+shot[game_key])
        s.js('__CAP.stop()')
        s.js('__CAP.seed(%d)' % SEED)    # 방해물 배치를 고정 — 캡처가 재현된다
        if shot.get('play'):
            s.js('__CAP.tap()')          # 메뉴 -> 플레이
        step = STEP_PLAY if shot.get('play') else STEP_IDLE
        t0 = time.time()
        for k in range(shot['n']):
            i = lo + k
            s.js(step)
            if not os.path.exists(fp(outdir,i)):
                s.shot(fp(outdir,i))
            if (k+1) % 50 == 0:
                el = time.time()-t0
                print('    %d/%d  %.1f fps' % (k+1, shot['n'], (k+1)/el), flush=True)
    finally:
        s.close()

def main():
    lo = 0; port = 9700
    for idx, shot in enumerate(SHOTS):
        print('[%d] %s %s  %df @ %d' % (idx, shot['kind'], shot['game'], shot['n'], lo), flush=True)
        run_shot(shot, lo, port, 'c%d'%idx, RAW); port += 1
        if shot['kind'] == 'split':      # 같은 구간의 스마트폰 화면을 따로 찍는다
            print('    + 스마트폰 화면', flush=True)
            ph = dict(shot); ph['game'] = shot['phone_game']; ph['frag'] = shot['phone_frag']
            run_shot(ph, lo, port, 'p%d'%idx, PHONE, w=390, h=844, dpr=2, mobile=True)
            port += 1
        lo += shot['n']
    print('완료: raw %d / phone %d' % (len(os.listdir(RAW)), len(os.listdir(PHONE))))

if __name__ == '__main__':
    main()

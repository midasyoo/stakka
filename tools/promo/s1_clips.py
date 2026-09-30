# -*- coding: utf-8 -*-
"""STAKKA 1 클립 캡처.
네 종류의 클립을 플랫폼별로 한 번만 찍어 두고, 30초/1분 두 편집본이 함께 쓴다.
 menu    : 메뉴 화면 (타이틀·카드 배경)
 early   : 처음부터 — 블록이 크고 느리다
 perfect : 조금 진행한 뒤 — PERFECT 가 이어지는 구간
 fast    : 많이 진행한 뒤 — 블록이 작고 빠르다
"""
import os, sys, time
S = r"C:/Users/ADMIN/AppData/Local/Temp/claude/c--Users-ADMIN-Antigravity/3fa05fad-ad53-453e-9e14-6af59210b93d/scratchpad"
sys.path.insert(0, S)
from sk import Sess

SEED = 42
CLIPS = [  # (이름, 프레임수, 워밍업 프레임, 플레이여부)
    ('menu',    96, 0,   False),
    ('early',  312, 0,   True),
    ('perfect',312, 240, True),
    ('fast',   312, 760, True),
]
PLATFORMS = {                       # 이름: (viewport w, h, dpr, mobile)
    'desk':  (1920, 1080, 1, False),
    'phone': (540,  960,  2, True),
}

def capture(plat, name, n, warm, play, port):
    w,h,dpr,mob = PLATFORMS[plat]
    d = os.path.join(S, 's1_%s_%s' % (plat, name)); os.makedirs(d, exist_ok=True)
    need = [i for i in range(n) if not os.path.exists(os.path.join(d,'f%05d.png'%i))]
    if not need: print('  %s/%s 완료됨' % (plat,name)); return
    s = Sess(port=port, w=w, h=h, dpr=dpr, mobile=mob, tag='%s_%s'%(plat,name))
    try:
        s.goto('Stakka')
        if not s.js('!!window.__CAP'): raise RuntimeError('__CAP 없음')
        s.js('__CAP.stop(); __CAP.seed(%d);' % SEED)
        if play:
            s.js('__CAP.tap()')
            if warm:      # 화면은 찍지 않고 물리만 돌려 후반 상태로 보낸다
                s.js("(function(){for(var i=0;i<%d;i++) __CAP.frame(1/24,10);})()" % warm)
        t0=time.time()
        for i in range(n):
            s.js('__CAP.frame(1/24,10)' if play else '__CAP.draw()')
            p = os.path.join(d,'f%05d.png'%i)
            if not os.path.exists(p): s.shot(p)
            if (i+1)%60==0: print('    %d/%d  %.1f fps'%(i+1,n,(i+1)/(time.time()-t0)), flush=True)
        print('  %s/%s  HUD=%s' % (plat,name,s.js('__CAP.hud()')), flush=True)
    finally: s.close()

if __name__ == '__main__':
    port = 9900
    for plat in PLATFORMS:
        for name,n,warm,play in CLIPS:
            print('[%s] %s  %df (warm %d)' % (plat,name,n,warm), flush=True)
            capture(plat,name,n,warm,play,port); port += 1
    print('클립 캡처 완료')

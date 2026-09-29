# -*- coding: utf-8 -*-
"""STAKKA 3부작 1분 홍보 영상 — 스토리보드.
24fps · 1440 frames · 1920x1080

데스크탑 레이아웃은 가운데 600px 세로 스테이지 + 좌우 여백이다.
그 여백을 자막 자리로 쓴다 — 게임 화면을 전혀 가리지 않는다.
"""
FPS = 24
W, H = 1920, 1080

SHOTS = [
  # 타이틀 — 1편 메뉴(로고 + 데모 타워)
  dict(n=96, kind='title', game='Stakka', frag='', play=False,
       title='STAKKA', sub='한 손가락 탑 쌓기 3부작',
       note='HTML 파일 하나 · 외부 의존성 0 · 설치 없이 바로'),

  # ① STAKKA 1
  dict(n=72, kind='card', game='Stakka', frag='', play=False,
       chapter='1', title='기본 규칙',
       sub='탭 한 번으로 블록을 쌓는다',
       note='정확히 맞추면 PERFECT — 줄어든 블록이 다시 커진다'),
  dict(n=312, kind='play', game='Stakka', frag='', play=True,
       cap=('STAKKA 1', '빗나간 만큼 잘려 나간다',
            'PERFECT 를 이어 붙이면 블록이 되살아난다')),

  # ② STAKKA 2
  dict(n=72, kind='card', game='Stakka2', frag='&lv=4', play=False,
       chapter='2', title='달까지 쌓아라',
       sub='10개 하늘 구역 · 체크포인트 스토리',
       note='올라갈수록 하늘이 바뀌고 방해물이 지나간다'),
  dict(n=312, kind='play', game='Stakka2', frag='&lv=4', play=True,
       cap=('STAKKA 2', '하늘 구역이 바뀐다',
            '방해물이 탑을 가로지를 땐 쌓지 말고 기다린다')),

  # ③ STAKKA 3
  dict(n=72, kind='card', game='Stakka3', frag='&lv=3', play=False,
       chapter='3', title='무너지는 하늘',
       sub='붕괴선이 바로 아래서 쫓아온다',
       note='머뭇거리면 삼켜진다 — 쌓는 속도가 곧 생존'),
  dict(n=312, kind='play', game='Stakka3', frag='&lv=3', play=True,
       cap=('STAKKA 3', '붕괴선이 쫓아온다',
            '균열 너머로 탈출할 때까지 멈출 수 없다')),

  # 데스크탑 / 스마트폰 (좌우 합성 — phone 프레임 별도 캡처)
  dict(n=120, kind='split', game='Stakka3', frag='&lv=3', play=True,
       phone_game='Stakka2', phone_frag='&lv=4',
       cap=('PC 와 스마트폰', '같은 파일 하나가 기기를 보고 바뀐다',
            'PC 는 마우스·스페이스바 · 폰은 전체 화면 터치')),

  # 클로징
  dict(n=72, kind='outro', game='Stakka3', frag='&lv=3', play=False,
       title='STAKKA 1 · 2 · 3',
       sub='설치 없이 브라우저에서 바로',
       note='midasyoo.github.io/stakka · /stakka2 · /stakka3'),
]

TOTAL = sum(s['n'] for s in SHOTS)

if __name__ == '__main__':
    print('샷 %d · 총 %d프레임 · %.2fs' % (len(SHOTS), TOTAL, TOTAL/FPS))
    t = 0
    for i, s in enumerate(SHOTS):
        lab = s.get('title') or (s.get('cap') or ('',))[0]
        print('  %2d  %5.1fs  %3df  %-6s %-8s %s' % (i, t/FPS, s['n'], s['kind'], s['game'], lab))
        t += s['n']

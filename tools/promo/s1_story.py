# -*- coding: utf-8 -*-
"""STAKKA 1 편집본 정의 — 30초/1분 x 데스크탑/스마트폰.
클립(s1_clips.py)에서 구간을 골라 이어 붙인다. 캡처는 한 번만 하고 편집만 달리 한다."""

# kind: title | card | play | split | outro
# clip: 어느 클립에서 · off: 클립 내 시작 프레임

EDITS = {}

EDITS[('desk', 60)] = [
  dict(n=96,  kind='title', clip='menu', off=0,
       title='STAKKA', sub='한 손가락 탑 쌓기',
       note='HTML 파일 하나 · 외부 의존성 0 · 설치 없이 바로'),
  dict(n=72,  kind='card',  clip='menu', off=0, chapter='1', title='규칙은 하나',
       sub='블록이 겹치는 순간 누른다',
       note='빗나간 만큼 잘려 나간다'),
  dict(n=312, kind='play',  clip='early', off=0,
       cap=('탭 한 번', '블록이 좌우로 왕복한다',
            '아래층과 겹치는 순간에 놓는다')),
  dict(n=72,  kind='card',  clip='perfect', off=0, chapter='2', title='PERFECT',
       sub='정확히 맞추면 블록이 되살아난다',
       note='이어 붙일수록 탑이 다시 두꺼워진다'),
  dict(n=312, kind='play',  clip='perfect', off=0,
       cap=('PERFECT', '줄어든 블록이 다시 커진다',
            '콤보를 이어 붙이는 것이 이 게임의 핵심')),
  dict(n=72,  kind='card',  clip='fast', off=0, chapter='3', title='점점 빨라진다',
       sub='올라갈수록 블록은 작고 빠르다',
       note='어디까지 쌓을 수 있나'),
  dict(n=312, kind='play',  clip='fast', off=0,
       cap=('높이 올라갈수록', '블록은 작아지고 왕복은 빨라진다',
            '한 번의 실수가 탑을 끝낸다')),
  dict(n=120, kind='split', clip='fast', off=312-120,
       cap=('PC 와 스마트폰', '같은 파일 하나가 기기를 보고 바뀐다',
            'PC 는 마우스·스페이스바 · 폰은 전체 화면 터치')),
  dict(n=72,  kind='outro', clip='menu', off=24,
       title='STAKKA', sub='설치 없이 브라우저에서 바로',
       note='midasyoo.github.io/stakka'),
]

EDITS[('desk', 30)] = [
  dict(n=72,  kind='title', clip='menu', off=0,
       title='STAKKA', sub='한 손가락 탑 쌓기',
       note='HTML 파일 하나 · 설치 없이 바로'),
  dict(n=240, kind='play',  clip='early', off=0,
       cap=('탭 한 번', '겹치는 순간에 놓는다',
            '빗나간 만큼 잘려 나간다')),
  dict(n=240, kind='play',  clip='perfect', off=40,
       cap=('PERFECT', '정확히 맞추면 블록이 되살아난다',
            '콤보를 이어 붙여라')),
  dict(n=96,  kind='play',  clip='fast', off=120,
       cap=('점점 빨라진다', '블록은 작아지고 왕복은 빨라진다',
            '어디까지 쌓을 수 있나')),
  dict(n=72,  kind='outro', clip='menu', off=24,
       title='STAKKA', sub='설치 없이 브라우저에서 바로',
       note='midasyoo.github.io/stakka'),
]

EDITS[('phone', 60)] = [
  dict(n=96,  kind='title', clip='menu', off=0,
       title='STAKKA', sub='한 손가락 탑 쌓기',
       note='설치 없이 바로'),
  dict(n=72,  kind='card',  clip='menu', off=0, chapter='1', title='규칙은 하나',
       sub='겹치는 순간 탭', note='빗나간 만큼 잘려 나간다'),
  dict(n=312, kind='play',  clip='early', off=0,
       cap=('탭 한 번', '겹치는 순간에 놓는다', '빗나간 만큼 잘려 나간다')),
  dict(n=72,  kind='card',  clip='perfect', off=0, chapter='2', title='PERFECT',
       sub='정확히 맞추면 되살아난다', note='콤보를 이어 붙여라'),
  dict(n=312, kind='play',  clip='perfect', off=0,
       cap=('PERFECT', '줄어든 블록이 다시 커진다', '콤보가 이 게임의 핵심')),
  dict(n=72,  kind='card',  clip='fast', off=0, chapter='3', title='점점 빨라진다',
       sub='블록은 작고 빠르게', note='어디까지 쌓을 수 있나'),
  dict(n=312, kind='play',  clip='fast', off=0,
       cap=('높이 올라갈수록', '블록은 작아지고 빨라진다', '한 번의 실수로 끝난다')),
  dict(n=120, kind='play',  clip='fast', off=312-120,
       cap=('홈 화면에 추가', '앱처럼 아이콘으로 실행된다', '오프라인에서도 열린다')),
  dict(n=72,  kind='outro', clip='menu', off=24,
       title='STAKKA', sub='브라우저에서 바로', note='midasyoo.github.io/stakka'),
]

EDITS[('phone', 30)] = [
  dict(n=72,  kind='title', clip='menu', off=0,
       title='STAKKA', sub='한 손가락 탑 쌓기', note='설치 없이 바로'),
  dict(n=240, kind='play',  clip='early', off=0,
       cap=('탭 한 번', '겹치는 순간에 놓는다', '빗나간 만큼 잘려 나간다')),
  dict(n=240, kind='play',  clip='perfect', off=40,
       cap=('PERFECT', '정확히 맞추면 되살아난다', '콤보를 이어 붙여라')),
  dict(n=96,  kind='play',  clip='fast', off=120,
       cap=('점점 빨라진다', '블록은 작아지고 빨라진다', '어디까지 쌓을 수 있나')),
  dict(n=72,  kind='outro', clip='menu', off=24,
       title='STAKKA', sub='브라우저에서 바로', note='midasyoo.github.io/stakka'),
]

SIZE = {'desk': (1920,1080), 'phone': (1080,1920)}

if __name__ == '__main__':
    for k, shots in EDITS.items():
        tot = sum(s['n'] for s in shots)
        print('%-6s %2ds : %d샷 %4d프레임 = %.2fs  %s' %
              (k[0], k[1], len(shots), tot, tot/24, 'OK' if tot == k[1]*24 else '불일치!'))

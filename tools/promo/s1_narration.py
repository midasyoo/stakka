# -*- coding: utf-8 -*-
"""STAKKA 1 내레이션 — 60초판 / 30초판.
한국어 신경망 TTS 는 자연스러운 속도에서 초당 5~6음절. limit x 5 음절이 상한."""
VOICE='ko-KR-InJoonNeural'; PITCH='-2Hz'
RATES=['+0%','+6%','+12%','+18%']

SCRIPTS = {}

SCRIPTS[60] = [
  dict(start= 0.6, limit=3.2, text='스타카. 손가락 하나로 쌓는 탑.'),
  dict(start= 4.4, limit=2.4, text='규칙은 하나입니다.'),
  dict(start= 7.4, limit=4.0, text='블록이 왕복합니다. 겹치는 순간 누릅니다.'),
  dict(start=12.4, limit=3.6, text='빗나간 만큼 잘려 나갑니다.'),
  dict(start=16.6, limit=3.2, text='탑은 점점 가늘어집니다.'),
  dict(start=20.4, limit=2.4, text='그런데 퍼펙트가 있습니다.'),
  dict(start=23.4, limit=4.0, text='정확히 맞추면 줄어든 블록이 다시 커집니다.'),
  dict(start=28.4, limit=4.0, text='콤보를 이어 붙이는 것이 이 게임의 핵심입니다.'),
  dict(start=33.2, limit=2.6, text='탑이 되살아납니다.'),
  dict(start=36.4, limit=2.4, text='그리고 점점 빨라집니다.'),
  dict(start=39.4, limit=4.0, text='올라갈수록 블록은 작아지고 왕복은 빨라집니다.'),
  dict(start=44.2, limit=4.0, text='단 한 번의 실수가 탑을 끝냅니다.'),
  dict(start=48.6, limit=3.2, text='어디까지 쌓을 수 있을까요.'),
  dict(start=52.3, limit=4.9, text='피시는 마우스로, 폰은 터치로. 같은 파일 하나가 알아서 바뀝니다.'),
  dict(start=57.4, limit=2.4, text='설치 없이, 브라우저에서 바로.'),
]

SCRIPTS[30] = [
  dict(start= 0.6, limit=2.4, text='스타카. 손가락 하나로 쌓는 탑.'),
  dict(start= 3.4, limit=3.6, text='블록이 왕복합니다. 겹치는 순간 누릅니다.'),
  dict(start= 7.6, limit=3.4, text='빗나간 만큼 잘려 나갑니다.'),
  dict(start=11.6, limit=3.4, text='정확히 맞추면 퍼펙트. 블록이 다시 커집니다.'),
  dict(start=15.6, limit=3.4, text='콤보를 이어 붙이면 탑이 되살아납니다.'),
  dict(start=19.6, limit=3.4, text='올라갈수록 작아지고 빨라집니다.'),
  dict(start=23.4, limit=3.2, text='어디까지 쌓을 수 있을까요.'),
  dict(start=27.2, limit=2.4, text='설치 없이, 브라우저에서 바로.'),
]

if __name__=='__main__':
    for secs, lines in SCRIPTS.items():
        print('=== %d초판 ===' % secs)
        for i,l in enumerate(lines):
            syl=len([c for c in l['text'] if '\uac00'<=c<='\ud7a3'])
            m='  ' if syl<=l['limit']*5.6 else '길'
            print(' %2d %s %5.1fs (~%.1fs) %2d음절  %s'%(i,m,l['start'],l['limit'],syl,l['text']))
        print('  %d줄 · 마지막 %.1fs\n'%(len(lines), lines[-1]['start']+lines[-1]['limit']))

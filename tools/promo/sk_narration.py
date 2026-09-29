# -*- coding: utf-8 -*-
"""내레이션 대본. 한국어 신경망 TTS 는 자연스러운 속도에서 초당 5~6음절이므로
limit 초에 들어가려면 대략 limit x 5 음절을 넘기지 않아야 한다."""
VOICE = 'ko-KR-InJoonNeural'
PITCH = '-2Hz'
RATES = ['+0%', '+6%', '+12%', '+18%']

LINES = [
  dict(start= 0.6, limit=3.5, text='스타카. 손가락 하나로 탑을 쌓는 게임 세 편.'),
  dict(start= 4.4, limit=2.4, text='첫째, 기본 규칙.'),
  dict(start= 7.4, limit=4.0, text='블록이 좌우로 왕복합니다. 아래층과 겹치는 순간 탭.'),
  dict(start=12.2, limit=4.0, text='빗나간 만큼 잘려 나갑니다.'),
  dict(start=16.4, limit=3.9, text='정확히 맞추면 퍼펙트. 줄어든 블록이 다시 커집니다.'),
  dict(start=20.4, limit=2.4, text='둘째, 달까지 쌓아라.'),
  dict(start=23.4, limit=4.0, text='열 개 하늘 구역을 지나 위로 올라갑니다.'),
  dict(start=28.4, limit=4.0, text='방해물이 탑을 가로지를 땐, 쌓지 말고 기다립니다.'),
  dict(start=33.0, limit=2.6, text='체크포인트부터 다시 시작합니다.'),
  dict(start=36.4, limit=2.4, text='셋째, 무너지는 하늘.'),
  dict(start=39.4, limit=4.0, text='붕괴선이 바로 아래에서 쫓아옵니다.'),
  dict(start=44.0, limit=4.0, text='머뭇거리면 삼켜집니다. 쌓는 속도가 곧 생존입니다.'),
  dict(start=48.6, limit=3.7, text='균열 너머로 탈출할 때까지 멈출 수 없습니다.'),
  dict(start=52.4, limit=4.8, text='피시는 마우스로, 폰은 터치로. 같은 파일 하나가 알아서 바뀝니다.'),
  dict(start=57.4, limit=2.4, text='설치 없이, 브라우저에서 바로.'),
]

if __name__ == '__main__':
    tot = 0
    for i, l in enumerate(LINES):
        syl = len([c for c in l['text'] if '\uac00' <= c <= '\ud7a3'])
        tot += syl
        mark = '  ' if syl <= l['limit']*5.6 else '길'
        print('%2d %s %5.1fs (~%.1fs) %2d음절  %s' % (i, mark, l['start'], l['limit'], syl, l['text']))
    print('\n%d줄 · %d음절 · 마지막 %.1fs' % (len(LINES), tot, LINES[-1]['start']+LINES[-1]['limit']))

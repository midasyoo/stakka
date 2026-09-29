# STAKKA 3부작 1분 홍보 영상

`stakka-trilogy-1min.mp4` (1920×1080 · 24fps · 60.00초 · 내레이션+배경음)를 다시 만드는 도구.

## 원리

게임 화면을 실시간으로 녹화하지 않는다. 헤드리스 캡처는 초당 1~2장이라 녹화하면
끊긴다. 대신 `index.html` 의 `#cap=1` 훅(`window.__CAP`)으로

1. 게임의 자체 rAF 루프를 멈추고 (`__CAP.stop()`)
2. 프레임마다 **고정 dt 로 물리를 직접 돌린 뒤** 한 장을 그린다 (`__CAP.frame(1/24, 10)`)

캡처가 얼마나 느리든 결과는 항상 같다.

### 자동 플레이

사람이 조작할 수 없으므로 `__CAP.autoTap()` 이 대신 놓는다.

- 블록이 아래층과 겹치는 순간에만 놓아 **PERFECT 가 이어진다**
- 24fps 로 한 번에 돌리면 블록이 중심을 건너뛰어 PERFECT 가 안 나온다 →
  한 프레임을 **물리 서브스텝 10회**로 나눈다
- 허용 오차는 속도에 비례한다 (레벨이 오르면 한 스텝 이동량이 커진다)
- `inDanger()` 가 참이면 놓지 않는다 — **방해물에 맞아 죽는 것을 피한다**
- 그래도 끝나면 `keepAlive()` 가 즉시 다시 시작한다

### 재현성

방해물 배치에 `Math.random` 이 쓰여 실행마다 달라진다. `__CAP.seed(42)` 로
난수를 고정해 캡처가 재현되게 했다.

## 구성

| 파일 | 역할 |
|---|---|
| `sk_story.py` | 스토리보드 — 샷 순서·길이·자막. **구성을 바꾸려면 여기만** |
| `sk.py` | 헤드리스 Chrome 을 CDP 로 붙잡는 래퍼 |
| `sk_capture.py` | 스토리보드대로 프레임 캡처 (중단 후 재개 가능) |
| `sk_compose.py` | 자막·챕터 카드·PC/폰 분할 화면 합성 |
| `sk_narration.py` | 내레이션 대본 — 줄마다 시작 시각과 허용 길이 |
| `sk_voice.py` | edge-tts 한국어 내레이션 (앞뒤 묵음 제거·속도 자동 조절) |
| `sk_music.py` | 배경음 합성 — 외부 음원 없이 직접 만든다 |
| `sk_mix.py` | 더킹 믹스 + 2패스 라우드니스 정규화 + 영상 결합 |

## 실행

```bash
pip install websocket-client pillow imageio-ffmpeg edge-tts numpy

python tools/promo/sk_story.py       # 구성 확인
python tools/promo/sk_capture.py     # 프레임 캡처 (약 20분)
python tools/promo/sk_compose.py     # 자막 합성

python -c "import imageio_ffmpeg as f;print(f.get_ffmpeg_exe())"
<ffmpeg> -y -framerate 24 -i sk_out/f%05d.png -c:v libx264 -preset slow -crf 19 \
  -pix_fmt yuv420p -movflags +faststart stakka-1min-silent.mp4

python tools/promo/sk_mix.py         # 내레이션 + 배경음 -> stakka-trilogy-1min.mp4
```

**자막을 왼쪽 여백에** 놓는 이유: 데스크탑 레이아웃은 가운데 600px 세로 스테이지라
좌우가 비어 있다. 그 공간을 쓰면 게임 화면을 전혀 가리지 않는다.

**대본을 고칠 때** — 한국어 신경망 TTS 는 자연스러운 속도에서 초당 5~6음절이다.
`limit` 초에 넣으려면 대략 `limit × 5` 음절을 넘기지 않아야 한다. 넘으면 속도를
올리지 말고 **문장을 줄이는 쪽**이 맞다.

## 구성 (60초)

| 시각 | 구간 |
|---|---|
| 0:00 | 타이틀 |
| 0:04 | **① 기본 규칙** — 카드 3초 + STAKKA 1 플레이 13초 |
| 0:20 | **② 달까지 쌓아라** — 카드 3초 + STAKKA 2 플레이 13초 |
| 0:36 | **③ 무너지는 하늘** — 카드 3초 + STAKKA 3 플레이 13초 |
| 0:52 | PC / 스마트폰 레이아웃 비교 5초 |
| 0:57 | 클로징 3초 |

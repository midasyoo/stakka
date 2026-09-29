# -*- coding: utf-8 -*-
"""자막·카드 합성. 데스크탑 레이아웃은 가운데 600px 스테이지 + 좌우 여백이라
자막을 왼쪽 여백에 놓으면 게임 화면을 전혀 가리지 않는다."""
import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S = r"C:/Users/ADMIN/AppData/Local/Temp/claude/c--Users-ADMIN-Antigravity/3fa05fad-ad53-453e-9e14-6af59210b93d/scratchpad"
sys.path.insert(0, S)
from sk_story import SHOTS, TOTAL, W, H

RAW=os.path.join(S,'sk_raw'); PHONE=os.path.join(S,'sk_phone'); OUT=os.path.join(S,'sk_out')
os.makedirs(OUT, exist_ok=True)
BD='C:/Windows/Fonts/malgunbd.ttf'; RG='C:/Windows/Fonts/malgun.ttf'
F=lambda p,s: ImageFont.truetype(p,s)
f_title=F(BD,92); f_sub=F(BD,36); f_note=F(RG,26)
f_cnum=F(BD,150); f_ctitle=F(BD,76)
f_tag=F(BD,30); f_head=F(BD,46); f_body=F(RG,28)

ACC=(255,209,102); INK=(238,243,252); DIM=(150,166,196)
LEFT_X=88; LEFT_W=540          # 왼쪽 여백 자막 영역 (스테이지는 화면 가운데 600px)

def ease(u): return u*u*(3-2*u)
def fade(u,i=.14,o=.14):
    a=1.0
    if u<i: a=ease(u/i)
    if u>1-o: a=ease((1-u)/o)
    return max(0.,min(1.,a))
def txt(d,xy,s,f,c,a,anchor='la'):
    d.text(xy,s,font=f,fill=c+(int(255*a),),anchor=anchor)

def wrap(d, s, font, maxw):
    out, line = [], ''
    for w in s.split(' '):
        t = (line+' '+w).strip()
        if d.textlength(t, font=font) <= maxw or not line: line = t
        else: out.append(line); line = w
    if line: out.append(line)
    return out

def side_caption(im, cap, a):
    """왼쪽 여백에 세로 가운데 정렬로 — 게임 화면을 가리지 않는다."""
    tag, head, body = cap
    d = ImageDraw.Draw(im)
    hl = wrap(d, head, f_head, LEFT_W)
    bl = wrap(d, body, f_body, LEFT_W)
    th = 46 + len(hl)*58 + 12 + len(bl)*40
    y = (H - th)//2
    d.rounded_rectangle((LEFT_X-26, y-30, LEFT_X+LEFT_W+26, y+th+30), 16,
                        fill=(8,11,20,int(150*a)))
    d.line((LEFT_X-6, y+4, LEFT_X-6, y+th-4), fill=ACC+(int(230*a),), width=5)
    txt(d,(LEFT_X+16,y),tag,f_tag,ACC,a); y+=46
    for l in hl: txt(d,(LEFT_X+16,y),l,f_head,INK,a); y+=58
    y+=12
    for l in bl: txt(d,(LEFT_X+16,y),l,f_body,DIM,a); y+=40
    return im

def card(im, s, a):
    sc=Image.new('RGBA',im.size,(5,8,16,int(234*a)))
    im=Image.alpha_composite(im.filter(ImageFilter.GaussianBlur(10)),sc)
    d=ImageDraw.Draw(im); cy=H//2
    txt(d,(W//2,cy-150),s['chapter'],f_cnum,ACC,a,'mm')
    txt(d,(W//2,cy-16),s['title'],f_ctitle,INK,a,'mm')
    d.line((W//2-140,cy+40,W//2+140,cy+40),fill=ACC+(int(200*a),),width=3)
    txt(d,(W//2,cy+88),s['sub'],f_sub,INK,a,'mm')
    txt(d,(W//2,cy+142),s['note'],f_note,DIM,a,'mm')
    return im

def title(im, s, a, outro=False):
    sc=Image.new('RGBA',im.size,(5,8,16,int((206 if not outro else 224)*a)))
    im=Image.alpha_composite(im.filter(ImageFilter.GaussianBlur(6 if not outro else 9)),sc)
    d=ImageDraw.Draw(im); cy=H//2-10
    txt(d,(W//2,cy-52),s['title'],f_title,INK,a,'mm')
    d.line((W//2-200,cy+8,W//2+200,cy+8),fill=ACC+(int(215*a),),width=3)
    txt(d,(W//2,cy+58),s['sub'],f_sub,ACC,a,'mm')
    txt(d,(W//2,cy+116),s['note'],f_note,DIM,a,'mm')
    return im

def bottom_caption(im, cap, a):
    """분할 화면용 — 아래 가운데. 좌우가 화면으로 차 있어 옆에는 놓을 수 없다."""
    tag, head, body = cap
    d = ImageDraw.Draw(im)
    tw = max(d.textlength(head, font=f_head), d.textlength(body, font=f_body),
             d.textlength(tag, font=f_tag)) + 96
    x0 = (W - tw)//2; y0 = H - 216
    d.rounded_rectangle((x0, y0, x0+tw, y0+168), 16, fill=(8,11,20,int(170*a)))
    d.line((x0+30, y0+26, x0+35, y0+142), fill=ACC+(int(230*a),), width=5)
    txt(d,(x0+56,y0+22),tag,f_tag,ACC,a)
    txt(d,(x0+56,y0+62),head,f_head,INK,a)
    txt(d,(x0+56,y0+120),body,f_body,DIM,a)
    return im

def split(im, ph, cap, a):
    """왼쪽 PC · 오른쪽 스마트폰. PC 는 가운데 스테이지 위주로 잘라 키운다
       (데스크탑 레이아웃은 좌우 여백이 넓어 그대로 줄이면 빈 화면만 보인다)."""
    bg = Image.new('RGBA',(W,H),(6,9,18,255))
    crop = im.crop(((W-1040)//2, 0, (W+1040)//2, H))
    dw, dh = 624, 648
    dk = crop.resize((dw, dh))
    dy = 120
    bg.paste(dk, (150, dy))
    pw = int(ph.width*(700/ph.height)); pm = ph.resize((pw,700))
    px = W - 190 - pw
    d = ImageDraw.Draw(bg)
    d.rounded_rectangle((150-10, dy-10, 150+dw+10, dy+dh+10), 14,
                        outline=(58,70,94,255), width=2)
    d.rounded_rectangle((px-16, dy-16, px+pw+16, dy+700+16), 26,
                        fill=(16,21,32,255), outline=(58,70,94,255), width=2)
    bg.paste(pm, (px, dy))
    txt(d,(150+dw//2, dy+dh+44),'PC',f_tag,DIM,1.0,'mm')
    txt(d,(px+pw//2, dy+700+50),'SMARTPHONE',f_tag,DIM,1.0,'mm')
    return bottom_caption(bg, cap, a)

def main():
    b,t=[],0
    for s in SHOTS: b.append((t,t+s['n'],s)); t+=s['n']
    made=0
    for i in range(TOTAL):
        src=os.path.join(RAW,'f%05d.png'%i); dst=os.path.join(OUT,'f%05d.png'%i)
        if not os.path.exists(src): print('누락:',src); return 1
        if os.path.exists(dst): continue
        lo,hi,s=next(x for x in b if x[0]<=i<x[1]); u=(i-lo)/max(hi-lo-1,1)
        im=Image.open(src).convert('RGBA'); k=s['kind']
        if k=='card':    im=card(im,s,fade(u,.18,.18))
        elif k=='title': im=title(im,s,fade(u,.16,.12))
        elif k=='outro': im=title(im,s,fade(u,.14,.10),True)
        elif k=='split':
            p=os.path.join(PHONE,'f%05d.png'%i)
            if not os.path.exists(p): print('폰 프레임 누락:',p); return 1
            im=split(im,Image.open(p).convert('RGBA'),s['cap'],fade(u,.16,.16))
        else: im=side_caption(im,s['cap'],fade(u,.16,.16))
        im.convert('RGB').save(dst); made+=1
        if made%150==0: print('  합성 %d'%made, flush=True)
    print('합성 완료 (신규 %d)'%made); return 0

if __name__=='__main__': sys.exit(main())

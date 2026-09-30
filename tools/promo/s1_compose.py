# -*- coding: utf-8 -*-
"""편집본 합성. 가로(데스크탑)는 왼쪽 여백에, 세로(스마트폰)는 아래에 자막을 둔다."""
import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S = r"C:/Users/ADMIN/AppData/Local/Temp/claude/c--Users-ADMIN-Antigravity/3fa05fad-ad53-453e-9e14-6af59210b93d/scratchpad"
sys.path.insert(0, S)
from s1_story import EDITS, SIZE

BD='C:/Windows/Fonts/malgunbd.ttf'; RG='C:/Windows/Fonts/malgun.ttf'
ACC=(255,209,102); INK=(238,243,252); DIM=(150,166,196)

def fonts(scale):
    f=lambda p,s: ImageFont.truetype(p, max(12,int(s*scale)))
    return dict(title=f(BD,92), sub=f(BD,36), note=f(RG,26), cnum=f(BD,150),
                ctitle=f(BD,76), tag=f(BD,30), head=f(BD,46), body=f(RG,28))

def ease(u): return u*u*(3-2*u)
def fade(u,i=.14,o=.14):
    a=1.0
    if u<i: a=ease(u/i)
    if u>1-o: a=ease((1-u)/o)
    return max(0.,min(1.,a))
def txt(d,xy,s,f,c,a,anchor='la'): d.text(xy,s,font=f,fill=c+(int(255*a),),anchor=anchor)
def wrap(d,s,f,mw):
    out,line=[],''
    for w in s.split(' '):
        t=(line+' '+w).strip()
        if d.textlength(t,font=f)<=mw or not line: line=t
        else: out.append(line); line=w
    if line: out.append(line)
    return out

def cap_side(im,cap,a,F,W,H):
    """가로판 — 왼쪽 여백 (스테이지가 가운데 600px 이라 좌우가 빈다)"""
    tag,head,body=cap; d=ImageDraw.Draw(im); X,MW=88,540
    hl=wrap(d,head,F['head'],MW); bl=wrap(d,body,F['body'],MW)
    th=46+len(hl)*58+12+len(bl)*40; y=(H-th)//2
    d.rounded_rectangle((X-26,y-30,X+MW+26,y+th+30),16,fill=(8,11,20,int(150*a)))
    d.line((X-6,y+4,X-6,y+th-4),fill=ACC+(int(230*a),),width=5)
    txt(d,(X+16,y),tag,F['tag'],ACC,a); y+=46
    for l in hl: txt(d,(X+16,y),l,F['head'],INK,a); y+=58
    y+=12
    for l in bl: txt(d,(X+16,y),l,F['body'],DIM,a); y+=40
    return im

def cap_bottom(im,cap,a,F,W,H):
    """세로판 — 아래쪽. 게임이 화면 전체를 쓰므로 옆에 놓을 자리가 없다."""
    tag,head,body=cap; d=ImageDraw.Draw(im); M=64; MW=W-2*M-56
    hl=wrap(d,head,F['head'],MW); bl=wrap(d,body,F['body'],MW)
    th=48+len(hl)*60+10+len(bl)*42
    y0=H-th-150
    d.rounded_rectangle((M,y0-34,W-M,y0+th+34),20,fill=(8,11,20,int(184*a)))
    d.line((M+26,y0+2,M+31,y0+th-2),fill=ACC+(int(230*a),),width=6)
    x=M+52; y=y0
    txt(d,(x,y),tag,F['tag'],ACC,a); y+=48
    for l in hl: txt(d,(x,y),l,F['head'],INK,a); y+=60
    y+=10
    for l in bl: txt(d,(x,y),l,F['body'],DIM,a); y+=42
    return im

def card(im,s,a,F,W,H):
    sc=Image.new('RGBA',im.size,(5,8,16,int(234*a)))
    im=Image.alpha_composite(im.filter(ImageFilter.GaussianBlur(10)),sc)
    d=ImageDraw.Draw(im); cy=H//2
    txt(d,(W//2,cy-150),s['chapter'],F['cnum'],ACC,a,'mm')
    txt(d,(W//2,cy-16),s['title'],F['ctitle'],INK,a,'mm')
    d.line((W//2-140,cy+40,W//2+140,cy+40),fill=ACC+(int(200*a),),width=3)
    txt(d,(W//2,cy+88),s['sub'],F['sub'],INK,a,'mm')
    txt(d,(W//2,cy+142),s['note'],F['note'],DIM,a,'mm')
    return im

def title(im,s,a,F,W,H,outro=False):
    sc=Image.new('RGBA',im.size,(5,8,16,int((206 if not outro else 224)*a)))
    im=Image.alpha_composite(im.filter(ImageFilter.GaussianBlur(6 if not outro else 9)),sc)
    d=ImageDraw.Draw(im); cy=H//2-10
    txt(d,(W//2,cy-52),s['title'],F['title'],INK,a,'mm')
    d.line((W//2-200,cy+8,W//2+200,cy+8),fill=ACC+(int(215*a),),width=3)
    txt(d,(W//2,cy+58),s['sub'],F['sub'],ACC,a,'mm')
    txt(d,(W//2,cy+116),s['note'],F['note'],DIM,a,'mm')
    return im

def split(im,ph,cap,a,F,W,H):
    bg=Image.new('RGBA',(W,H),(6,9,18,255))
    crop=im.crop(((W-1040)//2,0,(W+1040)//2,H)); dw,dh=624,648; dy=120
    bg.paste(crop.resize((dw,dh)),(150,dy))
    pw=int(ph.width*(700/ph.height)); px=W-190-pw
    d=ImageDraw.Draw(bg)
    d.rounded_rectangle((140,dy-10,150+dw+10,dy+dh+10),14,outline=(58,70,94,255),width=2)
    d.rounded_rectangle((px-16,dy-16,px+pw+16,dy+716),26,fill=(16,21,32,255),
                        outline=(58,70,94,255),width=2)
    bg.paste(ph.resize((pw,700)),(px,dy))
    txt(d,(150+dw//2,dy+dh+44),'PC',F['tag'],DIM,1.0,'mm')
    txt(d,(px+pw//2,dy+750),'SMARTPHONE',F['tag'],DIM,1.0,'mm')
    tag,head,body=cap
    tw=max(d.textlength(head,font=F['head']),d.textlength(body,font=F['body']))+96
    x0=(W-tw)//2; y0=H-216
    d.rounded_rectangle((x0,y0,x0+tw,y0+168),16,fill=(8,11,20,int(170*a)))
    d.line((x0+30,y0+26,x0+35,y0+142),fill=ACC+(int(230*a),),width=5)
    txt(d,(x0+56,y0+22),tag,F['tag'],ACC,a)
    txt(d,(x0+56,y0+62),head,F['head'],INK,a)
    txt(d,(x0+56,y0+120),body,F['body'],DIM,a)
    return bg

def build(plat, secs):
    shots = EDITS[(plat, secs)]
    W,H = SIZE[plat]
    F = fonts(1.0 if plat=='desk' else 1.06)
    out = os.path.join(S,'s1_out_%s_%d'%(plat,secs)); os.makedirs(out, exist_ok=True)
    capfn = cap_side if plat=='desk' else cap_bottom
    idx=0; made=0
    for s in shots:
        src = os.path.join(S,'s1_%s_%s'%(plat,s['clip']))
        for k in range(s['n']):
            dst=os.path.join(out,'f%05d.png'%idx); idx+=1
            if os.path.exists(dst): continue
            sp=os.path.join(src,'f%05d.png'%(s['off']+k))
            if not os.path.exists(sp): print('누락:',sp); return 1
            im=Image.open(sp).convert('RGBA')
            if im.size!=(W,H): im=im.resize((W,H))
            u=k/max(s['n']-1,1); kind=s['kind']
            if kind=='card':    im=card(im,s,fade(u,.18,.18),F,W,H)
            elif kind=='title': im=title(im,s,fade(u,.16,.12),F,W,H)
            elif kind=='outro': im=title(im,s,fade(u,.14,.10),F,W,H,True)
            elif kind=='split':
                p=os.path.join(S,'s1_phone_%s'%s['clip'],'f%05d.png'%(s['off']+k))
                im=split(im,Image.open(p).convert('RGBA'),s['cap'],fade(u,.16,.16),F,W,H)
            else: im=capfn(im,s['cap'],fade(u,.16,.16),F,W,H)
            im.convert('RGB').save(dst); made+=1
    print('  %s %ds : %d프레임 (신규 %d)'%(plat,secs,idx,made))
    return 0

if __name__=='__main__':
    for plat,secs in [('desk',60),('desk',30),('phone',60),('phone',30)]:
        if build(plat,secs): sys.exit(1)

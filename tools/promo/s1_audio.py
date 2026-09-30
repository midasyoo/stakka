# -*- coding: utf-8 -*-
"""STAKKA 1 오디오 — 길이별(60s/30s)로 내레이션+배경음을 만들어 네 영상에 붙인다.
같은 길이면 가로/세로가 오디오를 공유한다."""
import asyncio, json, os, re, subprocess, sys, wave
import numpy as np, edge_tts, imageio_ffmpeg
S = r"C:/Users/ADMIN/AppData/Local/Temp/claude/c--Users-ADMIN-Antigravity/3fa05fad-ad53-453e-9e14-6af59210b93d/scratchpad"
sys.path.insert(0, S)
import sk_music
from s1_narration import SCRIPTS, VOICE, PITCH, RATES

SR = sk_music.SR
FF = imageio_ffmpeg.get_ffmpeg_exe()
COMP = ('acompressor=threshold=-20dB:ratio=2.6:attack=6:release=140:makeup=2,'
        'alimiter=level_in=1:limit=0.85:attack=5:release=60')

def run(a): return subprocess.run([FF]+a, capture_output=True, text=True, errors='replace')
def smooth(x,ms):
    k=max(1,int(SR*ms/1000.)); return np.convolve(x,np.ones(k)/k,mode='same')
def wwav(p,x):
    with wave.open(p,'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(x,-1,1)*32767).astype(np.int16).tobytes())
def rwav(p):
    with wave.open(p,'rb') as f:
        return np.frombuffer(f.readframes(f.getnframes()),dtype=np.int16).astype(np.float32)/32768.
def trim(a,thr=0.012,pad=0.05):
    n=int(SR*0.02); m=len(a)//n*n
    if m==0: return a
    r=np.sqrt((a[:m].reshape(-1,n)**2).mean(axis=1)); idx=np.where(r>thr)[0]
    if not len(idx): return a
    return a[max(0,int(idx[0]*n-pad*SR)):min(len(a),int((idx[-1]+1)*n+pad*SR))]

def voice(secs):
    d=os.path.join(S,'s1_voice_%d'%secs); os.makedirs(d,exist_ok=True)
    clips=[]
    for i,l in enumerate(SCRIPTS[secs]):
        mp3=os.path.join(d,'l%02d.mp3'%i); wav=os.path.join(d,'l%02d.wav'%i)
        best=None
        for r in RATES:
            asyncio.run(edge_tts.Communicate(l['text'],VOICE,rate=r,pitch=PITCH).save(mp3))
            run(['-y','-loglevel','error','-i',mp3,'-ac','1','-ar',str(SR),wav])
            a=trim(rwav(wav)); best=(r,len(a)/SR,a)
            if best[1]<=l['limit']: break
        r,dur,a=best
        print('   %2d %s %-5s %4.2fs/%.1fs  %s'%(i,'OK ' if dur<=l['limit']+.02 else '초과',
              r,dur,l['limit'],l['text'][:26]), flush=True)
        clips.append((l['start'],a))
    for (s1,a1),(s2,_) in zip(clips,clips[1:]):
        if s1+len(a1)/SR > s2+0.02: print('   겹침 %.2f->%.2f'%(s1,s2))
    return clips

def build(secs):
    print(' [%ds] 내레이션'%secs, flush=True)
    n=int(secs*SR); clips=voice(secs)
    v=np.zeros(n)
    for st,a in clips:
        i=int(st*SR); j=min(n,i+len(a)); v[i:j]+=a[:j-i]
    g=(np.abs(v)>0.01).astype(np.float32)
    g=(smooth(g,260)>0.02).astype(np.float32); g=np.clip(smooth(g,420),0,1)
    print(' [%ds] 배경음'%secs, flush=True)
    m=sk_music.build(float(secs))[:n]
    v=v/(np.abs(v).max() or 1.)*0.86
    mix=v+m*(1.0-0.62*g)*0.30
    pk=np.abs(mix).max()
    if pk>0.99: mix*=0.99/pk
    raw=os.path.join(S,'s1_mix_%d.wav'%secs); wwav(raw,mix)
    comp=os.path.join(S,'s1_mix_%d_c.wav'%secs)
    run(['-y','-loglevel','error','-i',raw,'-af',COMP,'-ar',str(SR),'-ac','1',comp])
    r=run(['-i',comp,'-af','loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json','-f','null','-'])
    j=json.loads(re.search(r'\{[^{}]*\}',r.stderr,re.S).group(0))
    norm=os.path.join(S,'s1_mix_%d_n.wav'%secs)
    run(['-y','-loglevel','error','-i',comp,'-af',
         'loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=%s:measured_TP=%s:measured_LRA=%s:'
         'measured_thresh=%s,aresample=%d'%(j['input_i'],j['input_tp'],j['input_lra'],
                                            j['input_thresh'],SR),
         '-ar',str(SR),'-ac','1','-t',str(secs),norm])
    print(' [%ds] 오디오 완료 (측정 I=%s)'%(secs,j['input_i']), flush=True)
    return norm

if __name__=='__main__':
    for secs in (60,30):
        norm=build(secs)
        for plat in ('desk','phone'):
            src=os.path.join(S,'s1_%s_%d_silent.mp4'%(plat,secs))
            out=os.path.join(S,'stakka1-%ds-%s.mp4'%(secs,'desktop' if plat=='desk' else 'mobile'))
            run(['-y','-loglevel','error','-i',src,'-i',norm,'-c:v','copy','-c:a','aac',
                 '-b:a','192k','-ar',str(SR),'-ac','2','-shortest','-movflags','+faststart',out])
            print('  ->', os.path.basename(out), '%.1f MB'%(os.path.getsize(out)/1048576), flush=True)

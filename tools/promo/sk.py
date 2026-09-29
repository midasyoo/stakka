# -*- coding: utf-8 -*-
"""Stakka 캡처용 CDP 세션."""
import os, json, time, base64, subprocess, urllib.request, websocket
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
S = r"C:/Users/ADMIN/AppData/Local/Temp/claude/c--Users-ADMIN-Antigravity/3fa05fad-ad53-453e-9e14-6af59210b93d/scratchpad"

class Sess:
    def __init__(self, port=9600, w=1600, h=900, dpr=1, mobile=False, tag='s'):
        self.p = subprocess.Popen([CHROME,'--headless=new','--disable-gpu',
            '--use-angle=swiftshader','--enable-unsafe-swiftshader',
            '--remote-debugging-port=%d'%port,'--remote-allow-origins=*',
            '--user-data-dir='+os.path.join(S,'sk_'+tag),'--hide-scrollbars',
            '--allow-file-access-from-files','about:blank'],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        u=None
        for _ in range(120):
            try:
                for t in json.load(urllib.request.urlopen('http://127.0.0.1:%d/json'%port)):
                    if t.get('type')=='page': u=t['webSocketDebuggerUrl']; break
                if u: break
            except Exception: pass
            time.sleep(.25)
        if not u: raise RuntimeError('CDP 실패')
        self.ws=websocket.create_connection(u,timeout=180,suppress_origin=True); self.i=0
        self.cmd('Page.enable')
        self.cmd('Emulation.setDeviceMetricsOverride',width=w,height=h,
                 deviceScaleFactor=dpr,mobile=mobile,screenWidth=w,screenHeight=h)
    def cmd(self,m,**pr):
        self.i+=1; self.ws.send(json.dumps({'id':self.i,'method':m,'params':pr}))
        while True:
            r=json.loads(self.ws.recv())
            if r.get('id')==self.i:
                if 'error' in r: raise RuntimeError(str(r['error'])[:300])
                return r.get('result',{})
    def goto(self, game, frag='', wait=12):
        url='file:///C:/Users/ADMIN/Antigravity/%s/index.html?cap=1%s' % (game, frag)
        self.cmd('Page.navigate',url=url)
        t0=time.time()
        while time.time()-t0<wait:
            time.sleep(0.6)
            try:
                if self.js('!!window.__CAP'): break
            except Exception: pass
        time.sleep(1.2)
    def js(self,e): return self.cmd('Runtime.evaluate',expression=e,returnByValue=True)['result'].get('value')
    def shot(self,p):
        d=self.cmd('Page.captureScreenshot',format='png')['data']
        open(p,'wb').write(base64.b64decode(d)); return os.path.getsize(p)
    def close(self):
        try: self.ws.close()
        except Exception: pass
        self.p.terminate()

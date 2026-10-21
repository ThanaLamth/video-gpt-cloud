#!/usr/bin/env python3
"""gen.py  v2  -  KimQ intro (3s) + outro (5s)  -  single logo asset only"""
import base64, io, pathlib

CASE_DIR = pathlib.Path(r"C:\Users\admin\onetake\cases\kimc-brand")
LOGO_DIR = pathlib.Path(r"C:\Users\admin\Downloads\Telegram Desktop")

from PIL import Image
import numpy as np

def b64transparent(path, thr=238):
    img = Image.open(path).convert("RGBA")
    d = np.array(img)
    mask = (d[:,:,0] > thr) & (d[:,:,1] > thr) & (d[:,:,2] > thr)
    d[mask, 3] = 0
    buf = io.BytesIO()
    Image.fromarray(d).save(buf, "PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

# Only the full wordmark (already contains K-i-m-C with bird in C)
word_src = b64transparent(LOGO_DIR / "logo.png")
print(f"wordmark {len(word_src)//1024}KB")

# logo.png natural size ≈ 970×270 → display 620×172 (ratio 3.56)
LOGO_W, LOGO_H = 620, 174

# ─────────────────────────────────────────────────────────────────────
# SHARED JS snippet — draw logo + slogan once (used in both files)
# Layout (1080×1920):
#   Logo center:  (540, 840)   →  top=753  bottom=927
#   Slogan:  y=990
#   Separator:  y=1013
# ─────────────────────────────────────────────────────────────────────
SHARED_VARS = """
  var W=1080,H=1920,CX=540;
  var LCY=840, SLY=990, SEY=1013;
  var LW=__LW__, LH=__LH__;
  var GOLD='#C9A42A', GOLDL='#E8D488', WHITE='#FFFFFF', BG='#080808';
  function gp(a){return 'rgba(201,164,42,'+a+')';}
""".replace("__LW__", str(LOGO_W)).replace("__LH__", str(LOGO_H))

# ─────────────────────────────────────────────────────────────────────
# INTRO  3 s
# 0.00-0.48  ambient glow + seed dot + particles converge
# 0.40-1.30  wordmark popIn  (spring backOut)
# 1.28-2.00  slogan maskRise
# 1.95-2.40  separator grow
# 0.00-3.00  particles float after converge
# ─────────────────────────────────────────────────────────────────────
INTRO = r"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>*{margin:0;padding:0}body{background:#080808;overflow:hidden;width:1080px;height:1920px}canvas{display:block}</style>
</head><body>
<canvas id="c" width="1080" height="1920"></canvas>
<script src="../mirofish-30s/motion.js"></script>
<script>
(function(){
'use strict';
__SHARED__
  var O=window.OM;
  var cv=document.getElementById('c');
  var X=cv.getContext('2d');
  var wI=new Image(); wI.src='__WORD__';

  var rn=O.rng(42); var NP=55, pts=[];
  for(var i=0;i<NP;i++) pts.push({a:rn()*Math.PI*2,d:160+rn()*350,sp:0.5+rn()*0.7,r:1.4+rn()*2.8,ph:rn()*Math.PI*2});

  function __seek(t){
    X.clearRect(0,0,W,H);
    X.fillStyle=BG; X.fillRect(0,0,W,H);

    /* ambient glow */
    var ga=Math.min(t/0.45,1)*0.14;
    var g0=X.createRadialGradient(CX,LCY,0,CX,LCY,480);
    g0.addColorStop(0,gp(ga)); g0.addColorStop(1,'rgba(0,0,0,0)');
    X.fillStyle=g0; X.fillRect(0,0,W,H);

    /* particles */
    for(var i=0;i<NP;i++){
      var p=pts[i],px,py,pa;
      if(t<0.95){
        var ck=O.ease.expoOut(O.seg(t,0.0,0.95));
        px=CX+Math.cos(p.a)*p.d*(1-ck*0.90); py=LCY+Math.sin(p.a)*p.d*(1-ck*0.90);
        pa=ck*0.45;
      } else {
        var dt=(t-0.95)*p.sp;
        px=CX+Math.cos(p.a)*p.d*0.10+Math.sin(dt*1.8+p.ph)*14;
        py=LCY-dt*62+Math.sin(dt+p.ph)*9;
        pa=0.22*(1-O.seg(t,2.5,3.0));
      }
      X.globalAlpha=pa*(0.66+0.34*Math.sin(t*4.1+p.ph));
      X.fillStyle=GOLD; X.beginPath(); X.arc(px,py,p.r,0,Math.PI*2); X.fill();
    }
    X.globalAlpha=1;

    /* seed dot 0.02->0.48 */
    if(t<0.5){
      var dk=O.spring(t-0.02,0.6,22);
      if(dk>0){
        var dr=9*dk;
        var dg=X.createRadialGradient(CX,LCY,0,CX,LCY,dr*5);
        dg.addColorStop(0,'rgba(245,230,155,'+dk+')');
        dg.addColorStop(0.45,gp(dk*0.48)); dg.addColorStop(1,'rgba(0,0,0,0)');
        X.fillStyle=dg; X.beginPath(); X.arc(CX,LCY,dr*5,0,Math.PI*2); X.fill();
        X.fillStyle='#F5EA9E'; X.beginPath(); X.arc(CX,LCY,dr,0,Math.PI*2); X.fill();
      }
    }

    /* wordmark popIn 0.40->1.28 */
    var wk=O.popIn(t,0.40,{zeta:0.55,omega:16,rise:72});
    if(wk.op>0){
      var ws=LW*wk.s, wh=LH*wk.s;
      X.save(); X.globalAlpha=wk.op;
      X.drawImage(wI,CX-ws/2,LCY-wh/2+wk.dy,ws,wh);
      X.restore();
    }

    /* slogan maskRise 1.28->2.00 */
    var sl=O.maskRise(t,1.28,0,{dist:50,zeta:0.47,omega:17});
    if(sl.visible){
      X.save(); X.globalAlpha=O.seg(t,1.28,1.72);
      X.beginPath(); X.rect(0,SLY-52,W,56); X.clip();
      X.font='italic 500 32px Georgia,"Times New Roman",serif';
      X.fillStyle=GOLDL; X.textAlign='center'; X.letterSpacing='2.5px';
      X.fillText('Ancient Wisdom  \u00B7  Modern Intelligence',CX,SLY+sl.y);
      X.restore();
    }

    /* separator 1.95->2.38 */
    var sk=O.tween(t,1.95,2.36,O.ease.expoOut);
    if(sk>0){
      X.save(); X.globalAlpha=0.50*O.seg(t,1.95,2.22);
      X.strokeStyle=GOLD; X.lineWidth=1.1;
      X.beginPath(); X.moveTo(CX-85*sk,SEY); X.lineTo(CX+85*sk,SEY); X.stroke();
      X.restore();
    }

    /* hold glow 2.72->3.0 */
    if(t>2.72){
      X.save(); X.globalAlpha=0.06*O.seg(t,2.72,3.0);
      var hg=X.createRadialGradient(CX,LCY,0,CX,LCY,250);
      hg.addColorStop(0,GOLDL); hg.addColorStop(1,'rgba(0,0,0,0)');
      X.fillStyle=hg; X.beginPath(); X.arc(CX,LCY,250,0,Math.PI*2); X.fill();
      X.restore();
    }
  }

  var _res; window.__ready=new Promise(function(r){_res=r;});
  if(wI.complete)_res(); else wI.addEventListener('load',_res,{once:true});
  window.__seek=__seek;
  window.__meta={dur:3};
  window.__motion=function(t0,t1){return t1<0.95?320:t0<1.4?80:25;};
}());
</script></body></html>"""

# ─────────────────────────────────────────────────────────────────────
# OUTRO  5 s
# 0.00-0.55  full logo fadeIn
# 0.55-1.42  shimmer sweep L->R
# 1.42-2.12  "Theo doi KimQ" maskRise
# 2.12-2.82  "@KimQ.studio" typeOn
# 2.82-3.80  sparkles + breathing
# 3.80-5.00  fade to black
# ─────────────────────────────────────────────────────────────────────
OUTRO = r"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>*{margin:0;padding:0}body{background:#080808;overflow:hidden;width:1080px;height:1920px}canvas{display:block}</style>
</head><body>
<canvas id="c" width="1080" height="1920"></canvas>
<script src="../mirofish-30s/motion.js"></script>
<script>
(function(){
'use strict';
__SHARED__
  var CTAY=1130, HANDY=1205;
  var O=window.OM;
  var cv=document.getElementById('c');
  var X=cv.getContext('2d');
  var wI=new Image(); wI.src='__WORD__';

  var rn=O.rng(17); var NP=42, pts=[];
  for(var i=0;i<NP;i++) pts.push({a:rn()*Math.PI*2,d:100+rn()*260,sp:0.35+rn()*0.5,r:1.2+rn()*2.2,ph:rn()*Math.PI*2});

  function drawFull(alpha,sc){
    sc=sc||1;
    var ws=LW*sc, wh=LH*sc;
    X.save(); X.globalAlpha=alpha;
    X.drawImage(wI,CX-ws/2,LCY-wh/2,ws,wh);
    X.restore();
    X.save(); X.globalAlpha=alpha;
    X.font='italic 500 31px Georgia,"Times New Roman",serif';
    X.fillStyle=GOLDL; X.textAlign='center'; X.letterSpacing='2px';
    X.fillText('Ancient Wisdom  \u00B7  Modern Intelligence',CX,SLY);
    X.restore();
    X.save(); X.globalAlpha=alpha*0.46;
    X.strokeStyle=GOLD; X.lineWidth=1.1;
    X.beginPath(); X.moveTo(CX-86,SEY); X.lineTo(CX+86,SEY); X.stroke();
    X.restore();
  }

  function __seek(t){
    X.clearRect(0,0,W,H);
    X.fillStyle=BG; X.fillRect(0,0,W,H);

    var fadeOut=O.ease.quadOut(O.seg(t,3.80,5.0));
    var masterA=1-fadeOut;

    /* ambient glow */
    X.save(); X.globalAlpha=masterA*0.12;
    var g0=X.createRadialGradient(CX,LCY,0,CX,LCY,460);
    g0.addColorStop(0,gp(1)); g0.addColorStop(1,'rgba(0,0,0,0)');
    X.fillStyle=g0; X.fillRect(0,0,W,H); X.restore();

    /* particles */
    if(t>0.4 && masterA>0){
      for(var i=0;i<NP;i++){
        var p=pts[i];
        var dt=(t-0.4)*p.sp;
        var px=CX+Math.cos(p.a)*p.d*0.13+Math.sin(dt*1.6+p.ph)*13;
        var py=LCY-dt*52+Math.sin(dt+p.ph)*8;
        var pa=0.20*(1-O.seg(t,4.0,5.0));
        X.globalAlpha=pa*(0.62+0.38*Math.sin(t*3.9+p.ph));
        X.fillStyle=GOLD; X.beginPath(); X.arc(px,py,p.r,0,Math.PI*2); X.fill();
      }
      X.globalAlpha=1;
    }

    /* logo fadeIn + breathing */
    var logoA=O.seg(t,0.0,0.52)*masterA;
    var breath=1+0.016*Math.sin(O.seg(t,2.82,3.80)*Math.PI*2.2);
    var sc=t<2.82?1.0:breath;
    drawFull(logoA,sc);

    /* shimmer 0.55->1.42 */
    if(t>0.55 && t<1.52){
      var sw=O.tween(t,0.60,1.40,O.ease.cubicInOut);
      var swx=-140+sw*(W+280);
      var sg=X.createLinearGradient(swx-120,0,swx+120,0);
      sg.addColorStop(0,'rgba(255,246,200,0)');
      sg.addColorStop(0.5,'rgba(255,246,200,0.11)');
      sg.addColorStop(1,'rgba(255,246,200,0)');
      X.save(); X.fillStyle=sg;
      X.fillRect(0,LCY-100,W,380); X.restore();
    }

    /* CTA maskRise 1.42->2.12 */
    var ct=O.maskRise(t,1.42,0,{dist:56,zeta:0.45,omega:16});
    if(ct.visible){
      X.save(); X.globalAlpha=O.seg(t,1.42,1.85)*masterA;
      X.beginPath(); X.rect(0,CTAY-56,W,60); X.clip();
      X.font='700 50px "Segoe UI","Arial",sans-serif';
      X.fillStyle=WHITE; X.textAlign='center'; X.letterSpacing='1px';
      X.fillText('Theo d\u00F5i KimQ',CX,CTAY+ct.y);
      X.restore();
    }

    /* handle typeOn 2.12->2.82 */
    var to=O.typeOn(t,2.14,'@KimQ.studio  \u2022  youtube  \u2022  tiktok',{cps:17});
    if(to.n>0){
      X.save(); X.globalAlpha=O.seg(t,2.12,2.50)*masterA*0.70;
      X.font='400 27px "Segoe UI","Arial",sans-serif';
      X.fillStyle=GOLDL; X.textAlign='center'; X.letterSpacing='0.5px';
      X.fillText(to.str+(to.caret?'\u258C':''),CX,HANDY);
      X.restore();
    }

    /* sparkle dots 2.82->3.5 */
    if(t>2.82 && masterA>0){
      var spk=O.popIn(t,2.84,{zeta:0.5,omega:22,rise:0});
      if(spk.op>0){
        var offs=[[0,-180],[170,-90],[170,90],[0,180],[-170,-90],[-170,90]];
        for(var j=0;j<offs.length;j++){
          X.save(); X.globalAlpha=spk.op*0.32*masterA;
          X.fillStyle=GOLDL;
          X.beginPath(); X.arc(CX+offs[j][0],LCY+offs[j][1],3.2,0,Math.PI*2); X.fill();
          X.restore();
        }
      }
    }
  }

  var _res; window.__ready=new Promise(function(r){_res=r;});
  if(wI.complete)_res(); else wI.addEventListener('load',_res,{once:true});
  window.__seek=__seek;
  window.__meta={dur:5};
  window.__motion=function(t0,t1){return t1<0.6?25:t0<1.5?90:t1>3.8?55:22;};
}());
</script></body></html>"""

intro = INTRO.replace('__SHARED__', SHARED_VARS).replace('__WORD__', word_src)
outro = OUTRO.replace('__SHARED__', SHARED_VARS).replace('__WORD__', word_src)

(CASE_DIR / "kimc-intro.html").write_text(intro, encoding='utf-8')
(CASE_DIR / "kimc-outro.html").write_text(outro, encoding='utf-8')
print(f"intro {len(intro)//1024}KB  outro {len(outro)//1024}KB  - done")

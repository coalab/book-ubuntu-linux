#!/usr/bin/env python3
"""Build index.html for book-ubuntu-linux"""
import json, os, re

chapters_dir = os.path.join(os.path.dirname(__file__), 'chapters')

order = [f'ch{i:02d}.md' for i in range(1, 19)] + ['appendix.md']

chapters = []
for fname in order:
    path = os.path.join(chapters_dir, fname)
    with open(path, encoding='utf-8') as f:
        chapters.append(f.read())

chapters_json = json.dumps(chapters, ensure_ascii=False)

toc_lines = []
for i, ch in enumerate(chapters[:-1], 1):
    m = re.search(r'^#\s+(.+)', ch, re.MULTILINE)
    title = m.group(1) if m else f'챕터 {i}'
    toc_lines.append(f'CH{i:02d} {title}')
toc_lines.append('부록: 빠른 참조 가이드')
toc_str = '<br>'.join(toc_lines[:9]) + '<br>...'

html = f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>이것이 우분투 리눅스다</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#2c3e6b;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans KR',sans-serif;height:100vh;display:flex;flex-direction:column;overflow:hidden;user-select:none}}

/* 헤더 */
.hd{{background:linear-gradient(135deg,#1a2547,#1e3a8a);padding:8px 20px;display:flex;justify-content:space-between;align-items:center;flex-shrink:0;box-shadow:0 2px 10px rgba(0,0,0,.4);height:46px}}
.hd h1{{color:#93c5fd;font-size:.9rem;font-weight:700}}
.hd .inf{{color:#60a5fa;font-size:.78rem}}
.pdf-btn{{background:rgba(37,99,235,.7);color:#fff;border:none;padding:4px 12px;border-radius:12px;font-size:.72rem;cursor:pointer;transition:.2s;display:flex;align-items:center;gap:4px}}
.pdf-btn:hover{{background:#2563eb}}

/* 뷰어 */
.viewer{{flex:1;display:flex;align-items:center;justify-content:center;padding:16px 8px;min-height:0;gap:0}}

/* 네비게이션 버튼 */
.nav{{background:rgba(37,99,235,.7);color:#fff;border:none;width:38px;height:38px;border-radius:50%;font-size:1.1rem;cursor:pointer;transition:.2s;flex-shrink:0;margin:0 8px}}
.nav:hover{{background:#2563eb;transform:scale(1.1)}}
.nav:disabled{{background:rgba(255,255,255,.08);cursor:default;transform:none}}

/* 책 컨테이너 */
.book{{display:flex;box-shadow:0 20px 60px rgba(0,0,0,.7);border-radius:2px 6px 6px 2px;position:relative}}
.book::after{{content:'';position:absolute;top:0;left:50%;width:6px;height:100%;background:linear-gradient(90deg,rgba(0,0,0,.3),rgba(0,0,0,.05),rgba(0,0,0,.3));transform:translateX(-50%);z-index:10;pointer-events:none}}

/* 페이지 */
.page{{background:#fff;overflow:hidden;display:flex;flex-direction:column;flex-shrink:0}}
.page.left{{border-radius:2px 0 0 2px;box-shadow:-4px 0 15px rgba(0,0,0,.2)}}
.page.right{{border-radius:0 6px 6px 0;box-shadow:4px 0 15px rgba(0,0,0,.2)}}

/* 표지 */
.page.cover-l{{background:linear-gradient(135deg,#1a2547,#1e3a8a)}}
.page.cover-r{{background:linear-gradient(135deg,#1e3a8a,#2563eb)}}
.cover-content{{display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;text-align:center;padding:8%}}
.cov-ic{{font-size:3em;margin-bottom:.3em}}
.cov-t{{font-size:1.5em;font-weight:900;color:#fff;line-height:1.2;margin-bottom:.3em}}
.cov-t span{{color:#93c5fd}}
.cov-s{{color:#93c5fd;font-size:.65em;margin-bottom:1em;line-height:1.6}}
.cov-b{{background:#2563eb;color:#fff;padding:.3em .8em;border-radius:20px;font-size:.55em;font-weight:600;border:1px solid #93c5fd}}
.cov-toc{{color:#93c5fd;font-size:.52em;text-align:left;margin-top:1em;line-height:1.9;width:100%}}
.cov-toc strong{{color:#fff;display:block;margin-bottom:.3em;font-size:1.1em}}

/* 페이지 헤더 */
.pg-hd{{background:linear-gradient(90deg,#1e3a8a,#2563eb);color:#fff;padding:.35em .7em;font-size:.52em;font-weight:600;flex-shrink:0}}
.pg-hd em{{color:#93c5fd;font-style:normal;margin-right:.5em}}

/* 본문 */
.pg-bd{{flex:1;padding:.8em .95em;overflow:hidden;color:#1e293b;line-height:1.62;font-size:.68em}}
.pg-bd h1{{font-size:1.3em;font-weight:800;color:#1e3a8a;border-bottom:2px solid #2563eb;padding-bottom:.25em;margin-bottom:.5em;line-height:1.3}}
.pg-bd h2{{font-size:1em;font-weight:700;color:#1e3a8a;border-left:3px solid #2563eb;padding-left:.45em;margin:.6em 0 .3em}}
.pg-bd h3{{font-size:.88em;font-weight:600;color:#334155;margin:.4em 0 .2em}}
.pg-bd p{{margin-bottom:.38em}}
.pg-bd ul,.pg-bd ol{{padding-left:1.1em;margin:.2em 0 .4em}}
.pg-bd li{{margin:.1em 0}}
.pg-bd blockquote{{border-left:3px solid #2563eb;padding:.3em .6em;background:#eff6ff;color:#374151;font-style:italic;margin:.35em 0;font-size:.92em}}
.pg-bd pre{{background:#1e293b;color:#e2e8f0;padding:.5em .7em;border-radius:4px;font-size:.75em;overflow:hidden;margin:.35em 0;line-height:1.4;white-space:pre-wrap;word-break:break-all}}
.pg-bd code{{background:#eff6ff;color:#1d4ed8;padding:.1em .25em;border-radius:3px;font-size:.88em}}
.pg-bd pre code{{background:none;color:inherit;padding:0;font-size:1em}}
.pg-bd table{{width:100%;border-collapse:collapse;margin:.35em 0;font-size:.82em}}
.pg-bd th{{background:#1e3a8a;color:#fff;padding:.25em .4em;text-align:left}}
.pg-bd td{{padding:.2em .4em;border-bottom:1px solid #e2e8f0}}
.pg-bd tr:nth-child(even) td{{background:#f8fafc}}
.pg-bd strong{{color:#1e3a8a;font-weight:700}}
.pg-bd hr{{border:none;border-top:1px solid #e2e8f0;margin:.35em 0}}

/* 페이지 푸터 */
.pg-ft{{padding:.25em .7em;display:flex;justify-content:space-between;border-top:1px solid #e2e8f0;font-size:.46em;color:#94a3b8;background:#f8fafc;flex-shrink:0}}

/* 플립 애니메이션 */
.book.flip-next{{animation:fn .5s ease}}
.book.flip-prev{{animation:fp .5s ease}}
@keyframes fn{{0%{{transform:perspective(1200px) rotateY(0)}}40%{{transform:perspective(1200px) rotateY(-4deg)}}100%{{transform:perspective(1200px) rotateY(0)}}}}
@keyframes fp{{0%{{transform:perspective(1200px) rotateY(0)}}40%{{transform:perspective(1200px) rotateY(4deg)}}100%{{transform:perspective(1200px) rotateY(0)}}}}

/* 하단 바 */
.bottom{{flex-shrink:0;display:flex;align-items:center;justify-content:center;gap:12px;padding:6px 16px;background:rgba(0,0,0,.2)}}
.prog{{flex:1;max-width:300px;height:4px;background:rgba(255,255,255,.15);border-radius:2px;cursor:pointer}}
.prog-b{{height:100%;background:#2563eb;border-radius:2px;transition:width .3s}}
.pg-input{{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.2);color:#93c5fd;padding:2px 6px;border-radius:4px;font-size:.72rem;width:60px;text-align:center}}
.pg-input:focus{{outline:none;border-color:#2563eb}}

/* 모바일: 단일 페이지 */
@media(max-width:640px){{
  .page.right{{display:none}}
  .book::after{{display:none}}
  .page.left{{border-radius:4px}}
}}
</style>
</head>
<body>
<div class="hd">
  <h1>🐧 이것이 우분투 리눅스다</h1>
  <div style="display:flex;align-items:center;gap:12px">
    <div class="inf"><span id="pn">1</span> / <span id="pt">-</span></div>
    <button class="pdf-btn" onclick="window.print()">📄 인쇄/PDF</button>
  </div>
</div>
<div class="viewer">
  <button class="nav" id="pb" onclick="go(-1)" disabled>&#8592;</button>
  <div class="book" id="book">
    <div class="page left" id="pl"></div>
    <div class="page right" id="pr"></div>
  </div>
  <button class="nav" id="nb" onclick="go(1)">&#8594;</button>
</div>
<div class="bottom">
  <button class="nav" style="margin:0;width:30px;height:30px;font-size:.8rem" onclick="go(-1)" disabled id="pb2">&#8592;</button>
  <div class="prog" id="prog" onclick="jumpTo(event)"><div class="prog-b" id="bar"></div></div>
  <input class="pg-input" id="pi" value="1" onchange="jumpPage(this.value)" />
  <button class="nav" style="margin:0;width:30px;height:30px;font-size:.8rem" onclick="go(1)" id="nb2">&#8594;</button>
</div>
<script>
const CHAPTERS={chapters_json};

function md2html(t){{
  const esc=s=>s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  const inlineM=s=>{{
    s=s.replace(/`([^`]+)`/g,(_,c)=>'<code>'+esc(c)+'</code>');
    s=s.replace(/\*\*([^*]+)\*\*/g,'<strong>$1</strong>');
    s=s.replace(/\*([^*]+)\*/g,'<em>$1</em>');
    return s;
  }};
  const lines=t.split('\\n');
  let out='',inPre=false,inUl=false,inOl=false,buf='';
  const flush=()=>{{if(buf.trim()){{out+='<p>'+inlineM(buf.trim())+'</p>';buf='';}}}};
  const flushL=()=>{{if(inUl){{out+='</ul>';inUl=false;}}if(inOl){{out+='</ol>';inOl=false;}}}};
  for(const l of lines){{
    if(l.startsWith('```')){{if(!inPre){{flush();flushL();out+='<pre><code>';inPre=true;}}else{{out+='</code></pre>';inPre=false;}}continue;}}
    if(inPre){{out+=esc(l)+'\\n';continue;}}
    if(l.startsWith('> ')){{flush();flushL();out+='<blockquote>'+inlineM(l.slice(2))+'</blockquote>';continue;}}
    if(l.startsWith('# ')){{flush();flushL();out+='<h1>'+inlineM(l.slice(2))+'</h1>';continue;}}
    if(l.startsWith('## ')){{flush();flushL();out+='<h2>'+inlineM(l.slice(3))+'</h2>';continue;}}
    if(l.startsWith('### ')){{flush();flushL();out+='<h3>'+inlineM(l.slice(4))+'</h3>';continue;}}
    if(l.startsWith('- ')||l.startsWith('* ')){{flush();if(!inUl){{flushL();out+='<ul>';inUl=true;}}out+='<li>'+inlineM(l.slice(2))+'</li>';continue;}}
    if(/^\\d+\\.\\s/.test(l)){{flush();if(!inOl){{flushL();out+='<ol>';inOl=true;}}out+='<li>'+inlineM(l.replace(/^\\d+\\.\\s/,''))+'</li>';continue;}}
    if(/^---+$/.test(l)){{flush();flushL();out+='<hr>';continue;}}
    if(l.trim()===''){{flush();flushL();continue;}}
    buf+=(buf?' ':'')+l;
  }}
  flush();flushL();
  return out;
}}

function buildPages(){{
  const p=[];
  p.push({{type:'cover-l'}});
  p.push({{type:'cover-r'}});
  CHAPTERS.forEach((md,ci)=>{{
    const isAppendix=ci===CHAPTERS.length-1;
    const tm=md.match(/^#\\s+(.+)/m);
    const title=tm?tm[1]:(isAppendix?'부록':'챕터'+(ci+1));
    const parts=md.split(/\\n(?=##\\s)/);
    parts.forEach(pt=>{{if(pt.trim())p.push({{type:'c',title,num:isAppendix?'A':ci+1,md:pt.trim()}});}});
  }});
  if(p.length%2!==0)p.push({{type:'blank'}});
  return p;
}}

const PAGES=buildPages();
const SPREADS=Math.ceil(PAGES.length/2);
let cur=0;
let busy=false;

document.getElementById('pt').textContent=PAGES.length;

function resize(){{
  const vw=window.innerWidth,vh=window.innerHeight-46-38;
  const isMobile=vw<=640;
  let w,h;
  if(isMobile){{
    const avW=Math.min(vw-80,400),avH=vh-24;
    w=avW;h=w*1.414;
    if(h>avH){{h=avH;w=h/1.414;}}
    document.getElementById('pl').style.cssText='width:'+Math.floor(w)+'px;height:'+Math.floor(h)+'px;font-size:'+Math.floor(w/380*12)+'px';
  }} else {{
    const avW=Math.min((vw-120)/2,420),avH=vh-24;
    w=avW;h=w*1.414;
    if(h>avH){{h=avH;w=h/1.414;}}
    const fs=Math.floor(w/380*12)+'px';
    document.getElementById('pl').style.cssText='width:'+Math.floor(w)+'px;height:'+Math.floor(h)+'px;font-size:'+fs;
    document.getElementById('pr').style.cssText='width:'+Math.floor(w)+'px;height:'+Math.floor(h)+'px;font-size:'+fs;
  }}
}}

function renderPage(el,page,pgNum){{
  if(!page||page.type==='blank'){{el.innerHTML='<div style="width:100%;height:100%;background:#f8fafc"></div>';return;}}
  if(page.type==='cover-l'){{
    el.className='page left cover-l';
    el.innerHTML='<div class="cover-content"><div class="cov-ic">🐧</div><div class="cov-t">이것이<br><span>우분투 리눅스다</span></div><div class="cov-s">컴공 2학년을 위한 실전 우분투 가이드<br>설치부터 서버 운영, 자동화까지</div><div class="cov-b">18챕터 + 부록 &nbsp;|&nbsp; 실습 중심</div></div>';
    return;
  }}
  if(page.type==='cover-r'){{
    el.className='page right cover-r';
    el.innerHTML='<div class="cover-content"><div class="cov-toc"><strong>📚 목차</strong>{toc_str}</div></div>';
    return;
  }}
  const side=el.id==='pl'?'left':'right';
  el.className='page '+side;
  el.innerHTML='<div class="pg-hd"><em>CH'+page.num+'</em>'+page.title+'</div><div class="pg-bd">'+md2html(page.md)+'</div><div class="pg-ft"><span>이것이 우분투 리눅스다</span><span>'+pgNum+'</span></div>';
}}

function render(){{
  const li=cur*2,ri=cur*2+1;
  renderPage(document.getElementById('pl'),PAGES[li],li+1);
  renderPage(document.getElementById('pr'),PAGES[ri],ri+1);
}}

function ui(){{
  const disp=cur*2+1;
  document.getElementById('pn').textContent=disp;
  document.getElementById('pi').value=disp;
  ['pb','pb2'].forEach(id=>document.getElementById(id).disabled=cur===0);
  ['nb','nb2'].forEach(id=>document.getElementById(id).disabled=cur>=SPREADS-1);
  document.getElementById('bar').style.width=((cur+1)/SPREADS*100)+'%';
}}

function go(d){{
  if(busy)return;
  const n=cur+d;
  if(n<0||n>=SPREADS)return;
  busy=true;
  const book=document.getElementById('book');
  book.classList.add(d>0?'flip-next':'flip-prev');
  setTimeout(()=>{{cur=n;render();ui();book.classList.remove('flip-next','flip-prev');busy=false;}},250);
}}

function jumpTo(e){{
  const r=e.currentTarget.getBoundingClientRect();
  const ratio=(e.clientX-r.left)/r.width;
  cur=Math.floor(ratio*SPREADS);
  render();ui();
}}

function jumpPage(v){{
  const pg=parseInt(v);
  if(!isNaN(pg)&&pg>=1&&pg<=PAGES.length){{
    cur=Math.floor((pg-1)/2);render();ui();
  }}
}}

document.addEventListener('keydown',e=>{{
  if(e.key==='ArrowRight'||e.key==='ArrowDown')go(1);
  if(e.key==='ArrowLeft'||e.key==='ArrowUp')go(-1);
}});
let tx=0;
document.addEventListener('touchstart',e=>{{tx=e.touches[0].clientX;}},{{passive:true}});
document.addEventListener('touchend',e=>{{const d=tx-e.changedTouches[0].clientX;if(Math.abs(d)>40)go(d>0?1:-1);}},{{passive:true}});

window.addEventListener('resize',()=>{{resize();render();}});
resize();render();ui();
</script>
</body>
</html>'''

out_path = os.path.join(os.path.dirname(__file__), 'index.html')
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Generated index.html ({len(html):,} bytes)")
print(f"Chapters: {len(chapters)}")

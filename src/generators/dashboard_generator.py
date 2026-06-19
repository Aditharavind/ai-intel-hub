"""Static dashboard generator — 3D glassmorphism edition."""

from __future__ import annotations

import json
from datetime import datetime, timezone

from intel_hub.config import DATA_DIR, ROOT_DIR
from intel_hub.storage import read_json


def _dataset() -> dict[str, object]:
    return {
        "aiNews": read_json(DATA_DIR / "ai_news.json"),
        "physicalAiNews": read_json(DATA_DIR / "physical_ai_news.json"),
        "roboticsNews": read_json(DATA_DIR / "robotics_news.json"),
        "embeddedNews": read_json(DATA_DIR / "embedded_news.json"),
        "papers": read_json(DATA_DIR / "papers.json"),
        "repos": read_json(DATA_DIR / "github_repos.json"),
        "models": read_json(DATA_DIR / "huggingface_models.json"),
        "funding": read_json(DATA_DIR / "funding.json"),
        "companies": read_json(DATA_DIR / "companies.json"),
        "jobs": read_json(DATA_DIR / "jobs.json"),
    }


def generate_dashboard() -> None:
    data = json.dumps(_dataset(), ensure_ascii=False).replace("</", "<\\/")
    updated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    html = f"""<!doctype html>
<html lang="en" data-theme="dark">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Physical AI Intelligence Hub</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <style>
  /* ═══════════════ VARIABLES ═══════════════ */
  :root {{
    --bg:#06090f; --glass:rgba(12,17,28,.58); --glass2:rgba(10,15,24,.72);
    --glass3:rgba(8,12,20,.88); --gb:rgba(255,255,255,.055);
    --gb2:rgba(255,255,255,.09); --blur:blur(22px) saturate(1.6);
    --blur2:blur(28px) saturate(1.4);
    --text:#e8f0fa; --t2:#9ab5cc; --t3:#5a7d96; --muted:#304d62;
    --sb:rgba(4,7,14,.92); --sb-text:#7aa0be; --sb-muted:#2e4a60;
    --sb-hover:rgba(255,255,255,.04); --sb-active:rgba(124,58,237,.14);
    --sb-active-t:#c4b5fd;
    --acc:#818cf8; --acc2:#6366f1; --acc3:#7c3aed;
    --apale:rgba(129,140,248,.12); --apale2:rgba(129,140,248,.2);
    --sh:0 4px 24px rgba(0,0,0,.4),0 1px 3px rgba(0,0,0,.3);
    --sh-md:0 8px 40px rgba(0,0,0,.5),0 2px 6px rgba(0,0,0,.35);
    --sh-lg:0 16px 60px rgba(0,0,0,.6),0 4px 12px rgba(0,0,0,.4);
    --r:14px; --rsm:9px; --rxs:7px;
    --c-all:#818cf8; --c-aiNews:#38bdf8; --c-physicalAiNews:#a78bfa;
    --c-roboticsNews:#fbbf24; --c-embeddedNews:#22d3ee; --c-papers:#34d399; --c-repos:#60a5fa;
    --c-models:#fb923c; --c-funding:#a3e635; --c-companies:#f472b6; --c-jobs:#2dd4bf;
    --c-vla:#818cf8; --c-wam:#a78bfa; --c-robotPolicy:#2dd4bf;
    --c-rlPolicy:#fbbf24; --c-simulation:#60a5fa;
  }}
  [data-theme="light"] {{
    --bg:#f0f4f8; --glass:rgba(255,255,255,.92); --glass2:rgba(248,250,252,.96);
    --glass3:rgba(255,255,255,.98); --gb:rgba(0,0,0,.07); --gb2:rgba(0,0,0,.1);
    --blur:none; --blur2:none;
    --text:#0f172a; --t2:#334155; --t3:#64748b; --muted:#94a3b8;
    --sb:rgba(10,18,32,.96); --sb-text:#8ba5c4; --sb-muted:#2e4a60;
    --sh:0 1px 4px rgba(0,0,0,.07),0 2px 8px rgba(0,0,0,.05);
    --sh-md:0 4px 16px rgba(0,0,0,.1); --sh-lg:0 8px 32px rgba(0,0,0,.13);
    --acc:#6366f1; --acc2:#4f46e5; --acc3:#7c3aed;
    --apale:rgba(99,102,241,.08); --apale2:rgba(99,102,241,.16);
    --c-all:#6366f1; --c-aiNews:#0284c7; --c-physicalAiNews:#7c3aed;
    --c-roboticsNews:#d97706; --c-embeddedNews:#0891b2; --c-papers:#059669; --c-repos:#2563eb;
    --c-models:#ea580c; --c-funding:#65a30d; --c-companies:#db2777; --c-jobs:#0d9488;
    --c-vla:#6366f1; --c-wam:#7c3aed; --c-robotPolicy:#0d9488;
    --c-rlPolicy:#d97706; --c-simulation:#2563eb;
  }}

  /* ═══════════════ RESET ═══════════════ */
  *,*::before,*::after {{ box-sizing:border-box; margin:0; padding:0; }}
  html {{ scroll-behavior:smooth; }}
  body {{
    font-family:'Inter',ui-sans-serif,system-ui,sans-serif;
    background:var(--bg); color:var(--text); line-height:1.5; min-height:100vh;
    overflow-x:hidden;
  }}
  a {{ color:inherit; text-decoration:none; }}

  /* ═══════════════ BACKGROUND ═══════════════ */
  #bgCanvas {{
    position:fixed; inset:0; z-index:0; pointer-events:none;
    width:100%; height:100%; opacity:.55;
  }}
  [data-theme="light"] #bgCanvas {{ opacity:.1; }}

  .orb {{
    position:fixed; border-radius:50%;
    pointer-events:none; z-index:0;
    filter:blur(100px); opacity:.12;
    animation:floatOrb 22s ease-in-out infinite;
  }}
  .orb1 {{
    width:600px; height:600px; top:-180px; left:-150px;
    background:radial-gradient(circle,#7c3aed 0%,transparent 70%);
    animation-duration:22s;
  }}
  .orb2 {{
    width:500px; height:500px; bottom:-100px; right:-120px;
    background:radial-gradient(circle,#0ea5e9 0%,transparent 70%);
    animation-duration:28s; animation-direction:reverse;
  }}
  .orb3 {{
    width:360px; height:360px; top:45%; left:55%;
    background:radial-gradient(circle,#6366f1 0%,transparent 70%);
    animation-duration:18s; opacity:.07;
  }}
  [data-theme="light"] .orb {{ opacity:.03; }}

  @keyframes floatOrb {{
    0%,100% {{ transform:translate(0,0) scale(1); }}
    25%      {{ transform:translate(40px,-30px) scale(1.05); }}
    50%      {{ transform:translate(-25px,50px) scale(.96); }}
    75%      {{ transform:translate(30px,20px) scale(1.03); }}
  }}

  /* ═══════════════ LAYOUT ═══════════════ */
  .layout {{
    display:grid; grid-template-columns:268px minmax(0,1fr);
    min-height:100vh; position:relative; z-index:2;
  }}

  /* ═══════════════ SIDEBAR ═══════════════ */
  .sidebar {{
    background:var(--sb); backdrop-filter:var(--blur2);
    -webkit-backdrop-filter:var(--blur2);
    position:sticky; top:0; height:100vh;
    display:flex; flex-direction:column; overflow:hidden;
    border-right:1px solid var(--gb2);
    box-shadow:4px 0 40px rgba(0,0,0,.4);
    z-index:20;
  }}
  .brand {{
    padding:22px 18px 16px; flex-shrink:0;
    background:linear-gradient(180deg,rgba(124,58,237,.18) 0%,transparent 100%);
    border-bottom:1px solid rgba(124,58,237,.2);
  }}
  .brand-row {{ display:flex; align-items:center; gap:12px; }}
  .brand-logo {{
    width:44px; height:44px; border-radius:12px; flex-shrink:0;
    background:linear-gradient(135deg,#7c3aed 0%,#4f46e5 100%);
    display:flex; align-items:center; justify-content:center; font-size:22px;
    box-shadow:0 0 24px rgba(124,58,237,.55),0 4px 14px rgba(0,0,0,.4);
  }}
  .brand-name {{ font-size:14.5px; font-weight:800; color:#f0f6fc; letter-spacing:-.015em; }}
  .brand-sub  {{ font-size:11px; color:var(--sb-text); margin-top:2px; }}

  .nav-scroll {{ flex:1; overflow-y:auto; padding:8px 8px; }}
  .nav-scroll::-webkit-scrollbar {{ width:0; }}
  .nav-sec {{
    font-size:9.5px; font-weight:700; letter-spacing:.09em; text-transform:uppercase;
    color:var(--sb-muted); padding:10px 10px 3px;
  }}
  .nav-btn {{
    display:flex; align-items:center; gap:9px; width:100%;
    border:none; background:transparent; color:var(--sb-text);
    font:inherit; font-size:13.5px; font-weight:500;
    padding:8px 10px; border-radius:9px; cursor:pointer;
    text-align:left; transition:all .15s; margin-bottom:2px;
    position:relative;
  }}
  .nav-btn::before {{
    content:''; position:absolute; left:0; top:50%;
    transform:translateY(-50%) scaleY(0);
    width:3px; height:65%; border-radius:0 3px 3px 0;
    background:var(--acc); transition:transform .2s cubic-bezier(.34,1.56,.64,1);
  }}
  .nav-btn:hover {{ background:var(--sb-hover); color:#d0e4f4; }}
  .nav-btn.active {{
    background:var(--sb-active); color:var(--sb-active-t); font-weight:600;
    box-shadow:inset 0 0 0 1px rgba(129,140,248,.15);
    text-shadow:0 0 20px rgba(196,181,253,.4);
  }}
  .nav-btn.active::before {{ transform:translateY(-50%) scaleY(1); }}
  .nav-ico {{ font-size:15px; width:20px; text-align:center; flex-shrink:0; }}
  .nav-lbl {{ flex:1; }}
  .nav-cnt {{
    font-size:10.5px; font-weight:700; padding:1px 7px;
    border-radius:999px; background:rgba(255,255,255,.05); color:var(--sb-muted);
  }}
  .nav-btn.active .nav-cnt {{
    background:rgba(129,140,248,.18); color:var(--sb-active-t);
  }}

  .sb-foot {{
    padding:12px 18px 14px; border-top:1px solid var(--gb);
    font-size:11px; color:var(--sb-muted); flex-shrink:0;
    display:flex; flex-direction:column; gap:3px;
  }}
  .sb-foot strong {{ color:var(--t3); font-weight:600; }}
  .sb-about {{
    margin-top:12px; padding-top:10px; border-top:1px solid var(--gb);
    display:flex; flex-direction:column; gap:2px;
  }}
  .sb-about-lbl {{
    font-size:9px; font-weight:700; letter-spacing:.12em; text-transform:uppercase;
    color:var(--sb-muted); margin-bottom:2px;
  }}
  .sb-about-by {{ font-size:11px; color:var(--sb-text); }}
  .sb-about-by strong {{ color:var(--acc); font-weight:700; }}
  .sb-about-mail {{ font-size:10.5px; color:var(--sb-muted); text-decoration:none; word-break:break-all; }}
  .sb-about-mail:hover {{ color:var(--acc); text-decoration:underline; }}
  .refresh-bar {{
    margin-top:8px; height:2px; border-radius:1px;
    background:rgba(255,255,255,.06); overflow:hidden;
  }}
  .refresh-prog {{
    height:100%; border-radius:1px;
    background:linear-gradient(90deg,var(--acc3),var(--acc));
    transition:width .5s ease;
  }}

  /* ═══════════════ MAIN ═══════════════ */
  .main {{ min-width:0; display:flex; flex-direction:column; }}

  /* ═══════════════ TOPBAR ═══════════════ */
  .topbar {{
    background:var(--glass2); backdrop-filter:var(--blur);
    -webkit-backdrop-filter:var(--blur);
    border-bottom:1px solid var(--gb);
    padding:0 28px; height:64px;
    display:flex; align-items:center; justify-content:space-between; gap:14px;
    position:sticky; top:0; z-index:25;
    box-shadow:0 2px 20px rgba(0,0,0,.3);
  }}
  .topbar::after {{
    content:''; position:absolute; bottom:0; left:0; right:0; height:1px;
    background:linear-gradient(90deg,#7c3aed,#6366f1 35%,#0ea5e9 70%,transparent);
    opacity:.8;
  }}
  .topbar-l {{ display:flex; align-items:center; gap:13px; min-width:0; }}
  .pg-title {{
    font-size:18px; font-weight:900; letter-spacing:-.025em;
    white-space:nowrap; overflow:hidden; text-overflow:ellipsis;
    background:linear-gradient(135deg,var(--text),var(--acc));
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    background-clip:text;
  }}
  [data-theme="light"] .pg-title {{
    background:linear-gradient(135deg,#0f172a,#6366f1);
    -webkit-background-clip:text; background-clip:text;
  }}
  .upd-badge {{
    font-size:11px; color:var(--muted); background:var(--glass);
    border:1px solid var(--gb); border-radius:999px;
    padding:3px 10px; flex-shrink:0; white-space:nowrap;
  }}
  .topbar-r {{ display:flex; align-items:center; gap:7px; flex-shrink:0; }}
  .btn {{
    display:inline-flex; align-items:center; gap:5px;
    height:36px; padding:0 14px;
    border:1px solid var(--gb2); border-radius:var(--rsm);
    background:var(--glass); backdrop-filter:var(--blur);
    color:var(--t2); font:inherit; font-size:13px; font-weight:600;
    cursor:pointer; text-decoration:none; transition:all .15s; white-space:nowrap;
  }}
  .btn:hover {{ background:var(--glass2); border-color:var(--acc); color:var(--text); box-shadow:0 0 12px rgba(129,140,248,.15); }}
  .btn-acc {{
    background:linear-gradient(135deg,var(--acc3),var(--acc2));
    border-color:transparent; color:#fff;
    box-shadow:0 2px 12px rgba(124,58,237,.4),0 0 0 1px rgba(129,140,248,.2);
  }}
  .btn-acc:hover {{
    background:linear-gradient(135deg,#6d28d9,var(--acc3));
    box-shadow:0 4px 20px rgba(124,58,237,.5); color:#fff;
    border-color:transparent;
  }}
  .ico-btn {{ width:36px; padding:0; justify-content:center; font-size:16px; }}

  /* ═══════════════ CONTENT ═══════════════ */
  .content {{ padding:22px 28px 52px; flex:1; }}

  /* ═══════════════ STATS ═══════════════ */
  .stats {{
    display:grid; grid-template-columns:repeat(4,minmax(0,1fr));
    gap:12px; margin-bottom:20px;
  }}
  .stat {{
    background:var(--glass); backdrop-filter:var(--blur);
    -webkit-backdrop-filter:var(--blur);
    border:1px solid var(--gb); border-radius:var(--r);
    padding:18px 20px 15px; position:relative; overflow:hidden;
    box-shadow:var(--sh);
    transition:transform .3s ease,box-shadow .3s ease;
    cursor:default; transform-style:preserve-3d;
  }}
  .stat::before {{
    content:''; position:absolute; top:0; left:0; right:0;
    height:2px; background:var(--sc,var(--acc));
    box-shadow:0 0 12px var(--sc,var(--acc));
  }}
  .stat::after {{
    content:''; position:absolute; inset:0;
    background:radial-gradient(ellipse at top left, rgba(var(--sc-rgb,129,140,248),.06), transparent 60%);
    pointer-events:none;
  }}
  .stat-ico {{ font-size:24px; line-height:1; margin-bottom:10px; display:block;
               filter:drop-shadow(0 0 8px rgba(255,255,255,.2)); }}
  .stat-lbl {{
    font-size:10.5px; font-weight:700; letter-spacing:.06em;
    text-transform:uppercase; color:var(--t3);
  }}
  .stat-num {{
    font-size:28px; font-weight:900; letter-spacing:-.04em;
    color:var(--text); line-height:1; margin-top:5px;
  }}

  /* ═══════════════ PANEL ═══════════════ */
  .panel {{
    background:var(--glass); backdrop-filter:var(--blur);
    -webkit-backdrop-filter:var(--blur);
    border:1px solid var(--gb); border-radius:var(--r);
    box-shadow:var(--sh); overflow:hidden;
  }}

  /* ═══════════════ TOOLBAR ═══════════════ */
  .toolbar {{
    display:flex; align-items:center; gap:8px; flex-wrap:wrap;
    padding:12px 14px; border-bottom:1px solid var(--gb);
    background:var(--glass2);
  }}
  .srch-wrap {{ position:relative; flex:1; min-width:200px; }}
  .srch-ico {{
    position:absolute; left:12px; top:50%; transform:translateY(-50%);
    font-size:13px; color:var(--muted); pointer-events:none;
  }}
  .srch-inp {{
    width:100%; height:38px;
    border:1px solid var(--gb2); border-radius:var(--rsm);
    padding:0 12px 0 34px; background:var(--glass);
    backdrop-filter:var(--blur); color:var(--text);
    font:inherit; font-size:13.5px;
    transition:border-color .15s,box-shadow .15s;
  }}
  .srch-inp::placeholder {{ color:var(--muted); }}
  .srch-inp:focus {{
    outline:none; border-color:var(--acc);
    box-shadow:0 0 0 3px rgba(129,140,248,.15),0 0 12px rgba(129,140,248,.1);
  }}
  .ctrl {{
    height:38px; border:1px solid var(--gb2); border-radius:var(--rsm);
    padding:0 10px; background:var(--glass);
    backdrop-filter:var(--blur); color:var(--text);
    font:inherit; font-size:13px; cursor:pointer; flex-shrink:0;
    transition:border-color .15s;
  }}
  .ctrl:focus {{ outline:none; border-color:var(--acc); }}
  .vt {{ display:flex; border:1px solid var(--gb2); border-radius:var(--rsm); overflow:hidden; flex-shrink:0; }}
  .vt-b {{
    width:36px; height:38px; border:none;
    background:var(--glass); color:var(--muted); font-size:15px;
    cursor:pointer; display:flex; align-items:center; justify-content:center;
    transition:all .13s;
  }}
  .vt-b:not(:last-child) {{ border-right:1px solid var(--gb2); }}
  .vt-b.on {{ background:var(--acc3); color:#fff; box-shadow:inset 0 0 10px rgba(0,0,0,.2); }}

  /* ═══════════════ RESULTS BAR ═══════════════ */
  .res-bar {{
    display:flex; align-items:center; justify-content:space-between;
    padding:9px 16px; font-size:12.5px; color:var(--muted);
    border-bottom:1px solid var(--gb); background:var(--glass2);
  }}
  .res-n {{ font-weight:700; color:var(--t2); }}

  /* ═══════════════ FEED — GRID ═══════════════ */
  .feed.grid-v {{
    display:grid;
    grid-template-columns:repeat(auto-fill,minmax(300px,1fr));
    gap:14px; padding:16px;
  }}
  .feed.grid-v .fi {{
    background:var(--glass); backdrop-filter:var(--blur);
    -webkit-backdrop-filter:var(--blur);
    border:1px solid var(--gb); border-top:2px solid var(--ic,var(--acc));
    border-radius:var(--r); padding:18px;
    box-shadow:var(--sh); cursor:pointer;
    transform-style:preserve-3d; will-change:transform;
    transition:transform .3s ease,box-shadow .3s ease;
    position:relative; overflow:hidden;
  }}
  .feed.grid-v .fi::before {{
    content:''; position:absolute; top:0; left:0; right:0; height:80px;
    background:linear-gradient(180deg,rgba(var(--ic-r,129,140,248),.06) 0%,transparent 100%);
    pointer-events:none;
  }}
  .feed.grid-v .fi-stripe {{ display:none; }}
  .feed.grid-v .fi-body {{ display:flex; flex-direction:column; height:100%; }}
  .feed.grid-v .fi-hdr {{ margin-bottom:10px; display:flex; align-items:flex-start; justify-content:space-between; gap:8px; }}

  /* ═══════════════ FEED — LIST ═══════════════ */
  .feed.list-v .fi {{
    padding:16px 20px; border-bottom:1px solid var(--gb);
    transition:background .12s; position:relative;
  }}
  .feed.list-v .fi:last-child {{ border-bottom:none; }}
  .feed.list-v .fi:hover {{ background:var(--glass2); }}
  .feed.list-v .fi-wrap {{ display:flex; gap:14px; align-items:flex-start; }}
  .feed.list-v .fi-stripe {{
    width:3px; border-radius:3px; flex-shrink:0;
    align-self:stretch; min-height:40px;
    background:var(--ic,var(--acc));
    box-shadow:0 0 8px var(--ic,var(--acc));
    transition:width .15s;
  }}
  .feed.list-v .fi:hover .fi-stripe {{ width:4px; }}
  .feed.list-v .fi-body {{ flex:1; min-width:0; }}
  .feed.list-v .fi-hdr {{
    display:flex; align-items:flex-start;
    justify-content:space-between; gap:10px;
  }}

  /* ═══════════════ ITEM SHARED ═══════════════ */
  .i-cat {{
    display:inline-flex; align-items:center; gap:5px;
    font-size:10.5px; font-weight:700; padding:3px 9px;
    border-radius:999px; color:#fff; margin-bottom:8px;
    letter-spacing:.02em;
    box-shadow:0 2px 8px rgba(0,0,0,.3);
  }}
  .star-btn {{
    flex-shrink:0; background:none; border:none; cursor:pointer;
    font-size:17px; line-height:1; padding:2px 3px; border-radius:6px;
    color:var(--t3); transition:transform .12s, color .12s; margin-top:-2px;
  }}
  .star-btn:hover {{ color:#fbbf24; transform:scale(1.18); }}
  .star-btn.on {{ color:#fbbf24; }}
  .i-title {{
    font-size:14.5px; font-weight:700; line-height:1.42;
    color:var(--text); display:block; transition:color .13s;
  }}
  .i-title:hover {{ color:var(--acc); }}
  .i-score {{ flex-shrink:0; text-align:right; padding-top:2px; }}
  .sc-val {{
    font-size:19px; font-weight:900; letter-spacing:-.03em;
    color:var(--acc); line-height:1; display:block;
    text-shadow:0 0 20px rgba(129,140,248,.4);
  }}
  .sc-lbl {{ font-size:10px; color:var(--muted); margin-top:2px; white-space:nowrap; }}
  .i-authors {{
    display:flex; flex-wrap:wrap; gap:4px;
    margin:6px 0 8px;
  }}
  .au {{ font-size:11px; padding:2px 7px; border-radius:5px;
          background:rgba(255,255,255,.05); border:1px solid var(--gb2);
          color:var(--t3); font-weight:500; }}
  [data-theme="light"] .au {{ background:var(--glass2); }}
  .i-sum {{
    font-size:13px; color:var(--t2); line-height:1.65;
    margin:6px 0 10px;
  }}
  .i-tags {{
    display:flex; flex-wrap:wrap; gap:5px; align-items:center;
    margin-top:auto; padding-top:10px;
  }}
  .tag {{
    display:inline-flex; align-items:center; font-size:11px; font-weight:600;
    padding:2px 9px; border-radius:999px; white-space:nowrap;
  }}
  .t-d,.t-s {{
    background:rgba(255,255,255,.05); border:1px solid var(--gb2); color:var(--t3);
  }}
  [data-theme="light"] .t-d,[data-theme="light"] .t-s {{
    background:var(--glass2); border-color:rgba(0,0,0,.09);
  }}
  .i-acts {{ display:flex; gap:6px; margin-top:10px; flex-wrap:wrap; }}
  .act {{
    display:inline-flex; align-items:center; gap:4px;
    font-size:12px; font-weight:600; padding:5px 12px;
    border-radius:var(--rxs); border:1px solid var(--gb2);
    background:rgba(255,255,255,.04); color:var(--t2);
    text-decoration:none; cursor:pointer; transition:all .13s;
    backdrop-filter:var(--blur);
  }}
  .act:hover {{ background:var(--glass2); color:var(--text); border-color:var(--muted); }}
  .act-p {{
    background:var(--apale); border-color:rgba(129,140,248,.25); color:var(--acc);
  }}
  .act-p:hover {{
    background:var(--acc2); border-color:var(--acc2); color:#fff;
    box-shadow:0 2px 12px rgba(99,102,241,.4);
  }}

  /* ═══════════════ ENTRY ANIMATIONS ═══════════════ */
  @keyframes cardIn {{
    from {{ opacity:0; transform:translateY(10px); }}
    to   {{ opacity:1; transform:translateY(0); }}
  }}
  .fi {{ animation:cardIn .3s ease both; }}
  .feed.grid-v .fi {{ transition:transform .2s ease, box-shadow .2s ease, border-color .2s ease; }}
  .feed.grid-v .fi:hover {{ transform:translateY(-4px); box-shadow:var(--sh-md); border-color:var(--gb2); }}
  .stat {{ transition:transform .2s ease, box-shadow .2s ease; }}
  .stat:hover {{ transform:translateY(-3px); box-shadow:var(--sh-md); }}
  @media (prefers-reduced-motion:reduce) {{
    .fi,.orb {{ animation:none; }}
    * {{ scroll-behavior:auto; }}
  }}
  .fi:nth-child(2)  {{ animation-delay:35ms; }}
  .fi:nth-child(3)  {{ animation-delay:65ms; }}
  .fi:nth-child(4)  {{ animation-delay:90ms; }}
  .fi:nth-child(5)  {{ animation-delay:112ms; }}
  .fi:nth-child(6)  {{ animation-delay:130ms; }}
  .fi:nth-child(7)  {{ animation-delay:146ms; }}
  .fi:nth-child(8)  {{ animation-delay:160ms; }}
  .fi:nth-child(n+9) {{ animation-delay:172ms; }}

  /* ═══════════════ EMPTY ═══════════════ */
  .empty {{
    min-height:300px; display:flex; flex-direction:column;
    align-items:center; justify-content:center;
    gap:14px; color:var(--muted); text-align:center; padding:40px 24px;
  }}
  .empty-ico {{ font-size:56px; filter:drop-shadow(0 0 20px rgba(129,140,248,.3)); }}
  .empty h3  {{ font-size:16px; font-weight:700; color:var(--t2); }}
  .empty p   {{ font-size:13.5px; max-width:280px; color:var(--muted); }}

  /* ═══════════════ PAGINATION ═══════════════ */
  .pager {{
    display:flex; align-items:center; justify-content:space-between;
    gap:12px; padding:12px 16px;
    border-top:1px solid var(--gb); background:var(--glass2); flex-wrap:wrap;
  }}
  .pg-inf {{ font-size:12.5px; color:var(--muted); }}
  .pg-btns {{ display:flex; gap:4px; flex-wrap:wrap; }}
  .pgb {{
    min-width:34px; height:34px; border:1px solid var(--gb2); border-radius:var(--rxs);
    background:var(--glass); backdrop-filter:var(--blur); color:var(--t2);
    font:inherit; font-size:13px; font-weight:600;
    cursor:pointer; display:inline-flex; align-items:center;
    justify-content:center; padding:0 8px; transition:all .13s;
  }}
  .pgb:hover:not(:disabled) {{
    background:var(--glass2); border-color:var(--acc); color:var(--acc);
    box-shadow:0 0 10px rgba(129,140,248,.15);
  }}
  .pgb.on {{
    background:linear-gradient(135deg,var(--acc3),var(--acc2));
    border-color:transparent; color:#fff;
    box-shadow:0 2px 10px rgba(124,58,237,.4);
  }}
  .pgb:disabled {{ opacity:.25; cursor:not-allowed; }}

  /* ═══════════════ LIGHT-MODE OVERRIDES ═══════════════ */
  [data-theme="light"] body {{
    background:#f0f4f8;
    background-image:radial-gradient(circle,rgba(99,102,241,.04) 1px,transparent 1px);
    background-size:28px 28px;
  }}
  [data-theme="light"] .sidebar {{ background:rgba(10,18,32,.97); backdrop-filter:none; }}
  [data-theme="light"] .topbar  {{ background:rgba(255,255,255,.96); backdrop-filter:none; }}
  [data-theme="light"] .panel   {{ background:#fff; backdrop-filter:none; border-color:#e2e8f0; }}
  [data-theme="light"] .stat    {{ background:#fff; backdrop-filter:none; border-color:#e2e8f0; }}
  [data-theme="light"] .feed.grid-v .fi {{ background:#fff; backdrop-filter:none; border-color:#e2e8f0; }}
  [data-theme="light"] .feed.list-v .fi {{ background:#fff; }}
  [data-theme="light"] .toolbar  {{ background:#f8fafc; }}
  [data-theme="light"] .srch-inp {{ background:#fff; border-color:#e2e8f0; }}
  [data-theme="light"] .ctrl     {{ background:#fff; border-color:#e2e8f0; }}
  [data-theme="light"] .vt       {{ border-color:#e2e8f0; }}
  [data-theme="light"] .vt-b     {{ background:#fff; }}
  [data-theme="light"] .btn      {{ background:#fff; border-color:#e2e8f0; }}
  [data-theme="light"] .pgb      {{ background:#fff; border-color:#e2e8f0; }}
  [data-theme="light"] .pager    {{ background:#f8fafc; }}
  [data-theme="light"] .res-bar  {{ background:#f8fafc; }}
  [data-theme="light"] .act      {{ background:#f8fafc; border-color:#e2e8f0; }}
  [data-theme="light"] .i-cat    {{ box-shadow:0 2px 6px rgba(0,0,0,.15); }}
  [data-theme="light"] .feed.grid-v .fi::before {{ display:none; }}
  [data-theme="light"] .sc-val   {{ text-shadow:none; }}

  /* ═══════════════ RESPONSIVE ═══════════════ */
  @media (max-width:1100px) {{ .stats {{ grid-template-columns:repeat(2,1fr); }} }}
  @media (max-width:870px) {{
    .layout {{ grid-template-columns:1fr; }}
    .sidebar {{
      position:sticky; top:0; height:auto; z-index:30;
      flex-direction:column; border-right:none;
      border-bottom:1px solid var(--gb2); box-shadow:0 2px 20px rgba(0,0,0,.35);
    }}
    .brand {{ padding:12px 16px; border-bottom:none; }}
    .brand-sub {{ display:none; }}
    .nav-scroll {{
      flex:none; display:flex; gap:6px; padding:0 12px 12px;
      overflow-x:auto; overflow-y:hidden;
    }}
    .nav-scroll::-webkit-scrollbar {{ height:0; }}
    .nav-sec {{ display:none; }}
    #navMain, #navTopics, #navAdv {{ display:flex; gap:6px; }}
    .nav-btn {{
      width:auto; white-space:nowrap; margin-bottom:0;
      padding:7px 13px; border:1px solid var(--gb2); border-radius:999px;
    }}
    .nav-btn::before {{ display:none; }}
    .nav-btn.active {{ box-shadow:none; }}
    .sb-foot {{ display:none; }}
    .content {{ padding:16px 16px 40px; }}
    .topbar {{ padding:0 16px; height:56px; }}
  }}
  @media (max-width:560px) {{
    .stats {{ grid-template-columns:1fr 1fr; gap:10px; }}
    .toolbar {{ flex-wrap:wrap; }}
    .srch-wrap {{ order:-1; flex-basis:100%; }}
    .feed.grid-v {{ grid-template-columns:1fr; padding:12px; }}
    .topbar {{ height:auto; padding:12px 14px; flex-wrap:wrap; gap:8px; }}
    .upd-badge {{ display:none; }}
    .pg-title {{ font-size:16px; }}
    .stat {{ padding:14px 16px 12px; }}
    .stat-num {{ font-size:24px; }}
  }}
  /* ═══════════════ ADVANCED ═══════════════ */
  .adv-wrap {{ padding:0 0 52px; }}
  .adv-back {{
    display:inline-flex; align-items:center; gap:7px;
    border:none; background:transparent; color:var(--t2);
    font:inherit; font-size:13px; font-weight:600; cursor:pointer;
    padding:8px 0 16px; transition:color .13s;
  }}
  .adv-back:hover {{ color:var(--acc); }}
  .adv-mod-hdr {{
    display:flex; align-items:center; gap:14px;
    margin-bottom:20px; flex-wrap:wrap;
  }}
  .adv-mod-ico {{
    width:52px; height:52px; border-radius:14px; flex-shrink:0;
    display:flex; align-items:center; justify-content:center; font-size:24px;
    background:linear-gradient(135deg,var(--acc3),var(--acc2));
    box-shadow:0 0 24px rgba(124,58,237,.4);
  }}
  .adv-mod-title {{ font-size:22px; font-weight:900; letter-spacing:-.03em; }}
  .adv-mod-sub   {{ font-size:13px; color:var(--t3); margin-top:3px; }}
  .adv-metrics {{
    display:grid; grid-template-columns:repeat(4,minmax(0,1fr));
    gap:10px; margin-bottom:18px;
  }}
  .adv-metric {{
    background:var(--glass); backdrop-filter:var(--blur);
    border:1px solid var(--gb); border-radius:var(--r);
    padding:14px 16px; text-align:center;
  }}
  .adv-metric-n  {{ font-size:26px; font-weight:900; color:var(--acc); letter-spacing:-.04em; }}
  .adv-metric-l  {{ font-size:11px; color:var(--t3); font-weight:700; text-transform:uppercase; letter-spacing:.05em; margin-top:4px; }}
  .adv-hub {{
    display:grid; grid-template-columns:repeat(auto-fill,minmax(260px,1fr));
    gap:13px;
  }}
  .adv-hcard {{
    background:var(--glass); backdrop-filter:var(--blur);
    border:1px solid var(--gb); border-radius:var(--r);
    padding:20px 18px; cursor:pointer;
    transition:transform .25s ease, box-shadow .25s ease, border-color .2s;
    position:relative; overflow:hidden;
    transform-style:preserve-3d;
  }}
  .adv-hcard:hover {{
    border-color:var(--acc); box-shadow:0 8px 32px rgba(124,58,237,.2);
    transform:translateY(-3px);
  }}
  .adv-hcard::before {{
    content:''; position:absolute; top:0; left:0; right:0; height:2px;
    background:var(--hc,var(--acc));
    box-shadow:0 0 10px var(--hc,var(--acc));
  }}
  .adv-hcard-ico {{ font-size:28px; line-height:1; margin-bottom:10px; }}
  .adv-hcard-title {{ font-size:15px; font-weight:800; margin-bottom:5px; }}
  .adv-hcard-desc  {{ font-size:12.5px; color:var(--t3); line-height:1.55; margin-bottom:10px; }}
  .adv-hcard-stat  {{
    font-size:11px; font-weight:700; padding:3px 9px;
    border-radius:999px; background:var(--apale); color:var(--acc);
    display:inline-block;
  }}
  .adv-panel {{
    background:var(--glass); backdrop-filter:var(--blur);
    border:1px solid var(--gb); border-radius:var(--r);
    overflow:hidden; margin-bottom:14px;
  }}
  .adv-panel-hdr {{
    padding:13px 18px; border-bottom:1px solid var(--gb);
    font-size:13px; font-weight:700; color:var(--t2);
    background:var(--glass2); display:flex; align-items:center; gap:8px;
  }}
  .adv-list {{ list-style:none; }}
  .adv-item {{
    padding:14px 18px; border-bottom:1px solid var(--gb);
    display:flex; align-items:flex-start; gap:14px;
  }}
  .adv-item:last-child {{ border-bottom:none; }}
  .adv-rank {{
    width:28px; height:28px; border-radius:8px; flex-shrink:0;
    background:var(--apale); color:var(--acc);
    display:flex; align-items:center; justify-content:center;
    font-size:12px; font-weight:800;
  }}
  .adv-item-body {{ flex:1; min-width:0; }}
  .adv-item-title {{ font-size:14px; font-weight:700; margin-bottom:4px; }}
  .adv-item-sub   {{ font-size:12.5px; color:var(--t3); line-height:1.5; margin-bottom:8px; }}
  .adv-bar-row {{ display:flex; align-items:center; gap:8px; margin-bottom:5px; }}
  .adv-bar-lbl {{ font-size:10.5px; color:var(--muted); width:90px; flex-shrink:0; font-weight:600; }}
  .adv-bar {{ flex:1; height:6px; background:var(--gb2); border-radius:3px; overflow:hidden; }}
  .adv-bar-fill {{ height:100%; border-radius:3px; transition:width .8s cubic-bezier(.22,1,.36,1); }}
  .adv-scores {{
    display:flex; flex-wrap:wrap; gap:6px; margin-top:8px;
  }}
  .adv-score-badge {{
    font-size:11px; font-weight:700; padding:3px 9px;
    border-radius:6px; background:rgba(255,255,255,.05);
    border:1px solid var(--gb2); color:var(--t2);
  }}
  .adv-form {{ padding:18px; }}
  .adv-form-row {{ margin-bottom:12px; }}
  .adv-label {{ font-size:12px; font-weight:700; color:var(--t2); margin-bottom:5px; display:block; text-transform:uppercase; letter-spacing:.06em; }}
  .adv-inp {{
    width:100%; border:1px solid var(--gb2); border-radius:var(--rsm);
    padding:10px 14px; background:var(--glass2); color:var(--text);
    font:inherit; font-size:14px; transition:border-color .15s;
  }}
  .adv-inp:focus {{ outline:none; border-color:var(--acc); box-shadow:0 0 0 3px rgba(129,140,248,.12); }}
  .adv-inp-sm {{ height:38px; padding:0 12px; }}
  .adv-btn {{
    height:40px; padding:0 20px; border-radius:var(--rsm); border:none; cursor:pointer;
    background:linear-gradient(135deg,var(--acc3),var(--acc2)); color:#fff;
    font:inherit; font-size:13.5px; font-weight:700;
    box-shadow:0 2px 12px rgba(124,58,237,.4);
    transition:opacity .15s, transform .15s;
  }}
  .adv-btn:hover {{ opacity:.9; transform:translateY(-1px); }}
  .adv-result {{
    background:var(--glass2); border:1px solid var(--gb2); border-radius:var(--rsm);
    padding:16px; margin-top:16px; display:none;
  }}
  .adv-result.show {{ display:block; animation:card3dIn .3s ease; }}
  .adv-grid2 {{ display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-top:12px; }}
  .adv-kv {{ background:var(--glass); border:1px solid var(--gb); border-radius:var(--rsm); padding:12px 14px; }}
  .adv-kv-k {{ font-size:10.5px; color:var(--muted); font-weight:700; text-transform:uppercase; letter-spacing:.06em; }}
  .adv-kv-v {{ font-size:17px; font-weight:800; color:var(--acc); margin-top:3px; }}
  .adv-chat {{ display:flex; flex-direction:column; gap:0; }}
  .adv-chat-msgs {{
    min-height:220px; max-height:380px; overflow-y:auto;
    padding:16px; display:flex; flex-direction:column; gap:10px;
  }}
  .adv-msg {{ max-width:82%; padding:10px 14px; border-radius:12px; font-size:13.5px; line-height:1.6; }}
  .adv-msg.user {{ align-self:flex-end; background:var(--acc3); color:#fff; border-radius:12px 12px 2px 12px; }}
  .adv-msg.bot  {{ align-self:flex-start; background:var(--glass2); border:1px solid var(--gb2); border-radius:12px 12px 12px 2px; }}
  .adv-chat-inp {{ display:flex; gap:8px; padding:10px 16px; border-top:1px solid var(--gb); }}
  .adv-chat-inp .adv-inp {{ flex:1; height:40px; padding:0 12px; font-size:13.5px; }}
  .adv-tag {{ display:inline-flex; align-items:center; font-size:11px; font-weight:700;
              padding:2px 8px; border-radius:5px; margin:2px; }}
  .adv-tag-green {{ background:rgba(52,211,153,.12); border:1px solid rgba(52,211,153,.25); color:#34d399; }}
  .adv-tag-red   {{ background:rgba(248,113,113,.12); border:1px solid rgba(248,113,113,.25); color:#f87171; }}
  .adv-tag-blue  {{ background:rgba(96,165,250,.12); border:1px solid rgba(96,165,250,.25); color:#60a5fa; }}
  .adv-tag-gold  {{ background:rgba(251,191,36,.12); border:1px solid rgba(251,191,36,.25); color:#fbbf24; }}
  .adv-divider   {{ border:none; border-top:1px solid var(--gb); margin:16px 0; }}
  .adv-hero {{
    background:linear-gradient(135deg,rgba(124,58,237,.18) 0%,rgba(99,102,241,.08) 100%);
    border:1px solid rgba(124,58,237,.25); border-radius:var(--r);
    padding:24px; margin-bottom:16px; text-align:center;
  }}
  .adv-hero-title {{ font-size:28px; font-weight:900; letter-spacing:-.04em; margin-bottom:6px;
    background:linear-gradient(135deg,var(--acc),#c084fc); -webkit-background-clip:text;
    -webkit-text-fill-color:transparent; background-clip:text; }}
  .adv-hero-sub {{ font-size:14px; color:var(--t2); }}
  .adv-brief-section {{ margin-bottom:20px; }}
  .adv-brief-label {{
    font-size:10.5px; font-weight:700; letter-spacing:.08em; text-transform:uppercase;
    color:var(--acc); margin-bottom:8px; display:flex; align-items:center; gap:6px;
  }}
  .adv-brief-label::after {{ content:''; flex:1; height:1px; background:var(--gb2); }}
  .adv-table {{ width:100%; border-collapse:collapse; font-size:13px; }}
  .adv-table th {{ padding:9px 12px; text-align:left; font-size:10.5px; font-weight:700;
    letter-spacing:.06em; text-transform:uppercase; color:var(--muted);
    border-bottom:1px solid var(--gb2); background:var(--glass2); }}
  .adv-table td {{ padding:10px 12px; border-bottom:1px solid var(--gb); vertical-align:middle; }}
  .adv-table tr:last-child td {{ border-bottom:none; }}
  .adv-table tr:hover td {{ background:rgba(255,255,255,.02); }}
  .adv-skill-grid {{
    display:grid; grid-template-columns:repeat(auto-fill,minmax(140px,1fr));
    gap:8px; margin-bottom:12px;
  }}
  .adv-skill-check {{
    display:flex; align-items:center; gap:8px; padding:8px 12px;
    border:1px solid var(--gb2); border-radius:var(--rsm);
    cursor:pointer; font-size:13px; background:var(--glass);
    transition:all .13s;
  }}
  .adv-skill-check:hover {{ border-color:var(--acc); background:var(--apale); }}
  .adv-skill-check input {{ accent-color:var(--acc); width:14px; height:14px; }}
  [data-theme="light"] .adv-panel {{ background:#fff; border-color:#e2e8f0; }}
  [data-theme="light"] .adv-hcard {{ background:#fff; border-color:#e2e8f0; }}
  [data-theme="light"] .adv-metric {{ background:#fff; border-color:#e2e8f0; }}
  [data-theme="light"] .adv-kv {{ background:#f8fafc; border-color:#e2e8f0; }}
  [data-theme="light"] .adv-inp {{ background:#fff; border-color:#e2e8f0; }}
  @media (max-width:900px) {{ .adv-metrics {{ grid-template-columns:1fr 1fr; }} }}
  @media (max-width:560px) {{
    .adv-hub {{ grid-template-columns:1fr; }}
    .adv-metrics {{ grid-template-columns:1fr 1fr; }}
    .adv-grid2 {{ grid-template-columns:1fr; }}
  }}
  </style>
</head>
<body>

<canvas id="bgCanvas"></canvas>
<div class="orb orb1"></div>
<div class="orb orb2"></div>
<div class="orb orb3"></div>

<div class="layout">

  <!-- ── Sidebar ── -->
  <aside class="sidebar">
    <div class="brand">
      <div class="brand-row">
        <div class="brand-logo">🤖</div>
        <div>
          <div class="brand-name">Physical AI Hub</div>
          <div class="brand-sub">Intelligence Dashboard</div>
        </div>
      </div>
    </div>
    <div class="nav-scroll">
      <div class="nav-sec">By Source</div>
      <nav id="navMain"></nav>
      <div class="nav-sec" style="margin-top:6px">Research Topics</div>
      <nav id="navTopics"></nav>
      <div class="nav-sec" style="margin-top:6px">Intelligence Layer</div>
      <nav id="navAdv"></nav>
    </div>
    <div class="sb-foot">
      <strong>⏱ {updated}</strong>
      <span id="nextUpd">Next refresh: calculating…</span>
      <div class="refresh-bar"><div class="refresh-prog" id="refProg" style="width:100%"></div></div>
      <div class="sb-about">
        <span class="sb-about-lbl">About</span>
        <span class="sb-about-by">Made by <strong>Adith</strong></span>
        <a class="sb-about-mail" href="mailto:aditharavind03@gmail.com">aditharavind03@gmail.com</a>
      </div>
    </div>
  </aside>

  <!-- ── Main ── -->
  <div class="main">
    <div class="topbar">
      <div class="topbar-l">
        <h1 class="pg-title" id="pageTitle">All Intelligence</h1>
        <span class="upd-badge">⏱ {updated}</span>
      </div>
      <div class="topbar-r">
        <button class="btn ico-btn" id="themeBtn" title="Toggle theme">☀️</button>
        <a class="btn" href="README.md">📄 README</a>
        <a class="btn btn-acc" href="reports/weekly_report.md">📊 Report</a>
      </div>
    </div>

    <div class="content">
      <div class="stats" id="stats"></div>

      <div id="advWrap" class="adv-wrap" style="display:none"></div>

      <div class="panel" id="mainPanel">
        <div class="toolbar">
          <div class="srch-wrap">
            <span class="srch-ico">🔍</span>
            <input class="srch-inp" id="search" type="search"
              placeholder="Search titles, authors, sources, companies…">
          </div>
          <select class="ctrl" id="sort">
            <option value="newest">Newest first</option>
            <option value="score">Highest score</option>
            <option value="alpha">A → Z</option>
          </select>
          <select class="ctrl" id="dateRange">
            <option value="all">All time</option>
            <option value="today">Today</option>
            <option value="7d">Last 7 days</option>
            <option value="30d">Last 30 days</option>
            <option value="90d">Last 3 months</option>
          </select>
          <select class="ctrl" id="pageSize">
            <option value="20" selected>20 / page</option>
            <option value="10">10 / page</option>
            <option value="50">50 / page</option>
          </select>
          <div class="vt">
            <button class="vt-b" id="vGrid" title="Grid">⊞</button>
            <button class="vt-b" id="vList" title="List">☰</button>
          </div>
        </div>
        <div class="res-bar">
          <span class="res-n" id="resultCount">0 results</span>
          <span id="pageStatus">Page 1 of 1</span>
        </div>
        <div class="feed grid-v" id="feed"></div>
        <div class="pager">
          <span class="pg-inf" id="rangeStatus">Showing 0–0</span>
          <div class="pg-btns" id="pages"></div>
        </div>
      </div>
    </div>
  </div>
</div>

<script>
'use strict';
const data = {data};

/* ── constants ── */
const SRC_COLOR = {{
  all:'#818cf8',starred:'#fbbf24',aiNews:'#38bdf8',physicalAiNews:'#a78bfa',
  roboticsNews:'#fbbf24',embeddedNews:'#22d3ee',papers:'#34d399',repos:'#60a5fa',
  models:'#fb923c',funding:'#a3e635',companies:'#f472b6',jobs:'#2dd4bf',
}};
const SRC_ICON = {{
  all:'⚡',starred:'⭐',aiNews:'📰',physicalAiNews:'🦾',roboticsNews:'🤖',embeddedNews:'🔌',
  papers:'📄',repos:'💻',models:'🧠',funding:'💰',companies:'🏢',jobs:'💼',
}};
const SRC_LABEL = {{
  all:'All Intelligence',starred:'⭐ Starred',aiNews:'AI News',physicalAiNews:'Physical AI',
  roboticsNews:'Robotics',embeddedNews:'Embedded & Chips',papers:'Research Papers',repos:'GitHub Repos',
  models:'HF Models',funding:'Funding',companies:'Companies',jobs:'Jobs',
}};
const TOPICS = {{
  vla:{{ label:'VLA Models',    icon:'🎯', color:'#818cf8', kw:['vla','vision-language-action','vision language action'] }},
  wam:{{ label:'World Action',  icon:'🌍', color:'#a78bfa', kw:['wam','world action model','world-action','world model'] }},
  robotPolicy:{{ label:'Robot Policy',  icon:'🦿', color:'#2dd4bf', kw:['robot polic','manipulation polic','dexterous','locomotion','loco-manipul'] }},
  rlPolicy:{{    label:'RL Policy',     icon:'🧮', color:'#fbbf24', kw:['reinforcement learning','reward function','policy gradient','actor-critic','ppo ','rl agent'] }},
  simulation:{{  label:'Simulation',    icon:'🖥️', color:'#60a5fa', kw:['sim-to-real','simulation','simulator','simulated env','mujoco','isaac','sapien','robotwin','libero'] }},
}};

const state = {{ ds:'all',page:1,size:20,q:'',sort:'newest',view:'grid',dr:'all',advMod:null }};

/* ── helpers ── */
const esc = v => String(v??'').replace(/[&<>"']/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}}[c]));
const plain = v => {{ const d=document.createElement('div'); d.innerHTML=String(v??''); return d.textContent||''; }};
const titleOf = x => x.title||x.repo||x.model||x.company||'Untitled';
const dateOf  = x => x.date||x.published||x.posted||'';
const srcOf   = x => {{ const s=x.source; if (s && !/^https?:\/\//.test(s)) return s; return x.company||x.language||x.topic||x.category||''; }};
const scoreOf = x => Number(x.score||x.stars||x.downloads||0);
const isSeed  = x => {{ const u=x.url||x.pdf_url||''; return u.includes('example.com')||(x.title||'').toLowerCase().startsWith('example'); }};
const fmt = n => n>=1e6?(n/1e6).toFixed(1)+'M':n>=1000?(n/1000).toFixed(1)+'K':String(n);
const truncWords=(t,n=100)=>{{if(!t)return'';const w=t.trim().split(/\s+/);return w.length<=n?t:w.slice(0,n).join(' ')+'…';}};

/* ── stars (persist across data refreshes via localStorage, keyed by URL) ── */
const keyOf = x => x.url||x.pdf_url||titleOf(x);
let STARS = new Set(JSON.parse(localStorage.getItem('hub-stars')||'[]'));
const isStarred = x => STARS.has(keyOf(x));
function toggleStar(k) {{
  if (STARS.has(k)) STARS.delete(k); else STARS.add(k);
  localStorage.setItem('hub-stars', JSON.stringify([...STARS]));
}}
function starredRows() {{ return allRows().filter(isStarred); }}


function hrefOf(x) {{
  if (x.pdf_url) {{
    const m=x.pdf_url.match(/arxiv\.org\/(?:pdf|abs)\/([0-9]+\.[0-9]+)/);
    if (m) return 'https://arxiv.org/abs/'+m[1];
  }}
  if (x.url) return x.url;
  if (x.pdf_url) return x.pdf_url;
  if (x.source && /^https?:\/\//.test(x.source)) return x.source;
  return '#';
}}

function cutoff(r) {{
  if (r==='all') return '';
  const d=new Date();
  if (r==='today') d.setHours(0,0,0,0);
  else if (r==='7d')  d.setDate(d.getDate()-7);
  else if (r==='30d') d.setDate(d.getDate()-30);
  else if (r==='90d') d.setDate(d.getDate()-90);
  return d.toISOString().slice(0,10);
}}

function colorOf(k) {{ return SRC_COLOR[k]||(TOPICS[k]&&TOPICS[k].color)||'#818cf8'; }}
function labelOf(k) {{ return SRC_LABEL[k]||(TOPICS[k]&&TOPICS[k].label)||k; }}
function iconOf(k)  {{ return SRC_ICON[k]||(TOPICS[k]&&TOPICS[k].icon)||'•'; }}

/* ── rows ── */
function allRows() {{
  return Object.entries(data).flatMap(([k,rows])=>rows.filter(x=>!isSeed(x)).map(x=>( {{...x,_k:k}} )));
}}
function rowsFor(ds) {{
  if (ds==='starred') return starredRows();
  if (TOPICS[ds]) {{
    const t=TOPICS[ds];
    return (data.papers||[]).filter(x=>{{
      if (isSeed(x)) return false;
      const txt=(x.title+' '+(x.summary||'')).toLowerCase();
      return t.kw.some(k=>txt.includes(k));
    }}).map(x=>( {{...x,_k:ds}} ));
  }}
  return ds==='all'?allRows():(data[ds]||[]).filter(x=>!isSeed(x)).map(x=>( {{...x,_k:ds}} ));
}}
function filtered() {{
  const q=state.q.trim().toLowerCase(), from=cutoff(state.dr);
  let rows=rowsFor(state.ds);
  if (q) rows=rows.filter(x=>JSON.stringify(x).toLowerCase().includes(q));
  if (from) rows=rows.filter(x=>dateOf(x)>=from);
  return rows.sort((a,b)=>{{
    if (state.sort==='score') return scoreOf(b)-scoreOf(a);
    if (state.sort==='alpha') return titleOf(a).localeCompare(titleOf(b));
    return dateOf(b).localeCompare(dateOf(a));
  }});
}}

/* ── render nav ── */
function renderNav() {{
  const mk = (k,lbl,ico,n) => `
    <button class="nav-btn${{state.ds===k?' active':''}}" data-k="${{k}}">
      <span class="nav-ico">${{ico}}</span>
      <span class="nav-lbl">${{esc(lbl)}}</span>
      <span class="nav-cnt">${{n}}</span>
    </button>`;
  document.getElementById('navMain').innerHTML =
    [['all',allRows().length],['starred',starredRows().length],...Object.entries(data).map(([k,r])=>[k,r.length])]
      .map(([k,n])=>mk(k,SRC_LABEL[k]||k,SRC_ICON[k]||'•',n)).join('');
  document.getElementById('navTopics').innerHTML =
    Object.entries(TOPICS).map(([k,t])=>mk(k,t.label,t.icon,rowsFor(k).length)).join('');
  document.getElementById('navAdv').innerHTML =
    mk('__adv__','ADVANCED','🚀','18 modules');
  document.querySelectorAll('.nav-btn').forEach(b=>b.addEventListener('click',()=>{{
    state.ds=b.dataset.k; state.page=1; state.advMod=null; render();
  }}));
}}

/* ── render stats (with count-up) ── */
let lastDs='';
function renderStats() {{
  const rows=rowsFor(state.ds);
  const scored=rows.filter(x=>scoreOf(x)>0).length;
  const jobs=rows.filter(x=>x._k==='jobs').length;
  const latest=rows.map(dateOf).filter(Boolean).sort().pop()||'—';
  const items=[
    ['⚡','Total Signals',rows.length,'#818cf8'],
    ['🎯','Scored Items',scored,'#38bdf8'],
    ['💼','Job Postings',jobs,'#34d399'],
    ['📅','Latest',latest,'#fbbf24'],
  ];
  document.getElementById('stats').innerHTML = items.map(([ico,lbl,val,col])=>`
    <div class="stat" style="--sc:${{col}}">
      <span class="stat-ico">${{ico}}</span>
      <div class="stat-lbl">${{lbl}}</div>
      <div class="stat-num" data-target="${{typeof val==='number'?val:''}}"
           style="${{String(val).length>8?'font-size:15px;margin-top:8px':''}}">
        ${{typeof val==='number'?'0':esc(String(val))}}
      </div>
    </div>`).join('');

  /* stat hover handled by CSS lift */

  /* count-up */
  const doCount = state.ds!==lastDs;
  lastDs=state.ds;
  document.querySelectorAll('.stat-num[data-target]').forEach(el=>{{
    const t=Number(el.dataset.target);
    if (!t) return;
    if (!doCount) {{ el.textContent=t.toLocaleString(); return; }}
    const dur=1400, s=performance.now();
    const tick=now=>{{
      const p=Math.min((now-s)/dur,1), ease=1-Math.pow(1-p,3);
      el.textContent=Math.round(ease*t).toLocaleString();
      if (p<1) requestAnimationFrame(tick);
    }};
    requestAnimationFrame(tick);
  }});
}}

/* ── item template ── */
function itemHtml(x) {{
  const color=colorOf(x._k), t=titleOf(x), u=hrefOf(x),
        d=dateOf(x), s=srcOf(x),
        sum=truncWords(plain(x.summary||x.description||x.location||''),100),
        sc=scoreOf(x), lbl=labelOf(x._k), ico=iconOf(x._k);

  const isPaper = x._k==='papers'||!!TOPICS[x._k];
  let auHtml='';
  if (isPaper && Array.isArray(x.authors) && x.authors.length) {{
    const shown=x.authors.slice(0,5), more=x.authors.length-shown.length;
    auHtml=`<div class="i-authors">
      ${{shown.map(a=>`<span class="au">${{esc(a)}}</span>`).join('')}}
      ${{more?`<span class="au">+${{more}}</span>`:''}}
    </div>`;
  }}

  let acts='';
  if (isPaper) {{
    acts=`<div class="i-acts">
      <a class="act act-p" href="${{esc(u)}}" target="_blank" rel="noreferrer">📄 Abstract</a>
      ${{x.pdf_url?`<a class="act" href="${{esc(x.pdf_url)}}" target="_blank" rel="noreferrer">⬇️ PDF</a>`:''}}
    </div>`;
  }} else if (x._k==='repos') {{
    acts=`<div class="i-acts"><a class="act act-p" href="${{esc(u)}}" target="_blank" rel="noreferrer">💻 View Repo</a></div>`;
  }} else if (x._k==='jobs') {{
    acts=`<div class="i-acts"><a class="act act-p" href="${{esc(u)}}" target="_blank" rel="noreferrer">💼 Apply</a></div>`;
  }} else if (x._k==='models') {{
    acts=`<div class="i-acts"><a class="act act-p" href="${{esc(u)}}" target="_blank" rel="noreferrer">🧠 View Model</a></div>`;
  }} else if (u!=='#') {{
    acts=`<div class="i-acts"><a class="act act-p" href="${{esc(u)}}" target="_blank" rel="noreferrer">↗ Open</a></div>`;
  }}

  const scLbl=x._k==='repos'?'⭐ stars':x._k==='models'?'⬇️ dl':'score';
  const sk=keyOf(x), starred=STARS.has(sk);
  const starBtn=`<button class="star-btn${{starred?' on':''}}" data-star="${{esc(sk)}}" title="${{starred?'Remove from Starred':'Save to Starred'}}" aria-label="Star item">${{starred?'★':'☆'}}</button>`;
  const tags=`<div class="i-tags">
    ${{d?`<span class="tag t-d">📅 ${{esc(d)}}</span>`:''}}
    ${{s?`<span class="tag t-s">${{esc(s)}}</span>`:''}}
    ${{sc?`<span class="tag" style="background:var(--apale);border:1px solid var(--apale2);color:var(--acc)">${{fmt(sc)}} ${{scLbl}}</span>`:''}}
  </div>`;

  if (state.view==='grid') {{
    return `<article class="fi" style="--ic:${{color}}">
      <div class="fi-body">
        <div class="fi-hdr">
          <span class="i-cat" style="background:${{color}}">${{ico}} ${{esc(lbl)}}</span>
          ${{starBtn}}
        </div>
        <a class="i-title" href="${{esc(u)}}" target="_blank" rel="noreferrer">${{esc(t)}}</a>
        ${{auHtml}}
        ${{sum?`<div class="i-sum">${{esc(sum)}}</div>`:''}}
        ${{tags}}
        ${{acts}}
      </div>
    </article>`;
  }}

  /* list */
  return `<article class="fi" style="--ic:${{color}}">
    <div class="fi-wrap">
      <div class="fi-stripe" style="background:${{color}};box-shadow:0 0 8px ${{color}}"></div>
      <div class="fi-body">
        <div class="fi-hdr">
          <div>
            <span class="i-cat" style="background:${{color}};margin-bottom:5px">${{ico}} ${{esc(lbl)}}</span>
            <a class="i-title" href="${{esc(u)}}" target="_blank" rel="noreferrer">${{esc(t)}}</a>
          </div>
          <div style="display:flex;align-items:flex-start;gap:6px;flex-shrink:0">
            ${{sc?`<div class="i-score"><span class="sc-val">${{fmt(sc)}}</span><span class="sc-lbl">${{scLbl}}</span></div>`:''}}
            ${{starBtn}}
          </div>
        </div>
        ${{auHtml}}
        ${{sum?`<div class="i-sum">${{esc(sum)}}</div>`:''}}
        <div class="i-tags">
          ${{d?`<span class="tag t-d">📅 ${{esc(d)}}</span>`:''}}
          ${{s?`<span class="tag t-s">${{esc(s)}}</span>`:''}}
          ${{sc?`<span class="tag" style="background:var(--apale);border:1px solid var(--apale2);color:var(--acc)">${{fmt(sc)}} ${{scLbl}}</span>`:''}}
        </div>
        ${{acts}}
      </div>
    </div>
  </article>`;
}}

/* ── pagination ── */
function pageWin(c,t) {{
  const s=Math.max(1,c-2),e=Math.min(t,c+2);
  const ps=[];
  for(let p=s;p<=e;p++) ps.push(p);
  if(!ps.includes(1)){{ if(ps[0]>2) ps.unshift('…'); ps.unshift(1); }}
  if(!ps.includes(t)){{ if(ps[ps.length-1]<t-1) ps.push('…'); ps.push(t); }}
  return ps;
}}
function renderPag(tot) {{
  const el=document.getElementById('pages');
  el.innerHTML=[
    `<button class="pgb" data-p="${{state.page-1}}" ${{state.page===1?'disabled':''}}>‹ Prev</button>`,
    ...pageWin(state.page,tot).map(p=>p==='…'
      ?`<button class="pgb" disabled>…</button>`
      :`<button class="pgb${{p===state.page?' on':''}}" data-p="${{p}}">${{p}}</button>`),
    `<button class="pgb" data-p="${{state.page+1}}" ${{state.page===tot?'disabled':''}}>Next ›</button>`,
  ].join('');
  el.querySelectorAll('.pgb:not([disabled])').forEach(b=>b.addEventListener('click',()=>{{
    const p=Number(b.dataset.p);
    if(p&&p!==state.page){{ state.page=p; render(); document.querySelector('.panel').scrollIntoView({{behavior:'smooth',block:'start'}}); }}
  }}));
}}

/* ── main render ── */
function render() {{
  const isAdv = state.ds==='__adv__';
  document.getElementById('pageTitle').textContent =
    isAdv?(state.advMod?ADV_MODS.find(m=>m.id===state.advMod)?.label||'Advanced':'🚀 Advanced Intelligence')
    :SRC_LABEL[state.ds]||(TOPICS[state.ds]&&TOPICS[state.ds].label)||state.ds;
  renderNav();
  document.getElementById('mainPanel').style.display = isAdv?'none':'';
  document.getElementById('stats').style.display = isAdv?'none':'';
  document.getElementById('advWrap').style.display = isAdv?'':'none';
  if (isAdv) {{ renderAdvanced(); return; }}
  renderStats();
  const rows=filtered();
  const tot=Math.max(1,Math.ceil(rows.length/state.size));
  state.page=Math.min(state.page,tot);
  const s=(state.page-1)*state.size;
  const slice=rows.slice(s,s+state.size);
  document.getElementById('resultCount').textContent=
    rows.length.toLocaleString()+' result'+(rows.length!==1?'s':'');
  document.getElementById('pageStatus').textContent=`Page ${{state.page}} of ${{tot}}`;
  document.getElementById('rangeStatus').textContent=rows.length
    ?`Showing ${{s+1}}–${{s+slice.length}} of ${{rows.length}}`:'No results';
  const feed=document.getElementById('feed');
  feed.className='feed '+(state.view==='grid'?'grid-v':'list-v');
  feed.innerHTML=slice.length?slice.map(itemHtml).join('')
    :`<div class="empty">
        <div class="empty-ico">🔭</div>
        <h3>No matching signals</h3>
        <p>Try adjusting your search or selecting a different category.</p>
      </div>`;
  renderPag(tot);
  addTilts();
}}

/* ── events ── */
let tmr;
document.getElementById('search').addEventListener('input',e=>{{
  clearTimeout(tmr); tmr=setTimeout(()=>{{ state.q=e.target.value; state.page=1; render(); }},180);
}});
document.getElementById('sort').addEventListener('change',e=>{{ state.sort=e.target.value; state.page=1; render(); }});
document.getElementById('dateRange').addEventListener('change',e=>{{ state.dr=e.target.value; state.page=1; render(); }});
document.getElementById('pageSize').addEventListener('change',e=>{{ state.size=Number(e.target.value); state.page=1; render(); }});
document.getElementById('vGrid').addEventListener('click',()=>{{ state.view='grid'; state.page=1; syncVT(); render(); }});
document.getElementById('vList').addEventListener('click',()=>{{ state.view='list'; state.page=1; syncVT(); render(); }});
document.getElementById('feed').addEventListener('click',e=>{{
  const b=e.target.closest('.star-btn');
  if(!b) return;
  e.preventDefault(); e.stopPropagation();
  toggleStar(b.dataset.star);
  render();
}});
function syncVT() {{
  document.getElementById('vGrid').classList.toggle('on',state.view==='grid');
  document.getElementById('vList').classList.toggle('on',state.view==='list');
}}

/* ── theme ── */
const root=document.documentElement;
const themeBtn=document.getElementById('themeBtn');
const savedTheme=localStorage.getItem('hub-theme')||'dark';
root.setAttribute('data-theme',savedTheme);
themeBtn.textContent=savedTheme==='dark'?'☀️':'🌙';
themeBtn.addEventListener('click',()=>{{
  const n=root.getAttribute('data-theme')==='dark'?'light':'dark';
  root.setAttribute('data-theme',n);
  themeBtn.textContent=n==='dark'?'☀️':'🌙';
  localStorage.setItem('hub-theme',n);
}});

/* ── card hover handled by CSS lift ── */
function addTilts() {{}}

/* ══════════════════════════════════════════
   NEURAL NETWORK BACKGROUND ANIMATION
══════════════════════════════════════════ */
(function() {{
  const canvas=document.getElementById('bgCanvas');
  const ctx=canvas.getContext('2d');
  let W,H;
  function resize(){{ W=canvas.width=window.innerWidth; H=canvas.height=window.innerHeight; }}
  window.addEventListener('resize',resize); resize();

  const N=40, MAXD=150;
  const PCOLORS=['rgba(124,58,237,','rgba(99,102,241,','rgba(129,140,248,','rgba(14,165,233,'];
  const nodes=Array.from({{length:N}},()=>{{
    const c=PCOLORS[Math.floor(Math.random()*PCOLORS.length)];
    return {{
      x:Math.random()*window.innerWidth,
      y:Math.random()*window.innerHeight,
      vx:(Math.random()-.5)*.32,
      vy:(Math.random()-.5)*.32,
      r:Math.random()*1.8+.6,
      c, ph:Math.random()*Math.PI*2,
      ps:.008+Math.random()*.014,
    }};
  }});

  let mx=-2000,my=-2000;
  window.addEventListener('mousemove',e=>{{ mx=e.clientX; my=e.clientY; }});

  function frame() {{
    ctx.clearRect(0,0,W,H);
    nodes.forEach(n=>{{
      n.x+=n.vx; n.y+=n.vy; n.ph+=n.ps;
      if(n.x<0||n.x>W) n.vx*=-1;
      if(n.y<0||n.y>H) n.vy*=-1;
      n.x=Math.max(0,Math.min(W,n.x));
      n.y=Math.max(0,Math.min(H,n.y));
      const dx=n.x-mx,dy=n.y-my,md=Math.sqrt(dx*dx+dy*dy);
      if(md<110){{ n.vx+=(dx/md)*.012; n.vy+=(dy/md)*.012; }}
      n.vx=Math.max(-.7,Math.min(.7,n.vx*.997));
      n.vy=Math.max(-.7,Math.min(.7,n.vy*.997));
      const p=.35+Math.sin(n.ph)*.18;
      /* glow halo */
      const g=ctx.createRadialGradient(n.x,n.y,0,n.x,n.y,n.r*5);
      g.addColorStop(0,n.c+(p*.7)+')');
      g.addColorStop(1,n.c+'0)');
      ctx.beginPath(); ctx.arc(n.x,n.y,n.r*5,0,Math.PI*2);
      ctx.fillStyle=g; ctx.fill();
      /* core */
      ctx.beginPath(); ctx.arc(n.x,n.y,n.r,0,Math.PI*2);
      ctx.fillStyle=n.c+(p*1.4)+')'; ctx.fill();
    }});
    /* connections */
    for(let i=0;i<N;i++) for(let j=i+1;j<N;j++) {{
      const dx=nodes[i].x-nodes[j].x, dy=nodes[i].y-nodes[j].y;
      const d=Math.sqrt(dx*dx+dy*dy);
      if(d<MAXD) {{
        const a=(1-d/MAXD)*.14;
        ctx.beginPath();
        ctx.moveTo(nodes[i].x,nodes[i].y);
        ctx.lineTo(nodes[j].x,nodes[j].y);
        ctx.strokeStyle=`rgba(129,140,248,${{a}})`;
        ctx.lineWidth=.7; ctx.stroke();
      }}
    }}
    requestAnimationFrame(frame);
  }}
  frame();
}})();

/* ══════════════════════════════════════════
   AUTO-REFRESH COUNTDOWN (every 6 hours)
══════════════════════════════════════════ */
(function() {{
  const SIX_H=6*60*60*1000;
  const end=Date.now()+SIX_H;
  const updEl=document.getElementById('nextUpd');
  const progEl=document.getElementById('refProg');

  function tick() {{
    const left=end-Date.now();
    if(left<=0){{ location.reload(); return; }}
    const h=Math.floor(left/3600000);
    const m=Math.floor((left%3600000)/60000);
    const s=Math.floor((left%60000)/1000);
    if(updEl) updEl.textContent=`Refresh in ${{h}}h ${{m}}m ${{s}}s`;
    if(progEl) progEl.style.width=((left/SIX_H)*100).toFixed(2)+'%';
  }}
  tick();
  setInterval(tick,1000);
  setTimeout(()=>location.reload(),SIX_H);
}})();

/* ══════════════════════════════════════════════════════
   ADVANCED INTELLIGENCE ENGINE
══════════════════════════════════════════════════════ */

/* ── Market definitions ── */
const MKTS = {{
  humanoid:    {{ label:'Humanoid Robots',       icon:'🤖', color:'#f472b6', kw:['humanoid','bipedal','figure robot','optimus','atlas','digit'] }},
  vla:         {{ label:'VLA Models',            icon:'🎯', color:'#818cf8', kw:['vla','vision-language-action','vision language action'] }},
  worldModel:  {{ label:'World Models',          icon:'🌍', color:'#a78bfa', kw:['world model','world action','wam','world simulator'] }},
  synData:     {{ label:'Synthetic Data',        icon:'🔬', color:'#34d399', kw:['synthetic data','sim-to-real','data generation','procedural','mujoco','isaac','sapien'] }},
  robotInfra:  {{ label:'Robot Infrastructure', icon:'⚙️', color:'#60a5fa', kw:['robot infra','fleet manag','robot deployment','ros2','middleware','robot os'] }},
  embodied:    {{ label:'Embodied AI',           icon:'🦾', color:'#fb923c', kw:['embodied','physical ai','embodied intelligence','embodied agent'] }},
  manipulation:{{ label:'Dexterous Manipulation',icon:'✋', color:'#2dd4bf', kw:['manipulation','dexterous','grasping','pick and place','bimanual','hand'] }},
  locomotion:  {{ label:'Locomotion',            icon:'🦿', color:'#fbbf24', kw:['locomotion','legged','walking robot','running','parkour','quadruped'] }},
  agents:      {{ label:'AI Agents',             icon:'🧠', color:'#38bdf8', kw:['agent','agentic','multi-agent','autonomous agent','llm agent','tool use'] }},
  evalBench:   {{ label:'Evaluation & Benchmarks',icon:'📊', color:'#f87171', kw:['benchmark','evaluation','eval suite','leaderboard','assessment','metric'] }},
  dataInfra:   {{ label:'Robot Data Platforms',  icon:'🗄️', color:'#a3e635', kw:['data collect','teleoperat','dataset','demonstration','imitation learning','open-x'] }},
  multimodal:  {{ label:'Multimodal Foundation', icon:'👁️', color:'#c084fc', kw:['multimodal','vision language','vlm','visual language','clip','diffusion'] }},
}};

const ALL_TEXT = (arr) => arr.filter(x=>!isSeed(x)).map(x=>JSON.stringify(x).toLowerCase());

function mktScore(k) {{
  const kws=MKTS[k].kw;
  const has=txt=>kws.some(w=>txt.includes(w));
  const papers   =(data.papers||[]).filter(x=>!isSeed(x)&&has((x.title+' '+(x.summary||'')).toLowerCase())).length;
  const news     =[...(data.aiNews||[]),...(data.physicalAiNews||[]),...(data.roboticsNews||[]),...(data.embeddedNews||[])].filter(x=>!isSeed(x)&&has(JSON.stringify(x).toLowerCase())).length;
  const funding  =(data.funding||[]).filter(x=>!isSeed(x)&&has(JSON.stringify(x).toLowerCase())).length;
  const jobs     =(data.jobs||[]).filter(x=>!isSeed(x)&&has(JSON.stringify(x).toLowerCase())).length;
  const repos    =(data.repos||[]).filter(x=>!isSeed(x)&&has(JSON.stringify(x).toLowerCase())).length;
  const models   =(data.models||[]).filter(x=>!isSeed(x)&&has(JSON.stringify(x).toLowerCase())).length;
  const companies=(data.companies||[]).filter(x=>!isSeed(x)&&has(JSON.stringify(x).toLowerCase())).length;
  const research = papers*3+repos*2+models*2;
  const commercial= funding*5+companies*4;
  const demand = news*2+jobs*1;
  const total = research+commercial+demand;
  const momentum = Math.min(99,research*2+demand*3);
  const competition= Math.min(99,commercial*4);
  const opp = Math.min(99,Math.max(1,research*3+demand*2-competition*0.5+10));
  const gap = Math.max(0,research - commercial);
  return {{papers,news,funding,jobs,repos,models,companies,research,commercial,demand,total,momentum,competition,opp,gap}};
}}

/* ── Module registry ── */
const ADV_MODS = [
  {{id:'opportunity_radar',  label:'Opportunity Radar',       icon:'📡', color:'#818cf8', desc:'Ranked markets by momentum & whitespace'}},
  {{id:'gapfinder',          label:'GapFinder',               icon:'🔍', color:'#34d399', desc:'Research with demand but no solutions yet'}},
  {{id:'future_unicorn',     label:'Future Unicorn Predictor',icon:'🦄', color:'#f472b6', desc:'Companies most likely to hit $1B+'}},
  {{id:'startup_ideas',      label:'Startup Idea Engine',     icon:'💡', color:'#fbbf24', desc:'Auto-generated startup ideas from signals'}},
  {{id:'startup_validator',  label:'Startup Validator',       icon:'✅', color:'#2dd4bf', desc:'Validate your idea against market data'}},
  {{id:'builder_match',      label:'Builder Match & GPA',     icon:'🎓', color:'#60a5fa', desc:'Match your skills to the right opportunity'}},
  {{id:'problemmine',        label:'ProblemMine',             icon:'⛏️', color:'#fb923c', desc:'Real unsolved problems from research & community'}},
  {{id:'market_intel',       label:'Market Intelligence',     icon:'📈', color:'#a3e635', desc:'Full breakdown of every major market'}},
  {{id:'research_map',       label:'Research → Startup Map',  icon:'🗺️', color:'#a78bfa', desc:'Commercialization paths from papers to products'}},
  {{id:'startup_genome',     label:'Startup Genome',          icon:'🧬', color:'#f472b6', desc:'Deep profiles for every tracked company'}},
  {{id:'hidden_gems',        label:'Hidden Gem Scanner',      icon:'💎', color:'#38bdf8', desc:'Underrated repos, papers & technologies'}},
  {{id:'investor_mode',      label:'Investor Mode',           icon:'💰', color:'#a3e635', desc:'Funding trends & most investable markets'}},
  {{id:'graveyard',          label:'Startup Graveyard',       icon:'💀', color:'#f87171', desc:'Learn from failed AI & robotics startups'}},
  {{id:'time_machine',       label:'Opportunity Time Machine',icon:'⏰', color:'#fbbf24', desc:'Failed ideas that are viable today'}},
  {{id:'cofounder',          label:'AI Co-Founder',           icon:'🤝', color:'#818cf8', desc:'Ask anything about what to build next'}},
  {{id:'cert_hub',           label:'Certification & Career Hub',icon:'🎯',color:'#2dd4bf', desc:'Free certs, fellowships & learning paths'}},
  {{id:'daily_brief',        label:'Daily Founder Brief',     icon:'📋', color:'#60a5fa', desc:'Curated daily report for builders'}},
  {{id:'signal_engine',      label:'Signal Score Engine',     icon:'⚡', color:'#c084fc', desc:'Universal ranking across all entities'}},
];

/* ── helper: bar HTML ── */
function bar(label,pct,color) {{
  return `<div class="adv-bar-row">
    <span class="adv-bar-lbl">${{label}}</span>
    <div class="adv-bar"><div class="adv-bar-fill" style="width:${{pct}}%;background:${{color||'var(--acc)'}}"></div></div>
    <span style="font-size:11px;color:var(--t3);width:30px;text-align:right;flex-shrink:0">${{Math.round(pct)}}</span>
  </div>`;
}}

/* ── ADVANCED hub ── */
function renderAdvHub() {{
  const scores=Object.fromEntries(Object.keys(MKTS).map(k=>[k,mktScore(k)]));
  const topMkt=Object.entries(scores).sort((a,b)=>b[1].opp-a[1].opp)[0];
  const topGap=Object.entries(scores).sort((a,b)=>b[1].gap-a[1].gap)[0];
  const totalPapers=(data.papers||[]).filter(x=>!isSeed(x)).length;
  const totalFunding=(data.funding||[]).filter(x=>!isSeed(x)).length;
  return `
  <div class="adv-hero">
    <div class="adv-hero-title">🚀 Advanced Intelligence Layer</div>
    <div class="adv-hero-sub">Transform ecosystem signals into startup opportunities, market insights & founder intelligence</div>
  </div>
  <div class="adv-metrics">
    <div class="adv-metric"><div class="adv-metric-n">${{totalPapers}}</div><div class="adv-metric-l">Papers Analyzed</div></div>
    <div class="adv-metric"><div class="adv-metric-n">${{totalFunding}}</div><div class="adv-metric-l">Funding Rounds</div></div>
    <div class="adv-metric"><div class="adv-metric-n">${{Object.keys(MKTS).length}}</div><div class="adv-metric-l">Markets Tracked</div></div>
    <div class="adv-metric"><div class="adv-metric-n">${{ADV_MODS.length}}</div><div class="adv-metric-l">Intel Modules</div></div>
  </div>
  <div class="adv-hub">
    ${{ADV_MODS.map(m=>`
      <div class="adv-hcard" style="--hc:${{m.color}}" data-mod="${{m.id}}">
        <div class="adv-hcard-ico">${{m.icon}}</div>
        <div class="adv-hcard-title">${{m.label}}</div>
        <div class="adv-hcard-desc">${{m.desc}}</div>
        <span class="adv-hcard-stat" style="background:${{m.color}}22;color:${{m.color}}">Open →</span>
      </div>`).join('')}}
  </div>`;
}}

/* ── Module: Opportunity Radar ── */
function advOpportunityRadar() {{
  const ranked=Object.entries(MKTS).map(([k,m])=>{{const s=mktScore(k);return{{k,m,s}};}})
    .sort((a,b)=>b.s.opp-a.s.opp);
  return `
  <div class="adv-metrics">
    <div class="adv-metric"><div class="adv-metric-n">${{ranked[0].s.opp}}</div><div class="adv-metric-l">Top Opp Score</div></div>
    <div class="adv-metric"><div class="adv-metric-n">${{ranked.filter(r=>r.s.opp>60).length}}</div><div class="adv-metric-l">Hot Markets</div></div>
    <div class="adv-metric"><div class="adv-metric-n">${{ranked.reduce((a,r)=>a+r.s.papers,0)}}</div><div class="adv-metric-l">Papers Tracked</div></div>
    <div class="adv-metric"><div class="adv-metric-n">${{ranked.reduce((a,r)=>a+r.s.funding,0)}}</div><div class="adv-metric-l">Funding Signals</div></div>
  </div>
  <div class="adv-panel">
    <div class="adv-panel-hdr">📡 Market Opportunity Rankings</div>
    <ul class="adv-list">
      ${{ranked.map((r,i)=>`
        <li class="adv-item">
          <div class="adv-rank" style="background:${{r.m.color}}22;color:${{r.m.color}}">${{i+1}}</div>
          <div class="adv-item-body">
            <div class="adv-item-title">${{r.m.icon}} ${{r.m.label}}</div>
            ${{bar('Opportunity',r.s.opp,r.m.color)}}
            ${{bar('Momentum',r.s.momentum,r.m.color)}}
            ${{bar('Competition',r.s.competition,'#f87171')}}
            <div class="adv-scores">
              <span class="adv-score-badge">📄 ${{r.s.papers}} papers</span>
              <span class="adv-score-badge">💰 ${{r.s.funding}} funding</span>
              <span class="adv-score-badge">💼 ${{r.s.jobs}} jobs</span>
              <span class="adv-score-badge">💻 ${{r.s.repos}} repos</span>
            </div>
          </div>
          <div style="text-align:right;flex-shrink:0;padding-top:2px">
            <div style="font-size:28px;font-weight:900;color:${{r.m.color}};text-shadow:0 0 20px ${{r.m.color}}44">${{r.s.opp}}</div>
            <div style="font-size:10px;color:var(--muted)">opp score</div>
          </div>
        </li>`).join('')}}
    </ul>
  </div>`;
}}

/* ── Module: GapFinder ── */
function advGapFinder() {{
  const SUGGESTED = {{
    humanoid:'Humanoid Robot OS / Middleware Platform',vla:'VLA Fine-Tuning & Deployment API',
    worldModel:'World Model Evaluation Framework',synData:'Synthetic Training Data Marketplace',
    robotInfra:'Robot Fleet Monitoring & Orchestration',embodied:'Embodied AI Simulation Cloud',
    manipulation:'Dexterous Hand Teleop & Data Platform',locomotion:'Legged Robot Trail Dataset Hub',
    agents:'Embodied Agent Evaluation Suite',evalBench:'Open Physical Robot Benchmark',
    dataInfra:'Robot Demonstration Collection Platform',multimodal:'Embodied Multimodal Foundation API',
  }};
  const MARKET_SIZE = {{
    humanoid:'$38B by 2035',vla:'$2.4B by 2028',worldModel:'$5B by 2030',synData:'$1.8B by 2027',
    robotInfra:'$12B by 2030',embodied:'$22B by 2032',manipulation:'$8B by 2029',locomotion:'$4.5B by 2029',
    agents:'$47B by 2030',evalBench:'$800M by 2028',dataInfra:'$6B by 2029',multimodal:'$15B by 2030',
  }};
  const gaps=Object.entries(MKTS).map(([k,m])=>{{
    const s=mktScore(k);
    const gapScore=Math.min(99,Math.max(1,s.papers*4+s.news*2+s.jobs*3-s.funding*6-s.models*3+5));
    return {{k,m,s,gapScore,suggested:SUGGESTED[k]||'TBD',mktSize:MARKET_SIZE[k]||'Est. $1B+'}};
  }}).sort((a,b)=>b.gapScore-a.gapScore);
  return `
  <div class="adv-metrics">
    <div class="adv-metric"><div class="adv-metric-n">${{gaps.filter(g=>g.gapScore>60).length}}</div><div class="adv-metric-l">High-Value Gaps</div></div>
    <div class="adv-metric"><div class="adv-metric-n">${{gaps[0].gapScore}}</div><div class="adv-metric-l">Top Gap Score</div></div>
    <div class="adv-metric"><div class="adv-metric-n">${{gaps.reduce((a,g)=>a+g.s.papers,0)}}</div><div class="adv-metric-l">Papers w/ No Product</div></div>
    <div class="adv-metric"><div class="adv-metric-n">${{Object.keys(MKTS).length}}</div><div class="adv-metric-l">Markets Scanned</div></div>
  </div>
  <div class="adv-panel">
    <div class="adv-panel-hdr">🔍 Identified Market Gaps — Research exists, solutions do not</div>
    <ul class="adv-list">
      ${{gaps.map((g,i)=>`
        <li class="adv-item">
          <div class="adv-rank" style="background:${{g.m.color}}22;color:${{g.m.color}}">${{i+1}}</div>
          <div class="adv-item-body">
            <div class="adv-item-title">${{g.m.icon}} ${{g.m.label}} Gap</div>
            <div class="adv-item-sub">
              <strong>Suggested startup:</strong> ${{g.suggested}}<br>
              <strong>Est. market:</strong> ${{g.mktSize}}
            </div>
            ${{bar('Gap Score',g.gapScore,g.m.color)}}
            ${{bar('Research Depth',Math.min(99,g.s.papers*8),'#34d399')}}
            ${{bar('Commercial Vacuum',Math.min(99,Math.max(0,100-g.s.commercial*8)),'#fbbf24')}}
            <div class="adv-scores">
              <span class="adv-tag adv-tag-green">📄 ${{g.s.papers}} papers</span>
              <span class="adv-tag adv-tag-red">🏢 ${{g.s.companies}} companies</span>
              <span class="adv-tag adv-tag-blue">💼 ${{g.s.jobs}} open roles</span>
            </div>
          </div>
          <div style="text-align:right;flex-shrink:0;padding-top:2px">
            <div style="font-size:28px;font-weight:900;color:${{g.m.color}}">${{g.gapScore}}</div>
            <div style="font-size:10px;color:var(--muted)">gap score</div>
          </div>
        </li>`).join('')}}
    </ul>
  </div>`;
}}

/* ── Module: Future Unicorn Predictor ── */
function advFutureUnicorn() {{
  const KNOWN=[
    {{name:'Physical Intelligence (π)',tech:'VLA / Dexterous Manipulation',funding:'$400M+',stage:'Series B',score:97}},
    {{name:'Figure AI',tech:'Humanoid Robots',funding:'$675M',stage:'Series B',score:95}},
    {{name:'1X Technologies',tech:'Humanoid Robots',funding:'$100M+',stage:'Series B',score:88}},
    {{name:'Skild AI',tech:'General Robot Brain',funding:'$300M',stage:'Series B',score:91}},
    {{name:'Apptronik',tech:'Apollo Humanoid',funding:'$350M',stage:'Series B',score:86}},
    {{name:'Agility Robotics',tech:'Digit Humanoid (Amazon)',funding:'Strategic',stage:'Growth',score:83}},
    {{name:'Covariant',tech:'Robot Foundation Model',funding:'$222M',stage:'Series C',score:85}},
    {{name:'Machina Labs',tech:'AI Metal Forming',funding:'$125M',stage:'Series C',score:79}},
    {{name:'Dexterous Robotics',tech:'Manipulation Platform',funding:'Undisclosed',stage:'Early',score:71}},
    {{name:'Mytra',tech:'Warehouse Automation AI',funding:'$28M',stage:'Series B',score:68}},
  ];
  const fromData=(data.companies||[]).filter(x=>!isSeed(x)).slice(0,8).map(x=>{{
    const score=Math.min(95,40+Math.floor(Math.random()*35));
    return {{name:x.company||x.title||'Unknown',tech:x.category||x.description||'Physical AI',
             funding:x.funding||'Unknown',stage:x.stage||'Early',score}};
  }});
  const all=[...KNOWN,...fromData].sort((a,b)=>b.score-a.score).slice(0,15);
  return `
  <div class="adv-metrics">
    <div class="adv-metric"><div class="adv-metric-n">${{all.filter(c=>c.score>=90).length}}</div><div class="adv-metric-l">Likely Unicorns</div></div>
    <div class="adv-metric"><div class="adv-metric-n">${{all.filter(c=>c.score>=80).length}}</div><div class="adv-metric-l">Strong Contenders</div></div>
    <div class="adv-metric"><div class="adv-metric-n">${{all[0].score}}</div><div class="adv-metric-l">Top Score</div></div>
    <div class="adv-metric"><div class="adv-metric-n">$1B+</div><div class="adv-metric-l">Target Valuation</div></div>
  </div>
  <div class="adv-panel">
    <div class="adv-panel-hdr">🦄 Future Unicorn Predictions — Breakout probability by company</div>
    <ul class="adv-list">
      ${{all.map((c,i)=>{{
        const col=c.score>=90?'#f472b6':c.score>=80?'#818cf8':c.score>=70?'#60a5fa':'#34d399';
        return `<li class="adv-item">
          <div class="adv-rank" style="background:${{col}}22;color:${{col}}">${{i+1}}</div>
          <div class="adv-item-body">
            <div class="adv-item-title">${{c.name}}</div>
            <div class="adv-item-sub">${{c.tech}} · ${{c.stage}} · ${{c.funding}}</div>
            ${{bar('Unicorn Score',c.score,col)}}
          </div>
          <div style="text-align:right;flex-shrink:0;padding-top:2px">
            <div style="font-size:26px;font-weight:900;color:${{col}}">${{c.score}}</div>
            <div style="font-size:10px;color:var(--muted)">breakout %</div>
          </div>
        </li>`;
      }}).join('')}}
    </ul>
  </div>`;
}}

/* ── Module: Startup Idea Engine ── */
function advStartupIdeas() {{
  const recentPapers=(data.papers||[]).filter(x=>!isSeed(x)).sort((a,b)=>dateOf(b).localeCompare(dateOf(a))).slice(0,5);
  const IDEAS=[
    {{title:'Robot Data Flywheel',problem:'No scalable way to collect robot training data at low cost',solution:'Platform for crowdsourced teleoperation & synthetic data labeling',customer:'Robotics startups & research labs',market:'$6B by 2029',mvp:'Web-based teleoperation recorder + S3 pipeline',difficulty:3,score:91,icon:'🗄️'}},
    {{title:'VLA Fine-Tuning API',problem:'Foundation VLA models need expensive domain adaptation',solution:'1-click fine-tuning API for custom manipulation tasks',customer:'Industrial robot OEMs & integrators',market:'$2.4B by 2028',mvp:'LoRA wrapper around OpenVLA with REST API',difficulty:2,score:89,icon:'🎯'}},
    {{title:'Sim2Real Validator',problem:'No automated way to test if sim-trained policies work in real',solution:'Benchmarking-as-a-service with standardized real robot test rigs',customer:'Academic labs, robotics startups',market:'$800M by 2028',mvp:'5 test scenarios + leaderboard website',difficulty:3,score:85,icon:'🔬'}},
    {{title:'Humanoid Monitoring SaaS',problem:'Industrial operators cannot monitor fleets of humanoid robots at scale',solution:'Real-time dashboard + anomaly detection for humanoid fleet ops',customer:'Warehouse operators, manufacturers',market:'$12B by 2030',mvp:'OPC-UA connector + Grafana dashboard',difficulty:2,score:88,icon:'⚙️'}},
    {{title:'Physical AI Marketplace',problem:'No marketplace to buy/sell pre-trained robot policies',solution:'Hugging Face-style hub for task-specific robot skill modules',customer:'Integrators, OEMs, researchers',market:'$3B by 2030',mvp:'Git-LFS repo + model card standard',difficulty:2,score:83,icon:'🛒'}},
    {{title:'Robot Eval-as-a-Service',problem:'Researchers need standardized benchmarks but lack hardware access',solution:'Remote-access robot evaluation lab with standardized tasks',customer:'AI researchers, robot companies',market:'$500M by 2027',mvp:'ROS2 task runner + result API',difficulty:4,score:80,icon:'📊'}},
    {{title:'World Model Studio',problem:'Building world models requires specialized expertise & infrastructure',solution:'No-code world model training & deployment for robotics teams',customer:'Robotics startups, automotive OEMs',market:'$5B by 2030',mvp:'Dreamer-based trainer + visual editor',difficulty:4,score:82,icon:'🌍'}},
    {{title:'Robot Skills App Store',problem:'Robots cannot download new capabilities like smartphones can',solution:'OTA skill delivery platform for deployed robots',customer:'Robot manufacturers, operators',market:'$8B by 2030',mvp:'Docker-based skill capsules + fleet manager',difficulty:4,score:86,icon:'📱'}},
  ];
  const paperIdeas=recentPapers.slice(0,3).map((p,i)=>{{
    const sc=70+Math.floor(Math.random()*20);
    return {{title:`Build on: "${{truncWords(titleOf(p),8)}}"`,
      problem:`No commercial product exists for this research direction yet`,
      solution:`Productize the core technique from this paper into a developer API`,
      customer:'ML Engineers, Robotics teams',market:'$1B+ addressable',
      mvp:'Paper reproduction + API wrapper',difficulty:3,score:sc,icon:'📄',
      fromPaper:hrefOf(p)}};
  }});
  const all=[...IDEAS,...paperIdeas];
  return `
  <div class="adv-metrics">
    <div class="adv-metric"><div class="adv-metric-n">${{all.length}}</div><div class="adv-metric-l">Ideas Generated</div></div>
    <div class="adv-metric"><div class="adv-metric-n">${{all.filter(i=>i.score>=85).length}}</div><div class="adv-metric-l">High Potential</div></div>
    <div class="adv-metric"><div class="adv-metric-n">${{all.filter(i=>i.difficulty<=2).length}}</div><div class="adv-metric-l">Low Difficulty</div></div>
    <div class="adv-metric"><div class="adv-metric-n">Daily</div><div class="adv-metric-l">Refresh Rate</div></div>
  </div>
  <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(310px,1fr));gap:13px">
    ${{all.map(idea=>`
      <div class="adv-panel" style="margin:0">
        <div class="adv-panel-hdr" style="justify-content:space-between">
          <span>${{idea.icon}} ${{idea.title}}</span>
          <span style="font-size:16px;font-weight:900;color:var(--acc)">${{idea.score}}</span>
        </div>
        <div style="padding:14px 18px">
          <div style="font-size:11px;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;margin-bottom:3px">Problem</div>
          <div style="font-size:13px;color:var(--t2);margin-bottom:10px">${{idea.problem}}</div>
          <div style="font-size:11px;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;margin-bottom:3px">Solution</div>
          <div style="font-size:13px;color:var(--t2);margin-bottom:10px">${{idea.solution}}</div>
          <div class="adv-scores">
            <span class="adv-tag adv-tag-blue">👤 ${{idea.customer}}</span>
            <span class="adv-tag adv-tag-green">🌍 ${{idea.market}}</span>
            <span class="adv-tag adv-tag-gold">🔨 Difficulty ${{idea.difficulty}}/5</span>
          </div>
          <div style="margin-top:10px;font-size:12px;color:var(--t3)">
            <strong>MVP:</strong> ${{idea.mvp}}
          </div>
          ${{idea.fromPaper?`<a href="${{idea.fromPaper}}" target="_blank" style="display:inline-flex;align-items:center;gap:4px;margin-top:8px;font-size:12px;color:var(--acc)">📄 Source Paper ↗</a>`:''}}
        </div>
      </div>`).join('')}}
  </div>`;
}}

/* ── Module: Startup Validator ── */
function advStartupValidator() {{
  return `
  <div class="adv-panel">
    <div class="adv-panel-hdr">✅ Enter your startup idea for instant market validation</div>
    <div class="adv-form">
      <div class="adv-form-row">
        <label class="adv-label" for="val-idea">Your Startup Idea</label>
        <textarea class="adv-inp" id="val-idea" rows="3"
          placeholder="e.g. A platform for collecting robot teleoperation data from remote workers…"></textarea>
      </div>
      <div class="adv-form-row">
        <label class="adv-label" for="val-market">Target Market</label>
        <input class="adv-inp adv-inp-sm" id="val-market" placeholder="e.g. Industrial robotics, Healthcare robots…">
      </div>
      <button class="adv-btn" id="val-run">🔍 Validate Idea</button>
      <div class="adv-result" id="val-result"></div>
    </div>
  </div>`;
}}
function advStartupValidatorBind() {{
  const btn=document.getElementById('val-run');
  if(!btn) return;
  btn.addEventListener('click',()=>{{
    const idea=(document.getElementById('val-idea').value||'').toLowerCase();
    const mkt=(document.getElementById('val-market').value||'').toLowerCase();
    const combined=idea+' '+mkt;
    let bestMkt=null, bestScore=0;
    Object.entries(MKTS).forEach(([k,m])=>{{
      const s=mktScore(k);
      if(m.kw.some(w=>combined.includes(w.split(' ')[0]))){{
        if(s.opp>bestScore){{bestScore=s.opp;bestMkt={{k,m,s}};}}
      }}
    }});
    if(!bestMkt) {{ const e=Object.entries(MKTS).map(([k,m])=>{{return{{k,m,s:mktScore(k)}};}}); bestMkt=e.sort((a,b)=>b.s.opp-a.s.opp)[0]; }}
    const s=bestMkt.s;
    const valScore=Math.min(97,s.opp+s.demand-s.competition*0.3+Math.floor(Math.random()*10)+10);
    const r=document.getElementById('val-result');
    r.className='adv-result show';
    r.innerHTML=`
      <div style="font-size:15px;font-weight:800;margin-bottom:14px">Validation Results for: <span style="color:var(--acc)">${{esc(document.getElementById('val-idea').value.slice(0,60))}}</span></div>
      <div class="adv-grid2">
        <div class="adv-kv"><div class="adv-kv-k">Validation Score</div><div class="adv-kv-v" style="color:${{valScore>75?'#34d399':'#fbbf24'}}">${{valScore}}/100</div></div>
        <div class="adv-kv"><div class="adv-kv-k">Closest Market</div><div class="adv-kv-v" style="font-size:14px">${{bestMkt.m.icon}} ${{bestMkt.m.label}}</div></div>
        <div class="adv-kv"><div class="adv-kv-k">Research Activity</div><div class="adv-kv-v">${{s.papers}} papers</div></div>
        <div class="adv-kv"><div class="adv-kv-k">Funding Activity</div><div class="adv-kv-v">${{s.funding}} rounds</div></div>
        <div class="adv-kv"><div class="adv-kv-k">Hiring Demand</div><div class="adv-kv-v">${{s.jobs}} jobs</div></div>
        <div class="adv-kv"><div class="adv-kv-k">Competition Level</div><div class="adv-kv-v" style="color:${{s.competition<40?'#34d399':'#f87171'}}">${{s.competition<30?'Low':s.competition<60?'Medium':'High'}}</div></div>
      </div>
      <div style="margin-top:14px">
        ${{bar('Market Opportunity',s.opp,'#34d399')}}
        ${{bar('Demand Signals',Math.min(99,s.demand*4),'#60a5fa')}}
        ${{bar('Competition',s.competition,'#f87171')}}
        ${{bar('Tech Readiness',Math.min(99,s.papers*5),'#a78bfa')}}
      </div>
      <div style="margin-top:14px;padding:12px;background:var(--apale);border-radius:var(--rsm);font-size:13px;color:var(--t2)">
        <strong style="color:var(--acc)">💡 Verdict:</strong>
        ${{valScore>80?'Strong signal — research activity and demand both point to this being a viable market. Build the MVP now.'
          :valScore>60?'Moderate signal — the market exists but competition is growing. Differentiation will be key.'
          :'Early market — you are ahead of the curve. High risk, high reward. Find early design partners first.'}}
      </div>`;
  }});
}}

/* ── Module: Builder Match ── */
function advBuilderMatch() {{
  const SKILLS=[
    {{id:'ml',lbl:'Machine Learning'}},{{id:'robotics',lbl:'Robotics / ROS'}},
    {{id:'fullstack',lbl:'Full Stack Dev'}},{{id:'cloud',lbl:'Cloud / DevOps'}},
    {{id:'hardware',lbl:'Hardware / EE'}},{{id:'cv',lbl:'Computer Vision'}},
    {{id:'nlp',lbl:'NLP / LLMs'}},{{id:'sim',lbl:'Simulation / Unity/Unreal'}},
    {{id:'biz',lbl:'Biz Dev / Sales'}},{{id:'design',lbl:'UI/UX Design'}},
    {{id:'data',lbl:'Data Engineering'}},{{id:'pm',lbl:'Product Management'}},
  ];
  const MARKET_SKILLS={{
    humanoid:['robotics','hardware','ml','sim'],vla:['ml','cv','robotics','data'],
    worldModel:['ml','sim','cv'],synData:['sim','data','cloud'],
    robotInfra:['cloud','fullstack','robotics'],embodied:['ml','robotics','cv'],
    manipulation:['robotics','hardware','ml'],locomotion:['robotics','hardware','sim'],
    agents:['nlp','ml','fullstack'],evalBench:['robotics','ml','data'],
    dataInfra:['cloud','data','fullstack'],multimodal:['ml','cv','data'],
  }};
  return `
  <div class="adv-panel">
    <div class="adv-panel-hdr">🎓 Select your skills to get matched with the right opportunity</div>
    <div class="adv-form">
      <label class="adv-label">Your Skills (select all that apply)</label>
      <div class="adv-skill-grid">
        ${{SKILLS.map(s=>`<label class="adv-skill-check"><input type="checkbox" id="sk-${{s.id}}" value="${{s.id}}">${{s.lbl}}</label>`).join('')}}
      </div>
      <div class="adv-form-row" style="margin-top:4px">
        <label class="adv-label" for="bm-time">Time Available (hrs/week)</label>
        <input class="adv-inp adv-inp-sm" id="bm-time" type="number" min="1" max="80" value="20" style="width:100px">
      </div>
      <div class="adv-form-row">
        <label class="adv-label" for="bm-budget">Budget to Start ($)</label>
        <select class="adv-inp adv-inp-sm ctrl" id="bm-budget" style="width:200px">
          <option value="0">Bootstrapped ($0)</option>
          <option value="10000">$10K</option>
          <option value="100000">$100K</option>
          <option value="1000000">$1M+ (funded)</option>
        </select>
      </div>
      <button class="adv-btn" id="bm-run">🎯 Calculate Founder GPA</button>
      <div class="adv-result" id="bm-result"></div>
    </div>
  </div>`;
}}
function advBuilderMatchBind() {{
  const btn=document.getElementById('bm-run');
  if(!btn) return;
  btn.addEventListener('click',()=>{{
    const SKILLS_ARR=['ml','robotics','fullstack','cloud','hardware','cv','nlp','sim','biz','design','data','pm'];
    const MARKET_SKILLS={{
      humanoid:['robotics','hardware','ml','sim'],vla:['ml','cv','robotics','data'],
      worldModel:['ml','sim','cv'],synData:['sim','data','cloud'],
      robotInfra:['cloud','fullstack','robotics'],embodied:['ml','robotics','cv'],
      manipulation:['robotics','hardware','ml'],locomotion:['robotics','hardware','sim'],
      agents:['nlp','ml','fullstack'],evalBench:['robotics','ml','data'],
      dataInfra:['cloud','data','fullstack'],multimodal:['ml','cv','data'],
    }};
    const selected=SKILLS_ARR.filter(s=>document.getElementById('sk-'+s)?.checked);
    const time=Number(document.getElementById('bm-time').value)||20;
    const budget=Number(document.getElementById('bm-budget').value)||0;
    if(!selected.length){{alert('Please select at least one skill.'); return;}}
    const breadth=selected.length/SKILLS_ARR.length;
    const depth=selected.length>=4?1:selected.length/4;
    const timeBonus=Math.min(1,time/40);
    const budgetBonus=budget>0?Math.min(0.3,budget/1000000*0.3):0;
    const gpa=Math.min(4.0,((breadth*0.35+depth*0.4+timeBonus*0.25)*4+budgetBonus)).toFixed(2);
    const matched=Object.entries(MKTS).map(([k,m])=>{{
      const req=({{...{{humanoid:['robotics','hardware','ml','sim'],vla:['ml','cv','robotics','data'],worldModel:['ml','sim','cv'],synData:['sim','data','cloud'],robotInfra:['cloud','fullstack','robotics'],embodied:['ml','robotics','cv'],manipulation:['robotics','hardware','ml'],locomotion:['robotics','hardware','sim'],agents:['nlp','ml','fullstack'],evalBench:['robotics','ml','data'],dataInfra:['cloud','data','fullstack'],multimodal:['ml','cv','data']}}}})[k]||[];
      const overlap=req.filter(r=>selected.includes(r)).length;
      const matchPct=Math.round((overlap/Math.max(req.length,1))*100);
      const s=mktScore(k);
      return {{k,m,matchPct,opp:s.opp}};
    }}).sort((a,b)=>b.matchPct*0.7+b.opp*0.3-(a.matchPct*0.7+a.opp*0.3)).slice(0,5);
    const gaps=selected.length<6?['Consider adding ' + (['hardware','cloud','biz'].filter(s=>!selected.includes(s)).slice(0,2).join(' and ') || 'complementary skills')]:[];
    const r=document.getElementById('bm-result');
    r.className='adv-result show';
    r.innerHTML=`
      <div style="text-align:center;margin-bottom:16px">
        <div style="font-size:48px;font-weight:900;color:var(--acc)">${{gpa}}</div>
        <div style="font-size:14px;color:var(--t2)">Founder GPA</div>
        <div style="font-size:12px;color:var(--muted);margin-top:4px">${{gpa>=3.7?'🔥 Exceptional — you have what it takes to ship fast':gpa>=3.0?'⚡ Strong — solid foundation, identify co-founders for gaps':'💡 Good start — partner up in weak areas'}}</div>
      </div>
      <div style="font-size:12px;font-weight:700;color:var(--t3);text-transform:uppercase;letter-spacing:.06em;margin-bottom:8px">Best Market Matches</div>
      ${{matched.map((m,i)=>`
        <div style="display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid var(--gb)">
          <span style="font-size:18px">${{m.m.icon}}</span>
          <div style="flex:1">
            <div style="font-size:13px;font-weight:700">${{m.m.label}}</div>
            <div class="adv-bar" style="height:5px;margin-top:4px"><div class="adv-bar-fill" style="width:${{m.matchPct}}%;background:${{m.m.color}}"></div></div>
          </div>
          <span style="font-size:14px;font-weight:800;color:${{m.m.color}}">${{m.matchPct}}%</span>
        </div>`).join('')}}
      ${{gaps.length?`<div style="margin-top:14px;padding:10px 14px;background:rgba(251,191,36,.08);border:1px solid rgba(251,191,36,.2);border-radius:var(--rsm);font-size:12.5px;color:#fbbf24">⚠️ Skill gap: ${{gaps[0]}}</div>`:'<div style="margin-top:14px;padding:10px 14px;background:rgba(52,211,153,.08);border:1px solid rgba(52,211,153,.2);border-radius:var(--rsm);font-size:12.5px;color:#34d399">✅ Well-rounded skill set for your matched markets</div>'}}`;
  }});
}}

/* ── Module: ProblemMine ── */
function advProblemMine() {{
  const MARKERS=['challenge','problem','limitation','lack of','difficult','lacking','absence of','gap in','fail to','struggle','insufficient','unable to','barrier'];
  const problems=[];
  const allSrc=[...(data.papers||[]),...(data.aiNews||[]),...(data.roboticsNews||[]),...(data.physicalAiNews||[])].filter(x=>!isSeed(x));
  allSrc.forEach(x=>{{
    const text=plain(x.summary||x.description||'');
    if(!text) return;
    const sentences=text.split(/[.!?]/).map(s=>s.trim()).filter(s=>s.length>20&&s.length<200);
    sentences.forEach(s=>{{
      const sl=s.toLowerCase();
      if(MARKERS.some(m=>sl.includes(m))){{
        problems.push({{problem:s,source:titleOf(x),url:hrefOf(x),date:dateOf(x),
          opp:50+Math.floor(Math.random()*45)}});
      }}
    }});
  }});
  const unique=problems.filter((p,i)=>problems.findIndex(q=>q.problem.slice(0,30)===p.problem.slice(0,30))===i);
  const top=unique.sort((a,b)=>b.opp-a.opp).slice(0,20);
  return `
  <div class="adv-metrics">
    <div class="adv-metric"><div class="adv-metric-n">${{top.length}}</div><div class="adv-metric-l">Problems Found</div></div>
    <div class="adv-metric"><div class="adv-metric-n">${{top.filter(p=>p.opp>=80).length}}</div><div class="adv-metric-l">High-Value</div></div>
    <div class="adv-metric"><div class="adv-metric-n">${{new Set(top.map(p=>p.date.slice(0,7))).size}}</div><div class="adv-metric-l">Date Ranges</div></div>
    <div class="adv-metric"><div class="adv-metric-n">Live</div><div class="adv-metric-l">Data Source</div></div>
  </div>
  <div class="adv-panel">
    <div class="adv-panel-hdr">⛏️ Real problems extracted from research papers & news</div>
    <ul class="adv-list">
      ${{top.length?top.map((p,i)=>`
        <li class="adv-item">
          <div class="adv-rank">${{i+1}}</div>
          <div class="adv-item-body">
            <div class="adv-item-title" style="font-size:13.5px;font-weight:600;color:var(--t2)">"${{esc(p.problem)}}"</div>
            <div style="margin-top:6px;display:flex;gap:8px;flex-wrap:wrap;align-items:center">
              <a href="${{esc(p.url)}}" target="_blank" style="font-size:11.5px;color:var(--acc)">📄 ${{esc(truncWords(p.source,8))}}</a>
              ${{p.date?`<span style="font-size:11px;color:var(--muted)">${{p.date}}</span>`:''}}
              <span class="adv-tag adv-tag-green">Opp: ${{p.opp}}</span>
            </div>
          </div>
        </li>`).join('')
      :`<li class="adv-item"><div style="color:var(--muted);padding:20px">No problems extracted yet — add more papers with summaries.</div></li>`}}
    </ul>
  </div>`;
}}

/* ── Module: Market Intelligence ── */
function advMarketIntel() {{
  const rows=Object.entries(MKTS).map(([k,m])=>{{const s=mktScore(k);return{{k,m,s}};}})
    .sort((a,b)=>b.s.total-a.s.total);
  return `
  <div class="adv-panel" style="overflow-x:auto">
    <div class="adv-panel-hdr">📈 Complete Market Intelligence — all tracked markets</div>
    <table class="adv-table">
      <thead>
        <tr>
          <th>Market</th><th>Papers</th><th>Funding</th><th>Jobs</th><th>Repos</th>
          <th>Models</th><th>Momentum</th><th>Competition</th><th>Opportunity</th>
        </tr>
      </thead>
      <tbody>
        ${{rows.map(r=>`
          <tr>
            <td><span style="font-weight:700">${{r.m.icon}} ${{r.m.label}}</span></td>
            <td><span style="font-weight:700;color:#34d399">${{r.s.papers}}</span></td>
            <td><span style="font-weight:700;color:#a3e635">${{r.s.funding}}</span></td>
            <td><span style="font-weight:700;color:#2dd4bf">${{r.s.jobs}}</span></td>
            <td><span style="font-weight:700;color:#60a5fa">${{r.s.repos}}</span></td>
            <td><span style="font-weight:700;color:#fb923c">${{r.s.models}}</span></td>
            <td>
              <div style="display:flex;align-items:center;gap:6px">
                <div class="adv-bar" style="width:70px"><div class="adv-bar-fill" style="width:${{r.s.momentum}}%;background:${{r.m.color}}"></div></div>
                <span style="font-size:11px">${{r.s.momentum}}</span>
              </div>
            </td>
            <td>
              <div style="display:flex;align-items:center;gap:6px">
                <div class="adv-bar" style="width:70px"><div class="adv-bar-fill" style="width:${{r.s.competition}}%;background:#f87171"></div></div>
                <span style="font-size:11px">${{r.s.competition}}</span>
              </div>
            </td>
            <td>
              <span style="font-size:16px;font-weight:900;color:${{r.m.color}}">${{r.s.opp}}</span>
            </td>
          </tr>`).join('')}}
      </tbody>
    </table>
  </div>`;
}}

/* ── Module: Research Map ── */
function advResearchMap() {{
  const PIPELINES=[
    {{area:'VLA Models',icon:'🎯',color:'#818cf8',
      steps:['VLA Papers (π, OpenVLA)','Open-source weights (HF)','Fine-tuning APIs','Task-specific deployments','Physical Intelligence, Skild AI','$700M+ raised']}},
    {{area:'World Models',icon:'🌍',color:'#a78bfa',
      steps:['Dreamer / RSSM research','Open-source simulators (MuJoCo)','World model SDKs','Sim-to-real deployment tools','NVIDIA Cosmos, GenSim2','$200M+ raised']}},
    {{area:'Humanoid Robots',icon:'🤖',color:'#f472b6',
      steps:['Whole-body control papers','Open-source platforms (Isaac)','Embodied AI models','Humanoid SDKs','Figure, 1X, Apptronik','$1.2B+ raised']}},
    {{area:'Robot Data',icon:'🗄️',color:'#34d399',
      steps:['Imitation learning research','Open-X Embodiment dataset','Teleoperation tools','Data marketplaces','Covariant, Hugging Face','$300M+ raised']}},
    {{area:'Synthetic Data',icon:'🔬',color:'#60a5fa',
      steps:['Domain randomization papers','Isaac Sim, Sapien','Sim data pipelines','Cloud render farms','NVIDIA, Scale AI (robotics)','$500M+ in space']}},
    {{area:'Robot Evaluation',icon:'📊',color:'#fbbf24',
      steps:['LIBERO / RoboSuite papers','Open benchmark suites','Eval-as-a-service tools','Standardized test rigs','Emerging startups','Pre-seed opportunity']}},
  ];
  const STEP_LABELS=['Research','Open Source','Models','Products','Startups','Funding'];
  const STEP_COLORS=['#a78bfa','#34d399','#60a5fa','#fbbf24','#f472b6','#a3e635'];
  return `
  <div style="display:flex;flex-direction:column;gap:16px">
    ${{PIPELINES.map(p=>`
      <div class="adv-panel" style="margin:0">
        <div class="adv-panel-hdr">${{p.icon}} ${{p.area}}</div>
        <div style="padding:14px 18px;overflow-x:auto">
          <div style="display:flex;align-items:center;gap:0;min-width:600px">
            ${{p.steps.map((s,i)=>`
              <div style="flex:1;text-align:center;position:relative">
                <div style="width:36px;height:36px;border-radius:50%;background:${{STEP_COLORS[i]}}22;border:2px solid ${{STEP_COLORS[i]}};display:flex;align-items:center;justify-content:center;margin:0 auto 6px;font-size:12px;font-weight:700;color:${{STEP_COLORS[i]}}">${{i+1}}</div>
                <div style="font-size:9.5px;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;margin-bottom:3px">${{STEP_LABELS[i]}}</div>
                <div style="font-size:12px;color:var(--t2);font-weight:600;padding:0 4px">${{s}}</div>
                ${{i<p.steps.length-1?`<div style="position:absolute;top:18px;right:-10px;width:20px;height:2px;background:${{STEP_COLORS[i]}}66"></div>`:''}}
              </div>`).join('')}}
          </div>
        </div>
      </div>`).join('')}}
  </div>`;
}}

/* ── Module: Startup Genome ── */
function advStartupGenome() {{
  const BUILT_IN=[
    {{name:'Physical Intelligence (π)',icon:'🎯',market:'VLA / Manipulation',stage:'Series B',funding:'$400M+',tech:'VLA models, dexterous manipulation',moat:'Research talent + data flywheel',risk:'Low',growth:'🔥',innovation:'🔬'}},
    {{name:'Figure AI',icon:'🤖',market:'Humanoid Robots',stage:'Series B',funding:'$675M',tech:'End-to-end neural humanoid control',moat:'Microsoft partnership, BMW contract',risk:'Medium',growth:'🚀',innovation:'⚡'}},
    {{name:'Skild AI',icon:'🧠',market:'General Robot Policy',stage:'Series B',funding:'$300M',tech:'Foundation model for any robot',moat:'CMU spinout, cross-embodiment data',risk:'Low',growth:'🔥',innovation:'🔬'}},
    {{name:'Covariant',icon:'💡',market:'Industrial Manipulation',stage:'Series C',funding:'$222M',tech:'RFM-1 foundation model',moat:'Production deployments + proprietary data',risk:'Low',growth:'📈',innovation:'⚡'}},
    {{name:'Apptronik',icon:'🦾',market:'Humanoid Robots',stage:'Series B',funding:'$350M',tech:'Apollo humanoid + UT Austin lineage',moat:'NASA heritage, GE partnership',risk:'Medium',growth:'📈',innovation:'⚡'}},
  ];
  const fromData=(data.companies||[]).filter(x=>!isSeed(x)).slice(0,10).map(x=>{{
    return{{name:x.company||x.title,icon:'🏢',market:x.category||x.industry||'Physical AI',
      stage:x.stage||'Early',funding:x.funding||'Undisclosed',
      tech:truncWords(x.description||x.summary||'Physical AI technology',15),
      moat:'Proprietary data & team',risk:'Medium',growth:'📈',innovation:'⚡'}};
  }});
  const all=[...BUILT_IN,...fromData];
  return `
  <div class="adv-panel">
    <div class="adv-panel-hdr">🧬 Company Genome Profiles</div>
    <ul class="adv-list">
      ${{all.map(c=>`
        <li class="adv-item">
          <div class="adv-rank" style="font-size:18px;width:36px;height:36px">${{c.icon}}</div>
          <div class="adv-item-body">
            <div class="adv-item-title">${{c.name}}</div>
            <div class="adv-item-sub">${{c.market}} · ${{c.stage}} · ${{c.funding}}</div>
            <div style="font-size:12.5px;color:var(--t3);margin:4px 0"><strong>Tech:</strong> ${{c.tech}}</div>
            <div style="font-size:12.5px;color:var(--t3);margin-bottom:6px"><strong>Moat:</strong> ${{c.moat}}</div>
            <div class="adv-scores">
              <span class="adv-tag adv-tag-blue">Risk: ${{c.risk}}</span>
              <span class="adv-tag adv-tag-green">Growth: ${{c.growth}}</span>
              <span class="adv-tag adv-tag-gold">Innovation: ${{c.innovation}}</span>
            </div>
          </div>
        </li>`).join('')}}
    </ul>
  </div>`;
}}

/* ── Module: Hidden Gems ── */
function advHiddenGems() {{
  const repos=(data.repos||[]).filter(x=>!isSeed(x)&&scoreOf(x)<500&&scoreOf(x)>0);
  const papers=(data.papers||[]).filter(x=>!isSeed(x)&&scoreOf(x)>0);
  const models=(data.models||[]).filter(x=>!isSeed(x)&&scoreOf(x)<1000&&scoreOf(x)>0);
  const gems=[
    ...repos.map(x=>{{const gemScore=Math.min(99,30+scoreOf(x)/5+Math.floor(Math.random()*20));return{{...x,_type:'repo',gemScore}};}}).sort((a,b)=>b.gemScore-a.gemScore).slice(0,6),
    ...papers.map(x=>{{const gemScore=Math.min(99,50+scoreOf(x)*10+Math.floor(Math.random()*20));return{{...x,_type:'paper',gemScore}};}}).sort((a,b)=>b.gemScore-a.gemScore).slice(0,5),
    ...models.map(x=>{{const gemScore=Math.min(99,40+scoreOf(x)/20+Math.floor(Math.random()*25));return{{...x,_type:'model',gemScore}};}}).sort((a,b)=>b.gemScore-a.gemScore).slice(0,4),
  ].sort((a,b)=>b.gemScore-a.gemScore);
  return `
  <div class="adv-metrics">
    <div class="adv-metric"><div class="adv-metric-n">${{gems.length}}</div><div class="adv-metric-l">Gems Found</div></div>
    <div class="adv-metric"><div class="adv-metric-n">${{gems.filter(g=>g._type==='repo').length}}</div><div class="adv-metric-l">Repos</div></div>
    <div class="adv-metric"><div class="adv-metric-n">${{gems.filter(g=>g._type==='paper').length}}</div><div class="adv-metric-l">Papers</div></div>
    <div class="adv-metric"><div class="adv-metric-n">${{gems.filter(g=>g._type==='model').length}}</div><div class="adv-metric-l">Models</div></div>
  </div>
  <div class="adv-panel">
    <div class="adv-panel-hdr">💎 Hidden gems — high quality, low visibility</div>
    <ul class="adv-list">
      ${{gems.length?gems.map((g,i)=>{{
        const typeIcon={{repo:'💻',paper:'📄',model:'🧠'}}[g._type]||'•';
        const typeColor={{repo:'#60a5fa',paper:'#34d399',model:'#fb923c'}}[g._type]||'#818cf8';
        return `<li class="adv-item">
          <div class="adv-rank" style="background:${{typeColor}}22;color:${{typeColor}}">${{typeIcon}}</div>
          <div class="adv-item-body">
            <div class="adv-item-title"><a href="${{esc(hrefOf(g))}}" target="_blank" style="color:var(--text);text-decoration:none;hover:color:var(--acc)">${{esc(truncWords(titleOf(g),12))}}</a></div>
            <div class="adv-item-sub">${{esc(truncWords(plain(g.summary||g.description||''),20))}}</div>
            <div class="adv-scores">
              <span class="adv-tag" style="background:${{typeColor}}22;border:1px solid ${{typeColor}}44;color:${{typeColor}}">${{g._type}}</span>
              ${{scoreOf(g)?`<span class="adv-tag adv-tag-blue">${{fmt(scoreOf(g))}} ${{{{'repo':'⭐','model':'⬇️'}}[g._type]||'📊'}}</span>`:''}}</div>
          </div>
          <div style="text-align:right;flex-shrink:0">
            <div style="font-size:22px;font-weight:900;color:#38bdf8">${{g.gemScore}}</div>
            <div style="font-size:10px;color:var(--muted)">gem score</div>
          </div>
        </li>`;
      }}).join(''):`<li class="adv-item"><div style="color:var(--muted);padding:20px">No gems found in current data — try collecting more repos or models.</div></li>`}}
    </ul>
  </div>`;
}}

/* ── Module: Investor Mode ── */
function advInvestorMode() {{
  const funding=(data.funding||[]).filter(x=>!isSeed(x));
  const byMkt=Object.entries(MKTS).map(([k,m])=>{{
    const s=mktScore(k); return {{k,m,s}};
  }}).sort((a,b)=>b.s.funding-a.s.funding);
  const recent=funding.sort((a,b)=>dateOf(b).localeCompare(dateOf(a))).slice(0,10);
  return `
  <div class="adv-metrics">
    <div class="adv-metric"><div class="adv-metric-n">${{funding.length}}</div><div class="adv-metric-l">Rounds Tracked</div></div>
    <div class="adv-metric"><div class="adv-metric-n">${{byMkt[0].m.icon}} ${{truncWords(byMkt[0].m.label,3)}}</div><div class="adv-metric-l">Hottest Market</div></div>
    <div class="adv-metric"><div class="adv-metric-n">${{byMkt.filter(r=>r.s.funding>0).length}}</div><div class="adv-metric-l">Active Markets</div></div>
    <div class="adv-metric"><div class="adv-metric-n">2026</div><div class="adv-metric-l">Cycle Peak Est.</div></div>
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px">
    <div class="adv-panel" style="margin:0">
      <div class="adv-panel-hdr">💰 Most Funded Markets</div>
      <ul class="adv-list">
        ${{byMkt.slice(0,8).map((r,i)=>`
          <li class="adv-item" style="padding:10px 16px">
            <div class="adv-rank" style="background:${{r.m.color}}22;color:${{r.m.color}}">${{i+1}}</div>
            <div class="adv-item-body">
              <div style="font-size:13px;font-weight:700">${{r.m.icon}} ${{r.m.label}}</div>
              ${{bar('',Math.min(99,r.s.funding*12),r.m.color)}}
            </div>
            <span style="font-size:14px;font-weight:800;color:${{r.m.color}}">${{r.s.funding}}</span>
          </li>`).join('')}}
      </ul>
    </div>
    <div class="adv-panel" style="margin:0">
      <div class="adv-panel-hdr">📋 Recent Funding Activity</div>
      <ul class="adv-list">
        ${{recent.length?recent.map(f=>`
          <li class="adv-item" style="padding:10px 16px">
            <div class="adv-item-body">
              <div style="font-size:13px;font-weight:700">${{esc(truncWords(titleOf(f),10))}}</div>
              <div style="font-size:11.5px;color:var(--t3);margin-top:3px">
                ${{f.amount?`<span class="adv-tag adv-tag-green">${{esc(f.amount)}}</span>`:''}}
                ${{f.stage?`<span class="adv-tag adv-tag-blue">${{esc(f.stage)}}</span>`:''}}
                ${{dateOf(f)?`<span style="color:var(--muted)">${{dateOf(f)}}</span>`:''}}
              </div>
            </div>
          </li>`).join(''):`<li class="adv-item"><div style="color:var(--muted);padding:20px">No recent funding data.</div></li>`}}
      </ul>
    </div>
  </div>`;
}}

/* ── Module: Startup Graveyard ── */
function advGraveyard() {{
  const GRAVES=[
    {{name:'Anki',icon:'🤖',founded:2010,closed:2019,raised:'$182M',why:'Consumer robotics is brutally hard — high COGS, mass market expectations, thin margins. People buy a toy once.',lesson:'B2B with recurring revenue beats B2C hardware.',revive:'High — with LLMs enabling natural voice interaction and lower BOM costs.',score:78}},
    {{name:'Jibo',icon:'🤖',founded:2012,closed:2019,raised:'$73M',why:'Too early for its vision. No app ecosystem. Looked cool, lacked utility.',lesson:'Social robots need killer apps, not just personality.',revive:'Medium — companion AI market validated by Replika.',score:65}},
    {{name:'Rethink Robotics (Baxter)',icon:'🦾',founded:2008,closed:2018,raised:'$150M',why:'Collaborative robot market was real, but Baxter was too slow and imprecise. UR ate its lunch.',lesson:'Precision and speed matter more than safety theater in industrial robotics.',revive:'Low — collaborative robot market is mature now.',score:30}},
    {{name:'Mayfield Robotics (Kuri)',icon:'🏠',founded:2015,closed:2018,raised:'$20M+',why:'Home robot with no clear utility — navigation worked, but what does it actually do for you?',lesson:'Home robots need a specific job to be done.',revive:'High — with GPT-4V and cheap LiDAR, Kuri vision is now cheap to build.',score:81}},
    {{name:'Savioke (Relay)',icon:'🛎️',founded:2013,closed:2024,raised:'$35M',why:'Hotel delivery robots worked technically but hotels found limited ROI outside novelty.',lesson:'Automation ROI must be measurable and significant.',revive:'Medium — hospital logistics is more compelling than hotels.',score:55}},
    {{name:'Robby Technologies',icon:'📦',founded:2016,closed:2020,raised:'$4.7M',why:'Last-mile delivery robot — regulatory, sidewalk access, and business model challenges.',lesson:'Regulation kills good hardware ideas prematurely.',revive:'High — Amazon Scout is dead too but DoorDash still trying.',score:72}},
    {{name:'Marble',icon:'🚗',founded:2015,closed:2019,raised:'$13M',why:'Sidewalk delivery robot — same issues as Robby. SF regulations blocked scale.',lesson:'Geography-specific regulation can kill an otherwise good product.',revive:'High — Waymo for sidewalks has a real future.',score:75}},
    {{name:'Embodied (Moxie)',icon:'🧒',founded:2016,closed:2024,raised:'$70M',why:'Therapeutic robot for children — strong product, weak business model. Subscription canceled.',lesson:'Healthcare + hardware is a brutal combination. Payor dynamics are complex.',revive:'Medium — EdTech AI companions are exploding, different distribution.',score:60}},
    {{name:'Bossa Nova Robotics',icon:'🏪',founded:2005,closed:2020,raised:'$72M',why:'Walmart canceled the contract. Store scanning was solved by humans + phone cameras.',lesson:'Do not build a $50K robot to do a $15/hr job.',revive:'Low — computer vision in stores is now a software-only play.',score:25}},
    {{name:'Perceptive Automata',icon:'🚦',founded:2016,closed:2023,raised:'$20M',why:'Predicted pedestrian behavior for AV. AV market consolidation killed most buyers.',lesson:'Tooling companies die when their target market consolidates.',revive:'Medium — humanoid robots need pedestrian prediction too.',score:58}},
  ];
  return `
  <div class="adv-metrics">
    <div class="adv-metric"><div class="adv-metric-n">${{GRAVES.length}}</div><div class="adv-metric-l">Failed Startups</div></div>
    <div class="adv-metric"><div class="adv-metric-n">${{GRAVES.filter(g=>g.score>=70).length}}</div><div class="adv-metric-l">Revival Opportunities</div></div>
    <div class="adv-metric"><div class="adv-metric-n">$600M+</div><div class="adv-metric-l">Capital Lost</div></div>
    <div class="adv-metric"><div class="adv-metric-n">10+</div><div class="adv-metric-l">Lessons Learned</div></div>
  </div>
  <div class="adv-panel">
    <div class="adv-panel-hdr">💀 AI & Robotics Startup Graveyard — Learn before you build</div>
    <ul class="adv-list">
      ${{GRAVES.map((g,i)=>`
        <li class="adv-item">
          <div class="adv-rank" style="font-size:18px;width:36px;height:36px">${{g.icon}}</div>
          <div class="adv-item-body">
            <div class="adv-item-title" style="display:flex;align-items:center;gap:8px">
              ${{g.name}}
              <span style="font-size:11px;padding:2px 7px;border-radius:5px;background:rgba(248,113,113,.12);border:1px solid rgba(248,113,113,.25);color:#f87171">💀 ${{g.founded}}–${{g.closed}}</span>
              <span style="font-size:11px;padding:2px 7px;border-radius:5px;background:rgba(163,230,53,.1);border:1px solid rgba(163,230,53,.2);color:#a3e635">Raised ${{g.raised}}</span>
            </div>
            <div style="margin:6px 0;font-size:12.5px;color:var(--t3)"><strong>Why it failed:</strong> ${{g.why}}</div>
            <div style="font-size:12.5px;color:var(--t2);background:var(--apale);padding:8px 12px;border-radius:var(--rsm);border-left:3px solid var(--acc)">
              <strong>Lesson:</strong> ${{g.lesson}}
            </div>
            <div style="margin-top:8px;font-size:12.5px;color:var(--t3)"><strong>Revival today:</strong> ${{g.revive}}</div>
          </div>
          <div style="text-align:right;flex-shrink:0;padding-top:2px">
            <div style="font-size:22px;font-weight:900;color:${{g.score>=70?'#fbbf24':'#f87171'}}">${{g.score}}</div>
            <div style="font-size:10px;color:var(--muted)">revival score</div>
          </div>
        </li>`).join('')}}
    </ul>
  </div>`;
}}

/* ── Module: Time Machine ── */
function advTimeMachine() {{
  const IDEAS=[
    {{idea:'Voice-controlled home robot assistant',failed:'2012–2018',whyFailed:'NLP was too brittle; cost too high ($500+); no killer app',whyViable:'GPT-4o + cheap speakers + home automation APIs. Amazon Echo failed to add a body; you can.',score:92}},
    {{idea:'Autonomous last-mile delivery robots',failed:'2017–2020',whyFailed:'LiDAR cost $75K; sidewalk regulations blocked deployment; unit economics broken',whyViable:'LiDAR now $200; Waymo-style mapping done; regulation catching up in EU/US.',score:84}},
    {{idea:'Robotic elder care companion',failed:'2015–2020',whyFailed:'Too expensive; required certified medical devices; limited AI capability',whyViable:'LLMs enable real companionship; aging demographics make it urgent; Japan leads.',score:88}},
    {{idea:'Robot-as-a-Service for restaurants',failed:'2018–2022',whyFailed:'Miso Robotics Flippy flopped on ROI; hardware unreliable; staff resisted',whyViable:'Better manipulation models; staff shortages permanent; unit economics improved 10×.',score:79}},
    {{idea:'Open robot operating system / cloud',failed:'2014–2019',whyFailed:'ROS1 fragmented; cloud latency too high; no killer app beyond research',whyViable:'ROS2 stable; 5G/edge compute; VLA policies need model serving infrastructure.',score:82}},
    {{idea:'AI-powered prosthetic limbs',failed:'2016–2021',whyFailed:'FDA clearance too slow; battery life inadequate; price point $50K+',whyViable:'BCI advances; modern RL control policies; consumer-grade ML enables real-time inference.',score:76}},
    {{idea:'Drone delivery network',failed:'2014–2020',whyFailed:'FAA regulations; noise complaints; reliability; weather sensitivity',whyViable:'FAA Part 135 certification now possible; Wing proved viable; regulatory path exists.',score:71}},
    {{idea:'Robotic retail store shelf scanning',failed:'2017–2020',whyFailed:'Bossa Nova canceled by Walmart; computer vision not accurate enough; ROI unclear',whyViable:'Computer vision is now solved; combine with autonomous store checkout for clear ROI.',score:58}},
  ];
  return `
  <div class="adv-metrics">
    <div class="adv-metric"><div class="adv-metric-n">${{IDEAS.filter(i=>i.score>=80).length}}</div><div class="adv-metric-l">Highly Viable</div></div>
    <div class="adv-metric"><div class="adv-metric-n">${{IDEAS[0].score}}</div><div class="adv-metric-l">Top Revival Score</div></div>
    <div class="adv-metric"><div class="adv-metric-n">${{IDEAS.length}}</div><div class="adv-metric-l">Ideas Re-Evaluated</div></div>
    <div class="adv-metric"><div class="adv-metric-n">2026</div><div class="adv-metric-l">Evaluation Year</div></div>
  </div>
  <div class="adv-panel">
    <div class="adv-panel-hdr">⏰ Failed ideas that are now viable — The graveyard is a goldmine</div>
    <ul class="adv-list">
      ${{IDEAS.sort((a,b)=>b.score-a.score).map((idea,i)=>`
        <li class="adv-item">
          <div class="adv-rank">${{i+1}}</div>
          <div class="adv-item-body">
            <div class="adv-item-title">${{idea.idea}}</div>
            <div style="margin:5px 0;font-size:12px;color:#f87171"><strong>Failed:</strong> ${{idea.failed}} — ${{idea.whyFailed}}</div>
            <div style="font-size:12.5px;color:#34d399;background:rgba(52,211,153,.06);padding:8px 12px;border-radius:var(--rsm);border-left:3px solid #34d399">
              <strong>Viable now because:</strong> ${{idea.whyViable}}
            </div>
            ${{bar('Revival Score',idea.score,'#fbbf24')}}
          </div>
          <div style="text-align:right;flex-shrink:0;padding-top:2px">
            <div style="font-size:22px;font-weight:900;color:${{idea.score>=80?'#34d399':'#fbbf24'}}">${{idea.score}}</div>
            <div style="font-size:10px;color:var(--muted)">viable now</div>
          </div>
        </li>`).join('')}}
    </ul>
  </div>`;
}}

/* ── Module: AI Co-Founder ── */
function advCoFounder() {{
  return `
  <div class="adv-panel">
    <div class="adv-panel-hdr">🤝 AI Co-Founder — Ask anything about what to build next</div>
    <div class="adv-chat">
      <div class="adv-chat-msgs" id="cf-msgs">
        <div class="adv-msg bot">👋 Hi! I'm your AI Co-Founder. I have full access to this platform's data — papers, funding, jobs, companies, and market signals.<br><br>Ask me things like:<br>• "What startup should I build in robotics?"<br>• "What market is underserved right now?"<br>• "How do I monetize this paper about VLA models?"<br>• "What's the best opportunity in simulation?"</div>
      </div>
      <div class="adv-chat-inp">
        <input class="adv-inp" id="cf-inp" type="text" placeholder="Ask your AI Co-Founder…" autocomplete="off">
        <button class="adv-btn" id="cf-send" style="height:40px;padding:0 16px">Send</button>
      </div>
    </div>
  </div>`;
}}
function advCoFounderBind() {{
  const send=()=>{{
    const inp=document.getElementById('cf-inp');
    const msgs=document.getElementById('cf-msgs');
    if(!inp||!msgs) return;
    const q=(inp.value||'').trim();
    if(!q) return;
    msgs.innerHTML+=`<div class="adv-msg user">${{esc(q)}}</div>`;
    inp.value='';
    const ql=q.toLowerCase();
    let reply='';
    const topMkt=Object.entries(MKTS).map(([k,m])=>{{const s=mktScore(k);return{{k,m,s}};}}).sort((a,b)=>b.s.opp-a.s.opp)[0];
    const topGap=Object.entries(MKTS).map(([k,m])=>{{const s=mktScore(k);const g=Math.min(99,s.papers*4+s.news*2-s.funding*6);return{{k,m,g}};}}).sort((a,b)=>b.g-a.g)[0];
    if(ql.includes('startup')||ql.includes('build')||ql.includes('idea')) {{
      reply=`Based on current signals, the highest-opportunity startup right now is in <strong>${{topMkt.m.icon}} ${{topMkt.m.label}}</strong> (opportunity score: ${{topMkt.s.opp}}/100).<br><br>Specifically: I'd build a <strong>Robot Data Flywheel Platform</strong> — no scalable marketplace exists for robot demonstration data, yet VLA model training demands are exploding. Papers: ${{topMkt.s.papers}}, Funding rounds: ${{topMkt.s.funding}}, Open jobs: ${{topMkt.s.jobs}}.<br><br>MVP: Teleoperation recorder → S3 → data marketplace. Target: robotics researchers and startups as first customers.`;
    }} else if(ql.includes('underserved')||ql.includes('gap')||ql.includes('whitespace')) {{
      reply=`The biggest gap I see: <strong>${{topGap.m.icon}} ${{topGap.m.label}}</strong> — gap score ${{topGap.g}}/100. This means there's strong research activity (${{topGap.s?.papers||0}} papers) but very few commercial products exist yet.<br><br>This is classic "research valley of death" territory — the perfect place to build a bridge. The academic papers have proven the concept works; now someone needs to productize it.`;
    }} else if(ql.includes('fund')||ql.includes('invest')||ql.includes('raise')) {{
      const topFunded=Object.entries(MKTS).map(([k,m])=>{{const s=mktScore(k);return{{k,m,s}};}}).sort((a,b)=>b.s.funding-a.s.funding)[0];
      reply=`Investors are most active in <strong>${{topFunded.m.icon}} ${{topFunded.m.label}}</strong> right now (${{topFunded.s.funding}} tracked rounds).<br><br>To fundraise in 2026: 1) Show real robot demos, not slides. 2) Have a data story — how will you collect proprietary training data? 3) Target Khosla Ventures, Lux Capital, GV, and Coatue — all active in physical AI. 4) Your pre-seed ask should be $1-3M with a 12-month runway to robot demo.`;
    }} else if(ql.includes('simulation')||ql.includes('sim')) {{
      const s=mktScore('synData');
      reply=`Simulation is one of the hottest infrastructure bets. Key signals: ${{s.papers}} papers, ${{s.repos}} repos, ${{s.jobs}} open roles.<br><br>Opportunity: Build a <strong>Sim2Real Validation SaaS</strong> — companies training on Isaac Sim or MuJoCo have no standardized way to validate that their policy will actually work on real hardware. $800M addressable market by 2028.`;
    }} else if(ql.includes('vla')||ql.includes('vision language action')) {{
      const s=mktScore('vla');
      reply=`VLA models are the hottest research area right now. ${{s.papers}} papers, ${{s.funding}} funding rounds.<br><br>Best commercial angle: <strong>VLA Fine-Tuning API</strong> — Physical Intelligence and OpenVLA are releasing foundation models, but every industrial customer needs domain adaptation. Build the "Replicate for VLA" — 1-click fine-tuning on custom manipulation demos. $2.4B market by 2028.`;
    }} else if(ql.includes('paper')||ql.includes('research')||ql.includes('monetize')) {{
      const rp=(data.papers||[]).filter(x=>!isSeed(x)).sort((a,b)=>dateOf(b).localeCompare(dateOf(a)))[0];
      reply=`The fastest path from paper to product:<br>1. <strong>Reproduce it</strong> — get the code working as a Python package<br>2. <strong>API-ify it</strong> — wrap it in FastAPI or a Cloudflare Worker<br>3. <strong>Find 3 paying design partners</strong> — robotics startups who need this exact capability<br>4. <strong>Charge per inference</strong> — $0.01–0.10 per call<br><br>Latest paper to consider: <a href="${{esc(hrefOf(rp))}}" target="_blank" style="color:var(--acc)">${{esc(truncWords(titleOf(rp),15))}}</a>`;
    }} else if(ql.includes('job')||ql.includes('career')||ql.includes('skill')) {{
      const topJobMkt=Object.entries(MKTS).map(([k,m])=>{{const s=mktScore(k);return{{k,m,s}};}}).sort((a,b)=>b.s.jobs-a.s.jobs)[0];
      reply=`Most in-demand skills right now based on job postings:<br>1. 🤖 <strong>ROS2</strong> — every robotics company needs this<br>2. 🔬 <strong>PyTorch + transformers</strong> — foundation for robot learning<br>3. ☁️ <strong>Cloud infra (AWS/GCP)</strong> — robot data pipelines<br>4. 👁️ <strong>Computer vision</strong> — always in demand<br><br>Most hiring: ${{topJobMkt.m.icon}} ${{topJobMkt.m.label}} (${{topJobMkt.s.jobs}} open roles).<br><br>Check the Certification Hub module for free learning resources.`;
    }} else {{
      reply=`I analyzed the current signals for your question. Here's what the data says:<br><br>📊 <strong>Top market right now:</strong> ${{topMkt.m.icon}} ${{topMkt.m.label}} (score: ${{topMkt.s.opp}})<br>🔍 <strong>Biggest gap:</strong> ${{topGap.m.icon}} ${{topGap.m.label}} (gap: ${{topGap.g}})<br>📄 <strong>Research activity:</strong> ${{(data.papers||[]).filter(x=>!isSeed(x)).length}} papers tracked<br>💰 <strong>Funding activity:</strong> ${{(data.funding||[]).filter(x=>!isSeed(x)).length}} rounds<br><br>Try asking: "What startup should I build?", "What market is underserved?", or "How do I monetize a VLA paper?"`;
    }}
    setTimeout(()=>{{
      msgs.innerHTML+=`<div class="adv-msg bot">${{reply}}</div>`;
      msgs.scrollTop=msgs.scrollHeight;
    }},400);
    msgs.scrollTop=msgs.scrollHeight;
  }};
  const btn=document.getElementById('cf-send');
  const inp=document.getElementById('cf-inp');
  if(btn) btn.addEventListener('click',send);
  if(inp) inp.addEventListener('keydown',e=>{{ if(e.key==='Enter') send(); }});
}}

/* ── Module: Certification Hub ── */
function advCertHub() {{
  const CERTS=[
    {{name:'Deep Learning Specialization',org:'deeplearning.ai / Coursera',free:'Audit free',time:'3 months',level:'Intermediate',link:'https://www.coursera.org/specializations/deep-learning',skills:['PyTorch','Neural Networks','Computer Vision'],color:'#818cf8'}},
    {{name:'Self-Driving Cars Specialization',org:'University of Toronto / Coursera',free:'Audit free',time:'4 months',level:'Advanced',link:'https://www.coursera.org/specializations/self-driving-cars',skills:['State Estimation','Visual Perception','Motion Planning'],color:'#60a5fa'}},
    {{name:'Robot Operating System (ROS2)',org:'The Construct',free:'Free basics',time:'6 weeks',level:'Beginner',link:'https://www.theconstructsim.com/',skills:['ROS2','Gazebo','Python'],color:'#2dd4bf'}},
    {{name:'Reinforcement Learning Specialization',org:'University of Alberta',free:'Audit free',time:'4 months',level:'Intermediate',link:'https://www.coursera.org/specializations/reinforcement-learning',skills:['RL','Policy Gradient','Q-Learning'],color:'#fbbf24'}},
    {{name:'Hugging Face Course',org:'Hugging Face',free:'Completely free',time:'4 weeks',level:'Beginner',link:'https://huggingface.co/learn',skills:['Transformers','Fine-tuning','Diffusion'],color:'#fb923c'}},
    {{name:'Fast.ai Practical Deep Learning',org:'fast.ai',free:'Completely free',time:'7 weeks',level:'Intermediate',link:'https://course.fast.ai/',skills:['Computer Vision','NLP','Deployment'],color:'#34d399'}},
    {{name:'MIT OpenCourseWare: Robotics',org:'MIT OCW',free:'Completely free',time:'Self-paced',level:'Advanced',link:'https://ocw.mit.edu/search/?t=Robotics',skills:['Kinematics','Motion Planning','Control'],color:'#a78bfa'}},
    {{name:'Google ML Crash Course',org:'Google',free:'Completely free',time:'3 weeks',level:'Beginner',link:'https://developers.google.com/machine-learning/crash-course',skills:['TensorFlow','ML Fundamentals'],color:'#f472b6'}},
  ];
  const FELLOWSHIPS=[
    {{name:'NVIDIA AI Research Fellowship',award:'$50K grant + mentorship',deadline:'Annual',focus:'Deep learning & computer vision',link:'https://research.nvidia.com/'}},
    {{name:'Open Philanthropy AI Fellowship',award:'$50K–$100K',deadline:'Annual',focus:'AI safety & capability research',link:'https://www.openphilanthropy.org/'}},
    {{name:'Hertz Fellowship',award:'Up to $250K PhD funding',deadline:'Oct annually',focus:'Applied science & engineering',link:'https://www.hertzfoundation.org/'}},
    {{name:'NSF Graduate Research Fellowship',award:'$37K/yr stipend',deadline:'Oct annually',focus:'STEM research',link:'https://www.nsfgrfp.org/'}},
  ];
  return `
  <div class="adv-metrics">
    <div class="adv-metric"><div class="adv-metric-n">${{CERTS.length}}</div><div class="adv-metric-l">Free Courses</div></div>
    <div class="adv-metric"><div class="adv-metric-n">${{FELLOWSHIPS.length}}</div><div class="adv-metric-l">Fellowships</div></div>
    <div class="adv-metric"><div class="adv-metric-n">$0</div><div class="adv-metric-l">Cost to Start</div></div>
    <div class="adv-metric"><div class="adv-metric-n">ROS2</div><div class="adv-metric-l">Most In-Demand</div></div>
  </div>
  <div class="adv-panel" style="margin-bottom:14px">
    <div class="adv-panel-hdr">🎯 Free Certifications & Courses for Physical AI Builders</div>
    <ul class="adv-list">
      ${{CERTS.map(c=>`
        <li class="adv-item">
          <div class="adv-rank" style="background:${{c.color}}22;color:${{c.color}};font-size:16px">📚</div>
          <div class="adv-item-body">
            <div class="adv-item-title"><a href="${{esc(c.link)}}" target="_blank" style="color:var(--text)">${{c.name}}</a></div>
            <div class="adv-item-sub">${{c.org}} · ${{c.time}} · ${{c.level}}</div>
            <div class="adv-scores">
              <span class="adv-tag adv-tag-green">${{c.free}}</span>
              ${{c.skills.map(s=>`<span class="adv-tag adv-tag-blue">${{s}}</span>`).join('')}}
            </div>
          </div>
        </li>`).join('')}}
    </ul>
  </div>
  <div class="adv-panel">
    <div class="adv-panel-hdr">🏆 Fellowships & Grants for AI Researchers</div>
    <ul class="adv-list">
      ${{FELLOWSHIPS.map(f=>`
        <li class="adv-item">
          <div class="adv-rank" style="font-size:16px">🎓</div>
          <div class="adv-item-body">
            <div class="adv-item-title"><a href="${{esc(f.link)}}" target="_blank" style="color:var(--text)">${{f.name}}</a></div>
            <div class="adv-item-sub">${{f.focus}} · Deadline: ${{f.deadline}}</div>
            <span class="adv-tag adv-tag-green">${{f.award}}</span>
          </div>
        </li>`).join('')}}
    </ul>
  </div>`;
}}

/* ── Module: Daily Founder Brief ── */
function advDailyBrief() {{
  const topPaper=(data.papers||[]).filter(x=>!isSeed(x)).sort((a,b)=>dateOf(b).localeCompare(dateOf(a)))[0]||{{}};
  const topFunding=(data.funding||[]).filter(x=>!isSeed(x)).sort((a,b)=>dateOf(b).localeCompare(dateOf(a)))[0]||{{}};
  const topRepo=(data.repos||[]).filter(x=>!isSeed(x)).sort((a,b)=>scoreOf(b)-scoreOf(a))[0]||{{}};
  const topNews=[...(data.physicalAiNews||[]),...(data.roboticsNews||[])].filter(x=>!isSeed(x)).sort((a,b)=>dateOf(b).localeCompare(dateOf(a)))[0]||{{}};
  const topMkt=Object.entries(MKTS).map(([k,m])=>{{const s=mktScore(k);return{{k,m,s}};}}).sort((a,b)=>b.s.opp-a.s.opp)[0];
  const topGap=Object.entries(MKTS).map(([k,m])=>{{const s=mktScore(k);const g=Math.min(99,s.papers*4-s.funding*6+20);return{{k,m,g}};}}).sort((a,b)=>b.g-a.g)[0];
  const today=new Date().toLocaleDateString('en-US',{{weekday:'long',year:'numeric',month:'long',day:'numeric'}});
  const section=(label,icon,content)=>
    `<div class="adv-brief-section"><div class="adv-brief-label">${{icon}} ${{label}}</div>${{content}}</div>`;
  return `
  <div class="adv-hero" style="text-align:left;padding:20px 24px">
    <div style="font-size:12px;font-weight:700;color:var(--acc);letter-spacing:.08em;text-transform:uppercase;margin-bottom:5px">Daily Founder Brief</div>
    <div class="adv-hero-title" style="font-size:22px">${{today}}</div>
    <div class="adv-hero-sub">Your daily intelligence digest for Physical AI builders</div>
  </div>
  ${{section('Top Market Signal','📡',`
    <div class="adv-panel" style="padding:16px 18px;margin:0">
      <div style="font-size:15px;font-weight:800">${{topMkt.m.icon}} ${{topMkt.m.label}} — Opportunity Score ${{topMkt.s.opp}}</div>
      <div style="font-size:13px;color:var(--t2);margin-top:5px">
        ${{topMkt.s.papers}} papers · ${{topMkt.s.funding}} funding rounds · ${{topMkt.s.jobs}} open jobs
      </div>
      ${{bar('Momentum',topMkt.s.momentum,topMkt.m.color)}}
    </div>`)}}
  ${{section('Top Research Paper','📄',`
    <div class="adv-panel" style="padding:16px 18px;margin:0">
      <a href="${{esc(hrefOf(topPaper))}}" target="_blank" style="font-size:14px;font-weight:700;color:var(--text)">${{esc(truncWords(titleOf(topPaper),15))}}</a>
      ${{Array.isArray(topPaper.authors)&&topPaper.authors.length?`<div style="font-size:12px;color:var(--t3);margin-top:4px">${{topPaper.authors.slice(0,3).join(', ')}}${{topPaper.authors.length>3?' et al.':''}}</div>`:''}}</div>`)}}
  ${{section('Biggest Gap Opportunity','🔍',`
    <div class="adv-panel" style="padding:16px 18px;margin:0">
      <div style="font-size:14px;font-weight:700">${{topGap.m.icon}} ${{topGap.m.label}} — ${{topGap.g}} gap score</div>
      <div style="font-size:13px;color:var(--t2);margin-top:5px">Strong research activity. Few commercial solutions. High demand. Build here.</div>
    </div>`)}}
  ${{topFunding&&titleOf(topFunding)?section('Latest Funding Round','💰',`
    <div class="adv-panel" style="padding:16px 18px;margin:0">
      <div style="font-size:14px;font-weight:700">${{esc(truncWords(titleOf(topFunding),12))}}</div>
      <div style="font-size:13px;color:var(--t2);margin-top:4px">
        ${{topFunding.amount?`<span class="adv-tag adv-tag-green">${{esc(topFunding.amount)}}</span>`:''}}
        ${{topFunding.stage?`<span class="adv-tag adv-tag-blue">${{esc(topFunding.stage)}}</span>`:''}}
        ${{dateOf(topFunding)?`<span style="color:var(--muted);font-size:12px;margin-left:6px">${{dateOf(topFunding)}}</span>`:''}}
      </div>
    </div>`):''}}</div>`;
  return `<div class="adv-wrap">` + section('placeholder','','') + `</div>`;
}}

/* ── Module: Signal Score Engine ── */
function advSignalEngine() {{
  const WEIGHTS={{research:3,funding:5,hiring:1,openSource:2,news:2}};
  const calcSignal=(item,type)=>{{
    const txt=JSON.stringify(item).toLowerCase();
    const hasMkt=k=>MKTS[k].kw.some(w=>txt.includes(w));
    const mktBonus=Object.keys(MKTS).filter(hasMkt).length*4;
    if(type==='paper') return Math.min(99,scoreOf(item)*10+mktBonus+20);
    if(type==='repo')  return Math.min(99,Math.log1p(scoreOf(item))*10+mktBonus+10);
    if(type==='model') return Math.min(99,Math.log1p(scoreOf(item))*8+mktBonus+15);
    return Math.min(99,mktBonus+25);
  }};
  const allItems=[
    ...(data.papers||[]).filter(x=>!isSeed(x)).map(x=>{{return{{...x,_type:'paper',_sig:calcSignal(x,'paper')}};}}),
    ...(data.repos||[]).filter(x=>!isSeed(x)).map(x=>{{return{{...x,_type:'repo',_sig:calcSignal(x,'repo')}};}}),
    ...(data.models||[]).filter(x=>!isSeed(x)).map(x=>{{return{{...x,_type:'model',_sig:calcSignal(x,'model')}};}}),
    ...(data.funding||[]).filter(x=>!isSeed(x)).map(x=>{{return{{...x,_type:'funding',_sig:calcSignal(x,'funding')}};}}),
  ].sort((a,b)=>b._sig-a._sig).slice(0,25);
  const byType=t=>allItems.filter(x=>x._type===t).length;
  const typeIcon={{paper:'📄',repo:'💻',model:'🧠',funding:'💰'}};
  const typeColor={{paper:'#34d399',repo:'#60a5fa',model:'#fb923c',funding:'#a3e635'}};
  return `
  <div class="adv-metrics">
    <div class="adv-metric"><div class="adv-metric-n">${{allItems[0]?._sig||0}}</div><div class="adv-metric-l">Top Signal Score</div></div>
    <div class="adv-metric"><div class="adv-metric-n">${{allItems.filter(x=>x._sig>=80).length}}</div><div class="adv-metric-l">High Signal Items</div></div>
    <div class="adv-metric"><div class="adv-metric-n">${{allItems.length}}</div><div class="adv-metric-l">Items Ranked</div></div>
    <div class="adv-metric"><div class="adv-metric-n">Live</div><div class="adv-metric-l">Data Freshness</div></div>
  </div>
  <div class="adv-panel">
    <div class="adv-panel-hdr">⚡ Universal Signal Score Rankings — Top 25 signals across all categories</div>
    <ul class="adv-list">
      ${{allItems.map((x,i)=>{{
        const tc=typeColor[x._type]||'#818cf8';
        const ti=typeIcon[x._type]||'•';
        return `<li class="adv-item">
          <div class="adv-rank" style="background:${{tc}}22;color:${{tc}}">${{i+1}}</div>
          <div class="adv-item-body">
            <div class="adv-item-title">
              <a href="${{esc(hrefOf(x))}}" target="_blank" style="color:var(--text)">${{esc(truncWords(titleOf(x),12))}}</a>
            </div>
            <div class="adv-scores">
              <span class="adv-tag" style="background:${{tc}}22;border:1px solid ${{tc}}44;color:${{tc}}">${{ti}} ${{x._type}}</span>
              ${{scoreOf(x)?`<span class="adv-tag adv-tag-blue">${{fmt(scoreOf(x))}}</span>`:''}}</div>
          </div>
          <div style="text-align:right;flex-shrink:0">
            <div style="font-size:22px;font-weight:900;color:${{tc}}">${{x._sig}}</div>
            <div style="font-size:10px;color:var(--muted)">signal</div>
          </div>
        </li>`;
      }}).join('')}}
    </ul>
  </div>`;
}}

/* ── ADVANCED main renderer ── */
function renderAdvanced() {{
  const wrap=document.getElementById('advWrap');
  if(state.advMod) {{
    const mod=ADV_MODS.find(m=>m.id===state.advMod);
    let content='<div style="color:var(--muted);padding:40px;text-align:center">Module coming soon.</div>';
    if(state.advMod==='opportunity_radar') content=advOpportunityRadar();
    else if(state.advMod==='gapfinder')       content=advGapFinder();
    else if(state.advMod==='future_unicorn')  content=advFutureUnicorn();
    else if(state.advMod==='startup_ideas')   content=advStartupIdeas();
    else if(state.advMod==='startup_validator') content=advStartupValidator();
    else if(state.advMod==='builder_match')   content=advBuilderMatch();
    else if(state.advMod==='problemmine')     content=advProblemMine();
    else if(state.advMod==='market_intel')    content=advMarketIntel();
    else if(state.advMod==='research_map')    content=advResearchMap();
    else if(state.advMod==='startup_genome')  content=advStartupGenome();
    else if(state.advMod==='hidden_gems')     content=advHiddenGems();
    else if(state.advMod==='investor_mode')   content=advInvestorMode();
    else if(state.advMod==='graveyard')       content=advGraveyard();
    else if(state.advMod==='time_machine')    content=advTimeMachine();
    else if(state.advMod==='cofounder')       content=advCoFounder();
    else if(state.advMod==='cert_hub')        content=advCertHub();
    else if(state.advMod==='daily_brief')     content=advDailyBrief();
    else if(state.advMod==='signal_engine')   content=advSignalEngine();
    wrap.innerHTML=`
      <button class="adv-back" id="advBack">← Back to Advanced Hub</button>
      <div class="adv-mod-hdr">
        <div class="adv-mod-ico">${{mod?.icon||'🚀'}}</div>
        <div>
          <div class="adv-mod-title">${{mod?.label||state.advMod}}</div>
          <div class="adv-mod-sub">${{mod?.desc||''}}</div>
        </div>
      </div>
      ${{content}}`;
    document.getElementById('advBack')?.addEventListener('click',()=>{{
      state.advMod=null; renderAdvanced();
    }});
    /* bind interactive modules */
    if(state.advMod==='startup_validator') advStartupValidatorBind();
    else if(state.advMod==='builder_match') advBuilderMatchBind();
    else if(state.advMod==='cofounder') advCoFounderBind();
  }} else {{
    wrap.innerHTML=renderAdvHub();
    wrap.querySelectorAll('.adv-hcard').forEach(c=>c.addEventListener('click',()=>{{
      state.advMod=c.dataset.mod; renderAdvanced();
      document.querySelector('.main').scrollTo({{top:0,behavior:'smooth'}});
    }}));
  }}
}}

/* ── init ── */
syncVT();
render();
</script>
</body>
</html>
"""
    (ROOT_DIR / "index.html").write_text(html, encoding="utf-8")

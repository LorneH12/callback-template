"""Render Callback promo shorts (1080x1920) from real template screenshots.

Slides and caption layers are HTML rendered by headless Edge; ffmpeg animates the
template scrolls and stitches segments. No audio: add a trending sound in-app.
"""
import json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
IMG = ROOT.parent / "img"
OUT = ROOT / "out"
TMP = ROOT / "tmp"
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
W, H, FPS = 1080, 1920, 30
PHONE_W = 860            # phone.jpg is drawn at this width
PHONE_SRC_H = 8152 * PHONE_W / 390

FONTS = '<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,700&family=Inter:wght@500;700&display=swap" rel="stylesheet">'
BASE = """*{margin:0;box-sizing:border-box}html,body{width:1080px;height:1920px}
body{font-family:Inter,sans-serif;-webkit-font-smoothing:antialiased}
.h{font-family:Fraunces,serif;font-weight:700;letter-spacing:-.025em;line-height:1}
.cap{position:absolute;left:60px;right:60px;top:110px;display:flex;flex-direction:column;align-items:flex-start;gap:18px}
.cap span{background:#141210;color:#fff;font:700 64px/1.08 Inter,sans-serif;padding:14px 26px;border-radius:18px;text-transform:uppercase;letter-spacing:-.01em}
.cap span.k{background:#f6f2ea;color:#141210}
.tag{position:absolute;left:60px;bottom:96px;font:500 34px/1.3 Inter,sans-serif;color:#141210;background:#f6f2ea;padding:10px 20px;border-radius:14px}
"""


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"failed: {' '.join(map(str, cmd))}\n{r.stderr[-2000:]}")


def render_html(name, body, transparent=False):
    html = TMP / f"{name}.html"
    bg = "transparent" if transparent else "#f6f2ea"
    html.write_text(f"<!doctype html><html><head><meta charset=utf-8>{FONTS}<style>{BASE}body{{background:{bg};position:relative}}</style></head><body>{body}</body></html>", encoding="utf-8")
    png = TMP / f"{name}.png"
    cmd = [EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--window-size={W},{H}",
           "--virtual-time-budget=3000", f"--screenshot={png}", html.as_uri()]
    if transparent:
        cmd.insert(4, "--default-background-color=00000000")
    run(cmd)
    return png


def card(name, title, sub="", foot="", dark=False):
    bg, ink, soft = ("#141210", "#f6f2ea", "#cfc8bc") if dark else ("#f6f2ea", "#141210", "#4d473f")
    body = f"""<div style="position:absolute;inset:0;background:{bg};padding:120px 72px;display:flex;flex-direction:column;justify-content:center;gap:48px">
      <p class="h" style="font-size:120px;color:{ink}">{title}</p>
      {f'<p style="font:500 48px/1.35 Inter;color:{soft}">{sub}</p>' if sub else ''}
      {f'<p style="position:absolute;left:72px;right:72px;bottom:110px;font:700 40px/1.3 Inter;color:{ink}">{foot}</p>' if foot else ''}
    </div>"""
    return render_html(name, body)


def caption(name, lines, tag="I built this · Callback template"):
    spans = "".join(f'<span class="{"k" if i == len(lines) - 1 else ""}">{l}</span>' for i, l in enumerate(lines))
    return render_html(name, f'<div class="cap">{spans}</div><p class="tag">{tag}</p>', transparent=True)


def seg_card(name, png, secs):
    out = TMP / f"{name}.mp4"
    run(["ffmpeg", "-loglevel", "error", "-y", "-loop", "1", "-t", str(secs), "-i", png,
         "-vf", f"scale={W}:{H},zoompan=z='min(1+on/{secs*FPS}*0.04,1.04)':d=1:s={W}x{H}:fps={FPS},format=yuv420p",
         "-r", str(FPS), "-c:v", "libx264", "-crf", "20", "-preset", "medium", out])
    return out


def seg_scroll(name, y0, y1, secs, cap_png):
    """Scroll the phone screenshot from source-y y0 to y1 (in 390-wide units) under a caption."""
    s = PHONE_W / 390
    a, b = y0 * s, min(y1 * s, PHONE_SRC_H - 1360)
    win_h = 1360
    out = TMP / f"{name}.mp4"
    fc = (f"color=c=0x1f7a4d:s={W}x{H}:r={FPS}:d={secs}[bg];"
          f"[1:v]scale={PHONE_W}:-1,crop={PHONE_W}:{win_h}:0:'{a}+({b}-{a})*min(t/{secs*0.85},1)'[ph];"
          f"[bg][ph]overlay=(W-w)/2:470[v1];[v1][2:v]overlay=0:0,format=yuv420p[v]")
    run(["ffmpeg", "-loglevel", "error", "-y", "-f", "lavfi", "-i", "anullsrc", "-loop", "1", "-t", str(secs), "-i", IMG / "phone.jpg",
         "-loop", "1", "-t", str(secs), "-i", cap_png, "-filter_complex", fc, "-map", "[v]", "-t", str(secs), "-r", str(FPS),
         "-c:v", "libx264", "-crf", "20", "-preset", "medium", out])
    return out


def stitch(name, parts):
    lst = TMP / f"{name}.txt"
    lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in parts), encoding="utf-8")
    out = OUT / f"{name}.mp4"
    run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c:v", "libx264", "-crf", "21",
         "-preset", "medium", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out])
    run(["ffmpeg", "-loglevel", "error", "-y", "-ss", "0.5", "-i", out, "-frames:v", "1", "-q:v", "3", OUT / f"{name}-cover.jpg"])
    return out


ENDS = {
    "ig": ("Comment “CALLBACK”", "I’ll DM you the template link and a free website checklist.", "Follow so my DM lands in your inbox · I built and sell this template"),
    "link": ("Callback", "A Framer website template for local service businesses. $29.", "Link in bio · I built and sell this template"),
}


def main():
    OUT.mkdir(exist_ok=True); TMP.mkdir(exist_ok=True)
    for tag, end_text in ENDS.items():
        build(tag, seg_card(f"end-{tag}", card(f"end-{tag}", *end_text, dark=True), 3.5))


def build(tag, end):
    sfx = "" if tag == "link" else f"-{tag}"

    # 1. Three fixes (problem → solution)
    v1 = [seg_card("v1a", card("v1a", "Your website is losing you calls.", "3 fixes I built into a template for local businesses"), 2.5),
          seg_scroll("v1b", 0, 120, 6, caption("v1b", ["Fix 1", "Phone number", "on every screen"])),
          seg_scroll("v1c", 1340, 1900, 6, caption("v1c", ["Fix 2", "Prices", "up front"])),
          seg_scroll("v1d", 6250, 6900, 6, caption("v1d", ["Fix 3", "A quote form", "people finish"])),
          end]
    # 2. The whole template, fast
    v2 = [seg_card("v2a", card("v2a", "I built a website for cleaners.", "Here’s every section, in 15 seconds."), 2.2),
          seg_scroll("v2b", 0, 7400, 15, caption("v2b", ["The whole", "template"])),
          end]
    # 3. Checkout to live
    steps = [("Buy + open", "2 min"), ("Name, phone,", "colours: 20 min"), ("Photos +", "prices: 30 min"), ("Form → inbox", "5 min"), ("Publish", "15 min")]
    v3 = [seg_card("v3a", card("v3a", "From checkout to live in about 90 minutes.", "No code. Here’s the whole job."), 2.5)]
    ys = [0, 60, 1340, 6250, 7400]
    for i, (a, b) in enumerate(steps):
        v3.append(seg_scroll(f"v3s{i}", ys[i], ys[i] + 400, 3.2, caption(f"v3s{i}", [a, b])))
    v3.append(end)

    made = [stitch(f"callback-3-fixes{sfx}", v1), stitch(f"callback-whole-template{sfx}", v2), stitch(f"callback-90-minutes{sfx}", v3)]
    print(json.dumps([str(m) for m in made], indent=1))


if __name__ == "__main__":
    main()

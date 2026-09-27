import re, math
from xml.sax.saxutils import escape
from PIL import ImageFont
_FC = {}
def _font(size, bold):
    k = (round(size*4), bold)
    if k not in _FC:
        f = "/usr/share/fonts/opentype/noto/NotoSansCJK-%s.ttc" % ("Bold" if bold else "Regular")
        _FC[k] = ImageFont.truetype(f, size=k[0]/4*10, index=3)   # index 3 = TC
    return _FC[k]
_SPL = r"(_\{[^}]*\}|_.|\^\{[^}]*\}|\^.)"
def measure(s, size, bold=False):
    s = s.replace("'", "′"); w = 0.0
    for p in re.split(_SPL, s):
        if not p: continue
        if p[0] in "_^":
            t = p[2:-1] if p[1] == "{" else p[1:]
            w += _font(size*0.68, bold).getlength(t)/10
        else:
            w += _font(size, bold).getlength(p)/10
    return w
FONT = "Noto Sans CJK TC, Microsoft JhengHei, PingFang TC, sans-serif"
INK, MUTED, GRID, PANEL = "#1F2A37", "#6B7280", "#E3E7EC", "#F4F6F9"

def rich(s, size):
    """_x / _{xx} 下標；^x / ^{xx} 上標"""
    s = s.replace("'", "′")
    out, shift = [], 0.0
    for p in re.split(_SPL, s):
        if not p: continue
        if p[0] in "_^":
            t = p[2:-1] if p[1] == "{" else p[1:]
            target = size*0.28 if p[0] == "_" else -size*0.38
            out.append(f'<tspan font-size="{size*0.68:.1f}" dy="{target-shift:.1f}">{escape(t)}</tspan>'); shift = target
        else:
            if shift:
                out.append(f'<tspan dy="{-shift:.1f}">{escape(p)}</tspan>'); shift = 0.0
            else:
                out.append(escape(p))
    return "".join(out)

class SVG:
    def __init__(s, w, h, bg=None, ts=1.0):
        s.w, s.h, s.el, s.ts = w, h, [], ts
        if bg: s.rect(0, 0, w, h, fill=bg, stroke="none")
    def add(s, e): s.el.append(e); return s
    def text(s, x, y, t, size=18, color=INK, anchor="start", weight="normal", italic=False, bg=None, rot=None):
        size = size * s.ts; b = weight == "bold"
        wd = measure(t, size, b)
        x0 = x - (wd/2 if anchor == "middle" else wd if anchor == "end" else 0)
        if bg: s.rect(x0-4, y-size*0.92, wd+8, size*1.22, fill=bg, stroke="none", rx=3)
        st = ' font-style="italic"' if italic else ''
        tr = f' transform="rotate({rot} {x:.1f} {y:.1f})"' if rot is not None else ''
        return s.add(f'<text x="{x0:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size}" fill="{color}" font-weight="{weight}"{st}{tr}>{rich(t, size)}</text>')
    def rect(s, x, y, w, h, fill="none", stroke=INK, sw=1.5, rx=0, dash=None, op=None):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        o = f' fill-opacity="{op}"' if op is not None else ''
        return s.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}{o}/>')
    def line(s, x1, y1, x2, y2, color=INK, sw=2, dash=None, cap="butt"):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        return s.add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="{sw}" stroke-linecap="{cap}"{d}/>')
    def poly(s, pts, color=INK, sw=2, fill="none", dash=None, closed=False, op=None):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        o = f' fill-opacity="{op}"' if op is not None else ''
        tag = "polygon" if closed else "polyline"
        P = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        return s.add(f'<{tag} points="{P}" fill="{fill}" stroke="{color}" stroke-width="{sw}" stroke-linejoin="round"{d}{o}/>')
    def circle(s, x, y, r, fill=INK, stroke="#FFFFFF", sw=2.5):
        return s.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
    def arc(s, cx, cy, rad, a1, a2, color=INK, sw=1.6):
        """角度以數學方向（度，逆時針為正；SVG y 向下自動換算）"""
        x1, y1 = cx + rad*math.cos(math.radians(a1)), cy - rad*math.sin(math.radians(a1))
        x2, y2 = cx + rad*math.cos(math.radians(a2)), cy - rad*math.sin(math.radians(a2))
        large = 1 if abs(a2-a1) > 180 else 0; sweep = 0 if a2 > a1 else 1
        return s.add(f'<path d="M{x1:.1f},{y1:.1f} A{rad},{rad} 0 {large} {sweep} {x2:.1f},{y2:.1f}" fill="none" stroke="{color}" stroke-width="{sw}"/>')
    def arrow(s, x1, y1, x2, y2, color=INK, sw=2.2, head=11, dash=None):
        a = math.atan2(y2-y1, x2-x1)
        bx, by = x2 - head*math.cos(a), y2 - head*math.sin(a)
        s.line(x1, y1, bx, by, color, sw, dash)
        p2 = (bx + head*0.5*math.sin(a), by - head*0.5*math.cos(a))
        p3 = (bx - head*0.5*math.sin(a), by + head*0.5*math.cos(a))
        return s.poly([(x2, y2), p2, p3], color=color, sw=1, fill=color, closed=True)
    def save(s, path):
        body = "\n".join(s.el)
        open(path, "w", encoding="utf-8").write(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {s.w} {s.h}" width="{s.w}" height="{s.h}">\n{body}\n</svg>\n')

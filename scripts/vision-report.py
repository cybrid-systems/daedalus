#!/usr/bin/env python3
"""Photo → Grok 4.6 IR → schematic HTML + .tran waveform report.

Usage (from repo root):
  ./scripts/vision-report.sh examples/10-vision-pipeline/out/3led.jpeg
  ./scripts/vision-report.py photo.jpg --skip-extract   # reuse out/<stem>.json
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "examples" / "10-vision-pipeline" / "out"
KEY_FILE = Path.home() / "code" / "keys" / "grok"
DEFAULT_MODEL = "grok-4.6"

LED_COLORS = {
    "red": "#e11d48",
    "green": "#16a34a",
    "yellow": "#ca8a04",
    "orange": "#ea580c",
}
TRACE_FALLBACK = ("#2563eb", "#7c3aed", "#0f766e", "#b45309", "#334155")


def die(msg: str, code: int = 2) -> None:
    print(f"vision-report: {msg}", file=sys.stderr)
    raise SystemExit(code)


def load_xai_key() -> str:
    env = os.environ.get("XAI_API_KEY", "").strip()
    if env:
        return env
    if KEY_FILE.is_file():
        return KEY_FILE.read_text(encoding="utf-8").strip().replace("\n", "")
    die(f"no XAI_API_KEY and no key file {KEY_FILE}")


def stem_of(path: Path) -> str:
    return path.stem


def extract_ir(image: Path, json_path: Path, model: str) -> None:
    env = os.environ.copy()
    env["XAI_API_KEY"] = load_xai_key()
    env["DAEDALUS_VLM"] = "xai"
    env["DAEDALUS_VLM_MODEL"] = model
    cmd = [sys.executable, str(ROOT / "scripts" / "vlm-extract.py"), str(image), "-o", str(json_path)]
    print(f"vision-report: extract model={model} → {json_path}", file=sys.stderr)
    proc = subprocess.run(cmd, cwd=str(ROOT), env=env)
    if proc.returncode != 0:
        die("vlm-extract.py failed", proc.returncode or 1)


def aura_driver(json_path: Path, sch_path: Path, csv_path: Path, op_path: Path, dt: float, tstop: float, nudge: float) -> str:
    jp = json.dumps(str(json_path))
    sp = json.dumps(str(sch_path))
    cp = json.dumps(str(csv_path))
    op = json.dumps(str(op_path))
    return f"""(require "daedalus-min" all:)
(define ir (daed:ir-ingest {jp}))
(define r (daed:from-ir ir 12))
(display "op-ok=") (display (daed:pipe-ok? r))
(display " reason=") (display (daed:pipe-reason r)) (newline)
(define sch (daed:ir->schematic-html ir))
(define nw (write-file {sp} sch))
(display "schematic=") (display (if (> nw 0) {sp} "write-fail")) (newline)
(define ckt (daed:pipe-circuit r))
(define sim (daed:pipe-sim r))
(define mx (daed:max-node (daed:ckt-comps ckt)))
(define op-txt "")
(define k 0)
(while (lambda () (<= k mx))
  (lambda ()
    (set! op-txt (string-append op-txt (number->string k) " "
                                (number->string (daed:v sim k)) "
"))
    (set! k (+ k 1))))
(write-file {op} op-txt)
(define ckt-t (daed:clone-circuit ckt))
(define c1 (daed:find-comp ckt-t "C1"))
(if (and c1 (> {nudge} 0.0) (< {nudge} 1.0))
  (begin
    (daed:mutate-value! ckt-t "C1" (* {nudge} (daed:comp-value c1)))
    (display "nudge C1 *") (display {nudge}) (newline))
  0)
(define dt {dt})
(define ns (daed:nsteps-for {tstop} dt))
(display "tran dt=") (display dt)
(display " nsteps=") (display ns) (newline)
(define tr (daed:simulate-tran ckt-t dt ns))
(display "tran-ok=") (display (daed:tran-ok? tr))
(display " tstop=") (display (daed:tran-tstop tr)) (newline)
(define nc (write-file {cp} (daed:tran->csv tr)))
(display "csv=") (display (if (> nc 0) {cp} "write-fail")) (newline)
(if (and (daed:pipe-ok? r) (daed:tran-ok? tr) (> nw 0) (> nc 0))
  (begin (display "RESULT pass") (newline))
  (begin (display "RESULT fail") (newline)))
"""


def run_aura(script: str) -> str:
    runner = ROOT / "scripts" / "run-aura.sh"
    tmp = Path("/tmp/daed-vision-report.aura")
    tmp.write_text(script, encoding="utf-8")
    print("vision-report: simulate + schematic (Aura)", file=sys.stderr)
    proc = subprocess.run(
        [str(runner), str(tmp)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        timeout=600,
    )
    out = (proc.stdout or "") + (proc.stderr or "")
    sys.stderr.write(out)
    if proc.returncode != 0 and "RESULT pass" not in out:
        die("Aura driver failed", proc.returncode or 1)
    return out


def load_op(path: Path) -> dict[int, float]:
    volts: dict[int, float] = {}
    if not path.is_file():
        return volts
    for line in path.read_text(encoding="utf-8").splitlines():
        parts = line.split()
        if len(parts) >= 2:
            try:
                volts[int(float(parts[0]))] = float(parts[1])
            except ValueError:
                pass
    return volts


def load_csv(path: Path) -> tuple[list[float], dict[str, list[float]]]:
    times: list[float] = []
    series: dict[str, list[float]] = {}
    with path.open(encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        fields = [f for f in (reader.fieldnames or []) if f != "t"]
        for f in fields:
            series[f] = []
        for row in reader:
            times.append(float(row["t"]))
            for f in fields:
                series[f].append(float(row[f]))
    return times, series


def q_traces(ir: dict) -> list[dict]:
    comps = ir.get("comps") or []
    qs = sorted(
        (c for c in comps if isinstance(c, dict) and c.get("type") == "Q"),
        key=lambda c: str(c.get("name", "")),
    )
    ds = sorted(
        (c for c in comps if isinstance(c, dict) and c.get("type") == "D"),
        key=lambda c: str(c.get("name", "")),
    )
    out = []
    for i, q in enumerate(qs):
        color = TRACE_FALLBACK[i % len(TRACE_FALLBACK)]
        if i < len(ds):
            color = LED_COLORS.get(str(ds[i].get("value", "")).lower(), color)
        node = q.get("n1")
        out.append({
            "name": str(q.get("name") or "Q"),
            "col": f"v{node}",
            "node": node,
            "color": color,
        })
    return out


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def extract_svg(html: str) -> str:
    m = re.search(r"(<svg\b.*</svg>)", html, re.S | re.I)
    return m.group(1) if m else ""


def tag_led_polygons(svg: str, traces: list[dict]) -> str:
    cmap = {str(tr["color"]).lower(): tr["name"] for tr in traces}

    def repl(m: re.Match) -> str:
        fill = m.group(1)
        name = cmap.get(fill.lower())
        if not name or "data-trace=" in m.group(0):
            return m.group(0)
        return m.group(0).replace(
            "<polygon", f'<polygon class="led" data-trace="{esc(name)}"', 1
        )

    return re.sub(r'<polygon\b[^>]*fill="(#[0-9A-Fa-f]+)"[^>]*>', repl, svg)


def build_report(
    *,
    title: str,
    model: str,
    image: Path | None,
    ir: dict,
    sch_html: str,
    times: list[float],
    series: dict[str, list[float]],
    op: dict[int, float],
    dt: float,
    tstop: float,
    nudge: float,
    aura_log: str,
) -> str:
    traces = q_traces(ir)
    if not traces:
        traces = [
            {"name": k, "col": k, "node": int(k[1:]) if k[1:].isdigit() else 0, "color": TRACE_FALLBACK[i % len(TRACE_FALLBACK)]}
            for i, k in enumerate(sorted(series))
        ]
    svg = tag_led_polygons(extract_svg(sch_html), traces)
    t1 = times[-1] if times else tstop
    vals = [v for tr in traces for v in series.get(tr["col"], [])]
    vmin = min(vals) if vals else 0.0
    vmax = max(vals) if vals else 1.0
    pad = max(0.08 * (vmax - vmin), 0.05)
    vmin, vmax = vmin - pad, vmax + pad

    x0, y0, w, h = 56, 24, 720, 260
    grid = []
    for i in range(6):
        y = y0 + h * i / 5
        v = vmax - (vmax - vmin) * i / 5
        grid.append(
            f'<line x1="{x0}" y1="{y:.1f}" x2="{x0+w}" y2="{y:.1f}" class="grid"/>'
            f'<text x="{x0-8}" y="{y+4:.1f}" class="tick" text-anchor="end">{v:.2f}</text>'
        )
    for i in range(6):
        x = x0 + w * i / 5
        t = t1 * i / 5
        grid.append(
            f'<line x1="{x:.1f}" y1="{y0}" x2="{x:.1f}" y2="{y0+h}" class="grid"/>'
            f'<text x="{x:.1f}" y="{y0+h+18}" class="tick" text-anchor="middle">{t:.2f}s</text>'
        )
    path_shells = []
    dots = []
    legend = []
    wave_traces = []
    for tr in traces:
        ys = series.get(tr["col"], [])
        path_shells.append(
            f'<polyline class="trace" data-name="{esc(tr["name"])}" fill="none" '
            f'stroke="{tr["color"]}" stroke-width="2.2" points=""/>'
        )
        dots.append(
            f'<circle class="probe" data-name="{esc(tr["name"])}" r="4.2" '
            f'fill="{tr["color"]}" stroke="#fff" stroke-width="1.2" cx="-20" cy="-20"/>'
        )
        legend.append(
            f'<label class="lg"><input type="checkbox" checked data-trace="{esc(tr["name"])}"/>'
            f'<span class="sw" style="background:{tr["color"]}"></span>'
            f'{esc(tr["name"])} <span class="live" data-live="{esc(tr["name"])}">—</span></label>'
        )
        wave_traces.append({
            "name": tr["name"],
            "color": tr["color"],
            "v": [round(v, 5) for v in ys],
        })

    nudge_note = (
        f"C1 scaled ×{nudge:g} for .tran only (matched caps stay latched at DC). "
        if 0 < nudge < 1
        else ""
    )
    payload = {
        "t": [round(t, 6) for t in times],
        "traces": wave_traces,
        "x0": x0, "y0": y0, "w": w, "h": h,
        "vmin": vmin, "vmax": vmax, "t1": t1,
    }
    wave_json = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    html = """<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>__TITLE__ — vision report</title>
<style>
body{margin:0;padding:1.25rem 1.4rem 2rem;background:#f5f5f4;color:#1c1917;
  font-family:ui-sans-serif,system-ui,sans-serif;}
h1{font-size:1.2rem;margin:0 0 .25rem;font-weight:650;}
.sub{color:#57534e;font-size:.9rem;margin:0 0 1rem;}
.card{background:#fff;border:1px solid #d6d3d1;border-radius:10px;padding:1rem;margin-bottom:1rem;}
.schematic{width:100%;display:block;background:#fffef7;border-radius:8px;}
.chart{width:100%;height:auto;display:block;background:#fffefb;border-radius:8px;}
.grid{stroke:#e7e5e4;stroke-width:1;}
.tick{font-size:11px;fill:#78716c;font-family:ui-sans-serif,system-ui,sans-serif;}
.cursor{stroke:#1c1917;stroke-width:1.2;stroke-dasharray:3 3;}
.legend{display:flex;flex-wrap:wrap;gap:.6rem 1.1rem;margin:.75rem 0 0;}
.lg{display:flex;align-items:center;gap:.4rem;font-size:.9rem;cursor:pointer;}
.lg em{color:#78716c;font-style:normal;font-size:.8rem;margin-left:.25rem;}
.live{font-variant-numeric:tabular-nums;min-width:4.2rem;display:inline-block;}
.sw{width:.7rem;height:.7rem;border-radius:2px;display:inline-block;}
.hint{color:#57534e;font-size:.85rem;margin:.6rem 0 0;}
.ctrl{display:flex;flex-wrap:wrap;align-items:center;gap:.55rem .7rem;margin:0 0 .65rem;}
.ctrl button,.ctrl select{border:1px solid #d6d3d1;background:#fff;border-radius:7px;
  padding:.28rem .7rem;font:inherit;cursor:pointer;}
.ctrl button.primary{background:#1c1917;color:#fff;border-color:#1c1917;}
.ctrl input[type=range]{flex:1;min-width:140px;}
.clock{font-variant-numeric:tabular-nums;color:#44403c;min-width:7rem;}
polygon.led{transition:fill .08s linear,opacity .08s linear,filter .08s linear;}
pre{background:#1c1917;color:#e7e5e4;border-radius:8px;padding:.75rem 1rem;
  overflow:auto;font-size:.75rem;max-height:12rem;}
</style>
</head>
<body>
<h1>__TITLE__</h1>
<p class="sub">Grok __MODEL__ · schematic + .tran
 · dt=__DT__s · tstop=__TSTOP__s · __NSAMP__ samples</p>
<div class="card">__SVG__</div>
<div class="card">
<h2 style="font-size:1rem;margin:0 0 .4rem">Collector waveforms (.tran)</h2>
<div class="ctrl">
  <button type="button" class="primary" id="btn-play">Pause</button>
  <button type="button" id="btn-restart">Restart</button>
  <label>Speed
    <select id="spd">
      <option value="0.25">0.25×</option>
      <option value="0.5">0.5×</option>
      <option value="1" selected>1×</option>
      <option value="2">2×</option>
      <option value="5">5×</option>
      <option value="10">10×</option>
    </select>
  </label>
  <input type="range" id="scrub" min="0" max="1000" value="0"/>
  <span class="clock" id="clock">t = 0.000 s</span>
</div>
<svg class="chart" id="scope" viewBox="0 0 800 320" role="img" aria-label="transient waveforms">
__GRID__
<g id="traces">__PATHS__</g>
<line class="cursor" id="cursor" x1="56" y1="24" x2="56" y2="284"/>
<g id="probes">__DOTS__</g>
</svg>
<div class="legend">__LEGEND__</div>
<p class="hint">__NUDGE__Playback is the recorded .tran (not a live solver). 1× is one sim-second per wall-second. LEDs on the schematic follow collector voltage (low = on).</p>
</div>
<details class="card" style="margin-top:1rem">
<summary>Aura log</summary>
<pre>__LOG__</pre>
</details>
<script type="application/json" id="wave-data">__WAVE__</script>
<script>
(function(){
  var W = JSON.parse(document.getElementById('wave-data').textContent);
  var t = W.t || [];
  var traces = W.traces || [];
  var n = t.length;
  var t1 = W.t1 || (n ? t[n-1] : 1);
  var playing = true, speed = 1, tnow = 0, last = 0;
  var hidden = {};
  var playBtn = document.getElementById('btn-play');
  var scrub = document.getElementById('scrub');
  var clock = document.getElementById('clock');

  function xAt(tt){
    return W.x0 + (tt / Math.max(t1, 1e-12)) * W.w;
  }
  function yAt(v){
    var vr = Math.max(W.vmax - W.vmin, 1e-12);
    return W.y0 + W.h - ((v - W.vmin) / vr) * W.h;
  }
  function idxAt(tt){
    if (n === 0) return 0;
    if (tt <= t[0]) return 0;
    if (tt >= t[n-1]) return n-1;
    var lo = 0, hi = n-1;
    while (hi - lo > 1){
      var mid = (lo + hi) >> 1;
      if (t[mid] <= tt) lo = mid; else hi = mid;
    }
    return lo;
  }
  function lerp(tt){
    var i = idxAt(tt);
    if (i >= n-1) return n-1;
    var t0 = t[i], t2 = t[i+1], u = (t2 === t0) ? 0 : (tt - t0) / (t2 - t0);
    return i + u;
  }
  function vAt(vs, tt){
    var i = idxAt(tt);
    if (i >= n-1) return vs[n-1];
    var t0 = t[i], t2 = t[i+1], u = (t2 === t0) ? 0 : (tt - t0) / (t2 - t0);
    return vs[i] + (vs[i+1] - vs[i]) * u;
  }
  function pointsUpTo(vs, tt){
    var i = idxAt(tt), pts = [], k;
    for (k = 0; k <= i; k++) pts.push(xAt(t[k]).toFixed(2) + ',' + yAt(vs[k]).toFixed(2));
    if (i < n-1 && tt > t[i]){
      var v = vAt(vs, tt);
      pts.push(xAt(tt).toFixed(2) + ',' + yAt(v).toFixed(2));
    }
    return pts.join(' ');
  }
  function setLed(name, v){
    var el = document.querySelector('polygon.led[data-trace="'+name+'"]');
    if (!el) return;
    var on = Math.max(0, Math.min(1, (2.1 - v) / 1.9));
    el.style.opacity = String(0.22 + 0.78 * on);
    el.style.filter = on > 0.45 ? 'url(#led-glow)' : 'none';
  }
  function setNode(name, v){
    var el = document.querySelector('text.vnode[data-trace="'+name+'"]');
    if (el) el.textContent = name + ' ' + v.toFixed(2) + 'V';
  }
  function draw(){
    var i;
    for (i = 0; i < traces.length; i++){
      var tr = traces[i];
      var poly = document.querySelector('polyline.trace[data-name="'+tr.name+'"]');
      var dot = document.querySelector('circle.probe[data-name="'+tr.name+'"]');
      var live = document.querySelector('[data-live="'+tr.name+'"]');
      var v = vAt(tr.v, tnow);
      if (poly){
        poly.setAttribute('points', hidden[tr.name] ? '' : pointsUpTo(tr.v, tnow));
        poly.style.display = hidden[tr.name] ? 'none' : '';
      }
      if (dot){
        if (hidden[tr.name]) { dot.setAttribute('cx','-20'); }
        else { dot.setAttribute('cx', xAt(tnow)); dot.setAttribute('cy', yAt(v)); }
      }
      if (live) live.textContent = v.toFixed(3)+' V';
      if (!hidden[tr.name]) { setLed(tr.name, v); setNode(tr.name, v); }
    }
    var xc = xAt(tnow);
    var cur = document.getElementById('cursor');
    cur.setAttribute('x1', xc); cur.setAttribute('x2', xc);
    clock.textContent = 't = '+tnow.toFixed(3)+' s';
    if (document.activeElement !== scrub)
      scrub.value = String(Math.round((tnow / Math.max(t1, 1e-12)) * 1000));
  }
  function tick(ts){
    if (!last) last = ts;
    var dt = (ts - last) / 1000;
    last = ts;
    if (playing && n > 1){
      tnow += dt * speed;
      if (tnow >= t1){ tnow = 0; }
    }
    draw();
    requestAnimationFrame(tick);
  }
  playBtn.addEventListener('click', function(){
    playing = !playing;
    playBtn.textContent = playing ? 'Pause' : 'Play';
    last = 0;
  });
  document.getElementById('btn-restart').addEventListener('click', function(){
    tnow = 0; last = 0; draw();
  });
  document.getElementById('spd').addEventListener('change', function(e){
    speed = parseFloat(e.target.value) || 1;
  });
  scrub.addEventListener('input', function(){
    tnow = (parseInt(scrub.value, 10) / 1000) * t1;
    last = 0;
    draw();
  });
  document.querySelectorAll('input[data-trace]').forEach(function(box){
    box.addEventListener('change', function(){
      hidden[box.getAttribute('data-trace')] = !box.checked;
      draw();
    });
  });
  var svg = document.querySelector('svg.schematic');
  if (svg && !svg.querySelector('#led-glow')){
    var ns = 'http://www.w3.org/2000/svg';
    var defs = document.createElementNS(ns, 'defs');
    defs.innerHTML = '<filter id="led-glow" x="-50%" y="-50%" width="200%" height="200%">'
      + '<feGaussianBlur stdDeviation="1.6" result="b"/>'
      + '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>';
    svg.insertBefore(defs, svg.firstChild);
  }
  requestAnimationFrame(tick);
})();
</script>
</body>
</html>
"""
    return (
        html.replace("__TITLE__", esc(title))
        .replace("__MODEL__", esc(model))
        .replace("__DT__", f"{dt:g}")
        .replace("__TSTOP__", f"{tstop:g}")
        .replace("__NSAMP__", str(len(times)))
        .replace("__SVG__", svg or "<p>no schematic svg</p>")
        .replace("__GRID__", "".join(grid))
        .replace("__PATHS__", "".join(path_shells))
        .replace("__DOTS__", "".join(dots))
        .replace("__LEGEND__", "".join(legend))
        .replace("__NUDGE__", esc(nudge_note))
        .replace("__LOG__", esc(aura_log))
        .replace("__WAVE__", wave_json)
    )


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("image", type=Path, nargs="?", default=OUT_DIR / "3led.jpeg")
    ap.add_argument("--skip-extract", action="store_true", help="reuse out/<stem>.json")
    ap.add_argument("--json", type=Path, help="IR JSON path (implies skip extract)")
    ap.add_argument("--model", default=os.environ.get("DAEDALUS_VLM_MODEL", DEFAULT_MODEL))
    ap.add_argument("--dt", type=float, default=0.05)
    ap.add_argument("--tstop", type=float, default=4.0)
    ap.add_argument("--nudge-c", type=float, default=0.8, dest="nudge")
    ap.add_argument("--report-only", action="store_true",
                    help="rebuild HTML from existing json/csv/schematic")
    args = ap.parse_args()

    image = args.image.expanduser()
    if not image.is_file() and not args.json:
        die(f"not a file: {image}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    stem = stem_of(args.json if args.json else image)
    json_path = args.json.expanduser() if args.json else OUT_DIR / f"{stem}.json"
    sch_path = OUT_DIR / f"{stem}.html"
    csv_path = OUT_DIR / f"{stem}.tran.csv"
    op_path = OUT_DIR / f"{stem}.op.txt"
    report_path = OUT_DIR / f"{stem}-report.html"

    if image.is_file() and image.resolve().parent != OUT_DIR.resolve():
        dest = OUT_DIR / image.name
        dest.write_bytes(image.read_bytes())
        image = dest

    if args.json or args.report_only:
        args.skip_extract = True
    if not args.skip_extract:
        if not image.is_file():
            die(f"need an image to extract: {image}")
        extract_ir(image, json_path, args.model)
    if not json_path.is_file():
        die(f"missing IR json: {json_path}")

    ir = json.loads(json_path.read_text(encoding="utf-8"))
    if args.report_only:
        if not csv_path.is_file() or not sch_path.is_file():
            die("report-only needs existing schematic html and tran csv")
        log = "(report-only: reused previous Aura run)"
    else:
        log = run_aura(aura_driver(json_path, sch_path, csv_path, op_path, args.dt, args.tstop, args.nudge))
        if not csv_path.is_file() or not sch_path.is_file():
            die("Aura did not write schematic/csv")

    times, series = load_csv(csv_path)
    if args.report_only and times:
        args.tstop = times[-1]
        if len(times) > 1:
            args.dt = times[1] - times[0]
    op = load_op(op_path)
    sch_html = sch_path.read_text(encoding="utf-8")
    title = str(ir.get("title") or stem)
    report = build_report(
        title=title,
        model=args.model if not args.skip_extract else str((ir.get("source") or {}).get("model") or args.model),
        image=image if image.is_file() else None,
        ir=ir,
        sch_html=sch_html,
        times=times,
        series=series,
        op=op,
        dt=args.dt,
        tstop=args.tstop,
        nudge=args.nudge,
        aura_log=log,
    )
    report_path.write_text(report, encoding="utf-8")
    print(f"vision-report: json={json_path}")
    print(f"vision-report: schematic={sch_path}")
    print(f"vision-report: csv={csv_path}")
    print(f"vision-report: report={report_path}")
    if not args.report_only and "RESULT pass" not in log:
        die("pipeline finished but Aura did not print RESULT pass", 1)


if __name__ == "__main__":
    main()

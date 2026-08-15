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
            "name": f"{q.get('name', 'Q')}.C",
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


def polyline(times: list[float], ys: list[float], x0: float, y0: float, w: float, h: float, t1: float, vmin: float, vmax: float) -> str:
    if not times:
        return ""
    span = max(t1, 1e-12)
    vr = max(vmax - vmin, 1e-12)
    pts = []
    for t, v in zip(times, ys):
        x = x0 + (t / span) * w
        y = y0 + h - ((v - vmin) / vr) * h
        pts.append(f"{x:.2f},{y:.2f}")
    return " ".join(pts)


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
    svg = extract_svg(sch_html)
    traces = q_traces(ir)
    if not traces:
        traces = [
            {"name": k, "col": k, "node": int(k[1:]) if k[1:].isdigit() else 0, "color": TRACE_FALLBACK[i % len(TRACE_FALLBACK)]}
            for i, k in enumerate(sorted(series))
        ]
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
    paths = []
    legend = []
    for tr in traces:
        ys = series.get(tr["col"], [])
        pts = polyline(times, ys, x0, y0, w, h, t1, vmin, vmax)
        paths.append(
            f'<polyline class="trace" data-name="{esc(tr["name"])}" fill="none" '
            f'stroke="{tr["color"]}" stroke-width="2" points="{pts}"/>'
        )
        node = tr["node"]
        ov = op.get(node)
        ov_s = f"{ov:.3f} V" if isinstance(ov, float) else "—"
        legend.append(
            f'<label class="lg"><input type="checkbox" checked data-trace="{esc(tr["name"])}"/>'
            f'<span class="sw" style="background:{tr["color"]}"></span>'
            f'{esc(tr["name"])} <em>.op {ov_s}</em></label>'
        )

    photo = ""
    if image and image.is_file() and image.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp", ".gif"}:
        rel = os.path.relpath(image, OUT_DIR)
        photo = (
            f'<figure class="photo"><img src="{esc(rel)}" alt="source photo"/>'
            f"<figcaption>{esc(str(image.name))}</figcaption></figure>"
        )

    op_rows = "".join(
        f"<tr><td>n{k}</td><td>{v:.4f} V</td></tr>"
        for k, v in sorted(op.items()) if k > 0
    )
    notes = esc(str(ir.get("notes") or ""))
    nudge_note = (
        f"C1 scaled ×{nudge:g} for .tran only (matched caps stay latched at DC)."
        if 0 < nudge < 1
        else ""
    )
    return f"""<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{esc(title)} — vision report</title>
<style>
body{{margin:0;padding:1.25rem 1.4rem 2rem;background:#f5f5f4;color:#1c1917;
  font-family:ui-sans-serif,system-ui,sans-serif;}}
h1{{font-size:1.2rem;margin:0 0 .25rem;font-weight:650;}}
.sub{{color:#57534e;font-size:.9rem;margin:0 0 1rem;}}
.grid2{{display:grid;gap:1rem;grid-template-columns:1fr;}}
@media(min-width:960px){{.grid2{{grid-template-columns:1fr 1.4fr;}}}}
.card{{background:#fff;border:1px solid #d6d3d1;border-radius:10px;padding:1rem;}}
.schematic{{width:100%;display:block;background:#fffef7;border-radius:8px;}}
.photo img{{width:100%;border-radius:8px;display:block;}}
.photo figcaption{{color:#78716c;font-size:.8rem;margin-top:.4rem;}}
table{{border-collapse:collapse;font-size:.85rem;}}
td,th{{padding:.2rem .7rem .2rem 0;text-align:left;}}
td:last-child{{font-variant-numeric:tabular-nums;}}
.chart{{width:100%;height:auto;display:block;background:#fffefb;border-radius:8px;}}
.grid{{stroke:#e7e5e4;stroke-width:1;}}
.tick{{font-size:11px;fill:#78716c;font-family:ui-sans-serif,system-ui,sans-serif;}}
.legend{{display:flex;flex-wrap:wrap;gap:.6rem 1.1rem;margin:.75rem 0 0;}}
.lg{{display:flex;align-items:center;gap:.4rem;font-size:.9rem;cursor:pointer;}}
.lg em{{color:#78716c;font-style:normal;font-size:.8rem;margin-left:.25rem;}}
.sw{{width:.7rem;height:.7rem;border-radius:2px;display:inline-block;}}
.hint{{color:#57534e;font-size:.85rem;margin:.6rem 0 0;}}
pre{{background:#1c1917;color:#e7e5e4;border-radius:8px;padding:.75rem 1rem;
  overflow:auto;font-size:.75rem;max-height:12rem;}}
</style>
</head>
<body>
<h1>{esc(title)}</h1>
<p class="sub">Grok {esc(model)} · IR → schematic · .op + .tran
 · dt={dt:g}s · tstop={tstop:g}s · {len(times)} samples</p>
<div class="grid2">
  <div class="card">{photo or "<p class='hint'>no source photo</p>"}</div>
  <div class="card">{svg or "<p>no schematic svg</p>"}</div>
</div>
<div class="card" style="margin-top:1rem">
<h2 style="font-size:1rem;margin:0 0 .5rem">.op voltages</h2>
<table><thead><tr><th>node</th><th>V</th></tr></thead><tbody>{op_rows}</tbody></table>
<p class="hint">{notes}</p>
</div>
<div class="card" style="margin-top:1rem">
<h2 style="font-size:1rem;margin:0 0 .4rem">Collector waveforms (.tran)</h2>
<svg class="chart" viewBox="0 0 800 320" role="img" aria-label="transient waveforms">
{''.join(grid)}
{''.join(paths)}
</svg>
<div class="legend">{''.join(legend)}</div>
<p class="hint">{esc(nudge_note)} Click a legend item to hide a trace.</p>
</div>
<details class="card" style="margin-top:1rem">
<summary>Aura log</summary>
<pre>{esc(aura_log)}</pre>
</details>
<script>
document.querySelectorAll('input[data-trace]').forEach(function(box){{
  box.addEventListener('change', function(){{
    var name = box.getAttribute('data-trace');
    document.querySelectorAll('polyline.trace').forEach(function(p){{
      if (p.getAttribute('data-name') === name)
        p.style.display = box.checked ? '' : 'none';
    }});
  }});
}});
</script>
</body>
</html>
"""


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("image", type=Path, nargs="?", default=OUT_DIR / "3led.jpeg")
    ap.add_argument("--skip-extract", action="store_true", help="reuse out/<stem>.json")
    ap.add_argument("--json", type=Path, help="IR JSON path (implies skip extract)")
    ap.add_argument("--model", default=os.environ.get("DAEDALUS_VLM_MODEL", DEFAULT_MODEL))
    ap.add_argument("--dt", type=float, default=0.05)
    ap.add_argument("--tstop", type=float, default=4.0)
    ap.add_argument("--nudge-c", type=float, default=0.8, dest="nudge")
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

    if args.json:
        args.skip_extract = True
    if not args.skip_extract:
        if not image.is_file():
            die(f"need an image to extract: {image}")
        extract_ir(image, json_path, args.model)
    if not json_path.is_file():
        die(f"missing IR json: {json_path}")

    ir = json.loads(json_path.read_text(encoding="utf-8"))
    log = run_aura(aura_driver(json_path, sch_path, csv_path, op_path, args.dt, args.tstop, args.nudge))
    if not csv_path.is_file() or not sch_path.is_file():
        die("Aura did not write schematic/csv")

    times, series = load_csv(csv_path)
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
    if "RESULT pass" not in log:
        die("pipeline finished but Aura did not print RESULT pass", 1)


if __name__ == "__main__":
    main()

"""Notebook helper for the solve-assignment skill.

Usage (always with the repo's venv python):
  nb_tool.py outline <nb.ipynb>                 one line per cell: index, type, first line
  nb_tool.py dump    <nb.ipynb> <cells.md>      write cells to an editable text file
  nb_tool.py build   <cells.md> <nb.ipynb>      build a notebook from such a text file
  nb_tool.py check   <nb.ipynb> --stage skeleton|answers
  nb_tool.py run     <nb.ipynb>                 execute all code cells in place, store outputs

Cell text format used by dump/build: every cell starts with a marker line
  <!-- cell: markdown -->   or   <!-- cell: code -->
followed by the cell source.
"""
import json
import re
import sys
from pathlib import Path

MARKER = re.compile(r"^<!-- cell: (markdown|code) -->$")
ANCHOR = re.compile(r'^<a id="([^"]+)"></a>\s*$')
TOC_LINK = re.compile(r"\]\(#([^)\s]+)\)")
DEFAULT_META = {
    "kernelspec": {"display_name": ".venv", "language": "python", "name": "python3"},
    "language_info": {"name": "python"},
}


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save(nb, path):
    Path(path).write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


def src(cell):
    s = cell.get("source", "")
    return "".join(s) if isinstance(s, list) else s


def to_lines(text):
    lines = text.split("\n")
    return [l + "\n" for l in lines[:-1]] + ([lines[-1]] if lines[-1] else [])


def heading_level(text):
    """Level of the heading in a cell that is '<a id></a>' + heading, or a bare heading."""
    lines = [l for l in text.strip().split("\n") if l.strip()]
    if not lines:
        return None, None
    anchor = None
    m = ANCHOR.match(lines[0])
    if m:
        anchor = m.group(1)
        lines = lines[1:]
    if lines and re.match(r"^#{1,6} ", lines[0]):
        return len(lines[0]) - len(lines[0].lstrip("#")), anchor
    return None, anchor


def cmd_outline(path):
    for i, c in enumerate(load(path)["cells"]):
        first = next((l for l in src(c).split("\n") if l.strip() and not ANCHOR.match(l)), "")
        outs = len(c.get("outputs", [])) if c["cell_type"] == "code" else ""
        print(f"[{i:3}] {c['cell_type']:8} {outs!s:>2}  {first[:110]}")


def cmd_dump(path, out):
    parts = []
    for c in load(path)["cells"]:
        parts.append(f"<!-- cell: {c['cell_type']} -->\n{src(c).rstrip()}\n")
    Path(out).write_text("\n".join(parts), encoding="utf-8")
    print(f"wrote {out}")


def cmd_build(spec, out):
    cells, cur_type, buf = [], None, []

    def flush():
        if cur_type is None:
            return
        text = "\n".join(buf).strip("\n")
        cell = {"cell_type": cur_type, "metadata": {}, "source": to_lines(text)}
        if cur_type == "code":
            cell.update(execution_count=None, outputs=[])
        cells.append(cell)

    for line in Path(spec).read_text(encoding="utf-8").split("\n"):
        m = MARKER.match(line.strip())
        if m:
            flush()
            cur_type, buf = m.group(1), []
        else:
            buf.append(line)
    flush()

    meta = load(out)["metadata"] if Path(out).exists() else DEFAULT_META
    save({"cells": cells, "metadata": meta, "nbformat": 4, "nbformat_minor": 5}, out)
    print(f"wrote {out} ({len(cells)} cells)")


def cmd_check(path, stage):
    cells = load(path)["cells"]
    errors, warnings = [], []
    texts = [src(c) for c in cells]

    # 1. title + participants
    if not cells or cells[0]["cell_type"] != "markdown" or not texts[0].lstrip().startswith("### Assignment"):
        errors.append("cell 0 must be the markdown title '### Assignment N — Title ###'")
    elif "Participants:" not in texts[0]:
        errors.append("cell 0 must contain the 'Participants:' list")

    # 2. table of contents
    if len(cells) < 2 or not texts[1].lstrip().startswith("## Table of contents"):
        errors.append("cell 1 must be the '## Table of contents' markdown cell")
        toc_ids = []
    else:
        toc_ids = TOC_LINK.findall(texts[1])

    # 3. anchors and headings
    anchors, task_idx = {}, []
    for i, (c, t) in enumerate(zip(cells, texts)):
        if i < 2 or c["cell_type"] != "markdown":
            continue
        level, anchor = heading_level(t)
        if anchor:
            if anchor in anchors:
                errors.append(f"cell {i}: duplicate anchor '{anchor}' (also cell {anchors[anchor]})")
            anchors[anchor] = i
            if level is None:
                errors.append(f"cell {i}: anchor '{anchor}' is not followed by a heading")
        if level is not None and not anchor:
            errors.append(f"cell {i}: heading without '<a id=...></a>' anchor on the line above")
        if level == 4:
            task_idx.append(i)
            if len(re.findall(r"^#{1,6} ", t, flags=re.M)) > 1:
                errors.append(f"cell {i}: more than one heading in a task cell (one task per cell)")
        elif level is not None and level not in (2, 3):
            errors.append(f"cell {i}: unexpected heading level {level} "
                          "(## parts/setup, ### sub-sections, #### tasks)")

    for a in toc_ids:
        if a not in anchors:
            errors.append(f"table of contents links to '#{a}' but no cell has that anchor")
    for a, i in anchors.items():
        if a not in toc_ids:
            errors.append(f"cell {i}: anchor '{a}' is missing from the table of contents")
    if "setup" not in anchors:
        errors.append("missing the '<a id=\"setup\"></a>\\n## Setup — imports and data' cell")

    # 4. stage-specific rules
    heading_cells = {i for i, t in enumerate(texts) if i >= 2 and heading_level(t)[0] is not None}
    if stage == "skeleton":
        for i, c in enumerate(cells[2:], start=2):
            if c["cell_type"] == "code":
                errors.append(f"cell {i}: skeleton must not contain code cells")
            elif i not in heading_cells:
                errors.append(f"cell {i}: skeleton cell that is neither a part/setup heading nor a task (answer content?)")
    else:
        setup = anchors.get("setup")
        if setup is not None and (setup + 1 >= len(cells) or cells[setup + 1]["cell_type"] != "code"):
            errors.append("the Setup heading must be followed by the imports/data code cell")
        for i in task_idx:
            if i + 1 >= len(cells) or (i + 1) in heading_cells:
                errors.append(f"cell {i}: task has no answer cell directly after it")
        for i, (c, t) in enumerate(zip(cells, texts)):
            if i < 2 or i in heading_cells:
                continue
            if c["cell_type"] == "markdown" and re.search(r"^#{1,6} ", t, flags=re.M):
                warnings.append(f"cell {i}: answer markdown contains a heading (extra structure?)")
            if c["cell_type"] == "markdown" and re.match(r"^\s*\**(answer|solution)\b", t, flags=re.I):
                warnings.append(f"cell {i}: answer starts with an 'Answer/Solution' label")
            if c["cell_type"] == "code":
                if not t.strip():
                    errors.append(f"cell {i}: empty code cell")
                elif not c.get("outputs") and c.get("execution_count") is None:
                    warnings.append(f"cell {i}: code cell has not been executed")
                for o in c.get("outputs", []):
                    if o.get("output_type") == "error":
                        errors.append(f"cell {i}: code cell raised {o.get('ename')}: {o.get('evalue')}")
            if not t.strip():
                errors.append(f"cell {i}: empty cell")

    print(f"checked {path} (stage={stage}): {len(cells)} cells, {len(task_idx)} task cells")
    for e in errors:
        print("ERROR  ", e)
    for w in warnings:
        print("WARNING", w)
    if not errors:
        print("OK: no structural errors")
    return 1 if errors else 0


def cmd_run(path):
    from jupyter_client.manager import start_new_kernel

    nb = load(path)
    km, kc = start_new_kernel(kernel_name="python3", cwd=str(Path(path).resolve().parent))
    failed = None
    try:
        kc.execute_interactive("%matplotlib inline", timeout=120)
        count = 0
        for i, cell in enumerate(nb["cells"]):
            if cell["cell_type"] != "code":
                continue
            outputs = []

            def hook(msg, outputs=outputs):
                t, ct = msg["msg_type"], msg["content"]
                if t == "stream":
                    if outputs and outputs[-1]["output_type"] == "stream" and outputs[-1]["name"] == ct["name"]:
                        outputs[-1]["text"] += ct["text"]
                    else:
                        outputs.append({"output_type": "stream", "name": ct["name"], "text": ct["text"]})
                elif t in ("execute_result", "display_data"):
                    o = {"output_type": t, "data": ct["data"], "metadata": ct.get("metadata", {})}
                    if t == "execute_result":
                        o["execution_count"] = ct["execution_count"]
                    outputs.append(o)
                elif t == "error":
                    outputs.append({"output_type": "error", "ename": ct["ename"],
                                    "evalue": ct["evalue"], "traceback": ct["traceback"]})

            reply = kc.execute_interactive(src(cell), output_hook=hook, timeout=1800)
            count += 1
            for o in outputs:
                if o["output_type"] == "stream":
                    o["text"] = to_lines(o["text"])
            cell["outputs"] = outputs
            cell["execution_count"] = reply["content"].get("execution_count", count)
            if reply["content"]["status"] != "ok":
                failed = (i, reply["content"].get("ename"), reply["content"].get("evalue"))
                break
    finally:
        kc.stop_channels()
        km.shutdown_kernel(now=True)
    save(nb, path)
    if failed:
        print(f"ERROR: cell {failed[0]} raised {failed[1]}: {failed[2]} (outputs saved up to that cell)")
        return 1
    print(f"OK: executed all code cells of {path}")
    return 0


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    cmd, args = argv[0], argv[1:]
    if cmd == "outline":
        cmd_outline(args[0])
    elif cmd == "dump":
        cmd_dump(args[0], args[1])
    elif cmd == "build":
        cmd_build(args[0], args[1])
    elif cmd == "check":
        stage = args[args.index("--stage") + 1] if "--stage" in args else "answers"
        return cmd_check(args[0], stage)
    elif cmd == "run":
        return cmd_run(args[0])
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

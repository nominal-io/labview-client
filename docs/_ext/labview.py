"""The Reference and Examples sections, generated from the LabVIEW export in ``docs/lvdocs``.

The LabVIEW tool in ``docs/lvdocs`` writes ``lvdocstring.json`` (every VI on the palette),
``exampleinfo.json`` (every VI in ``lv_src/Examples``) and their images under ``assets/``. Their
formats are in ``_ext/lvdocstring.schema.json`` and ``_ext/exampleinfo.schema.json``. The palette
tree, names and order come from ``lv_src/.vipb``.

At ``builder-inited`` this writes, gitignored and only when their content changes (so live
preview doesn't loop):

- ``ref/index.md`` and ``ref/<palette>/index.md``: one page per palette, in palette order;
- ``ref/vi/<slug>.md``: one page per VI. A polymorphic VI's instances are sections of its page.
  The slug comes from the qualified name, so a page keeps its URL when the VI moves palettes;
- ``examples/index.md`` and ``examples/<slug>.md``: one page per example.

It also adds the ``lv`` domain. Each VI page registers its VI, so ``{lv:vi}`Create Nominal
Client``` (by palette name or qualified name) links to it, and VIs appear in the index and search.
"""

from __future__ import annotations

import json
import re
import struct
import urllib.parse
import xml.etree.ElementTree as ET
import zlib
from dataclasses import dataclass, field
from pathlib import Path, PureWindowsPath
from typing import Any, Iterator

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx import addnodes
from sphinx.application import Sphinx
from sphinx.builders import Builder
from sphinx.domains import Domain, ObjType
from sphinx.environment import BuildEnvironment
from sphinx.roles import XRefRole
from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective
from sphinx.util.nodes import make_refnode

logger = logging.getLogger(__name__)

# example file -> page title, in index order. Examples not listed follow, under their file name.
EXAMPLES = {
    "labview-quick-visualization.vi": "Quick visualization",
}

_ERROR_LABELS = re.compile(r"^error (in|out)\b", re.I)
_SCALARS = {"I8", "I16", "I32", "I64", "U8", "U16", "U32", "U64", "SGL", "DBL", "EXT", "CSG", "CDB", "CXT"}


# -- The export ---------------------------------------------------------------------------------


@dataclass
class Terminal:
    label: str
    caption: str
    direction: str
    type: str
    default: str
    description: str
    tip: str
    rule: str

    @property
    def name(self) -> str:
        return self.caption or self.label

    @property
    def is_error(self) -> bool:
        return bool(_ERROR_LABELS.match(self.label)) and self.type.startswith("Cluster")


@dataclass
class VI:
    id: str
    qname: str
    path: str
    description: str
    icon: str
    connpane: str
    terminals: list[Terminal]
    parent: str
    selector: str
    polymorphic: bool
    instances: list[VI] = field(default_factory=list)
    title: str = ""
    slug: str = ""
    palettes: list[Palette] = field(default_factory=list)
    merge: bool = False  # a merge VI: the palette drops its code, not a subVI


@dataclass
class Palette:
    name: str
    path: str  # names from the top palette, "/"-separated; "" for the top
    slug: str  # "files/multipart-file-upload"; "" for the top
    icon: bytes | None
    items: list[VI | Palette] = field(default_factory=list)


def _slugify(text: str) -> str:
    text = text.replace("[]", " array ")
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def _vi_slug(qname: str) -> str:
    """The innermost owner and the VI's name: "asset.lvclass:update.title.vi" -> "asset-update-title"."""
    parts = [re.sub(r"\.(lvclass|lvlib|vim?|ctl)$", "", p) for p in qname.split(":") if p]
    return _slugify(" ".join(parts[-2:]))


def _file(path: str) -> str:
    """The file name of an export path; "" for none."""
    return "" if not path or path.startswith("<") else PureWindowsPath(path).name


def _load_vis(export: Path) -> list[VI]:
    rows = json.loads((export / "lvdocstring.json").read_text(encoding="utf-8"))
    vis: dict[str, VI] = {}
    for r in rows:
        if r["id"] in vis:  # a VI on two palettes is exported once per palette
            continue
        kind = r["kind"]
        selector = ""
        if m := re.search(r"\[menu=(.*)\]\[selector=(.*)\]$", kind, re.S):
            selector = m.group(2) or m.group(1)
        vis[r["id"]] = VI(
            id=r["id"],
            qname=r["id"].split("::", 1)[-1],
            path=r["path"],
            description=r["description"],
            icon=_file(r["icon"]),
            connpane=_file(r["connpane"]),
            terminals=[
                Terminal(
                    label=t["label"],
                    caption=t["caption"],
                    direction=t["direction"],
                    type=t["type"].replace("\r\n", "").strip(),
                    default=t["default"],
                    description=t["description"],
                    tip=t["tip strip"],
                    rule=t["wiring rule"].lower(),
                )
                for t in r["terminals"]
            ],
            parent=r["parent ID"],
            selector=selector,
            polymorphic=kind != "vi" and not r["parent ID"],
        )
    for vi in vis.values():
        if vi.parent:
            if vi.parent not in vis:
                logger.warning("LabVIEW export: %s is an instance of %s, which isn't exported", vi.id, vi.parent)
                continue
            vis[vi.parent].instances.append(vi)
    return list(vis.values())


# -- The palette (lv_src/.vipb) ------------------------------------------------------------------


def _png(width: int, height: int, rgba: list[tuple[int, int, int, int]]) -> bytes:
    rows = b"".join(b"\x00" + bytes(c for px in rgba[y * width:(y + 1) * width] for c in px) for y in range(height))

    def chunk(kind: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))

    header = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header) + chunk(b"IDAT", zlib.compress(rows, 9)) + chunk(b"IEND", b"")


def _palette_icon(hexdata: str) -> bytes | None:
    """A sub-palette's icon, as VIPM stores it, as a PNG.

    After a big-endian length come one or more 3232-byte layers, drawn in order: a 32-byte
    header (width, height and depth at 14, 16 and 18), a 256-entry colour table (8 bytes each:
    2 unused, then 16-bit R, G, B), 32x32 one-byte pixels, then a 1-bit mask (1 = opaque).
    """
    if len(hexdata) <= 8:
        return None
    data = bytes.fromhex(hexdata)
    body = data[4:4 + int.from_bytes(data[:4], "big")]
    rgba = [(0, 0, 0, 0)] * 1024
    for k in range(len(body) // 3232):
        layer = body[3232 * k:3232 * (k + 1)]
        if struct.unpack(">HHH", layer[14:20]) != (32, 32, 8):
            return None
        colors = [(layer[34 + 8 * c], layer[36 + 8 * c], layer[38 + 8 * c]) for c in range(256)]
        pixels, mask = layer[2080:3104], layer[3104:3232]
        for i in range(1024):
            y, x = divmod(i, 32)
            if mask[y * 4 + x // 8] >> (7 - x % 8) & 1:
                rgba[i] = (*colors[pixels[i]], 255)
    return _png(32, 32, rgba)


def _load_palette(vipb: Path, vis: list[VI]) -> Palette:
    by_path = {vi.path.casefold(): vi for vi in vis if not vi.parent}
    defs = ET.parse(vipb).getroot().findall("Library_Palette_Definition/Functions_Palette_Data")
    placed: set[str] = set()

    def build(index: int, name: str, path: str, slug: str, icon: bytes | None) -> Palette:
        palette = Palette(name, path, slug, icon)
        items = defs[index].findall("Items_Data")
        items.sort(key=lambda it: (int(it.findtext("Position/Row") or 0), int(it.findtext("Position/Column") or 0)))
        for it in items:
            label = (it.findtext("NameSub_Menu_Name") or "").strip()
            if it.findtext("Type") == "Sub Palette":
                sub = int(it.findtext("Sub_Palette_Index") or -1)
                if sub >= 0:
                    sub_path = f"{path}/{label}" if path else label
                    sub_slug = f"{slug}/{_slugify(label)}" if slug else _slugify(label)
                    palette.items.append(build(sub, label, sub_path, sub_slug, _palette_icon(it.findtext("Icon") or "")))
                continue
            vi = by_path.get((it.findtext("Path") or "").casefold())
            if vi is None:
                logger.warning("LabVIEW export: %r on the %r palette isn't in lvdocstring.json", label, path or "top")
                continue
            if vi in palette.items:  # listed twice in one palette
                continue
            if vi.id not in placed:  # the first palette a VI appears in names it
                placed.add(vi.id)
                vi.title = re.sub(r"\.vim?$", "", label)
                vi.merge = it.findtext("is_Merge_VI") == "true"
            vi.palettes.append(palette)
            palette.items.append(vi)
        return palette

    return build(0, "", "", "", None)


def _walk(palette: Palette) -> Iterator[Palette]:
    yield palette
    for item in palette.items:
        if isinstance(item, Palette):
            yield from _walk(item)


# -- Text -----------------------------------------------------------------------------------------

_ESCAPE = re.compile(r"([\\*_\[\]<>{}|&])")
_BOLD = re.compile(r"<\s*(/?)\s*b\s*>", re.I)


def _inline(line: str) -> str:
    """One line of LabVIEW text as Markdown: <b> becomes bold, `code` stays code, the rest is literal."""
    out = []
    for i, part in enumerate(re.split(r"(`[^`\n]*`)", line)):
        if i % 2:
            out.append(part)
        else:
            out.append(_ESCAPE.sub(r"\\\1", part).replace("\x02", "**"))
    return "".join(out)


def lv_text(text: str) -> str:
    """A LabVIEW description as Markdown, with its line breaks kept, as Context Help shows them."""
    text = _BOLD.sub("\x02", text.replace("\r\n", "\n").replace("\r", "\n")).strip()
    paragraphs = re.split(r"\n\s*\n", text)
    return "\n\n".join("  \n".join(_inline(line.strip()) for line in p.split("\n") if line.strip()) for p in paragraphs if p.strip())


def _summary(text: str) -> str:
    """The first sentence or line, for palette cards."""
    first = _BOLD.sub("", text.replace("\r", "")).strip().split("\n")[0]
    first = re.split(r"(?<=[.!?])\s", first)[0]
    return _inline(first if len(first) <= 140 else first[:139].rstrip() + "…")


def _indent(text: str, by: str = "  ") -> str:
    return "\n".join(by + line if line else "" for line in text.split("\n"))


# -- Types and defaults ---------------------------------------------------------------------------


@dataclass
class TypeInfo:
    text: str
    elements: list[tuple[str, TypeInfo]] = field(default_factory=list)


def _value(xml: str) -> ET.Element | None:
    """The typed element of a terminal's <LvVariant> default."""
    try:
        root = ET.fromstring(xml)
    except ET.ParseError:
        return None
    return next((c for c in root if c.tag != "Name"), None)


def _describe(el: ET.Element) -> TypeInfo:
    tag = el.tag
    if tag in _SCALARS or tag in ("Boolean", "String", "Path", "Timestamp"):
        return TypeInfo(tag)
    if tag == "EW":
        return TypeInfo("Enum")
    if tag == "DBLWaveform":
        return TypeInfo("Waveform")
    if tag == "Object":
        return TypeInfo(el.findtext("Class") or el.findtext("Name") or "Class")
    if tag == "Cluster":
        elements = [((c.findtext("Name") or "").strip(), _describe(c)) for c in el if c.tag not in ("Name", "NumElts")]
        return TypeInfo("Cluster", elements)
    if tag == "Array":
        dims = len(el.findall("Dimsize"))
        inner = next((c for c in el if c.tag not in ("Name", "Dimsize")), None)
        info = _describe(inner) if inner is not None else TypeInfo("?")
        return TypeInfo(f"{dims}D Array of {info.text}", info.elements)
    return TypeInfo(tag)


def _type(t: Terminal, malleable: bool) -> TypeInfo:
    if t.is_error:
        return TypeInfo("Error cluster")
    if t.type == "Void" and malleable:
        return TypeInfo("Adapts to the wired type")
    if t.type.startswith("Map{"):
        return TypeInfo("Map (" + t.type[4:-1].replace("->", "→ ").replace("  ", " ") + ")")
    if t.type.startswith("enum["):
        return TypeInfo("Enum")
    el = _value(t.default)
    if el is None or el.tag in ("Default", "Map") or (el.tag == "Object" and t.type.endswith(".lvclass")):
        return TypeInfo(t.type)
    info = _describe(el)
    if m := re.match(r"Cluster\[(.+?)\]", t.type):  # a typedef
        info.text += f" ({m.group(1).split(':')[-1]})"
    return info


def _number(value: str) -> str:
    try:
        return f"{float(value):g}"
    except ValueError:
        return value


def _choices(t: Terminal) -> tuple[list[str], int]:
    el = _value(t.default)
    if el is None or el.tag != "EW":
        return [], -1
    try:
        selected = int(el.findtext("Val") or -1)
    except ValueError:
        selected = -1
    return [c.text or "" for c in el.findall("Choice")], selected


def _default(t: Terminal) -> str:
    """The default of an optional or recommended input, as text; "" when it isn't worth showing."""
    if t.direction != "input" or t.rule == "required" or t.is_error:
        return ""
    el = _value(t.default)
    if el is None:
        return ""
    value = el.findtext("Val") or ""
    if el.tag in _SCALARS:
        return _number(value) if value else ""
    if el.tag == "Boolean":
        return "TRUE" if value == "1" else "FALSE"
    if el.tag in ("String", "Path"):
        return value
    if el.tag == "EW":
        choices, selected = _choices(t)
        return choices[selected] if 0 <= selected < len(choices) else ""
    return ""


def _code(text: str) -> str:
    """Inline code that may itself contain backticks."""
    ticks = "``" if "`" in text else "`"
    pad = " " if ticks == "``" else ""
    return f"{ticks}{pad}{text}{pad}{ticks}"


def _elements(elements: list[tuple[str, TypeInfo]], depth: int = 0) -> list[str]:
    lines = []
    for name, info in elements:
        label = f"{_code(name)} " if name else ""
        lines.append("  " * depth + f"- {label}{_inline(info.text)}")
        lines += _elements(info.elements, depth + 1)
    return lines


# -- Pages ----------------------------------------------------------------------------------------


class Pages:
    def __init__(self, app: Sphinx) -> None:
        self.srcdir = Path(app.srcdir)
        self.export = Path(app.config.labview_export_dir)
        self.root = Path(app.config.labview_repo_root)
        self.github = app.config.labview_github_url.rstrip("/")
        try:
            self.images = "/" + self.export.relative_to(self.srcdir).as_posix() + "/assets"
        except ValueError:
            raise RuntimeError(f"labview_export_dir ({self.export}) must be inside the docs folder") from None
        self.submodules = self._submodules()
        self.written: set[Path] = set()

    # paths and links

    def _submodules(self) -> dict[str, str]:
        gitmodules = self.root / ".gitmodules"
        if not gitmodules.exists():
            return {}
        text = gitmodules.read_text(encoding="utf-8")
        found = {}
        for block in re.split(r"^\[submodule", text, flags=re.M)[1:]:
            path = re.search(r"^\s*path\s*=\s*(.+)$", block, re.M)
            url = re.search(r"^\s*url\s*=\s*(.+)$", block, re.M)
            if path and url:
                found[path.group(1).strip()] = re.sub(r"\.git$", "", url.group(1).strip())
        return found

    def source_url(self, lv_src_path: str) -> str:
        """GitHub link for a path relative to lv_src, which may reach into a submodule."""
        rel = (Path("lv_src") / PureWindowsPath(lv_src_path).as_posix()).as_posix()
        parts: list[str] = []
        for p in rel.split("/"):  # resolve ".."
            if p == "..":
                parts.pop()
            elif p not in ("", "."):
                parts.append(p)
        rel = "/".join(parts)
        for sub, url in self.submodules.items():
            if rel.startswith(sub + "/"):
                return f"{url}/blob/HEAD/{urllib.parse.quote(rel[len(sub) + 1:])}"
        return f"{self.github}/blob/HEAD/{urllib.parse.quote(rel)}"

    def image(self, name: str, folder: str = "") -> str | None:
        """The docs path of an exported image, or None (with a warning) if the file is missing."""
        if not name:
            return None
        rel = f"{folder}/{name}" if folder else name
        if not (self.export / "assets" / rel).exists():
            logger.warning("LabVIEW export: assets/%s is missing", rel)
            return None
        return f"{self.images}/{rel}"

    def write(self, rel: str, content: str | bytes) -> None:
        path = self.srcdir / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        data = content.encode("utf-8") if isinstance(content, str) else content
        if not path.exists() or path.read_bytes() != data:
            path.write_bytes(data)
        self.written.add(path)

    def prune(self, folder: str) -> None:
        """Remove generated files from an earlier build that this build didn't write."""
        base = self.srcdir / folder
        for path in sorted(base.rglob("*"), reverse=True):
            if path.is_file() and path not in self.written:
                path.unlink()
            elif path.is_dir() and not any(path.iterdir()):
                path.rmdir()

    # VI pages

    def terminals(self, vi: VI, heading: str) -> list[str]:
        malleable = vi.path.endswith(".vim")
        out: list[str] = []
        for direction, title in (("input", "Inputs"), ("output", "Outputs")):
            # exported in connector pane order; reversed, they read top to bottom as on the pane
            terms = [t for t in reversed(vi.terminals) if t.direction == direction]
            terms.sort(key=lambda t: t.is_error)
            if not terms:
                continue
            out += [f"{heading} {title}", ""]
            for t in terms:
                badge = {"required": " {bdg-primary-line}`required`", "optional": " {bdg-secondary-line}`optional`"}
                out.append(f"**{_inline(t.name)}**{badge.get(t.rule, '') if direction == 'input' else ''}")
                info = _type(t, malleable)
                first = _code(info.text)
                if default := _default(t):
                    first += f" · default {_code(default)}"
                body = [first]
                if info.elements:
                    body += ["", *_elements(info.elements)]
                choices, _ = _choices(t)
                if choices:
                    body += ["", "One of " + ", ".join(_code(c) for c in choices) + "."]
                text = "" if t.is_error else lv_text(t.description or t.tip)
                if text:
                    body += ["", text]
                out.append(": " + body[0])
                out += [_indent(line) if line else "" for line in "\n".join(body[1:]).split("\n")] if len(body) > 1 else []
                out.append("")
        return out

    def header(self, vi: VI, description: str) -> list[str]:
        icon = self.image(vi.icon)
        text = lv_text(description)
        lines = ["::::{container} lv-header"]
        if icon:
            lines += [f"![]({icon}){{.lv-icon}}", ""]
        if text:
            lines += [":::{container} lv-description", text, ":::"]
        return lines + ["::::", ""]

    def connpane(self, vi: VI) -> list[str]:
        image = self.image(vi.connpane) if vi.terminals else None
        return [f"![Connector pane of {_inline(vi.title or vi.qname)}]({image}){{.lv-connpane}}", ""] if image else []

    def vi_page(self, vi: VI) -> str:
        palettes = " · ".join(
            f"[{_inline(p.path.replace('/', ' › ') or 'Nominal')}]({self.palette_link(p, '../')})" for p in vi.palettes
        )
        lines = [
            f"# {_inline(vi.title)}",
            "",
            f"```{{lv:vi}} {vi.qname}",
            f":title: {vi.title}",
            "```",
            "",
            "{.lv-meta}",
            f"{_code(vi.qname)} · Palette: {palettes} · [Source]({self.source_url(vi.path)})",
            "",
        ]
        lines += self.header(vi, vi.description)
        if vi.polymorphic:
            lines += [f"This VI is polymorphic: it has {len(vi.instances)} instances, below. "
                      "Choose one with the polymorphic selector, or wire the inputs and LabVIEW picks it.", ""]
            for inst in vi.instances:
                name = inst.selector or re.sub(r"\.vim?$", "", inst.qname.split(":")[-1])
                lines += [f"## {_inline(name)}", "", f"```{{lv:vi}} {inst.qname}", f":title: {vi.title}: {name}", "```", "",
                          "{.lv-meta}", f"{_code(inst.qname)} · [Source]({self.source_url(inst.path)})", ""]
                if inst.description.strip() and inst.description.strip() != vi.description.strip():
                    lines += [lv_text(inst.description), ""]
                inst.title = inst.title or vi.title
                lines += self.connpane(inst)
                lines += self.terminals(inst, "###")
        else:
            if vi.merge:
                lines += ["{.lv-note}", "Dropping this VI from the palette adds its code to your block diagram, not a subVI.", ""]
            lines += self.connpane(vi)
            lines += self.terminals(vi, "##")
        return "\n".join(lines).rstrip() + "\n"

    # palette pages

    def palette_doc(self, palette: Palette) -> str:
        return f"ref/{palette.slug}/index" if palette.slug else "ref/index"

    def palette_link(self, palette: Palette, up: str) -> str:
        """A link to a palette page from ref/vi/ (up="../")."""
        return f"{up}{palette.slug}/index.md" if palette.slug else f"{up}index.md"

    def palette_page(self, palette: Palette) -> str:
        here = self.palette_doc(palette)
        depth = here.count("/")  # ref/index -> 1, ref/assets/index -> 2
        up = "../" * (depth - 1)
        title = palette.name or "Reference"
        lines = [f"# {_inline(title)}", ""]
        if not palette.slug:
            lines += ["{.lead}", "Every VI on the Nominal palette, organized as the palette is.", ""]
        toc, cards = [], []
        for item in palette.items:
            if isinstance(item, Palette):
                link = f"{up}{item.slug}/index" if palette.slug else f"{item.slug}/index"
                toc.append(link)
                icon = f"![](/{self.palette_icon_path(item)}){{.lv-card-icon}}" if item.icon else ""
                count = sum(1 for i in item.items if isinstance(i, VI))
                cards += [f":::{{grid-item-card}} {_inline(item.name)}", f":link: {link}", ":link-type: doc", "",
                          f"{icon}Palette · {count} VIs", ":::", ""]
            else:
                link = f"{up}vi/{item.slug}" if palette.slug else f"vi/{item.slug}"
                if item.palettes[0] is palette:
                    toc.append(link)
                icon = self.image(item.icon)
                icon_md = f"![]({icon}){{.lv-card-icon}}" if icon else ""
                cards += [f":::{{grid-item-card}} {_inline(item.title)}", f":link: {link}", ":link-type: doc", "",
                          f"{icon_md}{_summary(item.description)}", ":::", ""]
        lines += ["::::{grid} 1 2 2 3", ":gutter: 2", ":class-container: lv-palette", "", *cards, "::::", ""]
        lines += ["```{toctree}", ":hidden:", "", *toc, "```", ""]
        return "\n".join(lines)

    def palette_icon_path(self, palette: Palette) -> str:
        return f"ref/_palettes/{palette.slug.replace('/', '-')}.png"

    # examples

    def example_pages(self) -> None:
        rows = json.loads((self.export / "exampleinfo.json").read_text(encoding="utf-8"))
        order = list(EXAMPLES)
        rows.sort(key=lambda r: (order.index(r["vi name"]) if r["vi name"] in order else len(order), r["vi name"].lower()))
        entries = []
        for r in rows:
            name = r["vi name"]
            title = EXAMPLES.get(name) or re.sub(r"\.vi$", "", name)
            slug = _slugify(re.sub(r"\.vi$", "", name))
            if not (self.root / "lv_src" / "Examples" / name).exists():
                logger.warning("LabVIEW export: example %r isn't in lv_src/Examples", name)
            diagram = self.image(_file(r["diagram image"]), "examples")
            lines = [f"# {_inline(title)}", ""]
            if text := lv_text(r["description"]):
                lines += [text, ""]
            if diagram:
                lines += ["```{image} " + diagram, f":alt: Block diagram of {name}", ":class: lv-diagram", ":scale: 100", "```", ""]
            lines += ["{.lv-meta}", f"Source: [{_code('lv_src/Examples/' + name)}]({self.source_url('Examples/' + name)})", ""]
            self.write(f"examples/{slug}.md", "\n".join(lines))
            entries.append((slug, title, _summary(r["description"])))
        bullets = "".join(f"- [{_inline(t)}]({s}.md){': ' + d if d else ''}\n" for s, t, d in entries)
        toc = "".join(f"{s}\n" for s, _, _ in entries)
        self.write(
            "examples/index.md",
            "# Examples\n\n{.lead}\nExample VIs that install with the Nominal package, in LabVIEW's examples folder. "
            "Each page shows the example's block diagram.\n\n"
            f"{bullets}\n```{{toctree}}\n:hidden:\n\n{toc}```\n",
        )

    # all of it

    def generate(self) -> None:
        vis = _load_vis(self.export)
        top = _load_palette(self.root / "lv_src" / ".vipb", vis)
        pages = [vi for vi in vis if not vi.parent and vi.palettes]
        slugs: dict[str, str] = {}
        for vi in pages:
            vi.slug = _vi_slug(vi.qname)
            if vi.slug in slugs:
                raise RuntimeError(f"LabVIEW reference: {vi.qname} and {slugs[vi.slug]} would share ref/vi/{vi.slug}")
            slugs[vi.slug] = vi.qname
        for palette in _walk(top):
            self.write(self.palette_doc(palette) + ".md", self.palette_page(palette))
            if palette.icon:
                self.write(self.palette_icon_path(palette), palette.icon)
        for vi in pages:
            self.write(f"ref/vi/{vi.slug}.md", self.vi_page(vi))
        self.example_pages()
        self.prune("ref")
        self.prune("examples")
        missing = sum(1 for vi in pages if not vi.description.strip())
        logger.info("LabVIEW reference: %d VIs on %d palettes, %d without a description",
                    len(pages), sum(1 for _ in _walk(top)), missing)


# -- The lv domain --------------------------------------------------------------------------------


class VIDirective(SphinxDirective):
    """Registers a VI documented on this page: ``{lv:vi} <qualified name>`` with ``:title:``."""

    required_arguments = 1
    final_argument_whitespace = True
    option_spec = {"title": directives.unchanged}

    def run(self) -> list[nodes.Node]:
        qname = self.arguments[0].strip()
        title = self.options.get("title") or qname
        anchor = "lv-" + _slugify(qname)
        target = nodes.target("", "", ids=[anchor])
        self.state.document.note_explicit_target(target)
        index = addnodes.index(entries=[("single", f"{title} (LabVIEW VI)", anchor, "", None)])
        self.env.get_domain("lv").note_vi(qname, title, self.env.docname, anchor)  # type: ignore[attr-defined]
        return [index, target]


class LabVIEWDomain(Domain):
    name = "lv"
    label = "LabVIEW"
    object_types = {"vi": ObjType("VI", "vi")}
    directives = {"vi": VIDirective}
    roles = {"vi": XRefRole()}
    initial_data: dict[str, Any] = {"vis": {}}  # qualified name -> (docname, anchor, title)

    def note_vi(self, qname: str, title: str, docname: str, anchor: str) -> None:
        self.data["vis"][qname] = (docname, anchor, title)

    def clear_doc(self, docname: str) -> None:
        for qname, (doc, _, _) in list(self.data["vis"].items()):
            if doc == docname:
                del self.data["vis"][qname]

    def merge_domaindata(self, docnames: Any, otherdata: dict[str, Any]) -> None:
        for qname, entry in otherdata["vis"].items():
            if entry[0] in docnames:
                self.data["vis"][qname] = entry

    def _find(self, target: str) -> tuple[str, str, str] | None:
        vis = self.data["vis"]
        if target in vis:
            return vis[target]
        by_title = [e for e in vis.values() if e[2].casefold() == target.casefold()]
        return by_title[0] if len(by_title) == 1 else None

    def resolve_xref(self, env: BuildEnvironment, fromdocname: str, builder: Builder, typ: str, target: str,
                     node: addnodes.pending_xref, contnode: nodes.Element) -> nodes.reference | None:
        found = self._find(target)
        if found is None:
            logger.warning("no LabVIEW VI named %r (use its palette name or qualified name)", target, location=node)
            return None
        doc, anchor, title = found
        return make_refnode(builder, fromdocname, doc, anchor, contnode, title)

    def resolve_any_xref(self, env: BuildEnvironment, fromdocname: str, builder: Builder, target: str,
                         node: addnodes.pending_xref, contnode: nodes.Element) -> list[tuple[str, nodes.reference]]:
        found = self._find(target)
        if found is None:
            return []
        doc, anchor, title = found
        return [("lv:vi", make_refnode(builder, fromdocname, doc, anchor, contnode, title))]

    def get_objects(self) -> Iterator[tuple[str, str, str, str, str, int]]:
        for qname, (doc, anchor, title) in self.data["vis"].items():
            yield qname, title, "vi", doc, anchor, 1


def setup(app: Sphinx) -> dict[str, object]:
    here = Path(__file__).resolve().parent.parent
    app.add_config_value("labview_export_dir", str(here / "lvdocs"), "env")
    app.add_config_value("labview_repo_root", str(here.parent), "env")
    app.add_config_value("labview_github_url", "https://github.com/nominal-io/labview-client", "env")
    app.add_domain(LabVIEWDomain)
    app.connect("builder-inited", lambda app: Pages(app).generate())
    return {"version": "0.1", "parallel_read_safe": True, "parallel_write_safe": True}

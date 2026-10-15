"""Links from one project's pages to another project's: [text](site:/sql/reference/schema/#runs).

Each project in projects/ is its own Sphinx build, so Sphinx can't resolve or check a link into
another project. A site: link names the target by its path from the site root, as the site
publishes it (/{lang}/{project}/{page}/). This extension rewrites it to a path relative to the
page it's on, so it works wherever the site is served: its domain, a subpath, or the offline copy.

A copy of pub-docs' projects/_ext/site_links.py: this project builds here and is published by
pub-docs at /ni/labview/, so links to the rest of the site go through it too.
"""

from typing import Any

from docutils import nodes
from sphinx.application import Sphinx
from sphinx.config import Config

SCHEME = "site:"


def _allow_scheme(app: Sphinx, config: Config) -> None:
    # MyST treats a link with a scheme it doesn't know as a missing internal target
    schemes = config.myst_url_schemes
    if isinstance(schemes, dict):
        schemes.setdefault("site", None)
    else:
        config.myst_url_schemes = [*schemes, "site"]


def _rewrite(app: Sphinx, doctree: nodes.document, docname: str) -> None:
    # pages are published at /{lang}/{project}/..., two folders below the site root, plus the
    # page's own folders ("rest-api/query/" under dirhtml, "rest-api/query.html" under html)
    to_root = "../" * (2 + app.builder.get_target_uri(docname).count("/"))
    for ref in doctree.findall(nodes.reference):
        uri = ref.get("refuri", "")
        if uri.startswith(SCHEME):
            ref["refuri"] = to_root + uri.removeprefix(SCHEME).lstrip("/")
            # MyST counts it as external, so myst_links_external_new_tab would open it in a new tab
            for attr in ("target", "rel"):
                ref.attributes.pop(attr, None)


def setup(app: Sphinx) -> dict[str, Any]:
    app.connect("config-inited", _allow_scheme)
    app.connect("doctree-resolved", _rewrite)
    return {"parallel_read_safe": True, "parallel_write_safe": True}

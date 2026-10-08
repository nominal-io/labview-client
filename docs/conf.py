"""Sphinx config for the Nominal for LabVIEW docs. Reference and example pages come from the
LabVIEW export in lvdocs/ (see _ext/labview.py)."""

import sys
from pathlib import Path

from nominal_sphinx_theme import theme_options

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE / "_ext"))

project = "LabVIEW"  # the name in the header, after the Nominal Docs logo
copyright = "Nominal, Inc."

extensions = [
    "myst_parser",
    "sphinx_design",
    "sphinx_copybutton",
    "nominal_sphinx_theme",
    "labview",
]
myst_enable_extensions = ["colon_fence", "deflist", "attrs_inline", "attrs_block", "fieldlist"]
myst_heading_anchors = 6

# lvdocs/ holds the LabVIEW export and the tool that writes it: images only, no pages
exclude_patterns = ["_build", "lvdocs"]

html_theme = "shibuya"
html_title = "Nominal for LabVIEW"  # browser tabs and search results
html_copy_source = False
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_theme_options = theme_options(
    github_url="https://github.com/nominal-io/labview-client",
    nav_links=[
        {"title": "Guides", "url": "index"},
        {"title": "Examples", "url": "examples/index"},
        {"title": "Reference", "url": "ref/index"},
    ],
)

# list the recipes
default:
    @just --list

# Build the docs (docs/) into docs/_build/dirhtml; warnings fail the build, as in CI.
# The reference and examples come from the LabVIEW export in docs/lvdocs and the palette in lv_src/.vipb. Needs uv.
build-docs:
    uv run --group docs sphinx-build -E -W --keep-going -b dirhtml docs docs/_build/dirhtml

# Live-preview the docs on http://127.0.0.1:8000, rebuilding on page, export or palette edits
serve-docs:
    uv run --group docs --with sphinx-autobuild sphinx-autobuild -b dirhtml docs docs/_build/dirhtml --watch lv_src/.vipb --ignore "docs/ref/*" --ignore "docs/examples/*"

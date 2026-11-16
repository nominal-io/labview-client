# The docs build with the newest commit on nominal-sphinx-theme's main, without waiting for
# bump-theme.yml to move uv.lock. If GitHub can't be reached, they build with the commit in uv.lock.
theme := "https://github.com/nominal-io/nominal-sphinx-theme"

# list the recipes
default:
    @just --list

# Build the docs (docs/) into docs/_build/dirhtml; warnings fail the build, as in CI.
# The reference and examples come from the LabVIEW export in docs/lvdocs and the palette in lv_src/.vipb. Needs uv and git.
build-docs: (_docs "sphinx-build -E -W --keep-going -b dirhtml docs docs/_build/dirhtml")

# Live-preview the docs on http://127.0.0.1:8000, rebuilding on page, export or palette edits
serve-docs: (_docs "--with sphinx-autobuild sphinx-autobuild -b dirhtml docs docs/_build/dirhtml --watch lv_src/.vipb --ignore 'docs/ref/*' --ignore 'docs/examples/*'")

# `uv run` in the docs group, with the theme's newest commit layered over the one in uv.lock
_docs args:
    @sha=$(git ls-remote {{theme}} refs/heads/main | cut -f1); \
    if [ -n "$sha" ]; then echo "nominal-sphinx-theme: main, $sha" >&2; \
    else echo "nominal-sphinx-theme: can't reach GitHub, so building with the commit in uv.lock" >&2; fi; \
    uv run --group docs ${sha:+--with nominal-sphinx-theme@git+{{theme}}@$sha} {{args}}

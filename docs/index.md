# Nominal for LabVIEW

{.lead}
Stream data to [Nominal](https://nominal.io) from LabVIEW, and create and update the assets,
runs and events it belongs to.

```{toctree}
:hidden:
:caption: Guides

Overview <self>
```

```{toctree}
:hidden:
:caption: Examples

examples/index
```

```{toctree}
:hidden:
:caption: Reference

ref/index
```

## Install

Install the [Nominal IO Client](https://www.vipm.io/package/nominal_lib_nominal_io_client/)
package with VIPM. It needs LabVIEW 2020 SP1 or later. The VIs appear under **Data
Communication** on the Functions palette, and the examples in LabVIEW's examples folder.

A program opens a connection with {lv:vi}`Create Nominal Client` and closes it with
{lv:vi}`Destroy Nominal Client`.

::::{grid} 1 2 2 2
:gutter: 2

:::{grid-item-card} Examples
:link: examples/index
:link-type: doc

Example VIs that come with the package, with their block diagrams.
:::

:::{grid-item-card} Reference
:link: ref/index
:link-type: doc

Every VI on the palette: what it does, its inputs and outputs.
:::
::::

# LabVIEW Client for Nominal IO

<!-- labview-ci:dashboard -->
## LabVIEW CI

[![LabVIEW CI dashboard](https://img.shields.io/badge/LabVIEW%20CI-dashboard-2ea44f)](https://nominal-io.github.io/labview-client/)

LabVIEW CI runs on every pull request. See the [**CI dashboard**](https://nominal-io.github.io/labview-client/) for build status, VI Analyzer results, VI diffs, and mass-compile reports.

Streaming data to Nominal from LabVIEW.

[![Image](https://www.vipm.io/package/nominal_lib_nominal_io_client/badge.svg?metric=installs)](https://www.vipm.io/package/nominal_lib_nominal_io_client/) [![Image](https://www.vipm.io/package/nominal_lib_nominal_io_client/badge.svg?metric=stars)](https://www.vipm.io/package/nominal_lib_nominal_io_client/)


## Notes for developers
### LabVIEW Version
The sourcecode is written in **LabVIEW 2020 SP1** _32-bit or 64-bit_.

### Installing Dependencies
In the `lv_src` directory there is a `*.vipc` file. Apply this file using **VIPM**.

### Adding a development API Token
For development purposes, you can add a `.token` file to the `lv_src` directory of the repository containing your API token. LabVIEW will recognize this file for testing. The `.token` file is excluded from source control, allowing you to securely test your code without embedding your API token directly into the source code.

### Building the reuse package
In the `lv_src` directory there is a `*.vipb` file. This file is the build specification for **VIPM**.

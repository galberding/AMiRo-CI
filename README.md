# Configuration Builder and Tester
`amiroCI` is a testing tool written for the [AMiRo-OS](https://gitlab.ub.uni-bielefeld.de/AMiRo/AMiRo-OS.git) and [AMiRo-Apps](https://gitlab.ub.uni-bielefeld.de/AMiRo/AMiRo-Apps.git) project.
Goal is to utilize a configuration file that contains all desired parameters that should be tested, and apply those with the help of conditional compilation.
The results of all compile processes are gathered in a single report file,
presenting the used parameter configuration as well as _error_, _warn_ and _note_ messages.
This report can be compared to an existing one which generates an comparison containing only those compilations that does not exist or match those in the latter report.
The [Wiki](../../wikis/home) contains more detailed information about the capabilities and how
to use `amiroCI`.

## Setup
```bash
cd amiroci
pip install .
```

### Recommended Environment Setup
In order to test the Amiro-OS or Amiro-Apps the root needs to be provided.
This can be achieved on two different ways, with the CLI
or with environment variables:

```bash
export AOS_ROOT=path/to/Amiro-os
export AOS_APPS_ROOT=path/to/Amiro-apps
export AOS_REPLACE_CONF=path/to/replconf.yaml
```
The environment variables are interpreted as default but can be overwritten with the CLI.

### Execution

``` bash
amiroCI --help
```
For more detailed usage examples take a look at [CLI Usage](https://gitlab.ub.uni-bielefeld.de/AMiRo/amiroci/-/wikis/CLI%20Usage).

<!-- ## General Architecture -->
<!-- <img src="assets/architecture.png" -->
<!--      alt="Architecture" -->
<!--      style="float: left; margin-right: 10px;" /> -->

<!-- ## Search Module -->
<!-- ## Configuration Module -->
<!-- ## AutoCompile Module -->
<!-- ## Reporter Module -->
<!-- ## CLI -->

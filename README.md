# Configuration Builder and Tester
`amiroCI` is a testing tool written for the [AMiRo-OS]() and [AMiRo-Apps]() project.
Goal is to utilize a configuration file that contains all desired parameters that should be tested, and apply those with the help of conditional compilation.
The results of all compile processes are gathered in a single report file,
presenting the used parameter configuration as well as _error_, _warn_ and _note_ messages.
This report can be compared to an existing one which generates an comparison containing only those compilations that does not exist or match those in the latter report.
The [Wiki]() contains more detailed information about the capabilities and how
to use `amiroCI`.

## Setup
```bash
cd amiroci
pip install .
```

## Recommended Environment Setup
In order to test the Amiro-OS or Amiro-Apps the root needs to be provided.
This can be achieved on two different ways, with the CLI
or with environment variables:

```bash
export AOS_ROOT=path/to/Amiro-os
export AOS_APPS_ROOT=path/to/Amiro-apps
export AOS_REPLACE_CONF=path/to/replconf.yaml
```
The environment variables are interpreted as default but can be overwritten with the CLI.

## Replacement Configuration
The replacement config is intended to generate a configuration matrix.
This matrix can be edited and passed on to `amiroCI` in order to build all configurations listed.
The yaml config specifies what configurations to use for building the matrix.
All tags allowed are listed in the example below:

```yaml
# List of module names used for the test pipeline
Modules: ['DiWheelDrive_1-1']
# List of apps used for the pipeline
Apps: []

# Option Filter:
# Include or exclude specific groups
# Both take the hierarchy into account:
#   Include a subgroup requires including its parent
#   Excluding a parent means excluding its subgroups
IncludeGroups: []
ExcludeGroups: []

# Exclude combinations not matching the requirements
Dependencies:
  OS_CFG_TESTS_ENABLE:
    with_value: 'true'
    requires:
      OS_CFG_SHELL_ENABLE: 'true'

# Contains all option groups
Options:
    # Option or parent group
    AosconfOptionGroup:
        # Flag/Option passed to the compiler
        OS_CFG_DBG: ['true', 'false']
    UrtOptionGroup:
        ENABLE_TEST_MODE: ['true']
        # Subgroup or childgroup
        TestSetup:
            TEST_VLA1: [42, 100]
```
### Modules
* List of module names
* Used as target for the `Makefile`
* At least one Module is required

### Apps
* Used for Amiro-Apps build
* Is combined with `Modules`
* Leave it empty if the build only affects the `Amiro-OS`


### OptionGroups (e.g. AosconfOptions)
* Contains option groups
* Groups contain the configuration
* Groups can contain subgroups

### Option
* Consist of name followed by list of strings
* The values in the list are the configuration values used for the matrix

### Dependencies
* Basic filter to restrict matrix generation
* See #2

## Development

### Generate Documentation


### Test execution
```bash
# change to test directory
cd amiroci/test
# execute all tests
python test.py
```
<!-- ## General Architecture -->
<!-- <img src="assets/architecture.png" -->
<!--      alt="Architecture" -->
<!--      style="float: left; margin-right: 10px;" /> -->

<!-- ## Search Module -->
<!-- ## Configuration Module -->
<!-- ## AutoCompile Module -->
<!-- ## Reporter Module -->
<!-- ## CLI -->

# Configuration Builder and Tester
This tool is intended to detect conditional compilations, extract the specific flag
for a given module (aka directory) and store those in a database.
Furthermore, the extracted compilation parameters are used to create module specific configurations that
are used to build the project.
All possible combinations are tested. The results are saved and compared to a user provided configuration with
known errors and warnings.
Therefore, changes that cause undesired behavior for specific builds can be detected.

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
Modules: [
            'DiWheelDrive_1-1',
         ]
Apps: [

      ]

Options:
    AosconfOptions:
      # Flag to enable/disable debug API and logic.
      OS_CFG_DBG: ['true', 'false']

Dependencies:
  OS_CFG_TESTS_ENABLE:
    with_value: 'true'
    requires:
      OS_CFG_SHELL_ENABLE: 'true'
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
* Groups can be disabled when generating the config Matrix (TODO)

### Option
* Consist of name followed by list of strings
* The values in the list are the configuration values used for the matrix

### Dependencies
* Basic filter to restrict matrix generation
* See #2

## General Architecture
<img src="assets/architecture.png"
     alt="Architecture"
     style="float: left; margin-right: 10px;" />

<!-- ## Search Module -->
<!-- ## Configuration Module -->
<!-- ## AutoCompile Module -->
<!-- ## Reporter Module -->
<!-- ## CLI -->

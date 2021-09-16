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

# Option Filter:
IncludeOptions: []
ExcludeOptions: []


Options:
    AosconfOptionGroup:
      # Flag to enable/disable debug API and logic.
      OS_CFG_DBG: ['true', 'false']
    UrtOptionGroup:
		ENABLE_TEST_MODE: ['true']
		TEST_SETUP:
			TEST_VLA1: [42, 100]
			TEST_VAL2: [1, 2]

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

### Option Filter
With the `IncludeOptions` and `ExcludeOptions` tags it is possible to
activate or deactivate Option groups listed in `Options`
* `IncludeOptions` is always preferred
* Excluding a parent group that contains other groups automatically disables them, too
*

### OptionGroups (e.g. AosconfOptions)
* Contains option groups
* Groups contain the configuration
* Groups can be disabled when generating the config Matrix

### Option
* Consist of name followed by list of strings
* The values in the list are the configuration values used for the matrix

### Dependencies
* Basic filter to restrict matrix generation
* See #2

## Development

### Generate Documentation
The program is documented with Doxygen.
* Switch to the `doc` directory
* Generate documentation with `doxygen` or `doxywizard`
```bash
cd doc
doxygen Doxyfile
```
In order to use Doxygen commands inside the docstring it is required to
**place an exclamation mark** at the beginning of each comment.
Otherwise the commands are ignored.
```python
def myfunc(name: str) -> None:
	"""!Describe stuff here.
	@param name some fancy name

	@note
	Someting worth noting

	@return Nothing
	"""
```
All special command are listed [here](https://www.doxygen.nl/manual/commands.html#cmddef).

### Install
```bash
cd amiroci
pip install -e .
```
* This will fetch all required dependencies

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

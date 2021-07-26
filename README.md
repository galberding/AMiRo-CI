# Configuration Builder and Tester
This tool is intended to detect conditional compilations, extract the specific flag
for a given module (aka directory) and store those in a database.
Furthermore, the extracted compilation parameters are used to create module specific configurations that
are used to build the project.
All possible combinations are tested. The results are saved and compared to a user provided configuration with
known errors and warnings.
Therefore, changes that cause undesired behavior for specific builds can be detected.

## Default Configuration
The default configuration is stored in yaml format which is structured as follows:
```yaml
NUCLEO-L476RG:
  flags:
    BOARD_MPU6050_CONNECTED: [-DBOARD_MPU6050_CONNECTED]
    USE_COPT: [-std=c99, -fshort-enums]
    USE_CPPOPT: [-fno-rtti, -std=c++17]
    USE_EXCEPTIONS_STACKSIZE: ['0x400']
    USE_FPU: [softfp]
    USE_FPU_OPT: [-mfloat-abi=$(USE_FPU), -mfpu=fpv4-sp-d16]
    USE_LDOPT: [-lm]
    USE_LINK_GC: ['yes']
    USE_LTO: ['yes']
    USE_OPT: [-O2, -fstack-usage, '-Wl,--print-memory-usage']
    USE_PROCESS_STACKSIZE: ['0x400']
    USE_SMART_BUILD: ['no']
    USE_VERBOSE_COMPILE: ['no']
```

## General Architecture

<!-- ## Search Module -->
<!-- ## Configuration Module -->
<!-- ## AutoCompile Module -->
<!-- ## Reporter Module -->
<!-- ## CLI -->

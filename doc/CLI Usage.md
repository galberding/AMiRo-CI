This page contains general usage of the command line interface (CLI).
It involves setting up the correct paths to the projects and creating the replacement config.

## `amiroCI` CLI
```bash
> python amiroCI.py -h
usage: AmiroCI [-h] (--aos | --apps) [--project-root PROJECT_ROOT] [--repl-conf REPL_CONF]
               [--mat-name MAT_NAME] [--use-mat USE_MAT] [--execute]

optional arguments:
  -h, --help            show this help message and exit
  --aos                 Test Amiro-OS
  --apps                Test Amiro-Apps
  --project-root PROJECT_ROOT
                        Set path to project root, (Default: AOS_ROOT | AOS_APPS_ROOT)
  --repl-conf REPL_CONF
                        Set path to replacement config. (Default: AOS_REPLACE_CONF)
  --mat-name  MAT_NAME   Set name for config matrix (Default: conf_mat.tsv).
                        It is saved to the same directory as the replacement config.
  --use-mat USE_MAT, -m USE_MAT
                        Provide name for matrix to use.
  --execute, -e         Execute the test pipeline
```

## Default Paths
Per default the environment variables `AOS_ROOT`, `AOS_APPS_ROOT` and `AOS_REPLACE_CONF`
are evaluated and used for path the current project and replacement config.
Furthermore `AOS_REPLACE_CONF` specifies the directory for all artifacts such as the config matrix or
the generated reports.

An option to **override** those default paths is given with the `--project-root` and `--repl-conf` arguments.

## Select a Project
It is mandatory to select either AMiRo-OS (`--aos`) or AMiRo-Apps (`--apps`).
When using `--project-root` the path for the selected project is expected.
```bash
> python amiroCI --aos --project-root path/to/amiro-os
```

## Configuration Matrix
The matrix is always generates with name `conf_mat.tsv` at parent directory of `AOS_REPLACE_CONF`.
The name can be adjusted with `--mat-name`.
```bash
> python amiroCI --aos --mat-name test_mat.tsv
```
It is possible to use a previously generated matrix with `--use-mat`.
```bash
> python amiroCI --aos --use-mat test_mat.tsv
```
This however expects that the matrix with name `test_mat.tsv` is located at `AOS_REPLACE_CONF`.
**There is currently no functionality that allows specifying a path!**


## Check Configuration
Before executing the pipeline with `-e | --execute` take a look at the output that is
provided:
```bash
> python amiroCI.py --aos
INFO:amiroCI: Aos selected
INFO:amiroCI: Regenerate Matrix
INFO:amiroCI: Dump generated matrix to:
/home/schorschi/hiwi/amiroci/assets/conf_mat.tsv
INFO:amiroCI: Current Configuration:
    Project Root:	/home/schorschi/hiwi/AMiRo-OS
    Repl Config:	/home/schorschi/hiwi/amiroci/assets/repl_conf.yml
    Config Groups:	AosconfOption

INFO:amiroCI: Ready to go, use -e to execute the pipeline.
```
Here you can ensure that the selected configuration matches your expectation.
It shows:
* if a matrix was created and where it was written to
* the selected project root
* the replacement config path
* all selected [Config Groups]()

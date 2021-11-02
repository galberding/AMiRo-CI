## Installation
When you intend to develop it is useful to make an editable install with `pip`.
```bash
cd amiroci
pip install -e .
```
This will fetch and install all required dependencies.


## Test execution
At first all tests where written with the `unittest` framework.
Luckily `pytest` has full support for those tests.
I encourage you to use `pytest` for all new test implementations because of their superior fixture
system.
```bash
cd amiroci
pytest
```

## Logging
A simple but easy access logging system is available that can be added to
each class when needed for debugging or show information to the user.
Use the provided logger from `aos_logger` with `get_logger()`:
```python
from amiroci.tools.aos_logger import get_logger
class Foo:
	def __init__():
		self.log = get_logger(name, level, out)
```
Despite the `name` it is also possible to set the log `level` and output (`out`).
In default configuration all loggers write to `logs/genera.log`.
Setting `out = None` causes the logger to write to the terminal.


## Profiling
Using the CLI will automatically profile the application and write the results
to `logs/amiroci.perf`
One way to visualize the results is to use `snakeviz` which is easily installable
with `pip install snakeviz`.
The following will open a webserver and show the profiling results in the
browser:
```bash
snakeviz logs/amiroci.perf
```

## Documentation
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
All special commands are listed [here](https://www.doxygen.nl/manual/commands.html#cmddef).

## Formatting
In order to keep a consistent style the code formatter [yapf](https://github.com/google/yapf) is used.
Install it with:
```bash
pip install yapf
```
In order to quickly format all files in the repository issue
```bash
yapf --style='{based_on_style: facebook, indent_width: 4, split_before_logical_operator: True}' -r -p -i .
```

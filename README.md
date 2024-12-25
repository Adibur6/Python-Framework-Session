# Python Framework Session sample code

## install dependencies

Create and activate virtual environment

```
python3 -m venv .venv
source .venv/bin/activate
```

Install the dependencies

```
pip install -r requirements.txt
```

The `requirements.txt` is generated using a tool named `pip-tools` (`pip install pip-tools`). We can define our top level project dependencies in the `requirements.in` file and then run `pip-compile`. It will see the dependencies listed in the `requirements.in`, figure out all the dependencies of those dependencies as well, and then generate the `requirements.txt`.

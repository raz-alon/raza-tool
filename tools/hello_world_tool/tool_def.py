import os

from . import main
import inspect


from kubiya_sdk.tools.models import Tool, Arg, FileSpec
from kubiya_sdk.tools.registry import tool_registry

def _get_requirements_content() -> str:
    with open(os.path.join(os.path.dirname(__file__), '../../requirements.txt'), 'r') as f:
        return f.read()

hello_tool = Tool(
    name="say_hello2",
    type="docker",
    image="python:3.12",
    description="Prints hello {name}!",
    args=[Arg(name="name", description="name to say hello to", required=True)],
    content="""
curl -LsSf https://astral.sh/uv/install.sh | sh > /dev/null 2>&1
. $HOME/.cargo/env

uv venv > /dev/null 2>&1
. .venv/bin/activate > /dev/null 2>&1

uv pip install -r /tmp/requirements.txt > /dev/null 2>&1

python /tmp/main.py "{{ .name }}"
""",
    with_files=[
        FileSpec(
            destination="/tmp/main.py",
            content=inspect.getsource(main),
        ),
        FileSpec(
            destination="/tmp/requirements.txt",
            content=_get_requirements_content(),
        ),
    ],
)

tool_registry.register("hello", hello_tool)

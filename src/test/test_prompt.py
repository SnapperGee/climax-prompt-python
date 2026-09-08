import builtins
from collections.abc import Callable
from typing import Final
from unittest.mock import call, patch

from climax.prompt import StringInput, StringPrompt, StringValidator
from pytest import mark, raises

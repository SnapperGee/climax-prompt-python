"""Smoke tests that run against an installed copy of the package."""

import json
from importlib.metadata import distribution, version
from pathlib import Path

import climax.prompt


def main() -> None:
    installed_version = version("climax-prompt")
    assert installed_version, "Package metadata has no version."

    # Make sure Python imported the installed copy and not the source tree.
    module_path = Path(climax.prompt.__file__)
    assert "site-packages" in module_path.parts, f"Imported from {module_path}."

    def string_is_integer(string: climax.prompt.StringPromptInput) -> str | None:
        start_index = 1 if string.formatted.startswith("-") or string.formatted.startswith("+") else 0

        return (
            None
            if string.formatted[start_index:].isdecimal()
            else f'Provided input is not an integer: "{string.formatted}"\n'
        )

    def is_positive_even_integer(integer: int) -> str | None:
        if integer <= 0:
            return f"Integer isn't positive: {integer}\n"

        if integer % 2 != 0:
            return f"Integer isn't even: {integer}\n"

        return None

    string_prompt = climax.prompt.StringPrompt(
        "Input a positive even integer: ",
        string_validator=string_is_integer,
        formatter=lambda a_string: a_string.strip().lower(),
        ps1=">>> ",
    )

    _ = climax.prompt.Prompt[int](
        string_prompt,
        int,
        validator=is_positive_even_integer,
    )

    origin = json.loads(distribution("climax-prompt").read_text("direct_url.json") or "{}").get("url", "unknown")
    print(f"Smoke tests passed for climax-prompt {installed_version} (installed from {Path(origin).name}).")


if __name__ == "__main__":
    main()

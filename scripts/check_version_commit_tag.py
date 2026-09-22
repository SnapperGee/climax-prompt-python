from re import compile as re_compile
from subprocess import check_output
from sys import exit, stdin
from typing import Final

VERSION_TAG_PATTERN: Final = re_compile(r"v\d+\.\d+\.\d+")
TAG_REF_PREFIX: Final = "refs/tags/"


def get_expected_version() -> str:
    output: Final = check_output(("poetry", "version", "-s"), text=True)
    return "v" + output.strip()


def is_null_oid(oid: str) -> bool:
    return not oid.strip("0")


def pushed_tag_names(input_text: str) -> tuple[str, ...]:
    tags: list[str] = []

    for line in input_text.splitlines():
        fields = line.split()
        if len(fields) != 4:
            continue

        local_ref, local_oid, _remote_ref, _remote_oid = fields
        if is_null_oid(local_oid):
            # Tag deletion; nothing to validate.
            continue

        if local_ref.startswith(TAG_REF_PREFIX):
            tags.append(local_ref.removeprefix(TAG_REF_PREFIX))

    return tuple(tags)


def main() -> None:
    input_text: Final = stdin.read()
    candidate_tags: Final = pushed_tag_names(input_text)
    version_tags: Final = tuple(tag for tag in candidate_tags if VERSION_TAG_PATTERN.fullmatch(tag))

    if not version_tags:
        return

    expected: Final = get_expected_version()
    invalid_tags: Final = tuple(tag for tag in version_tags if tag != expected)

    if invalid_tags:
        print(f"Tag mismatch: {invalid_tags}. Expected: {expected}")
        exit(1)


if __name__ == "__main__":
    main()

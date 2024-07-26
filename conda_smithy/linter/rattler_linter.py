import os
from typing import Any, Dict, List, Optional

from conda_smithy.linter.utils import TEST_FILES

REQUIREMENTS_ORDER = ["build", "host", "run"]

EXPECTED_SINGLE_OUTPUT_SECTION_ORDER = [
    "context",
    "package",
    "source",
    "build",
    "requirements",
    "tests",
    "about",
    "extra",
]

EXPECTED_MULTIPLE_OUTPUT_SECTION_ORDER = [
    "context",
    "recipe",
    "source",
    "build",
    "outputs",
    "about",
    "extra",
]
TEST_KEYS = {"script", "python"}


def lint_recipe_tests(
    recipe_dir: Optional[str],
    test_section: Dict[str, Any],
    outputs_section: List[Dict[str, Any]],
    lints: List[str],
    hints: List[str],
):
    tests_lints = []
    tests_hints = []

    if not any(key in TEST_KEYS for key in test_section):
        a_test_file_exists = recipe_dir is not None and any(
            os.path.exists(os.path.join(recipe_dir, test_file))
            for test_file in TEST_FILES
        )
        if a_test_file_exists:
            return

        if not outputs_section:
            lints.append("The recipe must have some tests.")
        else:
            has_outputs_test = False
            no_test_hints = []
            for section in outputs_section:
                test_section = section.get("tests", {})
                if any(key in TEST_KEYS for key in test_section):
                    has_outputs_test = True
                else:
                    no_test_hints.append(
                        "It looks like the '{}' output doesn't "
                        "have any tests.".format(section.get("name", "???"))
                    )
            if has_outputs_test:
                hints.extend(no_test_hints)
            else:
                lints.append("The recipe must have some tests.")

    lints.extend(tests_lints)
    hints.extend(tests_hints)

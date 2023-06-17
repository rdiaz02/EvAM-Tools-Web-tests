import json
import argparse

from os import getenv, path, makedirs
from typing import List
from selenium_core.selenium_wrapper import validate_browser
from dotenv import load_dotenv

try:
    load_dotenv()
except FileNotFoundError:
    print(
        "No .env file found. Make sure you have a .env file in the root folder of the project"
    )
    exit(1)

TESTS_SELECTOR_PATH = getenv("TESTS_SELECTOR_PATH")
SCREENSHOTS_PATH = "screenshots/"
CHECK_FOLDER = path.isdir(SCREENSHOTS_PATH)


def main() -> None:
    """
    The entry point of the program.

    Parses command line arguments, validates the browser, selects the tests to run, and runs them.

    Returns:
        None
    """
    args = argparse.ArgumentParser()
    args.add_argument(
        "--tests_list",
        dest="tests_list",
        help="Name of the tests group to execute",
        default="active_tests",
        type=str,
    )
    args.add_argument(
        "--browser",
        dest="browser",
        help="Desired browser to execute the tests",
        default="firefox",
        type=str,
    )

    args = args.parse_args()

    if not validate_browser(args.browser):
        return

    if not CHECK_FOLDER:
        makedirs(SCREENSHOTS_PATH)
        print("Created folder : ", SCREENSHOTS_PATH)

    tests_to_run = select_tests(TESTS_SELECTOR_PATH)

    for tests_group in tests_to_run[args.tests_list]:
        run_test(tests_group)


def select_tests(path: str) -> List[dict]:
    """
    Reads a JSON file containing test data and returns a list of test dictionaries.

    Args:
        path (str): The path to the JSON file.

    Returns:
        List[dict]: A list of test dictionaries.
    """
    tests_file = open(path)
    data = json.load(tests_file)
    tests_file.close()

    return data


def run_test(tests_to_execute: dict) -> None:
    """
    Runs a test specified in the `tests_to_execute` dictionary.

    Args:
        tests_to_execute (dict): A dictionary containing the name of the test module and its arguments.

    Returns:
        None
    """
    test_name = tests_to_execute["module"]
    args = tests_to_execute["args"]
    args["name"] = test_name

    try:
        test_module = __import__("tests." + test_name)
    except ModuleNotFoundError:
        print(
            f"Test module [{test_name}] not found. Make sure this test is located in the tests folder"
        )
        return

    test_class = getattr(test_module, test_name)
    test_instance = test_class.TestMethod(**args)

    print("Running test: " + str(test_name))

    test_instance.run()


if __name__ == "__main__":
    main()

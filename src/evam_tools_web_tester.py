import json
import argparse

from os import getenv
from typing import List
from selenium_core.selenium_wrapper import validate_browser

TESTS_SELECTOR_PATH = getenv("TESTS_SELECTOR_PATH")


def main() -> None:
    """
    The entry point of the program.

    Parses command line arguments, validates the browser, selects the tests to run, and runs them.

    Returns:
        None
    """
    # Create an ArgumentParser object and add two arguments to it: tests_list and browser
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

    # Parse the command line arguments
    args = args.parse_args()

    # Validate the browser
    if not validate_browser(args.browser):
        return

    # Select the tests to run
    tests_to_run = select_tests(TESTS_SELECTOR_PATH)

    # Run the tests
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
    # Open the JSON file
    tests_file = open(path)

    # Load the JSON data into a Python object
    data = json.load(tests_file)

    # Close the file
    tests_file.close()

    # Return the list of test dictionaries
    return data


def run_test(tests_to_execute: dict) -> None:
    """
    Runs a test specified in the `tests_to_execute` dictionary.

    Args:
        tests_to_execute (dict): A dictionary containing the name of the test module and its arguments.

    Returns:
        None
    """
    # Get the name of the test module and its arguments from the `tests_to_execute` dictionary
    test_name = tests_to_execute["module"]
    args = tests_to_execute["args"]
    args["name"] = test_name

    try:
        # Import the test module
        test_module = __import__("tests." + test_name)
    except ModuleNotFoundError:
        print(
            f"Test module [{test_name}] not found. Make sure this test is located in the tests folder"
        )
        return

    # Get the test class from the test module
    test_class = getattr(test_module, test_name)

    # Create an instance of the test class with the specified arguments
    test_instance = test_class.TestMethod(**args)

    # Print a message indicating that the test is running
    print("Running test: " + str(test_name))

    # Run the test instance
    test_instance.run()


if __name__ == "__main__":
    main()

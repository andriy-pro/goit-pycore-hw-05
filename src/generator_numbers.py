import re
from typing import Callable, Generator


def generator_numbers(text: str) -> Generator[float, None, None]:
    """
    Analyzes a text, identifies all valid numbers considered parts of income, and returns them as a generator.

    Parameters
    ----------
    text : str
        The input text to analyze for valid numbers.

    Yields
    ------
    float
        The valid numbers found in the text.
    """
    # Regular expression to find numbers with optional comma or period as decimal separator
    pattern = re.compile(r" \d+(?:[.,]\d+)? ")

    for match in pattern.finditer(text):
        # Replace commas with periods for float conversion and strip any surrounding spaces
        yield float(match.group().replace(",", ".").strip())


def sum_profit(text: str, func: Callable[[str], Generator[float, None, None]]) -> float:
    """
    Uses the generator function to calculate the total sum of the numbers in the input string.

    Parameters
    ----------
    text : str
        The input text to analyze for valid numbers.
    func : Callable[[str], Generator[float, None, None]]
        The generator function that extracts numbers from the text.

    Returns
    -------
    float
        The total sum of the valid numbers in the text.
    """
    return sum(func(text))


# Example usage
if __name__ == "__main__":
    text = (
        "The total income of the employee consists of several parts: 1000.01 as the main income, "
        "supplemented by additional receipts of 27,45 , 324.00 and 100 dollars."
    )
    total_income = sum_profit(text, generator_numbers)
    print(f"Total income: {total_income}")

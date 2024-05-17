from typing import Callable, Dict


def caching_fibonacci() -> Callable[[int], int]:
    """
    Creates a Fibonacci function that uses a cache to store computed values.

    Returns
    -------
    Callable[[int], int]
        A function that computes the nth Fibonacci number using a cache.
    """
    cache: Dict[int, int] = {}

    def fibonacci(n: int) -> int:
        """
        Computes the nth Fibonacci number using a cache.

        Parameters
        ----------
        n : int
            The position in the Fibonacci sequence to compute.
            Must be a non-negative integer.

        Returns
        -------
        int
            The nth Fibonacci number.

        Raises
        ------
        ValueError
            If the input is a negative integer.
        """
        if n < 0:
            raise ValueError("Input must be a non-negative integer.")
        if n == 0:
            return 0
        if n == 1:
            return 1
        if n not in cache:
            # Store the computed value in cache to avoid redundant calculations
            cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        return cache[n]

    return fibonacci


# Example Usage
if __name__ == "__main__":
    fib = caching_fibonacci()
    print(fib(10))  # Outputs 55
    print(fib(15))  # Outputs 610

import sys
from typing import List, Dict, Literal, NamedTuple, Optional
from collections import Counter
from datetime import datetime, date, time

EXPECTED_FORMAT = "YYYY-MM-DD HH:MM:SS LEVEL Message"
LOG_LEVELS = {"INFO", "ERROR", "DEBUG", "WARNING"}


class LogEntry(NamedTuple):
    date: date
    time: time
    level: Literal["INFO", "ERROR", "DEBUG", "WARNING"]
    message: str


def error_message(message: str, line: str = "", details: str = ""):
    """
    Display an error message with details.

    Parameters
    ----------
    message : str
        The main error message.
    line : str, optional
        The log line that caused the error (default is "").
    details : str, optional
        Additional details about the error (default is "").
    """
    print(f"Error: {message}")
    if details:
        print(f"Details: {details}")
    if line:
        print(f"Line: {line.strip()}")
    print(f"Expected format: {EXPECTED_FORMAT}\n")


def parse_log_line(line: str) -> Optional[LogEntry]:
    """
    Parse a log line into its components.

    Parameters
    ----------
    line : str
        A single line from the log file.

    Returns
    -------
    Optional[LogEntry]
        A named tuple with parsed components if the line is valid, otherwise None.
    """
    parts = line.split(" ", 3)
    if len(parts) < 4:
        error_message("Invalid log string format", line)
        return None

    try:
        log_date = datetime.strptime(parts[0], "%Y-%m-%d").date()
        log_time = datetime.strptime(parts[1], "%H:%M:%S").time()
    except ValueError as e:
        error_message("Date or time format error", line, str(e))
        return None

    log_level = parts[2].upper()
    if log_level not in LOG_LEVELS:
        error_message("Invalid log level", line, f"'{log_level}' not in {LOG_LEVELS}")
        return None

    return LogEntry(
        date=log_date,
        time=log_time,
        level=log_level,
        message=parts[3].strip(),
    )


def load_logs(file_path: str) -> List[LogEntry]:
    """
    Load and parse logs from a file.

    Parameters
    ----------
    file_path : str
        The path to the log file.

    Returns
    -------
    List[LogEntry]
        A list of dictionaries, each representing a parsed log line.
    """
    logs = []
    try:
        with open(file_path, "r") as file:
            for line in file:
                parsed_line = parse_log_line(line.strip())
                if parsed_line:
                    logs.append(parsed_line)
    except FileNotFoundError:
        error_message(f"The file {file_path} does not exist.")
        sys.exit(1)
    except Exception as e:
        error_message("An error occurred while reading the file", "", str(e))
        sys.exit(1)

    if not logs:
        error_message("No valid log entries found. Please check the log file format.")
        sys.exit(1)

    return logs


def filter_logs_by_level(logs: List[LogEntry], level: str) -> List[LogEntry]:
    """
    Filter logs by logging level.

    Parameters
    ----------
    logs : List[LogEntry]
        A list of parsed log entries.
    level : str
        The logging level to filter by (e.g., 'INFO', 'ERROR').

    Returns
    -------
    List[LogEntry]
        A list of log entries that match the specified logging level.
    """
    return [log for log in logs if log.level == level.upper()]


def count_logs_by_level(logs: List[LogEntry]) -> Dict[str, int]:
    """
    Count the number of log entries for each logging level.

    Parameters
    ----------
    logs : List[LogEntry]
        A list of parsed log entries.

    Returns
    -------
    Dict[str, int]
        A dictionary with logging levels as keys and counts as values.
    """
    levels = [log.level for log in logs]
    return dict(Counter(levels))


def display_log_counts(counts: Dict[str, int]):
    """
    Display the log counts in a formatted table.

    Parameters
    ----------
    counts : Dict[str, int]
        A dictionary with logging levels as keys and counts as values.
    """
    print()
    print("Logging Level │ Count")
    print("──────────────┼──────")
    for level, count in sorted(counts.items()):
        print(f"{level:<13} │ {count}")


def display_filtered_logs(logs: List[LogEntry], level: str):
    """
    Display the details of filtered logs for a specific level.

    Parameters
    ----------
    logs : List[LogEntry]
        A list of log entries to display.
    level : str
        The logging level of the entries to display.
    """
    if not logs:
        print(f"No log entries found for level '{level.upper()}'.")
        return

    print(f"\nLog details for level '{level.upper()}':")
    for log in logs:
        print(f"{log.date} {log.time} - {log.message}")


def main():
    """
    Main function to run the log file analysis.
    """
    if len(sys.argv) < 2:
        error_message("Usage: python3 log_analyzer.py /path/to/logfile.log [level]")
        sys.exit(1)

    log_file_path = sys.argv[1]
    log_level = sys.argv[2].upper() if len(sys.argv) > 2 else None

    if log_level and log_level not in LOG_LEVELS:
        print(
            f"\nWarning: '{log_level}' is not a valid log level!\nValid levels are: {', '.join(LOG_LEVELS)}\n"
        )
        log_level = None

    logs = load_logs(log_file_path)
    counts = count_logs_by_level(logs)
    display_log_counts(counts)

    if log_level:
        filtered_logs = filter_logs_by_level(logs, log_level)
        display_filtered_logs(filtered_logs, log_level)


if __name__ == "__main__":
    main()

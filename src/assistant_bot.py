import sys
from typing import Callable, Dict, List, Optional
from colorama import Fore, Style, init


def input_error(handler: Callable) -> Callable:
    """Decorator for handling errors in command functions."""

    def wrapper(*args, **kwargs):
        try:
            return handler(*args, **kwargs)
        except TypeError as e:
            print(
                f"{Fore.RED}Error: Incorrect command.\n{Fore.MAGENTA}{e}{Style.RESET_ALL}"
            )
            help_command()
        except ValueError as e:
            print(
                f"{Fore.RED}Error: Incorrect arguments.\n{Fore.MAGENTA}{e}{Style.RESET_ALL}"
            )
        except KeyError as e:
            print(
                f"{Fore.RED}Error: Contact not found.\n{Fore.MAGENTA}{e}{Style.RESET_ALL}"
            )
        except IndexError as e:
            print(
                f"{Fore.RED}Error: Index out of range.\n{Fore.MAGENTA}{e}{Style.RESET_ALL}"
            )
        except Exception as e:
            print(
                f"{Fore.RED}An unexpected error occurred:\n{Fore.MAGENTA}{e}{Style.RESET_ALL}"
            )

    return wrapper


def parse_input(user_input: str) -> tuple[str, List[str]]:
    """Parse the user input into a command and arguments.

    Parameters
    ----------
    user_input : str
        The input string from the user.

    Returns
    -------
    tuple[str, List[str]]
        The command and a list of arguments.
    """
    parts = user_input.lower().split()
    command = parts[0] if parts else ""
    args = parts[1:] if len(parts) > 1 else []
    return command, args


@input_error
def handle_command(
    command_handlers: Dict[str, Callable[[Optional[List[str]]], None]],
    command: str,
    args: Optional[List[str]],
) -> None:
    """Handle the given command using the appropriate handler.

    Parameters
    ----------
    command_handlers : Dict[str, Callable[[Optional[List[str]]], None]]
        A dictionary mapping commands to their handlers.
    command : str
        The command to handle.
    args : Optional[List[str]]
        The arguments for the command.
    """
    if command in command_handlers:
        if args is not None:
            command_handlers[command](args)
        else:
            raise ValueError(f"The command '{command}' requires arguments.")
    else:
        raise TypeError(f"Unknown command '{command}'")


@input_error
def hello() -> None:
    """Greet the user."""
    print(f"{Fore.CYAN}How can I help you?{Style.RESET_ALL}")


@input_error
def add_contact(contacts: Dict[str, str], *args: str) -> None:
    """Add a new contact.

    Parameters
    ----------
    contacts : Dict[str, str]
        The dictionary of contacts.
    args : str
        The name and phone number of the new contact.
    """
    if len(args) != 2:
        raise ValueError("Usage: add [name] [phone number]")
    name, phone = args
    if name in contacts:
        if contacts[name] == phone:
            print(
                f'{Fore.YELLOW}Contact "{Fore.CYAN}{name}{Fore.YELLOW}" with phone number "{Fore.CYAN}{phone}{Fore.YELLOW}" already exists.{Style.RESET_ALL}'
            )
        else:
            current_phone = contacts[name]
            print(
                f'{Fore.YELLOW}Contact "{Fore.CYAN}{name}{Fore.YELLOW}" is already added with the number "{Fore.CYAN}{current_phone}{Fore.YELLOW}".\nTo change the number, use the "{Style.RESET_ALL}change{Fore.YELLOW}" command.{Style.RESET_ALL}'
            )
    else:
        contacts[name] = phone
        print(
            f'{Fore.GREEN}Contact "{Fore.CYAN}{name}{Fore.GREEN}" added with phone number "{Fore.CYAN}{phone}{Fore.GREEN}".{Style.RESET_ALL}'
        )


@input_error
def change_contact(contacts: Dict[str, str], *args: str) -> None:
    """Change an existing contact's phone number.

    Parameters
    ----------
    contacts : Dict[str, str]
        The dictionary of contacts.
    args : str
        The name and new phone number of the contact.
    """
    if len(args) != 2:
        raise ValueError("Usage: change [name] [new phone number]")
    name, new_phone = args
    if name in contacts:
        current_phone = contacts[name]
        if new_phone == current_phone:
            print(
                f'{Fore.YELLOW}Contact "{Fore.CYAN}{name}{Fore.YELLOW}" already has this phone number: "{Fore.CYAN}{new_phone}{Fore.YELLOW}". No changes were made.{Style.RESET_ALL}'
            )
        else:
            contacts[name] = new_phone
            print(
                f'{Fore.GREEN}For user {Fore.CYAN}"{name}"{Fore.GREEN}, the phone has been changed from "{Fore.CYAN}{current_phone}{Fore.GREEN}" to "{Fore.CYAN}{new_phone}{Fore.GREEN}".{Style.RESET_ALL}'
            )
    else:
        raise KeyError(f"Name '{name}' not found.")


@input_error
def show_phone(contacts: Dict[str, str], *args: str) -> None:
    """Show the phone number of a contact.

    Parameters
    ----------
    contacts : Dict[str, str]
        The dictionary of contacts.
    args : str
        The name of the contact.
    """
    if len(args) != 1:
        raise ValueError("Usage: phone [name]")
    name = args[0]
    if name in contacts:
        print(
            f'{Fore.GREEN}Phone number of "{Fore.CYAN}{name}{Fore.GREEN}": {Fore.CYAN}{contacts[name]}{Style.RESET_ALL}'
        )
    else:
        raise KeyError(f"Name '{name}' not found.")


@input_error
def show_all_contacts(contacts: Dict[str, str]) -> None:
    """Show all contacts.

    Parameters
    ----------
    contacts : Dict[str, str]
        The dictionary of contacts.
    """
    if contacts:
        for name, phone in contacts.items():
            print(f"{Fore.GREEN}{name}: {Fore.CYAN}{phone}{Style.RESET_ALL}")
    else:
        raise IndexError("No contacts available.")


def handle_exit() -> None:
    """Exit the program."""
    print(f"{Fore.GREEN}{Style.BRIGHT}Good bye!{Style.RESET_ALL}")
    sys.exit()


def help_command():
    """Display the help information with available commands."""
    print(f"{Fore.GREEN}This bot helps you manage your contacts.{Style.RESET_ALL}")
    print(f"{Fore.GREEN}You can use the following commands:{Style.RESET_ALL}")
    print(f"hello{Fore.GREEN} - Greets the user.{Style.RESET_ALL}")
    print(
        f"add [name] [phone number]{Fore.GREEN} - Adds a new contact.{Style.RESET_ALL}"
    )
    print(
        f"change [name] [new phone number]{Fore.GREEN} - Changes the phone number of an existing contact.{Style.RESET_ALL}"
    )
    print(
        f"phone [name]{Fore.GREEN} - Shows the phone number of a contact.{Style.RESET_ALL}"
    )
    print(f"all{Fore.GREEN} - Shows all contacts.{Style.RESET_ALL}")
    print(f"close, exit, quit{Fore.GREEN} - Exits the program.{Style.RESET_ALL}")
    print(f"help{Fore.GREEN} - Displays a list of available commands.{Style.RESET_ALL}")
    print()
    print(f"{Fore.CYAN}Example usage:{Style.RESET_ALL}")
    print(
        f"add John 1234567890{Fore.GREEN} - Adds a contact named {Fore.CYAN}John{Fore.GREEN} with phone number {Fore.CYAN}1234567890.{Style.RESET_ALL}"
    )
    print(
        f"phone John{Fore.GREEN} - Shows the phone number of {Fore.CYAN}John.{Style.RESET_ALL}\n"
    )


def main() -> None:
    """Main function that runs the command line interface for an assistant bot."""
    contacts: Dict[str, str] = {}
    command_handlers: Dict[str, Callable[[Optional[List[str]]], None]] = {
        "hello": lambda _: hello(),
        "add": lambda args: add_contact(contacts, *args),
        "change": lambda args: change_contact(contacts, *args),
        "phone": lambda args: show_phone(contacts, *args),
        "all": lambda _: show_all_contacts(contacts),
        "close": lambda _: handle_exit(),
        "exit": lambda _: handle_exit(),
        "quit": lambda _: handle_exit(),
        "help": lambda _: help_command(),
    }

    init(autoreset=True)  # Initialize colorama

    banner_part_1 = """
     _               _       _                 _     ____          _                ____  
    / \    ___  ___ (_) ___ | |_  __ _  _ __  | |_  | __ )   ___  | |_    __   __  |___ \ 
   / _ \  / __|/ __|| |/ __|| __|/ _` || '_ \ | __| |  _ \  / _ \ | __|   \ \ / /    __) |
  / ___ \ \__ \\\__ \| |\__ \| |_| (_| || | | || |_  | |_) || (_) || |_     \ V /_   / __/ 
 /_/   \_\|___/|___/|_||___/ \__|\__,_||_| |_| \__| |____/  \___/  \__|     \_/(_) |_____|
                                                                                          
"""
    print(f"{Fore.GREEN}{banner_part_1}{Style.RESET_ALL}")
    print()
    print(
        f"{Fore.CYAN}{Style.BRIGHT}Welcome to the Assistant Bot v.2!{Style.RESET_ALL}"
    )
    print()
    help_command()

    while True:
        user_input = input(f"{Fore.YELLOW}Enter a command: {Style.RESET_ALL}").strip()
        command, args = parse_input(user_input)
        handle_command(command_handlers, command, args)


if __name__ == "__main__":
    main()

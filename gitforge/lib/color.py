class ansi_color:
    """
    Only works on posix platforms
    """

    reset = "\033[0m"
    bold = "\033[01m"
    disable = "\033[02m"
    underline = "\033[04m"
    reverse = "\033[07m"
    strikethrough = "\033[09m"
    invisible = "\033[08m"

    class fg:
        black = "\033[30m"
        red = "\033[31m"
        green = "\033[32m"
        orange = "\033[33m"
        blue = "\033[34m"
        purple = "\033[35m"
        cyan = "\033[36m"
        lightgrey = "\033[37m"
        darkgrey = "\033[90m"
        lightred = "\033[91m"
        lightgreen = "\033[92m"
        yellow = "\033[93m"
        lightblue = "\033[94m"
        pink = "\033[95m"
        lightcyan = "\033[96m"

    class bg:
        black = "\033[40m"
        red = "\033[41m"
        green = "\033[42m"
        orange = "\033[43m"
        blue = "\033[44m"
        purple = "\033[45m"
        cyan = "\033[46m"
        lightgrey = "\033[47m"


class win_color:
    """
    Not implemented yet...
    """

    reset = "[0m"
    bold = "[1m"
    disable = "[0m"
    underline = "[4m"
    reverse = "[7m"

    class fg:
        black = "[30m"
        red = "[31m"
        green = "[32m"
        orange = "[33m"
        blue = "[34m"
        purple = "[35m"
        cyan = "[36m"
        lightgrey = "[37m"
        darkgrey = "[90m"
        lightred = "[91m"
        lightgreen = "[92m"
        yellow = "[93m"
        lightblue = "[94m"
        pink = "[95m"
        lightcyan = "[96m"

    class bg:
        black = "[40m"
        red = "[41m"
        green = "[42m"
        orange = "[43m"
        blue = "[44m"
        purple = "[45m"
        cyan = "[46m"
        lightgrey = "[47m"

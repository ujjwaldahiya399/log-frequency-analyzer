from colorama import Fore, Back, Style, init

# Auto-reset color after every print
init(autoreset=True)


# ── Text Colors ────────────────────────────────────────────

def red(text):
    return Fore.RED + str(text)

def green(text):
    return Fore.GREEN + str(text)

def yellow(text):
    return Fore.YELLOW + str(text)

def cyan(text):
    return Fore.CYAN + str(text)

def white(text):
    return Fore.WHITE + str(text)

def bright(text):
    return Style.BRIGHT + str(text)


# ── Semantic Helpers ───────────────────────────────────────
# These give meaning to colors so we use them consistently

def success(text):
    """Green — things that worked."""
    return Fore.GREEN + str(text)

def error(text):
    """Red — errors, failures, dangerous things."""
    return Fore.RED + str(text)

def warning(text):
    """Yellow — warnings, suspicious things."""
    return Fore.YELLOW + str(text)

def info(text):
    """Cyan — headers, labels, neutral info."""
    return Fore.CYAN + str(text)

def highlight(text):
    """Bright white — important values."""
    return Style.BRIGHT + Fore.WHITE + str(text)


# ── Status Code Coloring ───────────────────────────────────

def color_status(status):
    """Color a status code based on its group."""
    if status < 300:
        return green(status)     # 2xx success
    elif status < 400:
        return cyan(status)      # 3xx redirect
    elif status < 500:
        return yellow(status)    # 4xx client error
    else:
        return red(status)       # 5xx server error


# ── Bar Chart Coloring ─────────────────────────────────────

def color_bar(count, max_count):
    """Color a bar based on how high the count is relative to max."""
    ratio = count / max_count if max_count > 0 else 0
    bar = '█' * min(count, 40)
    if ratio > 0.7:
        return red(bar)          # high traffic — red
    elif ratio > 0.4:
        return yellow(bar)       # medium traffic — yellow
    else:
        return green(bar)        # low traffic — green
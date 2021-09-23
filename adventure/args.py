from adventure.formatting import error

def extra_args(cmd, args):
    if not args:
        return

    error(f'{cmd} received unknown arguments: {", ".join(args)}')

def validate(cmd, val, name, choices=[], options=[], klass=None):
    """."""
    if not val:
        return

    # check for type
    if klass:
        try:
            val = klass(val)
        except (TypeError, ValueError):
            error(f"({cmd}) {name} should be a {klass.__name__}. got: {val!r}")

    # check for valid option
    if (choices or options) and \
            val.lower() not in [str(x).lower() for x in list(choices)+list(options)]:
            error(f'({cmd}) {name} invalid: {val!r} ({", ".join(choices)})')

    return val

def require(cmd, val, name, choices=[], options=[], klass=None):
    """Validate required argument"""
    # check not blank
    if not val:
        message = f"{cmd} needs a {name}"
        if choices:
            message += f" ({', '.join(choices)})"
        error(message)

    return validate(cmd, val, name, choices, options, klass)


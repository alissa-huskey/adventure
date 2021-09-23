from sys import stderr
from collections import defaultdict
import re

from console import fg, bg, fx
from console.progress import ProgressBar, _ic, _if, _il
from console.utils import len_stripped

from blessed.terminal import Terminal

from adventure import NotFound, UserError, SilentError, UnexpectedError, themes
from adventure.player import state


TERM = Terminal()
WIDTH = 60
MARGIN = 3
MAX=WIDTH-MARGIN
DEBUG = False


class Grid:
    def __init__(self, size=4):
        self.size = size
        self.rows = (size//2), -(size//2)-1, -1
        self.cols = (0, size)
        self.data = defaultdict(lambda: defaultdict(str))
        self.data["x"][""] = ""

        for c in range(*self.cols):
            self.data["x"][c] = str(c)

        for row in range(*self.rows):
            self.data[row]["y"] = str(row)
            for col in range(*self.cols):
                self.data[row][col]

    def get(self, x, y):
        return self.data[x][y]

    def set(self, x, y, value):
        self.data[x][y] = value

    def render(self):
        indent = '     '
        sep, div = " | ", "-+-"
        width = max([max(map(len, r.values())) for r in self.data.values()])
        self.width = width

        line = indent + " +-" + div.join(["-"*width for _ in range(self.size+1)]) + "-+ \n"
        rows = [[TERM.center(c, width) for c in r.values()] for r in self.data.values()]
        rows = [indent + (sep.join([""]+row+[""]) + "\n") for row in rows]

        return line + f"{line}".join(rows) + line

class Bar(ProgressBar):
    """Progress bar that stays doesn't change when it reaches 100%'"""

    _clear_left = False

    def _update_status(self, ratio):
        super()._update_status(ratio)
        self.done = False
        self._comp_style = self.styles[_ic]
        self._first = self.styles[_if](self.icons[_if])
        self._last = self.styles[_il](self.icons[_il])
        self.oob_error = False
        self._lbl = self.label_fmt[0] % (ratio * 100)

class Formatter():
    def __init__(self, width, align):
        self.width = width
        self.align = align
        self.func = getattr(TERM, align)

    def __call__(self, text):
        return self.func(text, self.width)

class Table:
    def __init__(self, table=None, align=None, indent=6, padding=1, sizes=None):
        self.rows = table or []
        self.indent = indent

        self.padding = " " * padding
        self.margin = " " * indent

        self.align = defaultdict(lambda: "ljust")
        self.align.update(align or {})
        self.sizes = sizes or {}

    @property
    def columns(self):
        return len(self.first)

    def format_line(self, row):
        return self.padding.join(row)

    @property
    def first(self):
        for row in self.rows:
            if row: return row
        return []

    def append(self, row=[]):
        self.rows.append(row)

    def format_row(self, cells):
        if not cells:
            return []
        row = [self.formats[c](cells[c]) for c in range(self.columns)]
        return row

    @property
    def lines(self):
        return [self.format_line([self.margin]+self.format_row(row)) for row
                in self.rows]

    @property
    def text(self):
        return "\n".join(self.lines)

    @property
    def widths(self):
        try:
            self._widths = {
                i: max([len_stripped(row[i]) for row in filter(None, self.rows)])
                for i in range(self.columns)
            }
        except IndexError:
            error(
                f"Your rows have different lengths: {list(map(len, self.rows))}",
                user=False
            )
        self._widths.update(self.sizes)
        return self._widths

    @property
    def formats(self):
        return [
            Formatter(align=self.align[i], width=self.widths[i])
            for i in range(self.columns)
        ]

def bar(title, val):

    pb = Bar(width=MAX-len(title)-2)
    print(f"{title.title()} {pb(val-1)}")

def hr(char="=", width=WIDTH, margin=""):
    print(margin, char*width, sep="")

def mergelines(text):
    """Merge a block of indented text into a single line."""
    lines = text.strip().splitlines(keepends=True)
    joined = " ".join([x.strip() if x.strip() else "\n" for x in lines])
    return re.sub("\n ", "\n\n", joined)

def info(*args, before=0, after=0):
    message = " ".join(map(str, args))

    lines = TERM.wrap(
        message,
        width=MAX,
        initial_indent='      ',
        subsequent_indent='      ',
    )

    print("\n"*before, end="")
    print(*lines, sep="\n")
    print("\n"*after, end="")

def error(message="", silent=False, user=True):
    if silent:
        raise SilentError()
    elif user:
        raise UserError(message)
    else:
        raise UnexpectedError(message)

def print_error(err):
    parts = [fg.red("!"), err.message]
    if err.cmd:
        parts.insert(1, fg.red(f"{err.cmd}>"))
    print(*parts, file=stderr)

def debug(*args, **kwargs):
    if not DEBUG:
        return

    action = state().get("action")

    message = "# "

    if action:
        message += f"{action}> "

    message += " ".join(args)
    message += " ".join([f"{fx.dim}{fg.yellow}{k}{fx.end}{fx.dim}: {v!r}{fx.end}" for k,v in kwargs.items()])

    print(fx.dim(message))


from console import fg, bg, fx
from console.core import _PaletteEntry
from console.disabled import _EmptyAttribute

compass = fg.t_00CCCC           # robin egg blue
help_title = fg.magenta
cmd = fg.t_4FFFB0               # aquamarine
arg = fg.i111
arg_default = fg.i210
usage_arg = arg + fx.italic
items = fg.t_DA70D6             # orchid
header = fx.bold
hint = fg.darkgray + fx.italic

try:
    normal = _PaletteEntry(fg.white, "NORMAL", *fg.default._codes)
except AttributeError:
    normal = _EmptyAttribute()

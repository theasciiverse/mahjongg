#!/usr/bin/env python3
"""Records asciiverse/mahjongg.cast, the catalog preview, at 100x30
(hub/RECORDING.md): a fresh Turtle game played with the mouse. Each move
clicks Hint, waits for the pair to flash, then clicks both tiles. Ends by
opening the main menu, then quits (the game saves itself on the way out,
into a throwaway home, so nothing touches your own scores).

Needs asciinema 3.x and pyte (pip install pyte). Usage, from the repo root
with a release build: python3 asciiverse/record-preview.py [binary]"""
import os, pty, shutil, struct, fcntl, select, sys, tempfile, termios, time
import pyte

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
binary = sys.argv[1] if len(sys.argv) > 1 else f"{root}/target/release/mahjongg"
home = tempfile.mkdtemp(prefix="mahjongg-preview-")
env = dict(os.environ, TERM="xterm-256color", COLORTERM="truecolor", LANG="C.UTF-8",
           HOME=home, XDG_CONFIG_HOME=f"{home}/config", XDG_DATA_HOME=f"{home}/data")
COLS, ROWS, MOVES = 100, 30, 9

pid, fd = pty.fork()
if pid == 0:
    os.execvpe("asciinema", ["asciinema", "rec", "--overwrite", "-q", "-i", "2",
        "--capture-env", "TERM,COLORTERM,LANG", "--title", "Mahjongg", "-c", binary,
        f"{root}/asciiverse/mahjongg.cast"], env)
fcntl.ioctl(fd, termios.TIOCSWINSZ, struct.pack("HHHH", ROWS, COLS, 0, 0))
screen = pyte.Screen(COLS, ROWS)
stream = pyte.ByteStream(screen)

def pump(seconds):
    end = time.time() + seconds
    while time.time() < end:
        r, _, _ = select.select([fd], [], [], 0.02)
        if r:
            try: stream.feed(os.read(fd, 65536))
            except OSError: return

def click(col, row):
    """Left click at 0-based (col, row), as an SGR mouse press and release."""
    os.write(fd, f"\x1b[<0;{col + 1};{row + 1}M\x1b[<0;{col + 1};{row + 1}m".encode())

def backgrounds():
    return {(y, x): c.bg for y in range(3, ROWS) for x, c in screen.buffer[y].items()}

def hinted_tiles(before):
    """Click points of the two tiles whose face lit up: runs of changed cells
    on a tile's face row (edge rows are drawn with ▀ and ▝)."""
    changed = sorted(k for k, bg in backgrounds().items()
                     if before.get(k) != bg and screen.buffer[k[0]][k[1]].data not in "▀▝▐ ")
    runs = []
    for y, x in changed:
        if runs and runs[-1][0] == y and x - runs[-1][2] <= 2:
            runs[-1][2] = x
        else:
            runs.append([y, x, x])
    points = [(y, (a + b) // 2) for y, a, b in runs]
    if len(points) == 1 and runs[0][2] - runs[0][1] >= 5:  # two neighbours, one run
        y, a, b = runs[0]
        points = [(y, a + 1), (y, b - 1)]
    return points[:2]

pump(2.5)
for _ in range(MOVES):
    before = backgrounds()
    click(screen.display[0].index("Hint"), 0)
    pump(0.25)
    tiles = hinted_tiles(before)
    pump(1.2)
    for row, col in tiles:
        click(col, row)
        pump(0.7)
    pump(0.6)
click(screen.display[0].index("≡"), 0)
pump(3.0)
os.write(fd, b"\x1b")
pump(1.5)
os.write(fd, b"q")
pump(1.0)
for _ in range(50):
    if os.waitpid(pid, os.WNOHANG)[0]: break
    time.sleep(0.2)
shutil.rmtree(home, ignore_errors=True)

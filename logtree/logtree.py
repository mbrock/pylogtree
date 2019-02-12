import asyncio
import contextlib
import io
import os
import sys

__all__ = [
    "logtree",
    "install",
    "uninstall",
    "note",
    "moan",
    "cd",
    "run",
    "CommandFailed",
    "bold", "dim", "cyan", "dim",
]

@contextlib.contextmanager
def logtree():
    """Redirect :data:`sys.stdout` and :data:`sys.stderr` within a context.

    Example:
        >>> async def go():
        >>>     with note("Running task..."):
        >>>         await run(["task", "--verbose"])
        >>> with logtree():
        >>>     asyncio.run(go())
        * Running task...
          $ task --verbose
            [output from task]

    """
    stream = IndentingStringIO(sys.stdout)
    with contextlib.redirect_stdout(stream):
        with contextlib.redirect_stderr(stream):
            yield

old_stdout = sys.stdout
old_stderr = sys.stderr

def install():
    """Install the stream redirections imperatively.

    Note:
        This replaces :data:`sys.stdout` and :data:`sys.stderr` for
        your whole program until you call :meth:`uninstall`.

    Example:
        >>> install()
        >>> with note("Echoing 'foo'..."):
        >>>     cmd(["echo", "foo"])
        * Echoing 'foo'...
          $ echo foo
            foo

    """
    global old_stdout
    old_stdout = sys.stdout
    old_stderr = sys.stdout
    stream = IndentingStringIO(old_stdout)
    sys.stdout = stream
    sys.stderr = stream

def uninstall():
    """Undo the effect of :meth:`install`."""
    global old_stdout
    global old_stderr
    sys.stdout = old_stdout
    sys.stderr = old_stderr

def note(msg, prefix="* "):
    """Notes a message and opens an indent level.

    This can be used as a context, or not.

    Example:
        >>> with pipe():
        >>>    note("Hello.")
        >>>    with note("Starting task A."):
        >>>        note("Looks good...")

    Returns: 
        a context manager
    """
    print(f"{prefix}{msg}")
    return enter()

def moan(msg):
    """Like `note` with `prefix` set to ``"! "``."""
    return note(msg, prefix="! ")

@contextlib.contextmanager
def cd(path):
    """Verbosely enter a new working directory within a context.

    Example:
       >>> async def go():
       >>>     with pipe():
       >>>        with cd("/proc"):
       >>>           await run(["wc", "-l", "modules"])
       >>> asyncio.run(go())
       * Entering /proc.
         $ wc -l modules
           204 modules
    """
    old = os.getcwd()
    with note(f"Entering {cyan(os.path.abspath(path))}."):
        os.chdir(path)
        try:
            yield
        finally:
            os.chdir(old)

async def run(cmd, check=True, quiet=False, env=None):
    """Runs a command within a new indent level.

    Note:
        This pipes the output streams to a
        custom :class:`io.StringIO` instance.  If your command does
        funky things with the output, strange effects or errors may result.

    Args:
       cmd (List[str]): for example, ``["ls", "-al"]``
       check (bool): if `True`, raise :exc:`CommandFailed` on non-zero exit
       quiet (bool): if `True`, don't print the command or indent
       env (dict): an optional dictionary of extra environment variables

    Returns: 
       An :mod:`asyncio` coroutine.
    """
    async def print_lines(stream, function):
        while True:
            line = await stream.readline()
            if not line:
                break
            print(function(line.decode('utf-8').rstrip()))

    async def go():
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            env=(dict(os.environ, **env) if env else None),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)

        def styler(style):
            return lambda x: style(f"| {x}")

        tasks = [
            asyncio.create_task(x) for x in [
                print_lines(proc.stdout, lambda s: dim(f"{s}")),
                print_lines(proc.stderr, lambda s: dim(f"{s}")),
            ]
        ]

        await proc.wait()
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)

        if check and proc.returncode is not 0:
            raise CommandFailed(cmd)

        return proc.returncode == 0

    if quiet:
        return await go()
    else:
        with note(bold(' '.join(cmd)), prefix="$ "):
            return await go()

class CommandFailed(Exception):
    """Raised when a subprocess started by :meth:`run` exits with non-zero."""
    def __init__(self, command):
        self.command = command

current_level = 0

def spaces():
    global current_level
    return " " * (current_level * 2)

@contextlib.contextmanager
def enter():
    global current_level
    current_level = current_level + 1
    try:
        yield
    finally:
        current_level = current_level - 1

class IndentingStringIO(io.StringIO):
    def __init__(self, output):
        self.output = output

    def write(self, s):
        self.output.write(f"{spaces()}{s}")

def bold(x):
    """Format a string boldly.

    Returns:
       The string `x` made bold by terminal escape sequence.
    """
    return f"\033[1m{x}\033[0m"

def dim(x):
    """Format a string dimly.

    Returns:
       The string `x` made dim by terminal escape sequence.
    """
    return f"\033[2m{x}\033[0m"

def cyan(x):
    """Format a string in cyan.

    Returns:
       The string `x` made cyan by terminal escape sequence.
    """
    return f"\033[36m{x}\033[0m"

def red(x):
    """Format a string red.

    Returns:
       The string `x` made red by terminal escape sequence.
    """
    return f"\033[31m{x}\033[0m"

from logtree import *
import asyncio

async def go():
    with note("System check."):
        with note("Checking epoch date."):
            await run(["date", "-d", "@0", "--utc"])
        note("System check done.")
    with cd("/proc"):
        await run(["wc", "-l", "modules"])
    await run(["env"], env={"FOO": "BAR"})
    moan("Oops, error.")

async def go2():
    # Open a new output section.
    with note("Doing steps..."):
        # Run some commands.
        await run(["./step-1", "--flag"])
        await run(["./step-2", "--flag"])
        # Open an output subsection.
        with note("Cleaning up..."):
            # Run a command within an output `cd' section.
            with cd("./step-2-build"):
                 await run(["rm", "-rf", "tmp"])

    # Back at the root level, open yet another output section.
    with note("Notifying..."):
        await run(["say", "Important script done."])

with logtree():
    asyncio.run(go())

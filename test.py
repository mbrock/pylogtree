import logtree
import asyncio

# async def go():
#     with logtree():
#         with note("System check."):
#             with note("Checking epoch date."):
#                 await run(["date", "-d", "@0", "--utc"])
#             note("System check done.")
#         with cd("/proc"):
#             await run(["wc", "-l", "modules"])
#         moan("Oops, error.")

async def go2():
    # Open a new output section.
    with logtree.note("Doing steps..."):
        # Run some commands.
        await logtree.run(["./step-1", "--flag"])
        await logtree.run(["./step-2", "--flag"])
        # Open an output subsection.
        with logtree.note("Cleaning up..."):
            # Run a command within an output `cd' section.
            with logtree.cd("./step-2-build"):
                 await logtree.run(["rm", "-rf", "tmp"])

    # Back at the root level, open yet another output section.
    with logtree.note("Notifying..."):
        await logtree.run(["say", "Important script done."])

with logtree.logtree():
    asyncio.run(go2())

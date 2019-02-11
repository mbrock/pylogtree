logtree: cozy structured scripts
================================

This module helps make multi-step script output pretty and
pedagogical.  It's meant to be great for installers, build systems,
site generators, etc.

It mostly helps by indenting output---including when running
subcommands---so you don't have to print spaces yourself.

.. note::
   The current version redirects Python's :data:`sys.stdout`
   and :data:`sys.stderr`, but not the actual Unix file handles.

   This means that in order for subprocesses to work properly,
   you do need to use :meth:`logtree.run`.

Here's an example::

    import asyncio
    from logtree import logtree, note, run, cd

    async def go():
        with note("Doing steps..."):
            await run(["./step-1", "--flag"])
            await run(["./step-2", "--flag"])
            with note("Cleaning up...")
                with cd("./step-2-build"):
                     await run(["rm", "-rf", "tmp"])

        with note("Notifying...")
            await run(["say", "Important script done."])

    with logtree():
        asyncio.run(go())

The output might look like this---except colorized:

.. code-block:: none

   * Doing steps...
     $ ./step-1 --flag
       step 1 commencing...
       important things happening...
     $ ./step-2 --flag
       + mkdir -p step-2-build/tmp
       + touch step-2-build/tmp/tmp.dat
     * Cleaning up...
       * Entering /home/mbrock/src/foo/step-2-build.
         $ rm -rf tmp
   * Notifying...
     $ say Important script done.
       Important script done.

API
===

.. toctree::
   :maxdepth: 2
   :caption: Contents:

.. automodule:: logtree
   :members:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

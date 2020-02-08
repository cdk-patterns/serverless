.. _using:

===========================
 Using importlib_resources
===========================

``importlib_resources`` is a library that leverages Python's import system to
provide access to *resources* within *packages*.  Given that this library is
built on top of the import system, it is highly efficient and easy to use.
This library's philosophy is that, if you can import a package, you can access
resources within that package.  Resources can be opened or read, in either
binary or text mode.

What exactly do we mean by "a resource"?  It's easiest to think about the
metaphor of files and directories on the file system, though it's important to
keep in mind that this is just a metaphor.  Resources and packages **do not**
have to exist as physical files and directories on the file system.

If you have a file system layout such as::

    data/
        __init__.py
        one/
            __init__.py
            resource1.txt
        two/
            __init__.py
            resource2.txt

then the directories are ``data``, ``data/one``, and ``data/two``.  Each of
these are also Python packages by virtue of the fact that they all contain
``__init__.py`` files [#fn1]_.  That means that in Python, all of these import
statements work::

    import data
    import data.one
    from data import two

Each import statement gives you a Python *module* corresponding to the
``__init__.py`` file in each of the respective directories.  These modules are
packages since packages are just special module instances that have an
additional attribute, namely a ``__path__`` [#fn2]_.

In this analogy then, resources are just files within a package directory, so
``data/one/resource1.txt`` and ``data/two/resource2.txt`` are both resources,
as are the ``__init__.py`` files in all the directories.  However the package
directories themselves are *not* resources; anything that contains other
things (i.e. directories) are not themselves resources.

Resources are always accessed relative to the package that they live in.  You
cannot access a resource within a subdirectory inside a package.  This means
that ``resource1.txt`` is a resource within the ``data.one`` package, but
neither ``resource2.txt`` nor ``two/resource2.txt`` are resources within the
``data`` package.  If a directory isn't a package, it can't be imported and
thus can't contain resources.

Even when this hierarchical structure isn't represented by physical files and
directories, the model still holds.  So zip files can contain packages and
resources, as could databases or other storage medium.  In fact, while
``importlib_resources`` supports physical file systems and zip files by
default, anything that can be loaded with a Python import system `loader`_ can
provide resources, as long as the loader implements the `ResourceReader`_
abstract base class.


Example
=======

Let's say you are writing an email parsing library and in your test suite you
have a sample email message in a file called ``message.eml``.  You would like
to access the contents of this file for your tests, so you put this in your
project under the ``email/tests/data/message.eml`` path.  Let's say your unit
tests live in ``email/tests/test_email.py``.

Your test could read the data file by doing something like::

    data_dir = os.path.join(os.path.dirname(__file__), 'tests', 'data')
    data_path = os.path.join(data_dir, 'message.eml')
    with open(data_path, encoding='utf-8') as fp:
        eml = fp.read()

But there's a problem with this!  The use of ``__file__`` doesn't work if your
package lives inside a zip file, since in that case this code does not live on
the file system.

You could use the `pkg_resources API`_ like so::

    # In Python 3, resource_string() actually returns bytes!
    from pkg_resources import resource_string as resource_bytes
    eml = resource_bytes('email.tests.data', 'message.eml').decode('utf-8')

This requires you to make Python packages of both ``email/tests`` and
``email/tests/data``, by placing an empty ``__init__.py`` files in each of
those directories.

**This is a requirement for importlib_resources too!**

The problem with the ``pkg_resources`` approach is that, depending on the
structure of your package, ``pkg_resources`` can be very inefficient even to
just import.  ``pkg_resources`` is a sort of grab-bag of APIs and
functionalities, and to support all of this, it sometimes has to do a ton of
work at import time, e.g. to scan every package on your ``sys.path``.  This
can have a serious negative impact on things like command line startup time
for Python implement commands.

``importlib_resources`` solves this by being built entirely on the back of the
stdlib :py:mod:`importlib`.  By taking advantage of all the efficiencies in
Python's import system, and the fact that it's built into Python, using
``importlib_resources`` can be much more performant.  The equivalent code
using ``importlib_resources`` would look like::

    from importlib_resources import read_text
    # Reads contents with UTF-8 encoding and returns str.
    eml = read_text('email.tests.data', 'message.eml')


Packages or package names
=========================

All of the ``importlib_resources`` APIs take a *package* as their first
parameter, but this can either be a package name (as a ``str``) or an actual
module object, though the module *must* be a package [#fn3]_.  If a string is
passed in, it must name an importable Python package, and this is first
imported.  Thus the above example could also be written as::

    import email.tests.data
    eml = read_text(email.tests.data, 'message.eml')


File system or zip file
=======================

In general you never have to worry whether your package is on the file system
or in a zip file, as the ``importlib_resources`` APIs hide those details from
you.  Sometimes though, you need a path to an actual file on the file system.
For example, some SSL APIs require a certificate file to be specified by a
real file system path, and C's ``dlopen()`` function also requires a real file
system path.

To support this, ``importlib_resources`` provides an API that will extract the
resource from a zip file to a temporary file, and return the file system path
to this temporary file as a :py:class:`pathlib.Path` object.  In order to
properly clean up this temporary file, what's actually returned is a context
manager that you can use in a ``with``-statement::

    from importlib_resources import path
    with path(email.tests.data, 'message.eml') as eml:
        third_party_api_requiring_file_system_path(eml)

You can use all the standard :py:mod:`contextlib` APIs to manage this context
manager.

.. attention::

   There is an odd interaction with Python 3.4, 3.5, and 3.6 regarding adding
   zip or wheel file paths to ``sys.path``.  Due to limitations in `zipimport
   <https://docs.python.org/3/library/zipimport.html>`_, which can't be
   changed without breaking backward compatibility, you **must** use an
   absolute path to the zip/wheel file.  If you use a relative path, you will
   not be able to find resources inside these zip files.  E.g.:

   **No**::

       sys.path.append('relative/path/to/foo.whl')
       resource_bytes('foo/data.dat')  # This will fail!

   **Yes**::

       sys.path.append(os.path.abspath('relative/path/to/foo.whl'))
       resource_bytes('foo/data.dat')

Both relative and absolute paths work for Python 3.7 and newer.


.. rubric:: Footnotes

.. [#fn1] We're ignoring `PEP 420
          <https://www.python.org/dev/peps/pep-0420/>`_ style namespace
          packages, since ``importlib_resources`` does not support resources
          within namespace packages.  Also, the example assumes that the
          parent directory containing ``data/`` is on ``sys.path``.

.. [#fn2] As of `PEP 451 <https://www.python.org/dev/peps/pep-0451/>`_ this
          information is also available on the module's
          ``__spec__.submodule_search_locations`` attribute, which will not be
          ``None`` for packages.

.. [#fn3] Specifically, this means that in Python 2, the module object must
          have an ``__path__`` attribute, while in Python 3, the module's
          ``__spec__.submodule_search_locations`` must not be ``None``.
          Otherwise a ``TypeError`` is raised.


.. _`pkg_resources API`: http://setuptools.readthedocs.io/en/latest/pkg_resources.html#basic-resource-access
.. _`loader`: https://docs.python.org/3/reference/import.html#finders-and-loaders
.. _`ResourceReader`: https://docs.python.org/3.7/library/importlib.html#importlib.abc.ResourceReader

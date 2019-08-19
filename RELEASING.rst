=========
Releasing
=========

Releases are created via Travis or uploaded locally using `twine <https://github.com/pypa/twine>`_.

When the release is ready to go:

* Make sure ``HISTORY.rst`` and other documentation is up to date
* Bump version in ``watchman/__init__.py``
* Tag code: ``git tag 1.0.0``
* Push tag: ``git push origin 1.0.0``
* Create a release from the tag on Github

Travis will run the full test suite and deploy to pypi in a separate stage if everything passes.

Local fallback
~~~~~~~~~~~~~~

If Travis isn't available or working for releases for some reason, you can use `twine`_ to upload the release.

* Install and configure `twine`_
* Check dist locally: ``make dist``
* Deploy release: ``make release``

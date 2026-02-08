# Releasing

Releases are created via GitHub Actions (soon: <https://github.com/mwarkentin/django-watchman/issues/177>) or uploaded locally using [twine](https://github.com/pypa/twine).

When the release is ready to go:

- Make sure `CHANGELOG.md` and other documentation is up to date
- Bump version in `watchman/__init__.py`
- Tag code: `git tag 1.0.0`
- Push tag: `git push origin 1.0.0`
- Create a release from the tag on GitHub

## Local fallback

If GitHub Actions isn't available or working for releases for some reason, you can use [twine](https://github.com/pypa/twine) to upload the release.

- Install and configure [twine](https://github.com/pypa/twine)
- Check dist locally: `just dist`
- Deploy release: `just release`

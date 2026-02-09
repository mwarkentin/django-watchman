# Releasing

Releases are published to PyPI automatically via GitHub Actions using [trusted publishing](https://docs.pypi.org/trusted-publishers/).

## Release steps

1. Update `CHANGELOG.md` -- move items from "Unreleased" into a new version section with today's date
2. Bump `__version__` in `watchman/__init__.py` (this is the single source of version truth)
3. Commit the changes: `git commit -am "Release X.Y.Z"`
4. Tag the commit: `git tag X.Y.Z`
5. Push the commit and tag: `git push origin main --tags`
6. [Create a GitHub Release](https://github.com/mwarkentin/django-watchman/releases/new) from the tag -- paste the changelog entry as the release notes
7. The publish workflow will automatically run CI, build the package, publish to PyPI, and attach the artifacts to the release

## Local fallback

If GitHub Actions isn't available or working for some reason, you can publish locally:

- Check the dist locally: `just dist`
- Publish the release: `just release`

## One-time PyPI trusted publishing setup

To enable automated publishing, the repository maintainer needs to configure trusted publishing:

1. Go to the [django-watchman PyPI project settings](https://pypi.org/manage/project/django-watchman/settings/publishing/)
2. Add a new "Trusted Publisher" with:
   - **Owner**: `mwarkentin`
   - **Repository**: `django-watchman`
   - **Workflow name**: `publish.yml`
   - **Environment name**: `pypi`
3. In the [GitHub repository settings](https://github.com/mwarkentin/django-watchman/settings/environments), create an environment named `pypi` (optionally with deployment protection rules for an approval gate)

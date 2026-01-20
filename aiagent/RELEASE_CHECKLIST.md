# PyPI Release Checklist

## Pre-Release
- [ ] Update version in `setup.py`
- [ ] Update README.md with latest features
- [ ] Test all functionality locally
- [ ] Run tests: `python -m pytest`
- [ ] Clean previous builds: `rm -rf dist/ build/ *.egg-info/`
- [ ] Build package: `python -m build`

## TestPyPI Upload
- [ ] Upload to TestPyPI: `python -m twine upload --repository testpypi dist/*`
- [ ] Test installation from TestPyPI
- [ ] Verify CLI works: `forensiq-cli --help`
- [ ] Test core functionality

## PyPI Upload (Production)
- [ ] Upload to PyPI: `python -m twine upload dist/*`
- [ ] Verify installation: `pip install forensiq-aiagent`
- [ ] Test in clean environment
- [ ] Update GitHub release tags
- [ ] Update documentation

## Post-Release
- [ ] Monitor for issues
- [ ] Update project documentation
- [ ] Announce release (if applicable)

---

## 1.8.x Additional Notes and Tips

### After Twine Upload

- PyPI propagation can take a few minutes. If `pip install logiq-cli==<version>` fails immediately after upload:
  - Check versions visible to pip: `python -m pip index versions logiq-cli`
  - Force bypass cache/CDN: `python -m pip install --no-cache-dir --index-url https://pypi.org/simple logiq-cli==<version>`
  - Upgrade pip: `python -m pip install -U pip` and retry

### Windows: Invalid distribution warning

If you see `WARNING: Ignoring invalid distribution ~ogiq-cli (...)`, remove the stray folder in site-packages and clear pip cache:
  - Delete the tilde-prefixed leftover package directory under your Python `site-packages`
  - Purge cache: `python -m pip cache purge`
  - Retry install with `--no-cache-dir`

### Tagging & GitHub Release

1. Create and push tag:
   - `git tag v<version>`
   - `git push origin v<version>`
2. Create GitHub release for the tag with highlights (link to `RELEASE_NOTES_v<version>.md`).

# Release Process

## Version Management

This project uses `hatch-vcs` — the git tag is the single source of truth for
the version. There is no version string in any file to maintain manually.

Existing tags (`1.0.0`, `1.0.1`) have no `v` prefix; both forms are
understood. New tags conventionally use the `v` prefix.

## Prerequisites

### PyPI Trusted Publishing (one-time setup)

Both Test PyPI and PyPI use OIDC trusted publishing (no API tokens needed).

1. **Test PyPI**: Go to https://test.pypi.org/manage/project/pipforester/settings/publishing/
   - Add a GitHub publisher: owner=`collective`, repo=`pipforester`,
     workflow=`release.yaml`, environment=`release-test-pypi`

2. **PyPI**: Go to https://pypi.org/manage/project/pipforester/settings/publishing/
   - Add a GitHub publisher: owner=`collective`, repo=`pipforester`,
     workflow=`release.yaml`, environment=`release-pypi`

3. **GitHub Environments**: In the repo settings, create two environments:
   - `release-test-pypi`
   - `release-pypi` (optionally add required reviewers for extra safety)

### Tools

```bash
uv tool install hatch  # optional, for local builds
```

## Making a Release

### 1. Ensure `main` is clean and CI passes

```bash
git checkout main
git pull
pytest
```

### 2. Tag the release

Tags must follow PEP 440. The `v` prefix is optional but conventional:

```bash
git tag v1.0.2
```

For pre-releases:

```bash
git tag v1.0.2a1   # alpha
git tag v1.0.2b1   # beta
git tag v1.0.2rc1  # release candidate
```

### 3. Push the tag

```bash
git push origin v1.0.2
```

### 4. Create a GitHub Release

1. Go to https://github.com/collective/pipforester/releases/new
2. Select the tag you just pushed: `v1.0.2`
3. Set the release title: `v1.0.2`
4. Add release notes (or use "Generate release notes")
5. For pre-releases, check "Set as a pre-release"
6. Click "Publish release"

Publishing the GitHub Release triggers the release workflow, which builds
the sdist + wheel and publishes to **PyPI**. Every push to `main` also
publishes an in-dev version to **Test PyPI** automatically.

### 5. Verify

- Check https://pypi.org/project/pipforester/ for the new version
- Verify installation: `uv pip install pipforester==1.0.2`

## Building Locally (for testing)

```bash
hatch build           # creates sdist + wheel in dist/
ls dist/
# pipforester-1.0.2.tar.gz
# pipforester-1.0.2-py3-none-any.whl
```

Note: Without a git tag on the current commit, `hatch-vcs` generates a dev
version like `1.0.2.dev4`. This is expected and correct for development
builds.

## What Gets Published

| Artifact | Contents |
|----------|----------|
| sdist (`.tar.gz`) | Source code |
| wheel (`.whl`) | Pure Python wheel (`py3-none-any`), the `pipforester` package |

## Checklist

- [ ] All tests pass (`pytest`)
- [ ] CHANGES.md is up to date
- [ ] README.md is up to date
- [ ] `main` branch is clean (no uncommitted changes)
- [ ] Tag follows PEP 440 (`v1.0.2`, not `release-1.0.2`)
- [ ] GitHub Release created with release notes
- [ ] Package visible on PyPI

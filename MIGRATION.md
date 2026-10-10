# Migration to the Python 3.14 fork line

This is an unreleased documentation draft, not a publication or version decision.
The existing distribution name `pymultigen` and version `0.2.0`
remain unchanged. A PyPI fork name and release/prerelease version require a separate
human decision; no ownership of upstream names is implied.

CPython 3.12, 3.13 and 3.14 standard with GIL are qualified on Linux x86_64.
Python <3.12 is outside this line. Windows, macOS, other architectures, PyPy and
free-threaded Python are NOT_RUN. Metadata >=3.12 is not a promise about future
Python versions.

Import names remain multigen and multigen.jinja. Jinja2 >=3.1.6 and autopep8 >=2 are available through the existing extras.

Use local, provenance-checked ecosystem wheels together. The accepted T12 closure
passes 911 tests per environment for both supported-minimum and recent profiles,
each on 3.12/3.13/3.14 source and wheel. The supported closure uses setuptools
83.0.0, pytest 9.0.3, lxml 6.1.0, Jinja2 3.1.6, ordered-set 4.0.1, autopep8 2.0.0
and build 1.0.0; exact transitives are in the qualification locks. Historical
setuptools 77.0.1/pytest 8.0.0 compatibility results are not supported minimums.
Audits on 2026-10-09 reported no known advisories for the two supported profiles;
this is dated evidence, not a security guarantee.

For rollback, create a separate checkout at known qualified commit
`4178f9d855c84b54a8d73b12d55564917132514f` and reinstall the matching complete
closure from its hashed locks in a fresh environment. Do not mix isolated old
components with new ones or overwrite a dirty checkout. Back up models and
application-generated code before migration. The original upstream baseline
`3095c7579ab29199cb421b2e70d3088067a450bd` is historical, not qualified for Python
3.14 and not a safe default rollback environment.

Keep `LICENSE` and existing author/copyright notices with redistributed code.
The ecosystem delivery guide lives in the separate pyecore-codex-harness pilot
repository (`docs/MIGRATION_GUIDE.md`, `docs/PYTHON_SUPPORT.md`,
`docs/RELEASE_PLAN.md`). Documentation drafts are separate from the frozen T12
artifacts until reviewed and committed.

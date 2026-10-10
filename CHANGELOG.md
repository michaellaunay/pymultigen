# Changelog

## Unreleased — Python 3.14 migration (release decision pending)

- CPython >=3.12 metadata; qualified 3.12/3.13/3.14 standard with GIL on Linux x86_64 only.
- Build backend setuptools >=83.0.0 and test extra pytest >=9.0.3. Project/module names, nsURI, licenses and author credits are retained.
- Modern PEP 517 packaging replaces inherited test/build mechanisms.
- Renderer errors preserve existing output; Jinja resources and formatted generation are qualified from installed distributions.

Import names remain multigen and multigen.jinja. Jinja2 >=3.1.6 and autopep8 >=2 are available through the existing extras.


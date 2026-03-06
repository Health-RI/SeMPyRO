# Changelog

All notable changes to this project will be documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


##  [v2.2.0] - 2026-03-06

### What's Changed
- Docs/update docs by @qplevier in https://github.com/Health-RI/SeMPyRO/pull/112
- feat(healthdcat) add Healthdcat to Sempyro by @hcvdwerf in https://github.com/Health-RI/SeMPyRO/pull/119
- build(deps): bump actions/upload-artifact from 4 to 6 by @dependabot[bot] in https://github.com/Health-RI/SeMPyRO/pull/115
- build(deps): update ruamel-yaml requirement from ~=0.18.5 to >=0.18.5,<0.20.0 by @dependabot[bot] in https://github.com/Health-RI/SeMPyRO/pull/116
- build(deps): bump actions/checkout from 4 to 6 by @dependabot[bot] in https://github.com/Health-RI/SeMPyRO/pull/111
- build(deps): bump actions/download-artifact from 5 to 7 by @dependabot[bot] in https://github.com/Health-RI/SeMPyRO/pull/114
- build(deps): bump SonarSource/sonarqube-scan-action from 6 to 7 by @dependabot[bot] in https://github.com/Health-RI/SeMPyRO/pull/113
- Added Goe example by @hcvdwerf in https://github.com/Health-RI/SeMPyRO/pull/120
- fix: wrong rdf_term for temporal_resolution by @agjharms in https://github.com/Health-RI/SeMPyRO/pull/121
- Rename optional dependency group to 'notebook-docs' by @waakanni in https://github.com/Health-RI/SeMPyRO/pull/118
- fix: remove obsolete comment by @hcvdwerf in https://github.com/Health-RI/SeMPyRO/pull/125
- build(deps): bump actions/upload-artifact from 6 to 7 by @dependabot[bot] in https://github.com/Health-RI/SeMPyRO/pull/123
- build(deps): bump actions/download-artifact from 7 to 8 by @dependabot[bot] in https://github.com/Health-RI/SeMPyRO/pull/122


## [v2.1.0] - 2025-10-02

### Added
- feature: update GDI-notebook to include AF-beacon and fix some values. by @PatrickDekkerHealthRI in cec947f


### Changed
- docs: adds prompts for username and password by @Alexander Harms in 4d42c73
- restructure test run by @Hans-christian in 2187736
- build(deps): bump email-validator from 2.2.0 to 2.3.0 by @dependabot[bot] in aa3fd1a
- build(deps): bump actions/setup-python from 5 to 6 by @dependabot[bot] in ec8de5f
- build(deps): bump pypa/gh-action-pypi-publish from 1.12.4 to 1.13.0 by @dependabot[bot] in 0c37d6e


### Fixed
- fix(ci): changes version increment method by @Alexander Harms in 5a8e990
- fix: removes commented out code by @Alexander Harms in 09d7aa9
- fix sonar cloud by @Hans-christian in 43ec448
- fix(ci): fix ci dependencies by @Alexander Harms in 6ae54e6


## [v2.0.3] - 2025-07-17

### Changed
- docs: cleans up CHANGELOG.md by @Alexander Harms in 3691cd6
- doc: update CHANGELOG.md for v2.0.2 by @Health-RI Admin in d383f75
- docs: cleans up CHANGELOG.md by @Alexander Harms in 9808bce
- doc: update CHANGELOG.md for v2.0.2 by @Health-RI Admin in ae87d1d


### Fixed
- fix(ci): publish pypi on workflow dispatch, test on PR ready to review by @Alexander Harms in 7afc64b
- fix: fixes serialized models by @Alexander Harms in 3c7c7ac
- fix: corrects description of 'other identifier' by @Alexander Harms in 31fa331
- fix: update Jupyter notebook and serialized models by @Alexander Harms in da30ea0
- fix: other identifier in HRI Dataset should be a list by @Alexander Harms in 62ca85b
- fix(ci): publish pypi on workflow dispatch, test on PR ready to review by @Alexander Harms in 601d899


## [v2.0.2] - 2025-07-07

### Changed
- ci: adds sonarqube cloud and release workflow by @Alexander Harms in ac9f249
- Update pyproject.toml by @Daniel Kapitan in 7386f8c

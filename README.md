# vms

Automated Oracle VM VirtualBox Ubuntu build using Packer.

## Prerequisites

- Packer 1.6.5
  - One of `xorriso`, `mkisofs`, `hdiutil` (normally found in macOS) or `oscdimg` (normally found in Windows as part of the [Windows ADK](https://docs.microsoft.com/en-us/windows-hardware/get-started/adk-install)) is required by Packer
- Oracle VM VirtualBox 6.1.14
- Oracle VM VirtualBox Guest Additions 6.1.14
- Oracle VM VirtualBox Extension Pack 6.1.14

## Install

```text
pip install pipenv
pipenv shell
```

## Build

Run `python -m lib.build` or `python - lib.build --help` for usage information.

**Note**: if `base` is specified it'll be the first thing to be built, otherwise a `packer-{template}-{release}-base` named VM must exist with a snapshot attached to it called `Base`.

### Vagrant

Use the following to create a Vagrant box

```sh
python -m lib.build --debug --release 18.04 base --extra-base-config '
vagrant: true
user: vagrant
pass: vagrant
'
```

## Release

1. [Install GitHub CLI](https://cli.github.com/)
1. Create one or more personal access token with `repo` and/or `admin:org` scoped permissions
1. Run `gh auth login` and use one of the tokens
1. Run `python release.py` **after the build** to output the `gh` command that creates the release
1. Use `python release.py --owner <OWNER> --repo <REPO>` to specify which user/organization/repo to create the release at exactly

## Licenses

```text
Copyright 2020, Kohányi Róbert (<kohanyi.robert@gmail.com>)
Copyright 2012-2019, Chef Software, Inc. (<legal@chef.io>)
Copyright 2011-2012, Tim Dysinger (<tim@dysinger.net>)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

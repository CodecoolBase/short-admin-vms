# vms

Automated Oracle VM VirtualBox Ubuntu build using Packer.

## Prerequisites

- Packer 1.6.2
- Oracle VM VirtualBox 6.1.14
- Oracle VM VirtualBox Guest Additions 6.1.14
- Oracle VM VirtualBox Extension Pack 6.1.14

## Install

```text
pip install pipenv
pipenv shell
```

## Build

`python build.py` or `python build.py ubuntu-18.04 base nossh`

**Note**: `base` must be specified and it must be the first thing to build (all other variants are based on it).

## Release

[Install GitHub CLI](https://cli.github.com/), login with `gh auth login` then run `python release.py` **after the build**.
It'll output the `gh` command to run that creates the release.

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

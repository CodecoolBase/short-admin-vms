# Notice

Copyright 2012-2019, Chef Software, Inc. (<legal@chef.io>)

The following files are taken from the [Bento project][bento], version [`b7b8a9bd30e143514b61a694c7d37155733adea1`][version].

## Unmodified

- [packer_templates/_common/minimize.sh][minimize.sh.orig] &#10230;  [templates/ubuntu-18.04/scripts/minimize.sh][minimize.sh]
- [packer_templates/_common/virtualbox.sh][virtualbox.sh.orig] &#10230; [templates/ubuntu-18.04/scripts/virtualbox.sh][virtualbox.sh]
- [packer_templates/ubuntu/scripts/update.sh][update.sh.orig] &#10230; [templates/ubuntu-18.04/scripts/update.sh][update.sh]

## Modified

- [packer_templates/ubuntu/scripts/cleanup.sh][cleanup.sh.orig] &#10230; [templates/ubuntu-18.04/scripts/cleanup.sh][cleanup.sh]
  - Remove command that deletes documentation packages
  - Make deleting X11 related packages conditional
  - Omit deleting certain packages
- [packer_templates/ubuntu/ubuntu-18.04-amd64.json][ubuntu-18.04-amd64.json.orig] &#10230; [templates/ubuntu-18.04/base.json.j2][base.json.j2]
  - Remove unused builders and configuration keys
  - Remove script references from provisioner
  - Add new configuration keys
  - Make it a Jinja template
- [packer_templates/ubuntu/http/preseed.cfg][preseed.cfg.orig] &#10230; [templates/ubuntu-18.04/preseed/base.cfg.j2][base.cfg.j2]
  - Remove LVM configuration and use direct partitioning
  - Remove unused packages keep only `openssh-server` (for provisioning), `build-essential`, `dkms` and `linux-headers-$(uname -r)` (to build Virtual Box Guest Addition modules)
  - Make it a Jinja template

[bento]: https://github.com/chef/bento
[version]: https://github.com/chef/bento/tree/b7b8a9bd30e143514b61a694c7d37155733adea1
[minimize.sh.orig]: https://github.com/chef/bento/blob/b7b8a9bd30e143514b61a694c7d37155733adea1/packer_templates/_common/minimize.sh
[minimize.sh]: templates/ubuntu-18.04/scripts/minimize.sh
[virtualbox.sh.orig]: https://github.com/chef/bento/blob/b7b8a9bd30e143514b61a694c7d37155733adea1/packer_templates/_common/virtualbox.sh
[virtualbox.sh]: templates/ubuntu-18.04/scripts/virtualbox.sh
[update.sh.orig]: https://github.com/chef/bento/blob/b7b8a9bd30e143514b61a694c7d37155733adea1/packer_templates/ubuntu/scripts/update.sh
[update.sh]: templates/ubuntu-18.04/scripts/update.sh
[cleanup.sh.orig]: https://github.com/chef/bento/blob/b7b8a9bd30e143514b61a694c7d37155733adea1/packer_templates/ubuntu/scripts/cleanup.sh
[cleanup.sh]: templates/ubuntu-18.04/scripts/cleanup.sh
[ubuntu-18.04-amd64.json.orig]: https://github.com/chef/bento/blob/master/packer_templates/ubuntu/ubuntu-18.04-amd64.json
[base.json.j2]: templates/ubuntu-18.04/base.json.j2
[preseed.cfg.orig]: https://github.com/chef/bento/blob/master/packer_templates/ubuntu/http/preseed.cfg
[base.cfg.j2]: templates/ubuntu-18.04/preseed/base.cfg.j2

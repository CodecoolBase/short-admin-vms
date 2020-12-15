# Notice

Copyright 2012-2019, Chef Software, Inc. (<legal@chef.io>)

The following files are taken from the [Bento project][bento], version [`b7b8a9bd30e143514b61a694c7d37155733adea1`][version].

## Unmodified

- [packer_templates/_common/minimize.sh][minimize.sh.orig] &#10230;  [scripts/minimize.sh][minimize.sh]
- [packer_templates/_common/virtualbox.sh][virtualbox.sh.orig] &#10230; [scripts/virtualbox.sh][virtualbox.sh]
- [packer_templates/ubuntu/scripts/update.sh][ubuntu/update.sh.orig] &#10230; [scripts/ubuntu/update.sh][ubuntu/update.sh]
- [packer_templates/debian/scripts/update.sh][debian/update.sh.orig] &#10230; [scripts/debian/update.sh][debian/update.sh]

## Modified

- [packer_templates/ubuntu/scripts/cleanup.sh][ubuntu/cleanup.sh.orig] &#10230; [scripts/ubuntu/cleanup.sh][ubuntu/cleanup.sh]
  - Remove command that deletes documentation packages
  - Make deleting X11 related packages conditional
  - Omit deleting certain packages
- [packer_templates/debian/scripts/cleanup.sh][debian/cleanup.sh.orig] &#10230; [scripts/debian/cleanup.sh][debian/cleanup.sh]
  - Make deleting X11 related packages conditional
- [packer_templates/ubuntu/scripts/vagrant.sh][vagrant.sh.orig] &#10230; [scripts/vagrant.sh][vagrant.sh]
  - Use `ADMIN_USER` variable instead of `vagrant`
- [packer_templates/ubuntu/scripts/sudoers.sh][sudoers.sh.orig] &#10230; [scripts/vagrant_sudoers.sh][vagrant_sudoers.sh]
  - Use `ADMIN_USER` variable instead of `vagrant`
- [packer_templates/ubuntu/ubuntu-18.04-amd64.json][ubuntu-amd64.json.orig] &#10230; [root.json.j2][root.json.j2]
  - Remove unused builders and configuration keys
  - Remove script references from provisioner
  - Add new configuration keys
  - The contents of `boot_command` is moved to `config.yml` under the path `distros.ubuntu.'18.04'.boot_command`
  - Make it a Jinja template
- [packer_templates/debian/debian-10.5-amd64.json][ubuntu-amd64.json.orig] &#10230; [root.json.j2][root.json.j2]
  - Used only parts related to `boot_command`
  - The contents of `boot_command` is moved to `config.yml` under the path `distros.debian.'10.6.0'.boot_command`
- [packer_templates/ubuntu/http/preseed.cfg][ubuntu/preseed.cfg.orig] &#10230; [config.yml][config.yml]
  - Move preseed content to `config.yml` under the path `distros.ubuntu.'18.04'.preseed`
  - Remove LVM configuration and use direct partitioning
  - Remove unused packages keep only `openssh-server` (for provisioning), `build-essential`, `dkms` and `linux-headers-$(uname -r)` (to build Virtual Box Guest Addition modules)
  - Make it a Jinja template
- [packer_templates/debian/http/debian-9/preseed.cfg][debian/preseed.cfg.orig] &#10230; [config.yml][config.yml]
  - Move preseed content to `config.yml` under the path `distros.debian.'10.6.0'.preseed`
  - Remove LVM configuration and use direct partitioning
  - Add entries related to how CD/DVD installation media is handled by Debian
  - Change included packages, keep `sudo` and `curl`, and use the same packages as for Ubuntu 18.04 LTS

[bento]: https://github.com/chef/bento
[version]: https://github.com/chef/bento/tree/b7b8a9bd30e143514b61a694c7d37155733adea1
[minimize.sh.orig]: https://github.com/chef/bento/blob/b7b8a9bd30e143514b61a694c7d37155733adea1/packer_templates/_common/minimize.sh
[minimize.sh]: scripts/minimize.sh
[virtualbox.sh.orig]: https://github.com/chef/bento/blob/b7b8a9bd30e143514b61a694c7d37155733adea1/packer_templates/_common/virtualbox.sh
[virtualbox.sh]: scripts/virtualbox.sh
[sudoers.sh.orig]: https://github.com/chef/bento/blob/b7b8a9bd30e143514b61a694c7d37155733adea1/packer_templates/ubuntu/scripts/sudoers.sh
[vagrant_sudoers.sh]: scripts/vagrant_sudoers.sh
[ubuntu/update.sh.orig]: https://github.com/chef/bento/blob/b7b8a9bd30e143514b61a694c7d37155733adea1/packer_templates/ubuntu/scripts/update.sh
[ubuntu/update.sh]: scripts/ubuntu/update.sh
[debian/update.sh.orig]: https://github.com/chef/bento/blob/b7b8a9bd30e143514b61a694c7d37155733adea1/packer_templates/debian/scripts/update.sh
[debian/update.sh]: scripts/debian/update.sh
[ubuntu/cleanup.sh.orig]: https://github.com/chef/bento/blob/b7b8a9bd30e143514b61a694c7d37155733adea1/packer_templates/ubuntu/scripts/cleanup.sh
[ubuntu/cleanup.sh]: scripts/ubuntu/cleanup.sh
[debian/cleanup.sh.orig]: https://github.com/chef/bento/blob/b7b8a9bd30e143514b61a694c7d37155733adea1/packer_templates/debian/scripts/cleanup.sh
[debian/cleanup.sh]: scripts/debian/cleanup.sh
[ubuntu-amd64.json.orig]: https://github.com/chef/bento/blob/b7b8a9bd30e143514b61a694c7d37155733adea1/packer_templates/ubuntu/ubuntu-18.04-amd64.json
[debian-amd64.json.orig]: https://github.com/chef/bento/blob/b7b8a9bd30e143514b61a694c7d37155733adea1/packer_templates/debian/debian-10.5-amd64.json
[vagrant.sh.orig]: https://github.com/chef/bento/blob/b7b8a9bd30e143514b61a694c7d37155733adea1/packer_templates/ubuntu/scripts/vagrant.sh
[vagrant.sh]: scripts/vagrant.sh
[root.json.j2]: root.json.j2
[ubuntu/preseed.cfg.orig]: https://github.com/chef/bento/blob/b7b8a9bd30e143514b61a694c7d37155733adea1/packer_templates/ubuntu/http/preseed.cfg
[debian/preseed.cfg.orig]: https://github.com/chef/bento/blob/b7b8a9bd30e143514b61a694c7d37155733adea1/packer_templates/debian/http/debian-9/preseed.cfg
[config.yml]: config.yml

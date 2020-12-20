#!/bin/sh -eux
apt-get -y install --no-install-recommends task-lxde-desktop firefox-esr
# Configure shortcut to open terminal
sudo -u "$ADMIN_USER" -s <<EOF
mkdir -vp ~/.config/openbox
cp -v /etc/xdg/openbox/LXDE/rc.xml ~/.config/openbox/lxde-rc.xml
sed -i '/<\/keyboard>/i \
  <keybind key="C-A-T"> \
    <action name="Execute"> \
      <command>lxterminal</command> \
    </action> \
  </keybind>' ~/.config/openbox/lxde-rc.xml
EOF

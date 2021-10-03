#!/bin/bash

#flatpak remote-add --user --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
#flatpak install    --user -y flathub org.freedesktop.Platform//19.08
#flatpak install    --user -y flathub org.freedesktop.Sdk//19.08

if flatpak info --user org.jamovi.jamovi 1>/dev/null 2>/dev/null ; then
    echo "jamovi already installed"
else
    echo "installing jamovi"
    # until flatpak install --user -y flathub org.jamovi.jamovi; do echo "Trying again"; sleep 2; done
    until flatpak install --user -y https://dl.flathub.org/build-repo/59917/org.jamovi.jamovi.flatpakref; do echo "Trying again"; sleep 2; done
fi

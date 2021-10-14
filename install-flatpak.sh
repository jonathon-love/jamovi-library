#!/bin/bash

dpkg-reconfigure ca-certificates
flatpak remote-add --user --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo

#if flatpak info --user org.jamovi.jamovi 1>/dev/null 2>/dev/null ; then
#    echo "jamovi already installed"
#else
    echo "installing jamovi"
    flatpak install --user -y flathub org.jamovi.jamovi
    # until flatpak install --user -y https://dl.flathub.org/build-repo/59917/org.jamovi.jamovi.flatpakref; do echo "Trying again"; sleep 2; done
#fi

flatpak install    --user -y flathub org.freedesktop.Platform//21.08
flatpak install    --user -y flathub org.freedesktop.Sdk//21.08

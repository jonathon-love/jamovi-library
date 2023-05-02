#!/bin/bash

flatpak remote-add --user --if-not-exists flathub https://library.jamovi.org/flathub.flatpakrepo

if flatpak info --user org.jamovi.jamovi 1>/dev/null 2>/dev/null ; then
    echo "jamovi already installed"
else
    echo "installing jamovi"
    # flatpak install --user -y flathub org.jamovi.jamovi
    flatpak install --user https://dl.flathub.org/build-repo/21296/org.jamovi.jamovi.flatpakref
fi

flatpak install    --user -y flathub org.freedesktop.Platform//21.08
flatpak install    --user -y flathub org.freedesktop.Sdk//21.08

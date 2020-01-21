#!/bin/bash

flatpak remote-add --user --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
flatpak install    --user -y flathub org.freedesktop.Platform//18.08
flatpak install    --user -y flathub org.freedesktop.Sdk//18.08

if flatpak info --user org.jamovi.jamovi 1>/dev/null 2>/dev/null ; then
    echo "jamovi already installed"
else
    echo "installing jamovi"
    flatpak install    --user -y flathub org.jamovi.jamovi
fi

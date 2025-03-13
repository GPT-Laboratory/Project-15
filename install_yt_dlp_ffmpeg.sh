#!/bin/bash

if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root. Use: sudo $0"
    exit 1
fi

# Download FFmpeg static build from the correct link
wget https://github.com/yt-dlp/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-linux64-gpl.tar.xz

# Extract the tarball
tar -xvf ffmpeg-master-latest-linux64-gpl.tar.xz

# Move FFmpeg binaries from the 'bin' directory to a location in the system PATH
sudo mv ffmpeg-master-latest-linux64-gpl/bin/ffmpeg /usr/local/bin/
sudo mv ffmpeg-master-latest-linux64-gpl/bin/ffplay /usr/local/bin/
sudo mv ffmpeg-master-latest-linux64-gpl/bin/ffprobe /usr/local/bin/

# Verify FFmpeg installation
ffmpeg -version

# Clean up
rm -rf ffmpeg-master-latest-linux64-gpl
rm ffmpeg-master-latest-linux64-gpl.tar.xz

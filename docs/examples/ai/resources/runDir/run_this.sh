echo "Installing special libraries"
apt-get update && apt-get install -y vim && \
    apt-get autoremove && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
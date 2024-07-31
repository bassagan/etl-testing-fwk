# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
    . /etc/bashrc
fi

# Activate the virtual environment
if [ -d "/opt/venv" ]; then
    source /opt/venv/bin/activate
fi

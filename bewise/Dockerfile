FROM python:3.13-bullseye

RUN apt update -y && \
    apt install --no-install-recommends -y postgresql-client \
    postgresql \
    make \
    python3-dev \
    python3-pip \
    python3-venv \
    python3-virtualenv && \
    python3 -m pip install --user pipx && \
    python3 -m pipx ensurepath --global && \
    rm -rf /var/lib/apt/lists/*


RUN useradd -ms /bin/bash testuser
USER testuser
WORKDIR /home/testuser/

COPY . .
RUN python3 -m pip install --user pipx && \
    python3 -m pipx ensurepath --global && \
    python3 -m pipx install poetry==2.0.1

CMD ["bash", "setup.sh"]
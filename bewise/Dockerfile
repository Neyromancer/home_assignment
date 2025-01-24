FROM python:3.13-bullseye

RUN apt update -y && \
    apt install --no-install-recommends -y postgresql-client \
    postgresql \
    make \
    python3-dev \
    python3-pip && \
    rm -rf /var/lib/apt/lists/*


RUN pip install poetry==2.0.1

RUN useradd -ms /bin/bash testuser
WORKDIR /home/testuser/


COPY --chown=testuser:testuser . .
USER testuser

RUN make setup

RUN make test

EXPOSE 8000

CMD ["poetry", "run", "python", "-m", "app.main"]
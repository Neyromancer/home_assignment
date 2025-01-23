#!/bin/env bash

make setup
make test

poetry run python -m app.main
# docker buildx build --platform linux/amd64 -t test_build_bewise_img -f ./Dockerfile .
# docker run -d --name test_build_bewise test_build_bewise_img tail -f /dev/null
# docker exec -u testuser -it test_build_bewise /bin/bash
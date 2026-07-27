FROM python:3.13

WORKDIR /workspace

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        git \
        gh \
        curl \
        wget \
        tree \
        less \
        ripgrep \
        unzip \
        openssh-client \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip \
    && python -m pip install \
        ipykernel \
        jupyter \
        pandas \
        matplotlib \
        scikit-learn \
        fastapi \
        uvicorn
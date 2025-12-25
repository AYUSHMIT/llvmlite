# Dev container with Python and LLVM toolchain for llvmlite
FROM mcr.microsoft.com/devcontainers/python:3.11

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y wget gnupg lsb-release software-properties-common && \
    wget https://apt.llvm.org/llvm-snapshot.gpg.key -O /tmp/llvm.key && \
    apt-key add /tmp/llvm.key && \
    add-apt-repository "deb http://apt.llvm.org/$(lsb_release -cs)/ llvm-toolchain-$(lsb_release -cs)-15 main" && \
    apt-get update && \
    apt-get install -y \
      llvm-15 llvm-15-dev clang-15 \
      build-essential cmake ninja-build graphviz && \
    ln -sf /usr/bin/clang-15 /usr/bin/clang && \
    ln -sf /usr/bin/llvm-config-15 /usr/bin/llvm-config && \
    ln -sf /usr/bin/opt-15 /usr/bin/opt && \
    rm -rf /var/lib/apt/lists/*

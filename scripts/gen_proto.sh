#!/bin/bash

GOGOPROTOBUF_REPO="${GIT_HOME}/gogoprotobuf"
TENDERMINT_REPO="${GIT_HOME}/tendermint"

protoc \
  --proto_path="${GOGOPROTOBUF_REPO}" \
  --proto_path="${TENDERMINT_REPO}/proto" \
  --python_out=. \
  "${TENDERMINT_REPO}/proto/tendermint/types/types.proto" \
  "${TENDERMINT_REPO}/proto/tendermint/crypto/proof.proto" \
  "${TENDERMINT_REPO}/proto/tendermint/version/types.proto" \
  "${TENDERMINT_REPO}/proto/tendermint/types/validator.proto" \
  "${TENDERMINT_REPO}/proto/tendermint/crypto/keys.proto" \
  "${TENDERMINT_REPO}/proto/tendermint/types/block.proto" \
  "${TENDERMINT_REPO}/proto/tendermint/types/evidence.proto" \
  "${TENDERMINT_REPO}/proto/tendermint/store/types.proto" \

touch tendermint/__init__.py
touch tendermint/types/__init__.py
touch tendermint/crypto/__init__.py
touch tendermint/version/__init__.py
touch tendermint/store/__init__.py

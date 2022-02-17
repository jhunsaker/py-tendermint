# tendermint/store/store.go

import plyvel

from tendermint.store.types_pb2 import BlockStoreState
from tendermint.types.block_pb2 import Block
from tendermint.types.types_pb2 import BlockMeta, Part

BLOCK_STORE_KEY = b'blockStore'

BLOCK_META_PREFIX = b'H:'
BLOCK_META_PREFIX_LEN = len(BLOCK_META_PREFIX)
BLOCK_PART_PREFIX = b'P:'

class BlockStore:

  def __init__(self, name):

    self._db = plyvel.DB(name=name)
    state = self._load_block_store_state()
    self._base = state.base
    self._height = state.height

  def __del__(self):

    if self._db:
      self._db.close()
      self._db = None

  def _load_block_store_state(self):

    bz = self._db.get(BLOCK_STORE_KEY)
    assert bz
    state = BlockStoreState()
    state.ParseFromString(bz)
    return state

  @property
  def base(self):

    return self._base

  @property
  def height(self):

    return self._height

  def load_block_meta(self, height: int):

    key = calc_block_meta_key(height=height)
    bz = self._db.get(key)
    assert bz
    meta = BlockMeta()
    meta.ParseFromString(bz)
    return meta

  def load_block_part(self, height: int, index: int):

    key = calc_block_part_key(height=height, index=index)
    bz = self._db.get(key)
    assert bz
    part = Part()
    part.ParseFromString(bz)
    return part

  def load_block(self, height: int):

    meta = self.load_block_meta(height=height)
    parts = []
    for index in range(meta.block_id.part_set_header.total):
      part = self.load_block_part(height=height, index=index)
      parts.append(part.bytes)
    bz = b''.join(parts)
    block = Block()
    block.ParseFromString(bz)
    return block

def calc_block_meta_key(height: int) -> bytes:

  return b'%s%d' % (BLOCK_META_PREFIX, height)

def decode_block_meta_key(key: bytes) -> int:

  assert key.startswith(BLOCK_META_PREFIX)
  return int(key[BLOCK_META_PREFIX_LEN:])

def calc_block_part_key(height: int, index: int) -> bytes:

  return b'%s%d:%d' % (BLOCK_PART_PREFIX, height, index)

def calc_block_commit_key(height: int) -> bytes:

  return b'C:%d' % (height,)

def calc_seen_commit_key(height: int) -> bytes:

  return b'SC:%d' % (height,)

def calc_block_hash_key(hash: bytes) -> bytes:

  return b'BH:%s' % (hash.hex().encode('ascii'),)

import hashlib
from typing import List, Dict, Tuple
from dataclasses import dataclass, field
import heapq

@dataclass
class DatasetFile:
    uri: str
    tokens: int
    size_bytes: int

@dataclass
class ClusterTopology:
    data_parallel_size: int
    pipeline_parallel_size: int = 1
    tensor_parallel_size: int = 1

@dataclass
class ShardDef:
    shard_id: str
    files: List[DatasetFile] = field(default_factory=list)
    total_tokens: int = 0
    total_bytes: int = 0

@dataclass
class RoutingTable:
    version_hash: str
    dp_rank_to_shards: Dict[int, List[str]]

class ConsistentHashRing:
    def __init__(self, replicas: int = 100):
        self.replicas = replicas
        self.ring: Dict[int, int] = {}
        self.sorted_keys: List[int] = []

    def _hash(self, key: str) -> int:
        return int(hashlib.md5(key.encode('utf-8')).hexdigest(), 16)

    def add_node(self, node_id: int):
        for i in range(self.replicas):
            h = self._hash(f"{node_id}:{i}")
            self.ring[h] = node_id
            self.sorted_keys.append(h)
        self.sorted_keys.sort()

    def get_node(self, key: str) -> int:
        if not self.ring:
            return -1
        h = self._hash(key)
        # Binary search for the first key >= h
        left, right = 0, len(self.sorted_keys) - 1
        while left <= right:
            mid = (left + right) // 2
            if self.sorted_keys[mid] == h:
                return self.ring[self.sorted_keys[mid]]
            elif self.sorted_keys[mid] < h:
                left = mid + 1
            else:
                right = mid - 1
        
        if left == len(self.sorted_keys):
            left = 0
        return self.ring[self.sorted_keys[left]]

class ShardingAgent:
    def __init__(self, config: Dict):
        self.config = config
        self.target_shard_mb = config.get("target_shard_size_mb", 1024)
        
    def _bin_pack_files(self, files: List[DatasetFile], num_shards: int) -> List[ShardDef]:
        """Greedy capacity-aware bin packing to balance tokens across shards."""
        shards = [ShardDef(shard_id=f"shard_{i:04d}") for i in range(num_shards)]
        
        # Sort files by token count descending (largest first)
        sorted_files = sorted(files, key=lambda x: x.tokens, reverse=True)
        
        # Min-heap based on total_tokens to always assign to the emptiest shard
        heap = [(0, i, shards[i]) for i in range(num_shards)]
        
        for f in sorted_files:
            current_tokens, idx, shard = heapq.heappop(heap)
            
            shard.files.append(f)
            shard.total_tokens += f.tokens
            shard.total_bytes += f.size_bytes
            
            heapq.heappush(heap, (shard.total_tokens, idx, shard))
            
        return shards

    def partition_dataset(self, files: List[DatasetFile], topology: ClusterTopology, version_hash: str) -> Tuple[List[ShardDef], RoutingTable]:
        """Creates physical shards and routes them to DP ranks."""
        
        # 1. Determine number of shards. Must be a multiple of DP size.
        # Arbitrarily aim for ~10 shards per DP rank for good shuffling granularity.
        num_shards = topology.data_parallel_size * 10
        
        # 2. Pack files into balanced shards
        shards = self._bin_pack_files(files, num_shards)
        
        # 3. Route shards to DP ranks using Consistent Hashing
        # This ensures that if DP size changes slightly, data movement is minimized.
        ring = ConsistentHashRing()
        for dp_rank in range(topology.data_parallel_size):
            ring.add_node(dp_rank)
            
        routing = {rank: [] for rank in range(topology.data_parallel_size)}
        
        for shard in shards:
            assigned_rank = ring.get_node(shard.shard_id)
            routing[assigned_rank].append(shard.shard_id)
            
        table = RoutingTable(
            version_hash=version_hash,
            dp_rank_to_shards=routing
        )
        
        return shards, table

    def calculate_imbalance(self, shards: List[ShardDef]) -> float:
        """Calculates the max deviation from the mean shard size."""
        if not shards:
            return 0.0
        tokens = [s.total_tokens for s in shards]
        mean = sum(tokens) / len(tokens)
        if mean == 0:
            return 0.0
        max_dev = max(abs(t - mean) for t in tokens)
        return max_dev / mean

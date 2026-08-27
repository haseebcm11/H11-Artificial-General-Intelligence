import struct
import time
from dataclasses import dataclass
from typing import List, Dict

AGENT_ID = "H11-PROTOCOL"

@dataclass
class ProtocolInput:
    grpc_payloads: List[Dict[str, int]]
    ws_frames: List[bytes]
    token_rate: float
    token_capacity: int

@dataclass
class ProtocolOutput:
    http2_mux_streams: int
    encoded_protobufs: List[bytes]
    parsed_ws_opcodes: List[int]
    rate_limit_accepted: int

class ProtocolException(Exception):
    pass

class ProtocolAgent:
    """
    Implements HTTP/2 multiplexing limits, gRPC protobuf varint encoding, 
    WebSocket frame parsing, and Token Bucket rate limiting.
    """
    def _encode_varint(self, value: int) -> bytes:
        result = bytearray()
        while True:
            byte = value & 0x7F
            value >>= 7
            if value:
                result.append(byte | 0x80)
            else:
                result.append(byte)
                break
        return bytes(result)
        
    def _parse_ws_frame(self, frame: bytes) -> int:
        if not frame:
            raise ProtocolException("Empty WS frame")
        b1 = frame[0]
        opcode = b1 & 0x0F
        return opcode

    def process(self, input_data: ProtocolInput) -> ProtocolOutput:
        encoded_protos = []
        for p in input_data.grpc_payloads:
            for k, v in p.items():
                encoded_protos.append(self._encode_varint(v))
                
        opcodes = [self._parse_ws_frame(f) for f in input_data.ws_frames]
        
        # Token Bucket Algorithm
        tokens = input_data.token_capacity
        accepted = 0
        last_time = time.perf_counter()
        
        for _ in range(len(input_data.ws_frames)):
            current_time = time.perf_counter()
            elapsed = current_time - last_time
            tokens = min(input_data.token_capacity, tokens + elapsed * input_data.token_rate)
            last_time = current_time
            
            if tokens >= 1:
                tokens -= 1
                accepted += 1
                
        return ProtocolOutput(
            http2_mux_streams=len(input_data.grpc_payloads),
            encoded_protobufs=encoded_protos,
            parsed_ws_opcodes=opcodes,
            rate_limit_accepted=accepted
        )

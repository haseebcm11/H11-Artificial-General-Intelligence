"""h11_auction: Auction Mechanisms.

L16_multiagent_society - Substrate

This module implements a Combinatorial Vickrey-Clarke-Groves (VCG) auction.
It computes the optimal allocation of indivisible items to maximize social welfare
and calculates the exact VCG payments for each winning bidder to ensure truthfulness.
"""
from __future__ import annotations

import math
import time
from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple, Optional

AGENT_ID = "h11_auction"


class AuctionError(ValueError):
    """Domain-specific error for h11_auction."""
    pass


@dataclass(frozen=True)
class Bid:
    bidder_id: str
    items: frozenset[str]
    value: float


@dataclass(frozen=True)
class AuctionInput:
    available_items: frozenset[str]
    bids: List[Bid]
    reserve_price: float = 0.0


@dataclass(frozen=True)
class AuctionOutput:
    agent_id: str
    welfare: float
    allocation: Dict[str, List[str]]
    payments: Dict[str, float]
    execution_time_ms: float


class H11auctionAgent:
    """Analytical engine for Combinatorial VCG Auctions."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}

    def _winner_determination(self, bids: List[Bid], items: frozenset[str]) -> Tuple[float, List[Bid]]:
        """Exact winner determination using recursive backtracking for max weight independent set."""
        best_welfare = 0.0
        best_allocation: List[Bid] = []

        def search(index: int, current_welfare: float, allocated_items: Set[str], current_bids: List[Bid]):
            nonlocal best_welfare, best_allocation
            if index == len(bids):
                if current_welfare > best_welfare:
                    best_welfare = current_welfare
                    best_allocation = list(current_bids)
                return

            # Option 1: exclude bid
            search(index + 1, current_welfare, allocated_items, current_bids)

            # Option 2: include bid if feasible
            bid = bids[index]
            if not bid.items.isdisjoint(allocated_items):
                return
            if not bid.items.issubset(items):
                return
            
            allocated_items.update(bid.items)
            current_bids.append(bid)
            search(index + 1, current_welfare + bid.value, allocated_items, current_bids)
            current_bids.pop()
            allocated_items.difference_update(bid.items)

        search(0, 0.0, set(), [])
        return best_welfare, best_allocation

    def process(self, input_data: Any = None) -> Any:
        start_time = time.perf_counter()
        if input_data is None:
            raise AuctionError("Input data cannot be None")

        if isinstance(input_data, dict):
            raw_bids = input_data.get("bids", [])
            if raw_bids:
                # Single item Vickrey auction compatibility
                sorted_bids = sorted(raw_bids, key=lambda x: x.get("amount", x.get("value", 0)), reverse=True)
                winner = sorted_bids[0].get("bidder", sorted_bids[0].get("bidder_id", "winner"))
                price = sorted_bids[1].get("amount", sorted_bids[1].get("value", 0)) if len(sorted_bids) > 1 else input_data.get("reserve_price", 0.0)
                return {
                    "agent_id": AGENT_ID,
                    "winner": winner,
                    "price": price,
                    "mechanism": "vickrey",
                    "welfare": sorted_bids[0].get("amount", sorted_bids[0].get("value", 0)),
                }

        bids = [b for b in input_data.bids if b.value >= input_data.reserve_price]
        
        # 1. Compute optimal allocation and maximum social welfare (W)
        opt_welfare, opt_allocation = self._winner_determination(bids, input_data.available_items)
        
        allocation_dict: Dict[str, List[str]] = {}
        for b in opt_allocation:
            allocation_dict[b.bidder_id] = list(b.items)
            
        # 2. Compute VCG Payments
        payments: Dict[str, float] = {}
        for winner_bid in opt_allocation:
            winner = winner_bid.bidder_id
            welfare_others_opt = opt_welfare - winner_bid.value
            bids_without_i = [b for b in bids if b.bidder_id != winner]
            welfare_without_i, _ = self._winner_determination(bids_without_i, input_data.available_items)
            payment_i = welfare_without_i - welfare_others_opt
            payments[winner] = max(0.0, round(payment_i, 6))

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return AuctionOutput(
            agent_id=AGENT_ID,
            welfare=opt_welfare,
            allocation=allocation_dict,
            payments=payments,
            execution_time_ms=round(elapsed_ms, 4)
        )


# Backwards compatibility alias
AUCTIONAgent = H11auctionAgent

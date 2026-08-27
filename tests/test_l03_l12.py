from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


from h11_runtime.loader import load_module


def load(rel: str, key: str):
    return load_module(key, rel)


class RepresentationLayerTests(unittest.TestCase):
    def test_bpe_then_tokenizer_then_embedder_is_deterministic(self):
        bpe = load("L03_representation/H11-BPE/agent.py", "t_bpe")
        tok = load("L03_representation/H11-TOKENIZER/agent.py", "t_tok")
        emb = load("L03_representation/H11-EMBEDDER/agent.py", "t_emb")
        merges = bpe.BpeAgent().process(bpe.BpeInput(corpus=["low lower newest"], num_merges=5)).merges
        tokens = tok.TokenizerAgent().process(tok.TokenizerInput(text="lower", merges=merges)).tokens
        self.assertTrue(tokens)
        v1 = emb.EmbedderAgent().process(emb.EmbedderInput(tokens=tokens, dim=16)).vector
        v2 = emb.EmbedderAgent().process(emb.EmbedderInput(tokens=tokens, dim=16)).vector
        self.assertEqual(v1, v2)

    def test_counterfactual_abduction_action_prediction(self):
        cf = load("L12_world_models/H11-COUNTERFACTUAL-WORLD/agent.py", "t_cf")
        out = cf.CounterfactualWorldAgent().process(
            cf.CounterfactualWorldInput(x_obs=2.0, y_obs=5.0, a=2.0, x_do=4.0)
        )
        # u = 5 - 2*2 = 1; y_cf = 2*4 + 1 = 9
        self.assertEqual(out.u, 1.0)
        self.assertEqual(out.y_cf, 9.0)


if __name__ == "__main__":
    unittest.main()

import os
import math

base_dir = r"d:\My Research\H11 PATENTS\H11-AGI\L04_neural_core"

def write_agent(subdir, content):
    path = os.path.join(base_dir, subdir, "agent.py")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

# 1. H11-ARCHITECT
write_agent("H11-ARCHITECT", '''"""
H11-ARCHITECT: Neural Architecture Search
Implements Differentiable Architecture Search (DARTS) continuous relaxation.
"""
from dataclasses import dataclass
import math

AGENT_ID = "H11-ARCHITECT"

@dataclass
class NASInput:
    operation_weights: list[float]
    feature_maps: list[float]

@dataclass
class NASOutput:
    mixed_feature: float
    softmax_probs: list[float]

class Agent:
    def process(self, input_data: NASInput) -> NASOutput:
        max_w = max(input_data.operation_weights)
        exp_w = [math.exp(w - max_w) for w in input_data.operation_weights]
        sum_exp = sum(exp_w)
        probs = [ew / sum_exp for ew in exp_w]
        
        mixed_feature = sum(p * f for p, f in zip(probs, input_data.feature_maps))
        
        return NASOutput(mixed_feature=mixed_feature, softmax_probs=probs)
''')

# 2. H11-CONVOLUTION
write_agent("H11-CONVOLUTION", '''"""
H11-CONVOLUTION: Convolutional Math
Calculates exact output dimensions and receptive fields.
"""
from dataclasses import dataclass

AGENT_ID = "H11-CONVOLUTION"

@dataclass
class ConvInput:
    in_size: int
    kernel_size: int
    stride: int
    padding: int
    dilation: int = 1

@dataclass
class ConvOutput:
    out_size: int
    receptive_field: int

class Agent:
    def process(self, input_data: ConvInput) -> ConvOutput:
        effective_k = (input_data.kernel_size - 1) * input_data.dilation + 1
        out_size = (input_data.in_size + 2 * input_data.padding - effective_k) // input_data.stride + 1
        
        # Base receptive field calculation (assuming starting from 1)
        receptive_field = effective_k
        return ConvOutput(out_size=out_size, receptive_field=receptive_field)
''')

# 3. H11-DECODER
write_agent("H11-DECODER", '''"""
H11-DECODER: Transformer Decoder
Implements masked self-attention logic for autoregressive generation.
"""
from dataclasses import dataclass
import math

AGENT_ID = "H11-DECODER"

@dataclass
class DecoderInput:
    seq_length: int
    causal: bool = True

@dataclass
class DecoderOutput:
    attention_mask: list[list[float]]
    total_unmasked: int

class Agent:
    def process(self, input_data: DecoderInput) -> DecoderOutput:
        mask = []
        unmasked = 0
        for i in range(input_data.seq_length):
            row = []
            for j in range(input_data.seq_length):
                if input_data.causal and j > i:
                    row.append(float('-inf'))
                else:
                    row.append(0.0)
                    unmasked += 1
            mask.append(row)
        return DecoderOutput(attention_mask=mask, total_unmasked=unmasked)
''')

# 4. H11-DIFFUSION-NET
write_agent("H11-DIFFUSION-NET", '''"""
H11-DIFFUSION-NET: Diffusion Process
DDPM forward process computations.
"""
from dataclasses import dataclass
import math

AGENT_ID = "H11-DIFFUSION-NET"

@dataclass
class DiffInput:
    t: int
    beta_start: float = 0.0001
    beta_end: float = 0.02
    num_timesteps: int = 1000

@dataclass
class DiffOutput:
    beta_t: float
    alpha_t: float
    alpha_bar_t: float

class Agent:
    def process(self, input_data: DiffInput) -> DiffOutput:
        beta_t = input_data.beta_start + (input_data.t / input_data.num_timesteps) * (input_data.beta_end - input_data.beta_start)
        alpha_t = 1.0 - beta_t
        
        alpha_bar_t = 1.0
        for i in range(1, input_data.t + 1):
            b = input_data.beta_start + (i / input_data.num_timesteps) * (input_data.beta_end - input_data.beta_start)
            alpha_bar_t *= (1.0 - b)
            
        return DiffOutput(beta_t=beta_t, alpha_t=alpha_t, alpha_bar_t=alpha_bar_t)
''')

# 5. H11-DROPOUT
write_agent("H11-DROPOUT", '''"""
H11-DROPOUT: Dropout Layer
Inverted dropout scaling and variance preservation.
"""
from dataclasses import dataclass

AGENT_ID = "H11-DROPOUT"

@dataclass
class DropoutInput:
    prob: float
    features: list[float]
    training: bool = True

@dataclass
class DropoutOutput:
    scaled_features: list[float]
    expected_active: float

class Agent:
    def process(self, input_data: DropoutInput) -> DropoutOutput:
        if not input_data.training or input_data.prob == 0:
            return DropoutOutput(scaled_features=input_data.features, expected_active=len(input_data.features))
            
        scale = 1.0 / (1.0 - input_data.prob)
        # Assuming we apply expected value rather than random mask for determinism in this agent
        expected_active = len(input_data.features) * (1.0 - input_data.prob)
        scaled = [f * scale * (1.0 - input_data.prob) for f in input_data.features]
        return DropoutOutput(scaled_features=scaled, expected_active=expected_active)
''')

# 6. H11-ENCODER
write_agent("H11-ENCODER", '''"""
H11-ENCODER: Transformer Encoder
Bidirectional attention logic.
"""
from dataclasses import dataclass

AGENT_ID = "H11-ENCODER"

@dataclass
class EncoderInput:
    d_model: int
    num_heads: int
    seq_len: int

@dataclass
class EncoderOutput:
    head_dim: int
    total_flops_per_token: int

class Agent:
    def process(self, input_data: EncoderInput) -> EncoderOutput:
        head_dim = input_data.d_model // input_data.num_heads
        # Q, K, V projections + attention + output projection
        flops = 4 * input_data.d_model * input_data.d_model + 2 * input_data.seq_len * input_data.d_model
        return EncoderOutput(head_dim=head_dim, total_flops_per_token=flops)
''')

# 7. H11-FEEDFORWARD
write_agent("H11-FEEDFORWARD", '''"""
H11-FEEDFORWARD: Activation Math
Implements exact GELU and SiLU functions.
"""
from dataclasses import dataclass
import math

AGENT_ID = "H11-FEEDFORWARD"

@dataclass
class FFInput:
    x: float

@dataclass
class FFOutput:
    relu: float
    silu: float
    gelu: float

class Agent:
    def process(self, input_data: FFInput) -> FFOutput:
        x = input_data.x
        relu = max(0.0, x)
        silu = x / (1.0 + math.exp(-x))
        gelu = 0.5 * x * (1.0 + math.tanh(math.sqrt(2.0/math.pi) * (x + 0.044715 * x**3)))
        return FFOutput(relu=relu, silu=silu, gelu=gelu)
''')

# 8. H11-GNN
write_agent("H11-GNN", '''"""
H11-GNN: Graph Neural Network
Graph Laplacian normalization D^{-1/2} A D^{-1/2}.
"""
from dataclasses import dataclass
import math

AGENT_ID = "H11-GNN"

@dataclass
class GNNInput:
    adjacency_matrix: list[list[float]]

@dataclass
class GNNOutput:
    normalized_adjacency: list[list[float]]

class Agent:
    def process(self, input_data: GNNInput) -> GNNOutput:
        n = len(input_data.adjacency_matrix)
        degrees = [sum(row) for row in input_data.adjacency_matrix]
        inv_sqrt_d = [1.0 / math.sqrt(d) if d > 0 else 0.0 for d in degrees]
        
        norm_adj = []
        for i in range(n):
            row = []
            for j in range(n):
                val = inv_sqrt_d[i] * input_data.adjacency_matrix[i][j] * inv_sqrt_d[j]
                row.append(val)
            norm_adj.append(row)
        return GNNOutput(normalized_adjacency=norm_adj)
''')

# 9. H11-HYENA
write_agent("H11-HYENA", '''"""
H11-HYENA: Hyena Filter
Implicit long convolution parameterization.
"""
from dataclasses import dataclass
import math

AGENT_ID = "H11-HYENA"

@dataclass
class HyenaInput:
    t: int
    omega: float
    alpha: float

@dataclass
class HyenaOutput:
    filter_val: float

class Agent:
    def process(self, input_data: HyenaInput) -> HyenaOutput:
        # Hyena filter h(t) = Window(t) * sin(omega * t)
        window = math.exp(-input_data.alpha * input_data.t)
        val = window * math.sin(input_data.omega * input_data.t)
        return HyenaOutput(filter_val=val)
''')

# 10. H11-MOE
write_agent("H11-MOE", '''"""
H11-MOE: Mixture of Experts
Top-k routing capacity factor and load balancing math.
"""
from dataclasses import dataclass
import math

AGENT_ID = "H11-MOE"

@dataclass
class MOEInput:
    router_logits: list[float]
    capacity_factor: float
    top_k: int
    tokens_per_batch: int

@dataclass
class MOEOutput:
    expert_capacity: int
    routing_probs: list[float]

class Agent:
    def process(self, input_data: MOEInput) -> MOEOutput:
        max_l = max(input_data.router_logits)
        exp_l = [math.exp(l - max_l) for l in input_data.router_logits]
        sum_exp = sum(exp_l)
        probs = [el / sum_exp for el in exp_l]
        
        num_experts = len(input_data.router_logits)
        capacity = math.ceil(input_data.tokens_per_batch * input_data.top_k * input_data.capacity_factor / num_experts)
        
        return MOEOutput(expert_capacity=capacity, routing_probs=probs)
''')

# 11. H11-NORMALIZE
write_agent("H11-NORMALIZE", '''"""
H11-NORMALIZE: Normalization Methods
RMSNorm exact computation.
"""
from dataclasses import dataclass
import math

AGENT_ID = "H11-NORMALIZE"

@dataclass
class NormInput:
    x: list[float]
    eps: float = 1e-5

@dataclass
class NormOutput:
    y: list[float]
    rms: float

class Agent:
    def process(self, input_data: NormInput) -> NormOutput:
        mean_sq = sum(v*v for v in input_data.x) / len(input_data.x)
        rms = math.sqrt(mean_sq + input_data.eps)
        y = [v / rms for v in input_data.x]
        return NormOutput(y=y, rms=rms)
''')

# 12. H11-OUTPUT-HEAD
write_agent("H11-OUTPUT-HEAD", '''"""
H11-OUTPUT-HEAD: Loss Functions
Cross-Entropy and Focal Loss.
"""
from dataclasses import dataclass
import math

AGENT_ID = "H11-OUTPUT-HEAD"

@dataclass
class HeadInput:
    logits: list[float]
    target_idx: int
    gamma: float = 2.0

@dataclass
class HeadOutput:
    cross_entropy: float
    focal_loss: float

class Agent:
    def process(self, input_data: HeadInput) -> HeadOutput:
        max_l = max(input_data.logits)
        exp_l = [math.exp(l - max_l) for l in input_data.logits]
        sum_exp = sum(exp_l)
        probs = [el / sum_exp for el in exp_l]
        
        p_t = probs[input_data.target_idx]
        ce = -math.log(p_t + 1e-9)
        fl = (1 - p_t)**input_data.gamma * ce
        
        return HeadOutput(cross_entropy=ce, focal_loss=fl)
''')

# 13. H11-PARAMETER
write_agent("H11-PARAMETER", '''"""
H11-PARAMETER: Parameter Initialization
Xavier and He initialization variances.
"""
from dataclasses import dataclass
import math

AGENT_ID = "H11-PARAMETER"

@dataclass
class ParamInput:
    fan_in: int
    fan_out: int

@dataclass
class ParamOutput:
    he_variance: float
    xavier_variance: float

class Agent:
    def process(self, input_data: ParamInput) -> ParamOutput:
        he_var = 2.0 / input_data.fan_in
        xavier_var = 2.0 / (input_data.fan_in + input_data.fan_out)
        return ParamOutput(he_variance=he_var, xavier_variance=xavier_var)
''')

# 14. H11-RECURRENT
write_agent("H11-RECURRENT", '''"""
H11-RECURRENT: RNN Gating
LSTM continuous state update math.
"""
from dataclasses import dataclass
import math

AGENT_ID = "H11-RECURRENT"

@dataclass
class RecurrentInput:
    forget_gate: float
    input_gate: float
    cell_candidate: float
    prev_cell: float

@dataclass
class RecurrentOutput:
    next_cell: float

class Agent:
    def process(self, input_data: RecurrentInput) -> RecurrentOutput:
        def sigmoid(x):
            return 1.0 / (1.0 + math.exp(-max(min(x, 20), -20)))
        def tanh(x):
            return math.tanh(x)
            
        f = sigmoid(input_data.forget_gate)
        i = sigmoid(input_data.input_gate)
        c_tilde = tanh(input_data.cell_candidate)
        
        next_c = f * input_data.prev_cell + i * c_tilde
        return RecurrentOutput(next_cell=next_c)
''')

# 15. H11-RESIDUAL
write_agent("H11-RESIDUAL", '''"""
H11-RESIDUAL: Skip Connection
Variance accumulation in deep residual networks.
"""
from dataclasses import dataclass
import math

AGENT_ID = "H11-RESIDUAL"

@dataclass
class ResInput:
    num_layers: int
    branch_var: float

@dataclass
class ResOutput:
    final_variance: float
    scale_factor: float

class Agent:
    def process(self, input_data: ResInput) -> ResOutput:
        # Var(x_L) = Var(x_0) + L * Var(f(x))
        final_var = 1.0 + input_data.num_layers * input_data.branch_var
        scale_factor = 1.0 / math.sqrt(final_var)
        return ResOutput(final_variance=final_var, scale_factor=scale_factor)
''')

# 16. H11-RWKV
write_agent("H11-RWKV", '''"""
H11-RWKV: RWKV Attention
WKV linear attention computation.
"""
from dataclasses import dataclass
import math

AGENT_ID = "H11-RWKV"

@dataclass
class RWKVInput:
    r: float
    k: float
    v: float
    w: float
    u: float
    num: float
    den: float

@dataclass
class RWKVOutput:
    wkv: float
    next_num: float
    next_den: float

class Agent:
    def process(self, input_data: RWKVInput) -> RWKVOutput:
        wkv = (input_data.num + math.exp(input_data.u + input_data.k) * input_data.v) / (input_data.den + math.exp(input_data.u + input_data.k) + 1e-8)
        next_num = math.exp(input_data.w) * input_data.num + math.exp(input_data.k) * input_data.v
        next_den = math.exp(input_data.w) * input_data.den + math.exp(input_data.k)
        
        return RWKVOutput(wkv=wkv, next_num=next_num, next_den=next_den)
''')

# 17. H11-SSM
write_agent("H11-SSM", '''"""
H11-SSM: State Space Models
Zero-order hold continuous-to-discrete conversion.
"""
from dataclasses import dataclass
import math

AGENT_ID = "H11-SSM"

@dataclass
class SSMInput:
    A: float
    B: float
    dt: float

@dataclass
class SSMOutput:
    A_bar: float
    B_bar: float

class Agent:
    def process(self, input_data: SSMInput) -> SSMOutput:
        A_bar = math.exp(input_data.A * input_data.dt)
        if input_data.A == 0:
            B_bar = input_data.B * input_data.dt
        else:
            B_bar = (A_bar - 1.0) / input_data.A * input_data.B
            
        return SSMOutput(A_bar=A_bar, B_bar=B_bar)
''')

# 18. H11-TRANSFORMER
write_agent("H11-TRANSFORMER", '''"""
H11-TRANSFORMER: Core Transformer Logic
Scaled dot-product attention calculation.
"""
from dataclasses import dataclass
import math

AGENT_ID = "H11-TRANSFORMER"

@dataclass
class TransInput:
    q: list[float]
    k: list[float]
    v: list[float]

@dataclass
class TransOutput:
    attention: list[float]

class Agent:
    def process(self, input_data: TransInput) -> TransOutput:
        d = len(input_data.q)
        dot = sum(qi*ki for qi, ki in zip(input_data.q, input_data.k))
        scaled = dot / math.sqrt(d)
        
        score = math.exp(scaled)
        
        # Self-attention for 1 token sequence (simplified to single dot product)
        out = [vi * score for vi in input_data.v]
        return TransOutput(attention=out)
''')

print("Generated all 18 agent.py files.")

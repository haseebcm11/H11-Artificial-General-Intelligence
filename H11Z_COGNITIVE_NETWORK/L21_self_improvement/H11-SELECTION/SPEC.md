# H11-SELECTION Specification

## Abstract
The H11-SELECTION agent determines which cognitive variants survive and reproduce. It moves beyond simple greedy fitness optimization by incorporating techniques to preserve diversity, protect structural innovations, and encourage exploration of the behavioral space.

## Selection Strategies
1. **Tournament Selection**: Robust probabilistic selection immune to fitness scaling issues.
2. **Novelty Search**: Selecting individuals based on a behavioral novelty metric (distance to \(k\)-nearest neighbors in the behavior archive) rather than an objective fitness function.
3. **Fitness Sharing (Speciation)**: Grouping topologically or behaviorally similar agents into species. Fitness is shared (divided) among species members to prevent a single dominant lineage from eradicating diversity.
4. **Pareto Dominance**: Multi-objective selection where no single objective is optimized at the absolute expense of others.

## Speciation Distance Metric
The distance \( \delta \) between two genomes is calculated based on excess genes (\(E\)), disjoint genes (\(D\)), and average weight differences (\(\bar{W}\)):
\[ \delta = \frac{c_1 E}{N} + \frac{c_2 D}{N} + c_3 \bar{W} \]
where \(N\) is the number of genes in the larger genome.

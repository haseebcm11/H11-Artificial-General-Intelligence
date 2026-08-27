> **Layer 2** · Data Plane & Ingestion · `H11-CRAWLER`

## Purpose

H11-CRAWLER handles autonomous traversal and extraction of interconnected web pages, graph data, and linked documents. It acts as the substrate's exploratory sensory organ, mapping out external information spaces. 

Unlike simple scrapers, H11-CRAWLER is a fully distributed system designed to crawl billions of pages while strictly adhering to complex politeness policies. It dynamically resolves dynamic DOMs using headless JavaScript execution, handles tarpits/spider traps gracefully, and builds high-fidelity structural mappings of web corpuses.

## Technical Deep-Dive

The core architecture follows the Mercator web crawler design. It utilizes a bifurcated URL Frontier: a set of "front" queues prioritizing URLs based on novelty and PageRank estimation, and "back" queues guaranteeing politeness. The back queues are mapped 1:1 with host domains, and an asynchronous worker pool drains them ensuring a strict intra-request delay (e.g., 2 seconds per domain) without blocking parallel extraction from other domains.

For deduplication, it employs Content-Seen techniques using an in-memory Bloom Filter combined with SimHash over the raw HTML text to avoid crawling near-duplicate pages (e.g., URL parameters that don't change content). 

DOM rendering is deferred to a farm of headless browsers orchestrating CDP (Chrome DevTools Protocol). The crawler uses a heuristic DOM snapshotter that listens for the cessation of network idle events and DOM node mutations to determine when a single-page application (SPA) has fully loaded before scraping.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `seed_urls` | `List[URL]` | Initial nodes to begin the crawl frontier |
| `max_depth` | `int` | Maximum link depth from seeds |
| `politeness_delay_ms` | `int` | Delay to enforce between hits to same host |
| `render_js` | `bool` | Whether to route through CDP rendering |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `page_graph` | `Digraph` | Edges discovered between documents |
| `extracted_doms` | `List[Document]` | Parsed text, metadata, and structural features |
| `frontier_exhausted`| `bool` | True if natural crawl exhaustion occurred |

### State Schema
- `bloom_filter`: Bit array for exact URL deduplication.
- `simhash_signatures`: Set of structural hashes for near-duplicate detection.
- `mercator_queues`: The active priority queues organizing the frontier.

## Dependencies

### Upstream (depends on)
- `H11-CONFIG`: Global policies on allowed domains and banned IPs.

### Downstream (feeds into)
- `H11-CLEANSER`: Sends raw DOM strings for tag stripping and UTF normalization.

## Failure Modes
1. **Spider Traps**: Infinite dynamic URL generation (e.g., calendar widgets). Mitigated by maximum depth and path-complexity heuristics.
2. **CDP Zombie Processes**: Headless browsers hanging on infinite loops in target JS. Requires strict wall-clock sandboxing.
3. **Robots.txt Poisoning**: Malformed or hostile robots files causing parsing infinite loops.

## Performance Characteristics
- **Concurrency**: Can maintain 10,000 parallel back-queue connections per instance.
- **Memory**: Bloom filter tuned for 1 billion URLs requires ~1.2GB RAM.

## Research References
- "Mercator: A scalable, extensible web crawler" (Heydon & Najork).
- "Detecting near-duplicates for web crawling" (Manku et al., WWW 2007).
- "Spider traps and how to avoid them in large-scale crawling" (Baeza-Yates).

## Implementation Notes
URL canonicalization is critical. Must strip default ports, sort query parameters, and resolve relative links rigorously before checking the Bloom Filter.

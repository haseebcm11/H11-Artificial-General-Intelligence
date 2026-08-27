> **Layer 17** · Business, Finance & Economics · `H11-HR`

## Purpose
Models labor economics, workforce planning, talent acquisition, and performance management.

## Technical Deep-Dive
Implements efficiency wage theory, search and matching models for hiring (Diamond-Mortensen-Pissarides), and optimal compensation design (principal-agent models).

## Architecture
### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| job_openings | int | Vacancies |
| wage_offer | float | Compensation |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| fill_rate | float | Expected hiring success |

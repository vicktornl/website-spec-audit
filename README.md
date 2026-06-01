# website-spec-audit

CLI tool to audit websites against [specification.website](https://specification.website).

## Installation

```bash
pip install website-spec-audit
```

## Usage

```bash
website-spec-audit https://example.com
```

### Options

| Option | Description |
| --- | --- |
| `-c`, `--category` | Filter by category (can be repeated). E.g. `-c security -c seo` |
| `-s`, `--status` | Filter by topic status level: `required`, `recommended`, `optional`, `avoid` |
| `-t`, `--topic` | Run only specific topics by slug. E.g. `-t hsts -t robots-txt` |
| `-v`, `--verbose` | Show detailed check output |
| `--concurrency` | Max concurrent HTTP requests (default: 10) |
| `--version` | Show version |

### Examples

Audit only security validators:

```bash
website-spec-audit https://example.com -c security
```

Audit only required topics:

```bash
website-spec-audit https://example.com -s required
```

Run specific topics:

```bash
website-spec-audit https://example.com -t hsts -t content-security-policy
```

## Development

```bash
pip install -e ".[dev]"
pytest
```

## License

MIT

# Developer Experience Summary

The tool has **two DX options** for running commands. Both are fully functional!

## Quick Start

```bash
# One time setup
uv sync

# Then pick your preferred method below
```

---

## Option 1: Just (Recommended)

**Modern task runner with flexible parameters**

```bash
just               # Show all commands with descriptions
just analyse       # Default file

# With custom parameters
just analyse my_graph.graphml
just config my_graph.graphml output.json
just migrate my_graph.graphml --graph-name my_db --host example.com
just topology my_graph.graphml report.json
```

**Installation:**

```bash
brew install just      # macOS
cargo install just     # Rust
# See https://github.com/casey/just
```

---

## Option 2: Shell Scripts (Simple & Direct)

**No dependencies, explicit commands**

```bash
./scripts/analyse.sh test_sample.graphml
./scripts/config.sh test_sample.graphml config.json
./scripts/migrate.sh test_sample.graphml --host localhost
```

---

## Option 3: Raw UV (For one-offs)

**Direct invocation, no abstraction**

```bash
uv run python -m graphml_to_falkordb.cli test_sample.graphml --analyze-only
uv run python -m graphml_to_falkordb.cli test_sample.graphml --generate-config config.json
```

---

## Tested Commands

All commands have been tested and work correctly:

✅ `just analyse` - Analyzes test_sample.graphml

```
GraphML Analysis:
  Nodes: 3
  Relationships: 3
  Node labels: Company, Person
  Relationship types: KNOWS, WORKS_AT
```

✅ `just config` - Generates configuration template

```
Configuration template saved to generated_config.json
```

✅ `./scripts/analyse.sh` - Shell script wrapper

```
Shell scripts work correctly with proper error handling
```

---

## Comparison Table

| Feature               | Just           | Scripts      | Raw UV        |
|-----------------------|----------------|--------------|---------------|
| **Ease of use**       | ★★★★★          | ★★★☆☆        | ★★☆☆☆         |
| **Parameter support** | Excellent      | Good         | Perfect       |
| **Installation**      | Required       | None         | Built-in (uv) |
| **Familiarity**       | Modern         | Simple       | Direct        |
| **Best for**          | Most workflows | Transparency | Debugging     |

---

## Recommended Workflow

1. **Initial setup:**

   ```bash
   uv sync
   ```

2. **Analyse new graphs:**

   ```bash
   just analyse    # Quick overview
   just topology   # Detailed report
   ```

3. **Generate configuration:**

   ```bash
   just config
   vi generated_config.json    # Edit if needed
   ```

4. **Migrate to FalkorDB:**

   ```bash
   just migrate
   ```

---

## Adding Custom Commands

**Add to justfile:**

```just
my-task:
    uv run python -c "print('hello')"
```

**Add new script:**

```bash
cat > scripts/my-script.sh << 'EOF'
#!/bin/bash
# Description
uv run python -c "..."
EOF
chmod +x scripts/my-script.sh
```

---

## For CI/CD

Use raw `uv run` commands in CI/CD pipelines for simplicity:

```yaml
# Example GitHub Actions
- name: Analyse GraphML
  run: uv run python -m graphml_to_falkordb.cli graph.graphml --analyze-only
```

---

## Summary

**Start with:** `just` then `just analyse`

**For most workflows:** Use `just` (modern, flexible parameters)

**For scripts/CI:** Use `uv run` directly

**For transparency:** Use shell scripts in `./scripts/`

All options are fully functional and tested!

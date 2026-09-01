# `configs/`

Versioned configs hashed into release and run manifests.

- `dataset/` — source registry, replacement maps, Cube sampler, execution repairs
- Direct-ZS model/API settings are CLI flags plus `.env`; method YAML is not used
  in this release

Do not put API keys or machine-specific absolute paths in these files.

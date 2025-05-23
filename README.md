# aimee (working name)

**aimee** is a local-first thought processor with a rich terminal UI and built-in LLM-powered semantic linking between notes.

it helps you capture, explore, and interconnect your thoughts—without ever touching the cloud.

---

## core idea

- write your thoughts in plain text.
- a local AI reads and structures them.
- a graph of ideas emerges—automatically.

no tags. no backlinks. no manual linking.

just thought → file → meaning → map

## features (planned)

- terminal UI (TUI) with panels for notes, graph, and prompts
- local markdown note storage
- automatic semantic connections between notes
- fast, local LLM processing using quantized models
- offline, zero telemetry, zero cloud

## tech stack

- language: `rust`
- terminal ui: [`ratatui`](https://github.com/ratatui-org/ratatui)
- ai backend: [`llm`](https://github.com/rustformers/llm) or llama.cpp bindings
- graph logic: [`petgraph`](https://docs.rs/petgraph/)
- storage: local filesystem + optional `sled` or `sqlite` for metadata

## status

early development phase. no guarantees.  
feel free to watch, fork, or build alongside :)




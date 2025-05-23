# aimee (working name)

**aimee** is a local-first thought processor with a rich terminal UI and built-in LLM-powered semantic linking between notes.

it helps you capture, explore, and interconnect your thoughts—without ever touching the cloud.

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

- language: `c`
- compiler: `gcc`
- build system: `make`
- terminal ui: [`notcurses`](https://github.com/dankamongmen/notcurses)
- ai backend: [`llama.cpp`](https://github.com/ggerganov/llama.cpp)
- graph logic: custom structs + [`uthash`](https://troydhanson.github.io/uthash/)
- storage: local filesystem with `cjson` for parsing and [`cmark`](https://github.com/commonmark/cmark) for markdown

## status

early development phase. no guarantees.  
feel free to watch, fork, or build alongside :)




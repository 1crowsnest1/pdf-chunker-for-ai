<pre style="font-family:'Courier New',Courier,monospace;font-size:12px;line-height:1.17;white-space:pre;background-color:#000;color:#fff;padding:8px;margin:0;"><span style="color:#AAAAAA">╒═════╗ ╒══════╗ ╒═════╗      ╒═════╗ ╒═╗ ╒═╗ ╒═╗ ╒═╗ ╒═══╗  ╒═╗ ╒═╗ ╒══╗ ╒═════╗ ╒══════╗     </span>
<span style="color:#AAAAAA">│ ╓─┐ ║ └┐ ╓─┐ ║ │ ╓───╜      │ ╓─┐ ║ │ ║ │ ║ │ ║ │ ║ │   ╚╗ │ ║ │ ║╒╛ ╓╜ │ ╓───╜ │ ╓──┐ ║     </span>
<span style="color:#AAAAAA">│ ╚═╛ ║  │ ║ │ ║ │ ╚═╗        │ ║ └─╜ │ ╚═╛ ║ │ ║ │ ║ │ ╟┐ ╚╗│ ║ │ ╚╛ ╚═╗ │ ╚═╗   │ ╚══╛ ║     </span>
<span style="color:#AAAAAA">│ ╓───╜  │ ║ │ ║ │ ╓─╜        │ ║ ╒═╗ │ ╓─┐ ║ │ ║ │ ║ │ ║└┐ ╚╡ ║ │ ╓──┐ ║ │ ╓─╜   │ ╓─┐ ╓╜     </span>
<span style="color:#AAAAAA">│ ║     ╒╛ ╚═╛ ║ │ ║          │ ╚═╛ ║ │ ║ │ ║ │ ╚═╛ ║ │ ║ └┐   ║ │ ║  │ ║ │ ╚═══╗ │ ║ │ ╚╗     </span>
<span style="color:#AAAAAA">└─╜     └──────╜ └─╜          └─────╜ └─╜ └─╜ └─────╜ └─╜  └───╜ └─╜  └─╜ └─────╜ └─╜ └──╜     </span>
<span style="color:#AAAAAA">                              ╒═════╗ ╒══════╗ ╒══════╗      ╒══════╗ ╒═══╗</span>
<span style="color:#AAAAAA">                              │ ╓───╜ │ ╓──┐ ║ │ ╓──┐ ║      │ ╓──┐ ║ └┐ ╓╜</span>
<span style="color:#AAAAAA">                              │ ╚═╗   │ ║  │ ║ │ ╚══╛ ║      │ ╚══╛ ║  │ ║ </span>
<span style="color:#AAAAAA">                              │ ╓─╜   │ ║  │ ║ │ ╓─┐ ╓╜      │ ╓──┐ ║  │ ║ </span>
<span style="color:#AAAAAA">                              │ ║     │ ╚══╛ ║ │ ║ │ ╚╗      │ ║  │ ║ ╒╛ ╚╗</span>
<span style="color:#AAAAAA">                              └─╜     └──────╜ └─╜ └──╜      └─╜  └─╜ └───╜</span></pre>


# PDF Chunker for AI

Split PDFs into **AI-ready chunks** under page & size limits.

For every `Something.pdf` this tool:

1. Creates a folder `Something/`
2. Splits the PDF into chunks that are **at most N pages** *and* **at most M megabytes**
3. Names each chunk `Something_p001-015.pdf`, `Something_p016-030.pdf`, …
4. Writes the chunks into that folder

Default limits (15 pages / 15 MB) match common **ChatGPT, Claude, and other LLM** upload caps.

## Why this exists

Large PDFs get rejected by AI assistants. This tool automatically produces smaller pieces that stay under both page-count and file-size limits so you can upload them one by one (or in parallel) to LLMs, RAG pipelines, or document-AI services.

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

## Usage

```bash
# defaults: ≤15 pages AND ≤15 MB
python pdf_chunker.py --input-dir ./pdfs

# custom limits + output root
python pdf_chunker.py -i ./pdfs -o ./chunks --max-pages 10 --max-mb 8
```

### Output layout

```
pdfs/
  MyDoc.pdf
  MyDoc/
    MyDoc_p001-015.pdf
    MyDoc_p016-030.pdf
    …
```

## Options

| Flag | Default | Meaning |
|------|---------|---------|
| `-i / --input-dir` | `./pdfs` | Folder containing source PDFs |
| `-o / --output-dir` | same as input | Root for per-document subfolders |
| `-p / --max-pages` | `15` | Max pages per chunk |
| `-m / --max-mb` | `15` | Max size per chunk (MB) |

## Topics

`pdf` · `chunking` · `ai-upload` · `llm` · `chatgpt` · `claude` · `document-splitting` · `pymupdf` · `python-cli` · `research-tools`

## License

MIT – see [LICENSE](LICENSE).

# CLAUDE.md - DNA Editor

## Project Overview

A Vim-inspired command-line DNA sequence editor for bioinformatics. Provides modal editing (Normal/Insert/Visual) for DNA manipulation, CRISPR simulation, transcription, translation, alignment, and visualization.

## Tech Stack

- **Language**: Python 3
- **Dependencies**: numpy, scikit-learn, matplotlib, biopython (see `requirements.txt`)
- **No build system, CI/CD, or test framework** is configured

## Project Structure

```
Sequence/
├── main.py              # CLI entry point, help text, main loop
├── dna-editor.py        # Core DNAEditor class (named dna_editor.py as module)
├── requirements.txt     # Python dependencies
├── README.md            # User-facing overview
└── Wiki DNA Editor.md   # Detailed feature documentation
```

This is a flat repository — all source code lives at the root level.

## Running the Project

```bash
pip install -r requirements.txt
python main.py
```

## Architecture

### Core Class: `DNAEditor` (dna-editor.py)

Single class that manages all state and operations:

- **State**: `dna` (list of chars), `cursor`, `clipboard`, `mode`, `history`/`future` (undo/redo stacks), `annotations`
- **Modes**: `"NORMAL"`, `"INSERT"`, `"VISUAL"`
- **Entry point**: `execute(command)` — dispatches commands based on current mode

### Command Routing

Commands are routed via string prefix matching in `execute()`:
- Single chars / short prefixes for editing (`x`, `r<nuc>`, `c<count>`, `dd`, `yy`, `p`)
- `/` prefix for search
- `:` prefix for colon commands (`:transcribe`, `:translate`, `:cas`, `:save`, etc.)
- Mode-specific behavior (INSERT mode interprets input as nucleotide insertion)

### Import Note

The file is named `dna-editor.py` on disk but imported as `dna_editor` in `main.py` (Python resolves the hyphen).

## Code Conventions

- **Snake_case** for all methods and variables
- **Type hints** used on method signatures (`List`, `Tuple`, `Dict` from `typing`)
- **No docstrings** on methods — function names are self-descriptive
- **No error handling** for most operations (file I/O, malformed commands)
- DNA stored as uppercase character list; all inputs are `.upper()`'d on entry

## Known Issues / Incomplete Features

- `yank_visual()` and `delete_visual()` are stubs (empty `pass`)
- `change()` calls `self.delete_sequence(count)` but `delete_sequence()` takes no arguments — crashes when count > 0
- `r` command conflicts: both `replace` (prefix `r<nuc>`) and `redo` (exact `r`) match — `replace` takes priority, so redo is unreachable
- No input validation in the main loop
- `analyze_mutations` in `main.py` runs after `:mutate`/`:recombine` but sequence length may have changed, causing an error return

## Development Guidelines

- Keep the flat file structure — no need for packages or subdirectories
- The `DNAEditor` class is the single source of truth for sequence state
- All sequence manipulation should go through `DNAEditor` methods, not direct list manipulation in `main.py`
- When adding new commands, add the prefix match in `execute()` and a corresponding help entry in `print_help()`
- Preserve the modal editing paradigm (Normal/Insert/Visual) when adding features

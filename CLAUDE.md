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
├── main.py              # CLI entry point, help text, main loop (62 lines)
├── dna-editor.py        # Core DNAEditor class (268 lines)
├── requirements.txt     # Python dependencies
├── README.md            # User-facing overview
└── Wiki DNA Editor.md   # Detailed feature documentation
```

This is a flat repository — all source code lives at the root level. Do not create subdirectories or packages.

## Running & Verifying

```bash
pip install -r requirements.txt
python main.py
```

There are no tests. To verify changes don't break imports or syntax:
```bash
python -c "from dna_editor import DNAEditor; e = DNAEditor('ATGCATGC'); print(e.get_dna())"
```

To smoke-test a specific method (example — transcribe):
```bash
python -c "from dna_editor import DNAEditor; e = DNAEditor('ATGCATGC'); print(e.transcribe())"
```

## Architecture

### Core Class: `DNAEditor` (dna-editor.py)

Single class that manages all state and operations:

- **State fields**: `dna` (list of chars), `cursor` (int), `clipboard` (str), `mode` (str), `history`/`future` (list of list — undo/redo stacks), `annotations` (list of tuples)
- **Modes**: `"NORMAL"`, `"INSERT"`, `"VISUAL"`
- **Entry point**: `execute(command)` — dispatches commands based on current mode, then calls `save_state()`

### Command Routing (execute method, dna-editor.py:26-96)

Commands are routed via if/elif chain with string prefix matching. **Order matters** — earlier matches shadow later ones.

Normal mode dispatch order:
1. Exact matches first: `i`, `v`, `x`, `dd`, `yy`, `p`, `u`
2. Prefix matches: `r<nuc>` (line 34), `c<count>` (line 37), `/<pattern>` (line 44)
3. Colon commands: `:cas`, `:transcribe`, `:translate`, `:gc_content`, `:one_hot`, `:recombine`, `:mutate`, `:align`, `:visualize`, `:save`, `:load`, `:annotate`, `:analyze_mutations`

Insert mode (line 83-87): `ESC` returns to NORMAL, anything else calls `insert()`.
Visual mode (line 88-94): `ESC` returns to NORMAL, `y` yanks, `d` deletes.

### main.py Structure (main.py:5-30)

- Creates `DNAEditor` with hardcoded seed sequence `"ATGGCTAGCTAGCTAGCTAGC"`
- REPL loop: reads input, dispatches to `editor.execute()`, prints result and current DNA
- Post-command hook (line 25-30): after `:mutate` or `:recombine`, runs `analyze_mutations` against original sequence
- `print_help()` (line 32-59): static help text — must be updated when adding commands

### Import Note

The file is named `dna-editor.py` on disk but imported as `dna_editor` in `main.py` (Python resolves the hyphen).

## Code Conventions

- **Snake_case** for all methods and variables
- **Type hints** on method signatures (`List`, `Tuple`, `Dict` from `typing`)
- **No docstrings** — function names are self-descriptive; do not add docstrings
- **No error handling** for most operations — do not add try/except unless fixing a specific bug
- DNA stored as **uppercase character list**; all inputs are `.upper()`'d on entry
- Methods that produce output `return` a value; void operations return `None`
- `save_state()` is called once at the end of `execute()` — individual methods should NOT call it

## Known Bugs (with locations)

These are real bugs in the codebase. Fix them only if the user asks.

1. **`change()` crashes** (dna-editor.py:145-148): Calls `self.delete_sequence(count)` but `delete_sequence()` accepts no arguments. Fix: add a `count` parameter to `delete_sequence()` or change `change()` to call the right method.

2. **`redo` unreachable** (dna-editor.py:34 vs 48): `r` prefix match on line 34 (`self.replace(command[1])`) fires before the exact `r` match on line 48 (`self.redo()`). The `r` command always goes to `replace`. Fix: check `command == "r"` before `command.startswith("r")`.

3. **`yank_visual()` and `delete_visual()` are stubs** (dna-editor.py:239-245): Both are empty `pass`. Visual mode selection is not tracked (no `visual_start` field).

4. **`analyze_mutations` length mismatch** (main.py:25-30): After `:mutate`/`:recombine`, sequence length may change (insertions/deletions), but `analyze_mutations` requires equal-length sequences. Returns error dict instead of useful output.

## How to Add a New Command

Follow this checklist for every new command:

1. **Add the method** to `DNAEditor` in `dna-editor.py`. Follow existing patterns: accept typed parameters, return a value if the command produces output, mutate `self.dna` in place for edits.

2. **Add routing** in `execute()` (dna-editor.py:26-82). Place it in the correct position:
   - Exact-match commands (`==`) must come BEFORE prefix-match commands (`startswith`) for the same prefix
   - Colon commands go in the `:` block (after line 50)
   - If the method returns a value, use `return self.method()` so `execute()` passes it back

3. **Add help text** in `print_help()` (main.py:32-59). Match the existing format: `    :command_name - Description`.

4. **Verify** with: `python -c "from dna_editor import DNAEditor; e = DNAEditor('ATGCATGC'); print(e.execute(':your_command'))"`

## How to Fix a Bug

1. Read the relevant method and its callers before changing anything
2. Make the minimal fix — do not refactor surrounding code
3. Verify with a one-liner smoke test (see above)
4. If fixing command routing order, be careful not to shadow other commands

## Key Methods Reference

| Method | Location | Purpose |
|--------|----------|---------|
| `execute(command)` | line 26 | Command dispatcher — all commands flow through here |
| `delete()` | line 98 | Delete single nucleotide at cursor |
| `delete_sequence()` | line 102 | Delete from cursor to next ATG codon |
| `insert(nucleotide)` | line 122 | Insert nucleotide at cursor position |
| `find(sequence)` | line 116 | Move cursor to next occurrence of pattern |
| `cas_edit(guide_rna)` | line 150 | CRISPR-Cas9 simulation (random NHEJ) |
| `transcribe()` | line 163 | DNA → RNA via Biopython |
| `translate()` | line 166 | DNA → amino acids via Biopython |
| `gc_content()` | line 169 | Overall + sliding window GC content |
| `mutate(rate)` | line 194 | Random substitutions, insertions, deletions |
| `recombine(sequence2)` | line 185 | Two-point crossover recombination |
| `align(sequence2)` | line 210 | Pairwise global alignment via Biopython |
| `save_to_file(filename)` | line 226 | Write to FASTA format |
| `load_from_file(filename)` | line 230 | Read from FASTA format |
| `save_state()` | line 136 | Push current DNA to history stack |
| `undo()` / `redo()` | line 126/132 | History navigation |
| `get_dna()` | line 252 | Return current sequence as string |

# DNA Editing Language Documentation

## Overview

The DNA Editing Language is a powerful tool designed for manipulating and analyzing DNA sequences. It combines the familiarity of Vim-like commands with specialized functions for DNA manipulation, making it an ideal choice for bioinformaticians, computational biologists, and researchers working with genetic data.

## Key Features

1. **Vim-inspired Interface**: Utilizes familiar Vim keybindings for efficient editing.
2. **DNA Manipulation**: Perform operations like insertion, deletion, copying, and pasting of nucleotides.
3. **CRISPR-Cas9 Simulation**: Simulate CRISPR-Cas9 edits on DNA sequences.
4. **Transcription and Translation**: Convert DNA to RNA and amino acid sequences.
5. **GC Content Analysis**: Calculate the GC content of DNA sequences.
6. **Machine Learning Integration**: One-hot encode DNA sequences for ML applications.
7. **Undo/Redo Functionality**: Track and revert changes to your sequences.
8. **Recombination Simulation**: Perform simple recombination between two DNA sequences.
9. **Mutation Introduction and Analysis**: Introduce random mutations and analyze their effects.

## Getting Started

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/ariankh/sequence.git
   ```
2. Navigate to the project directory:
   ```
   cd dna-editing.py
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

### Basic Usage

Run the main script:
```
python main.py
```

You'll be prompted to enter commands. Here are some basic commands to get started:

- `i`: Enter insert mode
- `ESC`: Return to normal mode
- `x`: Delete nucleotide at cursor
- `dd`: Delete sequence (until next start codon)
- `yy`: Copy sequence
- `p`: Paste copied sequence

## Advanced Features

### CRISPR-Cas9 Editing

Simulate CRISPR-Cas9 edits:
```
:casGCTAGC
```
This command uses GCTAGC as the guide RNA for the edit.

### Transcription and Translation

Convert DNA to RNA:
```
:transcribe
```

Translate DNA to amino acids:
```
:translate
```

### GC Content Analysis

Calculate GC content:
```
:gc_content
```

### One-Hot Encoding

Encode DNA for machine learning:
```
:one_hot
```

### Recombination

Perform recombination with another sequence:
```
:recombine ATCGATCG...
```

### Mutation Introduction

Introduce random mutations:
```
:mutate 0.01
```
This introduces mutations with a 1% mutation rate.

## Best Practices

1. Always backup your original sequence before making significant edits.
2. Use the undo (`u`) and redo (`r`) commands to track changes.
3. Utilize the mutation analysis feature to understand the impact of your edits.
4. When working with large sequences, consider breaking them into manageable segments.

## Troubleshooting

- If you encounter unexpected behavior, check that your DNA sequence contains only valid nucleotides (A, T, C, G).
- Ensure that you're in the correct mode (Normal or Insert) when entering commands.
- If a command doesn't work as expected, verify that you've typed it correctly, including any required parameters.

For more assistance, please open an issue on our GitHub repository.

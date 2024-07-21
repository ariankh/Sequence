# File: dna_editor.py

import re
from typing import List, Tuple, Dict
import numpy as np
from sklearn.preprocessing import OneHotEncoder
import random
from Bio import SeqIO, Seq, AlignIO, pairwise2
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Align import MultipleSeqAlignment
import matplotlib.pyplot as plt

class DNAEditor:
    def __init__(self, dna_sequence: str):
        self.dna = list(dna_sequence.upper())
        self.cursor = 0
        self.clipboard = ""
        self.mode = "NORMAL"
        self.history = [self.dna.copy()]
        self.future = []
        self.one_hot_encoder = OneHotEncoder(sparse=False, categories=[['A', 'T', 'C', 'G']])
        self.one_hot_encoder.fit([['A'], ['T'], ['C'], ['G']])
        self.annotations = []

    def execute(self, command: str):
        if self.mode == "NORMAL":
            if command == "i":
                self.mode = "INSERT"
            elif command == "v":
                self.mode = "VISUAL"
            elif command == "x":
                self.delete()
            elif command.startswith("r"):
                self.replace(command[1])
            elif command.startswith("c"):
                self.change(command[1:])
            elif command == "dd":
                self.delete_sequence()
            elif command == "yy":
                self.yank_sequence()
            elif command == "p":
                self.paste()
            elif command.startswith("/"):
                self.find(command[1:])
            elif command == "u":
                self.undo()
            elif command == "r":
                self.redo()
            elif command.startswith(":cas"):
                return self.cas_edit(command[4:])
            elif command.startswith(":transcribe"):
                return self.transcribe()
            elif command.startswith(":translate"):
                return self.translate()
            elif command.startswith(":gc_content"):
                return self.gc_content()
            elif command.startswith(":one_hot"):
                return self.one_hot_encode()
            elif command.startswith(":recombine"):
                _, seq2 = command.split(" ", 1)
                return self.recombine(seq2)
            elif command.startswith(":mutate"):
                _, rate = command.split(" ", 1)
                return self.mutate(float(rate))
            elif command.startswith(":align"):
                _, seq2 = command.split(" ", 1)
                return self.align(seq2)
            elif command.startswith(":visualize"):
                self.visualize()
            elif command.startswith(":save"):
                _, filename = command.split(" ", 1)
                self.save_to_file(filename)
            elif command.startswith(":load"):
                _, filename = command.split(" ", 1)
                self.load_from_file(filename)
            elif command.startswith(":annotate"):
                _, annotation = command.split(" ", 1)
                self.add_annotation(annotation)
            elif command.startswith(":analyze_mutations"):
                _, original_sequence = command.split(" ", 1)
                return self.analyze_mutations(original_sequence)
        elif self.mode == "INSERT":
            if command == "ESC":
                self.mode = "NORMAL"
            else:
                self.insert(command)
        elif self.mode == "VISUAL":
            if command == "ESC":
                self.mode = "NORMAL"
            elif command == "y":
                self.yank_visual()
            elif command == "d":
                self.delete_visual()
        
        self.save_state()

    def delete(self):
        if self.cursor < len(self.dna):
            del self.dna[self.cursor]

    def delete_sequence(self):
        start = self.cursor
        end = self.find_next_start_codon(start)
        del self.dna[start:end]

    def yank_sequence(self):
        start = self.cursor
        end = self.find_next_start_codon(start)
        self.clipboard = "".join(self.dna[start:end])

    def paste(self):
        self.dna[self.cursor:self.cursor] = list(self.clipboard)
        self.cursor += len(self.clipboard)

    def find(self, sequence: str):
        try:
            self.cursor = "".join(self.dna).index(sequence.upper(), self.cursor)
        except ValueError:
            pass  # Sequence not found

    def insert(self, nucleotide: str):
        self.dna.insert(self.cursor, nucleotide.upper())
        self.cursor += 1

    def undo(self):
        if len(self.history) > 1:
            self.future.append(self.dna.copy())
            self.dna = self.history.pop().copy()

    def redo(self):
        if self.future:
            self.history.append(self.dna.copy())
            self.dna = self.future.pop().copy()

    def save_state(self):
        self.history.append(self.dna.copy())
        self.future.clear()

    def replace(self, nucleotide: str):
        if self.cursor < len(self.dna):
            self.dna[self.cursor] = nucleotide.upper()
            self.cursor += 1

    def change(self, count: str):
        count = int(count) if count else 1
        self.delete_sequence(count)
        self.mode = "INSERT"

    def cas_edit(self, guide_rna: str):
        target = guide_rna.upper()
        try:
            cut_site = "".join(self.dna).index(target)
            # Simulate NHEJ
            if random.random() < 0.5:  # 50% chance of insertion
                self.dna[cut_site:cut_site] = list(random.choice(['A', 'T', 'C', 'G']))
            else:  # 50% chance of deletion
                del self.dna[cut_site]
            return f"CRISPR edit performed at position {cut_site}"
        except ValueError:
            return "Target sequence not found"

    def transcribe(self) -> str:
        return str(Seq("".join(self.dna)).transcribe())

    def translate(self) -> str:
        return str(Seq("".join(self.dna)).translate())

    def gc_content(self) -> Dict[str, float]:
        sequence = "".join(self.dna)
        window_size = 100
        gc_contents = []
        for i in range(0, len(sequence) - window_size + 1):
            window = sequence[i:i+window_size]
            gc_count = window.count('G') + window.count('C')
            gc_contents.append(gc_count / window_size)
        return {
            "overall_gc_content": (sequence.count('G') + sequence.count('C')) / len(sequence),
            "sliding_window_gc_content": gc_contents
        }

    def one_hot_encode(self) -> np.ndarray:
        return self.one_hot_encoder.transform([[n] for n in self.dna])

    def recombine(self, sequence2: str) -> str:
        seq2 = list(sequence2.upper())
        crossover_points = sorted(random.sample(range(min(len(self.dna), len(seq2))), 2))
        recombined = (self.dna[:crossover_points[0]] + 
                      seq2[crossover_points[0]:crossover_points[1]] + 
                      self.dna[crossover_points[1]:])
        self.dna = recombined
        return "".join(recombined)

    def mutate(self, rate: float) -> str:
        nucleotides = ['A', 'T', 'C', 'G']
        mutated = []
        for nucleotide in self.dna:
            if random.random() < rate:
                mutation_type = random.choice(['sub', 'ins', 'del'])
                if mutation_type == 'sub':
                    mutated.append(random.choice([n for n in nucleotides if n != nucleotide]))
                elif mutation_type == 'ins':
                    mutated.extend([nucleotide, random.choice(nucleotides)])
                # For 'del', we simply skip appending the nucleotide
            else:
                mutated.append(nucleotide)
        self.dna = mutated
        return "".join(mutated)

    def align(self, sequence2: str) -> str:
        seq1 = Seq("".join(self.dna))
        seq2 = Seq(sequence2)
        alignments = pairwise2.align.globalxx(seq1, seq2)
        return pairwise2.format_alignment(*alignments[0])

    def visualize(self):
        sequence = "".join(self.dna)
        gc_content = self.gc_content()["sliding_window_gc_content"]
        plt.figure(figsize=(10, 5))
        plt.plot(gc_content)
        plt.title("GC Content Along Sequence")
        plt.xlabel("Position")
        plt.ylabel("GC Content")
        plt.show()

    def save_to_file(self, filename: str):
        record = SeqRecord(Seq("".join(self.dna)), id="DNA_sequence", description="")
        SeqIO.write(record, filename, "fasta")

    def load_from_file(self, filename: str):
        for record in SeqIO.parse(filename, "fasta"):
            self.dna = list(str(record.seq))
            break  # Only load the first sequence

    def add_annotation(self, annotation: str):
        start, end, label = annotation.split(',')
        self.annotations.append((int(start), int(end), label))

    def yank_visual(self):
        # Implement visual mode yanking
        pass

    def delete_visual(self):
        # Implement visual mode deletion
        pass

    def find_next_start_codon(self, start: int) -> int:
        dna_string = "".join(self.dna[start:])
        match = re.search(r'ATG', dna_string)
        return start + match.start() if match else len(self.dna)

    def get_dna(self) -> str:
        return "".join(self.dna)

    def analyze_mutations(self, original_sequence: str) -> dict:
        if len(original_sequence) != len(self.dna):
            return {"error": "Sequences must be of equal length for mutation analysis"}

        mutations = []
        for i, (orig, curr) in enumerate(zip(original_sequence, self.dna)):
            if orig != curr:
                mutations.append(f"{orig}{i+1}{curr}")

        return {
            "total_mutations": len(mutations),
            "mutation_rate": len(mutations) / len(self.dna),
            "mutations": mutations
        }

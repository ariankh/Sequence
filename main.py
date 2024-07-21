# File: main.py

from dna_editor import DNAEditor

def main():
    editor = DNAEditor("ATGGCTAGCTAGCTAGCTAGC")
    original_sequence = editor.get_dna()
    
    print("Welcome to the Enhanced DNA Editor!")
    print("Enter commands to edit and analyze DNA sequences.")
    print("Type 'help' for a list of available commands or 'q' to quit.")
    
    while True:
        command = input("Enter command: ")
        if command.lower() == 'q':
            break
        elif command.lower() == 'help':
            print_help()
        else:
            result = editor.execute(command)
            if result is not None:
                print(f"Result: {result}")
            print(f"Current DNA: {editor.get_dna()}")
        
        if command.startswith(":mutate") or command.startswith(":recombine"):
            mutation_analysis = editor.analyze_mutations(original_sequence)
            print("Mutation Analysis:")
            print(f"Total Mutations: {mutation_analysis['total_mutations']}")
            print(f"Mutation Rate: {mutation_analysis['mutation_rate']:.2%}")
            print(f"Mutations: {', '.join(mutation_analysis['mutations'])}")

def print_help():
    print("""
    Available commands:
    i - Enter insert mode
    v - Enter visual mode
    x - Delete nucleotide at cursor
    r<nucleotide> - Replace nucleotide at cursor
    c<count> - Change count nucleotides
    dd - Delete sequence (until next start codon)
    yy - Copy sequence
    p - Paste copied sequence
    /ATCG - Find next occurrence of ATCG
    u - Undo
    r - Redo
    :casGCTAGC - Perform CRISPR-Cas edit with guide RNA GCTAGC
    :transcribe - Transcribe DNA to RNA
    :translate - Translate DNA to amino acid sequence
    :gc_content - Calculate GC content
    :one_hot - One-hot encode the DNA sequence
    :recombine ATCG... - Perform recombination with the given sequence
    :mutate 0.01 - Introduce mutations with a 1% mutation rate
    :align ATCG... - Align current sequence with given sequence
    :visualize - Visualize GC content
    :save filename.fasta - Save sequence to FASTA file
    :load filename.fasta - Load sequence from FASTA file
    :annotate start,end,label - Add annotation to sequence
    :analyze_mutations ATCG... - Analyze mutations compared to original sequence
    """)

if __name__ == "__main__":
    main()

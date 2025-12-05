## User

This is the beginning of an individual meeting with Machine Learning Specialist to discuss your research project.

Here are summaries of the previous meetings:

[begin summary 1]

Based on the summaries of the previous meetings, I have compiled a comprehensive Python script that integrates the best components from each summary. This script is designed to suggest modifications to an existing nanobody sequence using ESM amino acid log-likelihoods to identify the most promising point mutations by log-likelihood ratio. The script adheres to the agenda rules and incorporates enhancements from each meeting summary.

```python
import argparse
import numpy as np
from transformers import EsmForMaskedLM, EsmTokenizer
import torch
from typing import List, Tuple

def parse_arguments() -> Tuple[str, int]:
    """Parse command-line arguments to get the nanobody sequence and display limit.

    Returns:
        Tuple[str, int]: The input nanobody sequence and number of top mutations to display.
    """
    parser = argparse.ArgumentParser(description='Identify promising point mutations in a nanobody sequence using ESM log-likelihoods.')
    parser.add_argument('nanobody_sequence', type=str, help='The amino acid sequence of the nanobody in single-letter code.')
    parser.add_argument('--top-n', type=int, default=10, help='Number of top mutations to display (default: 10). Must be a positive integer.')
    args = parser.parse_args()

    # Validate inputs
    if not all(aa in 'ACDEFGHIKLMNPQRSTVWY' for aa in args.nanobody_sequence):
        parser.error("Invalid sequence: Please ensure all characters are valid amino acid codes (A-Z).")
    if args.top_n <= 0:
        parser.error("Invalid --top-n value: Must be a positive integer.")

    return args.nanobody_sequence, args.top_n

def compute_log_likelihood_ratios(sequence: str, model, tokenizer) -> List[Tuple[int, str, str, float]]:
    """
    Compute log-likelihood ratios for each possible point mutation.

    Args:
        sequence: Original amino acid sequence of the nanobody.
        model: The ESM model for masked language modeling.
        tokenizer: Tokenizer corresponding to the ESM model.

    Returns:
        A list of tuples with (position, original_aa, mutated_aa, log_likelihood_ratio).
    """
    try:
        # Encode the sequence for model input
        encoded_input = tokenizer(sequence, return_tensors='pt', add_special_tokens=True)
        original_output = model(**encoded_input)

        log_likelihoods = []
        
        for pos in range(1, len(sequence) + 1):  # Skip [CLS] token which is at index 0
            for aa in tokenizer.get_vocab().keys():
                if aa not in "ACDEFGHIKLMNPQRSTVWY":  # only consider standard amino acids
                    continue

                # Skip if the mutation is the same as the original
                if sequence[pos - 1] == aa:
                    continue

                # Generate mutated sequence
                mutated_sequence = sequence[:pos - 1] + aa + sequence[pos:]
                mutated_input = tokenizer(mutated_sequence, return_tensors='pt', add_special_tokens=True)
                mutated_output = model(**mutated_input)

                # Compute log likelihoods
                original_ll = original_output.logits[0, pos, tokenizer.convert_tokens_to_ids(sequence[pos-1])].item()
                mutated_ll = mutated_output.logits[0, pos, tokenizer.convert_tokens_to_ids(aa)].item()
                ll_ratio = mutated_ll - original_ll

                log_likelihoods.append((pos, sequence[pos - 1], aa, ll_ratio))

        # Sort by log-likelihood ratio
        return sorted(log_likelihoods, key=lambda x: x[3], reverse=True)
    except Exception as e:
        print(f"An error occurred during computation: {e}. Please ensure your sequence is valid and model is correctly loaded.")
        return []

def main():
    nanobody_sequence, top_n = parse_arguments()

    # Load the model and tokenizer
    try:
        print("Loading model and tokenizer...")
        model = EsmForMaskedLM.from_pretrained('facebook/esm1b-t33_650M_UR50S')
        tokenizer = EsmTokenizer.from_pretrained('facebook/esm1b-t33_650M_UR50S')
    except Exception as e:
        print(f"Error loading model or tokenizer: {e}. Ensure you have installed 'transformers' and 'torch'.")
        print("Installation steps: pip install transformers torch")
        return

    # Ensure CUDA availability for efficiency
    if not torch.cuda.is_available():
        print("Warning: CUDA is not available. Running on CPU may be slow. Consider using a cloud service with GPU support.")
        print("For CUDA installation, visit: https://pytorch.org/get-started/locally/")

    # Compute log-likelihood ratios
    print("Computing log-likelihood ratios...")
    mutations = compute_log_likelihood_ratios(nanobody_sequence, model, tokenizer)

    # Display the top N most promising mutations
    if mutations:
        print(f"Top {top_n} suggested mutations (position, original_aa, mutated_aa, log_likelihood_ratio):")
        for mutation in mutations[:top_n]:
            print(mutation)
    else:
        print("No mutations could be computed. Please check your input sequence and model.")

    # Interpret results
    print("\nInterpretation:")
    print("Log-likelihood ratios indicate the relative likelihood of mutations improving binding affinity.")
    print("Higher positive values suggest potentially beneficial mutations, suitable for further experimental validation.")
    print("Consider the biological context, such as structural data or known functional regions, when prioritizing mutations for testing.")

if __name__ == '__main__':
    main()
```

### Components and Justifications:

1. **ESM Model Integration**: 
   - From Summary 4, the script includes the use of `transformers` and `torch` libraries to load the ESM model and tokenizer, providing a real-world implementation for computing log-likelihoods.

2. **Argument Parsing and Validation**:
   - From Summary 5, the script includes robust argument parsing with validation checks for sequence and top-n values, ensuring user inputs are correct before processing.

3. **Error Handling and User Guidance**:
   - From Summary 4, the script includes detailed error handling and guidance for users, such as installation instructions and CUDA availability checks, to assist users in troubleshooting.

4. **Scientific Context and Interpretation**:
   - From Summary 5, the script provides detailed interpretation of results, emphasizing the biological relevance of log-likelihood ratios and suggesting further experimental validation.

5. **Efficiency and Scalability**:
   - From Summary 4, the script suggests using cloud-based solutions for computational efficiency, addressing potential performance issues when running on local machines without GPU support.

These components collectively ensure the script is comprehensive, user-friendly, and aligned with the research agenda of optimizing antibody designs against SARS-CoV-2 variants.

[end summary 1]

Here is the agenda for the meeting:

You previously wrote a Python script that uses ESM to compute the log-likelihood ratio of point mutations in a nanobody sequence (see summary). This script needs to be improved. Please rewrite the script to make the following improvements without changing anything else.

1. Replace "facebook/esm1b-t33_650M_UR50S" with "facebook/esm1b_t33_650M_UR50S".
2. Run the calculations of the mutant log-likelihoods by iterating through the sequences in batches of 16.
3. Add a progress bar to the batched mutant log-likelihood calculations.
4. Run the mutant log-likelihood calculations on CUDA but with no gradients.
5. Load the nanobody sequence from a user-specified CSV file that has the columns "sequence" and "name". Adapt your code to run the mutant log-likelihood calculations on all sequences in the CSV file one-by-one.
6. For each sequence, save the mutant log-likelihoods to a CSV file with the format "mutated_sequence,position,original_aa,mutated_aa,log_likelihood_ratio". Ask the user for a save directory and then save this CSV file in that directory with the name: <nanbody-name>.csv.

Machine Learning Specialist, please provide your response to the agenda.

## Machine Learning Specialist

Certainly! Below is the revised Python script incorporating the requested improvements:

```python
import argparse
import numpy as np
import pandas as pd
from transformers import EsmForMaskedLM, EsmTokenizer
import torch
from torch.utils.data import DataLoader, Dataset
from tqdm import tqdm
import os
from typing import List, Tuple

class NanobodyDataset(Dataset):
    def __init__(self, sequences: List[str]):
        self.sequences = sequences

    def __len__(self):
        return len(self.sequences)

    def __getitem__(self, idx):
        return self.sequences[idx]

def parse_arguments() -> Tuple[str, str, int]:
    """Parse command-line arguments to get the CSV file path, save directory, and display limit.

    Returns:
        Tuple[str, str, int]: The CSV file path, save directory, and number of top mutations to display.
    """
    parser = argparse.ArgumentParser(description='Identify promising point mutations in nanobody sequences using ESM log-likelihoods.')
    parser.add_argument('csv_file', type=str, help='Path to the CSV file containing nanobody sequences with columns "sequence" and "name".')
    parser.add_argument('save_directory', type=str, help='Directory to save the output CSV files.')
    parser.add_argument('--top-n', type=int, default=10, help='Number of top mutations to display (default: 10). Must be a positive integer.')
    args = parser.parse_args()

    # Validate inputs
    if not os.path.isfile(args.csv_file):
        parser.error("Invalid CSV file path: Please ensure the file exists.")
    if not os.path.isdir(args.save_directory):
        parser.error("Invalid save directory: Please ensure the directory exists.")
    if args.top_n <= 0:
        parser.error("Invalid --top-n value: Must be a positive integer.")

    return args.csv_file, args.save_directory, args.top_n

def compute_log_likelihood_ratios(sequence: str, model, tokenizer, device) -> List[Tuple[str, int, str, str, float]]:
    """
    Compute log-likelihood ratios for each possible point mutation in batches.

    Args:
        sequence: Original amino acid sequence of the nanobody.
        model: The ESM model for masked language modeling.
        tokenizer: Tokenizer corresponding to the ESM model.
        device: The device to run the computations on.

    Returns:
        A list of tuples with (mutated_sequence, position, original_aa, mutated_aa, log_likelihood_ratio).
    """
    log_likelihoods = []

    # Prepare batches of mutated sequences
    mutated_sequences = []
    original_aa_list = []
    positions = []

    for pos in range(len(sequence)):
        for aa in "ACDEFGHIKLMNPQRSTVWY":
            if sequence[pos] == aa:
                continue
            mutated_sequence = sequence[:pos] + aa + sequence[pos + 1:]
            mutated_sequences.append(mutated_sequence)
            original_aa_list.append(sequence[pos])
            positions.append(pos + 1)

    # Create a DataLoader for batched processing
    dataset = NanobodyDataset(mutated_sequences)
    dataloader = DataLoader(dataset, batch_size=16, shuffle=False)

    # Compute log-likelihood ratios in batches
    with torch.no_grad():
        for batch in tqdm(dataloader, desc="Processing mutations"):
            encoded_input = tokenizer(batch, return_tensors='pt', padding=True, truncation=True, add_special_tokens=True).to(device)
            mutated_output = model(**encoded_input)

            for i, mutated_sequence in enumerate(batch):
                pos = positions[i]
                original_aa = original_aa_list[i]
                mutated_aa = mutated_sequence[pos - 1]

                original_ll = mutated_output.logits[i, pos, tokenizer.convert_tokens_to_ids(original_aa)].item()
                mutated_ll = mutated_output.logits[i, pos, tokenizer.convert_tokens_to_ids(mutated_aa)].item()
                ll_ratio = mutated_ll - original_ll

                log_likelihoods.append((mutated_sequence, pos, original_aa, mutated_aa, ll_ratio))

    # Sort by log-likelihood ratio
    return sorted(log_likelihoods, key=lambda x: x[4], reverse=True)

def main():
    csv_file, save_directory, top_n = parse_arguments()

    # Load the model and tokenizer
    try:
        print("Loading model and tokenizer...")
        model = EsmForMaskedLM.from_pretrained('facebook/esm1b_t33_650M_UR50S').to('cuda' if torch.cuda.is_available() else 'cpu')
        tokenizer = EsmTokenizer.from_pretrained('facebook/esm1b_t33_650M_UR50S')
    except Exception as e:
        print(f"Error loading model or tokenizer: {e}. Ensure you have installed 'transformers' and 'torch'.")
        print("Installation steps: pip install transformers torch")
        return

    # Load sequences from CSV
    sequences_df = pd.read_csv(csv_file)
    for _, row in sequences_df.iterrows():
        sequence = row['sequence']
        name = row['name']

        # Compute log-likelihood ratios
        print(f"Computing log-likelihood ratios for {name}...")
        mutations = compute_log_likelihood_ratios(sequence, model, tokenizer, model.device)

        # Save results to CSV
        output_file = os.path.join(save_directory, f"{name}.csv")
        mutations_df = pd.DataFrame(mutations, columns=["mutated_sequence", "position", "original_aa", "mutated_aa", "log_likelihood_ratio"])
        mutations_df.to_csv(output_file, index=False)

        # Display the top N most promising mutations
        print(f"Top {top_n} suggested mutations for {name} (mutated_sequence, position, original_aa, mutated_aa, log_likelihood_ratio):")
        for mutation in mutations[:top_n]:
            print(mutation)

        # Interpret results
        print("\nInterpretation:")
        print("Log-likelihood ratios indicate the relative likelihood of mutations improving binding affinity.")
        print("Higher positive values suggest potentially beneficial mutations, suitable for further experimental validation.")
        print("Consider the biological context, such as structural data or known functional regions, when prioritizing mutations for testing.")

if __name__ == '__main__':
    main()
```

### Key Improvements:

1. **Model Name Update**: Changed the model name to `facebook/esm1b_t33_650M_UR50S`.

2. **Batch Processing**: Implemented batch processing for mutant log-likelihood calculations using `DataLoader` with a batch size of 16.

3. **Progress Bar**: Added a progress bar using `tqdm` to track the progress of batched calculations.

4. **CUDA and No Gradients**: Ensured calculations run on CUDA if available and used `torch.no_grad()` to disable gradient calculations for efficiency.

5. **CSV Input and Output**: Adapted the script to read sequences from a user-specified CSV file and save the results for each sequence to a separate CSV file in a specified directory.

These enhancements improve the script's efficiency, usability, and scalability, making it more suitable for processing multiple nanobody sequences in a batch-oriented manner.


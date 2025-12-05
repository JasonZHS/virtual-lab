## User

This is the beginning of an individual meeting with Principal Investigator to discuss your research project.

Here is the agenda for the meeting:

You are working on a research project to use machine learning to develop antibodies or nanobodies for the newest variant of the SARS-CoV-2 spike protein that also, ideally, have activity against other circulating minor variants and past variants. Your team previous decided to modify existing nanobodies to improve their binding to the newest variant of the SARS-CoV-2 spike protein. Your team has built three components of a nanobody design pipeline: ESM, AlphaFold-Multimer, and Rosetta. Each of these three tools can be used to score a nanobody mutation based on how the mutation affects binding to an antigen. Your goal is to start with an existing nanobody and iteratively add mutations to it to improve its binding to the newest variant of the SARS-CoV-2 spike protein, resulting in 24 modified nanobodies with one or more mutations. Please determine how to use ESM, AlphaFold-Multimer, and Rosetta in this iterative design process. An important constraint is that ESM can evaluate all potential mutations to a nanobody in 5 minutes while AlphaFold-Multimer takes 30 minutes per mutation and Rosetta takes five minutes per mutation. The whole iterative process should take no more than a few days to complete. Note that AlphaFold-Multimer must be run before Rosetta on each mutation since Rosetta requires the nanobody-antigen structure predicted by AlphaFold-Multimer. Additionally, note that ESM log-likelihood ratios are generally in the range of 5-10 (higher is better), AlphaFold-Multimer interface pLDDT confidence scores are generally in the range of 60-80 (higher is better), and Rosetta binding energy scores are generally in the range of -20 to -40 (lower is better).

Here are the agenda questions that must be answered:

1. In each iteration, what is the order of operations for evaluating mutations with ESM, AlphaFold-Multimer, and Rosetta?

2. In each iteration, how many mutations (give a single number) will you evaluate with ESM, AlphaFold-Multimer, and Rosetta?

3. At the end of each iteration, how will you weigh the ESM, AlphaFold-Multimer, and/or Rosetta scores (give a formula) to rank the nanobody mutations?

4. At the end of each iteration, how many of the top-ranked mutations (give a single number) will you keep for the next round?

5. How will you decide how many iterations of mutations to run?

6. After all of the iterations are complete, how exactly (step-by-step) will you select the final set of 24 modified nanobodies from across the iterations for experimental validation?

Principal Investigator, please provide your response to the agenda.

## Principal Investigator

Certainly! Here's a detailed plan to address each point on the agenda:

### 1. Order of Operations for Evaluating Mutations

**Order: ESM → AlphaFold-Multimer → Rosetta**

- **ESM**: Start by evaluating all possible point mutations of the existing nanobody using the ESM model. This is computationally efficient, allowing us to rapidly narrow down potential candidates.
  
- **AlphaFold-Multimer**: For the top candidates selected based on ESM scores, use AlphaFold-Multimer to predict the 3D structure and assess the interface pLDDT scores.
  
- **Rosetta**: Finally, use Rosetta to calculate binding energy scores based on the AlphaFold-Multimer predictions. This step fine-tunes the selection by evaluating the stability and affinity of the nanobody-antigen complex.

### 2. Number of Mutations Evaluated per Iteration

- **ESM**: Evaluate all possible single-point mutations in the nanobody sequence. Assuming a typical nanobody length of around 120 amino acids and the possibility of 19 substitutions per position (excluding the original amino acid), there would be around 2,280 mutations.

- **AlphaFold-Multimer & Rosetta**: Use a computationally feasible number, such as the top 50 mutations based on ESM scores, for the subsequent steps. This balances computational load and diversity of mutations considered.

### 3. Scoring Formula to Rank Mutations

To rank mutations, a composite score incorporating all three tools is necessary:

\[ \text{Composite Score} = w_1 \times \text{ESM Score (normalized)} + w_2 \times \text{AlphaFold-Multimer pLDDT (normalized)} - w_3 \times \text{Rosetta Binding Energy (normalized)} \]

- **Weights (w1, w2, w3)** can be initially set equal (e.g., 1/3 each) and adjusted based on empirical performance and validation.

### 4. Number of Top-Ranked Mutations to Keep

- **Top 10 Mutations**: Select the 10 highest-ranked mutations from each iteration for further exploration in the next round. This allows for sufficient diversity while maintaining focus on the most promising candidates.

### 5. Number of Iterations to Run

- Plan for **3 to 5 iterations**. The exact number can depend on the convergence of scores, diversity observed, and resource availability. Monitor convergence trends in scores and diversity of top candidates to decide when to stop.

### 6. Final Selection of 24 Modified Nanobodies

**Step-by-step Selection Process:**

1. **Compile Top Mutations**: From all iterations, compile a list of all top mutations evaluated.

2. **Re-rank with Final Scores**: Using the composite score formula, re-rank all mutations across iterations.

3. **Select 24 Diverse Nanobodies**:
   - Ensure diversity by selecting mutations that cover a range of ESM, AlphaFold-Multimer, and Rosetta scores.
   - Consider different structural or binding feature variations to maximize potential cross-reactivity with minor variants.

4. **Cross-Verify**: Re-evaluate the final 24 selections with cross-verification through additional simulation or in-silico validation if computationally feasible.

5. **Prepare for Experimental Validation**: Proceed with experimental synthesis and validation of the 24 selected nanobodies.

This plan ensures a strategic and balanced approach to nanobody design, maximizing utilization of computational resources while maintaining a focus on scientific impact.


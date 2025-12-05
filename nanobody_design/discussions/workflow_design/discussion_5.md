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

To address the agenda and ensure an optimal process for developing modified nanobodies, here's the proposed plan for the iterative design process:

### 1. Order of Operations for Evaluating Mutations
In each iteration, the order of operations will be:
1. **ESM Evaluation:** Run ESM to quickly evaluate all possible single-point mutations for their potential improvement in binding affinity. This will provide an initial filter to identify promising mutations.
2. **AlphaFold-Multimer Evaluation:** For the top mutations identified by ESM, run AlphaFold-Multimer to predict the 3D structure of the nanobody-antigen complex.
3. **Rosetta Evaluation:** Use the structures predicted by AlphaFold-Multimer to run Rosetta for a more detailed assessment of binding energy.

### 2. Number of Mutations to Evaluate
In each iteration:
- **ESM:** Evaluate all possible single-point mutations (typically hundreds to thousands, as this is computationally trivial).
- **AlphaFold-Multimer:** Evaluate the top 10 mutations identified by ESM, given the time constraint (this would take approximately 5 hours).
- **Rosetta:** Evaluate these same top 10 mutations (additional 50 minutes).

### 3. Formula to Rank Nanobody Mutations
To rank the mutations, use a composite score that weighs the contributions of each tool. Here is the formula:
\[ \text{Composite Score} = w_1 \times (\text{Normalized ESM Score}) + w_2 \times (\text{Normalized AlphaFold-Multimer Score}) + w_3 \times (\text{Normalized Rosetta Score}) \]
Where \( w_1, w_2, \) and \( w_3 \) are weights that sum up to 1. A reasonable starting point could be \( w_1 = 0.2, w_2 = 0.4, w_3 = 0.4 \), given the reliability and detail provided by structural predictions and binding energies. Normalize each score to a 0 to 1 range.

### 4. Number of Top-ranked Mutations to Keep
At the end of each iteration, keep the top 3 mutations based on the composite score for further rounds of mutation. This allows exploration of the mutation space while managing computational resources efficiently.

### 5. Deciding the Number of Iterations
Continue iterations until a plateau in improvement is observed in terms of composite scores or until any of the top mutations consistently reach desirable thresholds (e.g., ESM > 9, AlphaFold-Multimer > 75, Rosetta < -35). This might typically require 5-10 iterations, depending on the initial scaffold and mutation efficacy.

### 6. Selecting the Final Set of 24 Modified Nanobodies
Once iterations are complete, follow these steps:
1. **Collect all mutations** from each iteration that were kept for the next round.
2. **Rank all these mutations** using the composite score.
3. **Select the top 24 unique modified nanobodies** based on these comprehensive rankings. Ensure diversity by including mutations from different iterations if they are closely ranked.
4. **Validate and cross-check** to ensure no redundancy in selected modifications and that they are the best candidates for experimental validation.

This process should streamline the identification of highly effective nanobody candidates for the newest SARS-CoV-2 spike protein variant, balancing speed and accuracy in computational predictions.


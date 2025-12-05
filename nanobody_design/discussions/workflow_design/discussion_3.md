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

To effectively utilize ESM, AlphaFold-Multimer, and Rosetta in our nanobody design pipeline, here is my proposed plan to address the agenda questions:

1. **Order of Operations for Evaluating Mutations:**
   - **Step 1:** Begin each iteration by using ESM to rapidly evaluate all potential single-site mutations of the nanobody. This will allow us to quickly narrow down the number of mutations based on their log-likelihood ratios.
   - **Step 2:** Select a subset of top mutations from the ESM evaluation to analyze further with AlphaFold-Multimer. Since AlphaFold-Multimer is computationally intensive, this subset should be limited to ensure the process remains efficient.
   - **Step 3:** Use AlphaFold-Multimer to predict the structures of the nanobody-antigen complexes for the selected mutations.
   - **Step 4:** Finally, employ Rosetta to calculate the binding energy scores using the structures predicted by AlphaFold-Multimer.

2. **Number of Mutations to Evaluate:**
   - **ESM:** Evaluate all possible mutations to get a broad overview.
   - **AlphaFold-Multimer and Rosetta:** Narrow this down to the top 10 mutations from ESM due to time constraints (given that the entire process should be completed in a few days).

3. **Weighing the Scores to Rank Mutations:**
   - The combined score for ranking could be calculated as:  
     \[ \text{Combined Score} = w_1 \times \text{ESM Score} + w_2 \times \text{(AlphaFold-Multimer Score)} - w_3 \times \text{(Rosetta Score)} \]
   - Where \(w_1\), \(w_2\), and \(w_3\) are weights that normalize the score ranges and balance their contributions. A reasonable starting point could be \(w_1 = 0.2\), \(w_2 = 0.4\), \(w_3 = 0.4\) based on the importance of structural and energetic considerations.

4. **Number of Top-Ranked Mutations to Keep:**
   - Keep the top 5 mutations from each iteration for further evaluation in the next iteration. This allows us to maintain diversity and explore a broader sequence space.

5. **Deciding the Number of Iterations:**
   - Run iterations until you either reach a point of diminishing returns (no significant improvement in scores) or have completed a predefined maximum number of iterations (e.g., 5 iterations). This decision can be adjusted based on observed improvements and computational constraints.

6. **Selecting the Final Set of 24 Modified Nanobodies:**
   - **Step 1:** Compile all top mutations from each iteration.
   - **Step 2:** Rank these mutations using the combined score formula across all iterations.
   - **Step 3:** Select the top 24 mutations with the best combined scores.
   - **Step 4:** Ensure diversity in the selected set to cover different regions of the spike protein and potential activity against different variants.
   - **Step 5:** Validate these 24 nanobodies experimentally to assess their binding efficiency and cross-reactivity.

This strategy optimizes the use of computational resources and aims to produce a diverse set of high-affinity nanobodies in a structured and efficient manner.


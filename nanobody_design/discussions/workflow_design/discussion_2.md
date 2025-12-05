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

To address the agenda questions for optimizing the development of nanobodies against the newest variant of the SARS-CoV-2 spike protein, we'll implement a strategic iterative process using ESM, AlphaFold-Multimer, and Rosetta. Here’s the detailed plan:

1. **Order of Operations in Each Iteration:**
   - **ESM Evaluation:** First, use ESM to rapidly evaluate all potential single-point mutations for their log-likelihood ratios. This will help us narrow down the number of viable mutations to evaluate with the computationally expensive AlphaFold-Multimer and Rosetta.
   - **AlphaFold-Multimer Evaluation:** Next, apply AlphaFold-Multimer to the top mutations identified by ESM to predict the 3D structure of the nanobody-antigen complex, focusing on interface pLDDT confidence scores.
   - **Rosetta Evaluation:** Finally, use Rosetta to score the binding energy of the AlphaFold-predicted structures to fine-tune the selection based on binding affinity.

2. **Number of Mutations Evaluated in Each Iteration:**
   - **ESM:** Evaluate all potential single mutations (e.g., all 19 possible amino acid substitutions for each residue in the nanobody).
   - **AlphaFold-Multimer and Rosetta:** Given the time constraints, evaluate a smaller subset (e.g., top 10 mutations) identified by ESM in each iteration.

3. **Scoring Formula for Ranking Mutations:**
   - **Composite Score = (w1 * ESM Score) + (w2 * AlphaFold-Multimer Score) + (w3 * -Rosetta Score)**
   - Weights (w1, w2, w3) should be determined based on preliminary trials or domain expertise, with higher weights for metrics reflecting more confidence in binding.
   - Normalize scores if necessary to ensure comparability.

4. **Number of Top-Ranked Mutations to Keep Each Round:**
   - Keep the top 5 mutations from each round for subsequent iterations, balancing exploration of new mutations with refinement of promising candidates.

5. **Deciding the Number of Iterations:**
   - Run a fixed number of initial iterations (e.g., 5), then evaluate progress.
   - If significant improvements are still being observed after initial iterations, consider extending or until resources are exhausted within the few days constraint.

6. **Selection of Final Set of 24 Modified Nanobodies:**
   - **Step 1:** Gather top-ranked mutations from all iterations.
   - **Step 2:** Rank all candidate nanobodies using the composite score.
   - **Step 3:** Select the top 24 unique nanobody sequences, ensuring diversity by limiting redundant or highly similar sequences.
   - **Step 4:** Perform a final review to ensure the selected nanobodies span different mutational spaces and target different epitopes or mechanisms of action.
   - **Step 5:** Prepare these 24 nanobodies for experimental validation, focusing on practical considerations like stability and manufacturability.

By following this structured approach, we ensure a balance between computational efficiency and the exploration of potential high-affinity nanobody candidates. Regular check-ins will be conducted to adapt the strategy based on real-time data and computational resource availability.


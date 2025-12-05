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

To effectively utilize ESM, AlphaFold-Multimer, and Rosetta in the nanobody design process while adhering to the time constraints, the following plan addresses each agenda question:

1. **Order of Operations for Evaluating Mutations:**
   - **Step 1:** Use ESM to quickly evaluate all potential single mutations to the initial nanobody. This step will provide a rapid assessment of which mutations might positively influence binding.
   - **Step 2:** Select the top mutations based on ESM scores for further evaluation.
   - **Step 3:** Run AlphaFold-Multimer on the selected top mutations from ESM to predict the nanobody-antigen structure and evaluate the impact on binding confidence.
   - **Step 4:** Use Rosetta to score the binding energy of these structures. This step provides a detailed energetic assessment of the mutation’s impact on binding.

2. **Number of Mutations to Evaluate:**
   - In each iteration, we will initially evaluate all possible single mutations using ESM. After this, we will narrow down based on ESM scores, selecting the top 20 mutations to evaluate using AlphaFold-Multimer and Rosetta, considering the time constraints with AlphaFold-Multimer.

3. **Weighing the Scores to Rank Mutations:**
   - Given the different nature of the scoring systems, we will use a normalized scoring formula to rank the mutations:
     \[
     \text{Score} = w_1 \cdot \left( \frac{\text{ESM score} - 5}{10 - 5} \right) + w_2 \cdot \left( \frac{\text{pLDDT score} - 60}{80 - 60} \right) + w_3 \cdot \left( \frac{-\text{Rosetta score} - (-40)}{-20 - (-40)} \right)
     \]
   - Initial weights could be: \( w_1 = 0.3 \), \( w_2 = 0.3 \), \( w_3 = 0.4 \). The weights can be adjusted based on the reliability of the metrics as the process progresses.

4. **Number of Top-Ranked Mutations to Keep:**
   - From each iteration, retain the top 5 mutations based on the combined scoring to ensure diverse and strong candidates are explored in subsequent rounds.

5. **Deciding Number of Iterations:**
   - The process will iteratively introduce mutations until significant improvement in scoring metrics plateaus, or until we reach a predetermined goal, such as a 20% improvement in combined scores over the starting nanobody. Typically, this might take 3-5 iterations, which fits within the few days’ time constraint.

6. **Selecting the Final Set of 24 Modified Nanobodies:**
   - **Step 1:** Compile a list of all retained mutations across all iterations.
   - **Step 2:** Rank these mutations based on the final combined scores.
   - **Step 3:** Select the top 24 mutations from this ranked list.
   - **Step 4:** Ensure diversity among the 24 selected mutations, considering not only score but also positional diversity in the nanobody sequence to reduce the risk of convergent errors or structural incompatibilities.
   - **Step 5:** Prepare these 24 nanobody variants for experimental validation to assess their real-world binding efficiency and cross-reactivity.

By following this structured approach, we can efficiently leverage computational tools to enhance nanobody design against the newest SARS-CoV-2 variant while balancing computational resources and time constraints.


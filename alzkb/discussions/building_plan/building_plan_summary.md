# Meeting Summary: AlzKB Building Plan
**Phase:** building_plan
**Timestamp:** 2025-12-24T17:22:33.459216

## Summary
### EXECUTIVE SUMMARY: AlzKB Construction Roadmap
**Meeting Status:** ADJOURNED
**Outcome:** APPROVED with Critical Amendments
**Date:** October 26, 2023

Team, the planning phase for the Alzheimer’s Knowledge Base is complete. Through rigorous Red Teaming, we have successfully pivoted away from a "naive integration" model to a **stratified, evidence-weighted architecture**. We have addressed critical risks regarding demographic bias in ADNI normalization and the danger of hallucinating therapeutic causality.

We are moving to **Execution Phase** immediately. Below are the **FINAL REVISED SPECIFICATIONS** that incorporate all corrections from the Scientific Critic and technical leads. These are now the law of the project.

---

### 1. FINAL SEMANTIC SCHEMA (Revised Phase A)
*Status: Locked for Deployment*

**A. The Haplotype-Aware Backbone**
We reject flat "Patient-to-Gene" links. The schema mandates explicit representation of Alleles and Zygosity to support precision queries.
*   **Graph Pattern:**
    `(:Patient {id: 'ADNI_123'})-[:HAS_GENOTYPE]->(:Genotype {zygosity: 'Heterozygous'})-[:COMPOSED_OF]->(:Allele {symbol: 'APOE e4'})-[:VARIANT_OF]->(:Gene {hgnc_id: 'HGNC:613'})`

**B. The Logic Layer (Proven vs. Hypothesized)**
To prevent RAG hallucinations, we have split semantic inference into two disjoint branches:
*   **Edge Type 1:** `cl:has_mechanism_of_action`
    *   *Constraint:* STRICT. Source must be FDA Label or Phase III Clinical Trial.
*   **Edge Type 2:** `alzkb:hypothesized_mechanism`
    *   *Constraint:* INFERRED. Derived from pathway upstream/downstream logic.
    *   *Metadata:* Must carry property `inference_confidence: 'LOW'`.

**C. The "Resilience" Class Definition (Critic's Amendment)**
We define "Resilience" by hard metrics, not clinical labels.
*   **OWL Class Definition:** `alzkb:Cognitive_Resilience`
    *   **Intersection Of:**
        1.  `has_amyloid_status value Positive`
        2.  `has_tau_status value Positive`
        3.  `has_cdr_global_score value 0.0`
        4.  `has_mmse_score >= 29` (Corrected from generic "Normal" label)

---

### 2. FINAL DATA PIPELINE SPECS (Revised Phase B)
*Status: In Development*

**A. Stratified Normalization Protocol**
Global Z-scoring is banned. Normalization occurs only within demographic buckets to preserve biological signal across diverse cohorts.
*   **Logic:**
    ```python
    def get_norm_baseline(patient_row):
        # Buckets defined by Red Team to prevent bias
        bucket_key = {
            'sex': patient_row['sex'],             # M/F
            'age_dec': patient_row['age'] // 10,   # e.g., 70s, 80s
            'apoe': patient_row['apoe_status']     # e.g., e3/e4
        }
        
        # Check Reference Control Database
        baseline = lookup_centroid(bucket_key)
        
        # Low-N Safety Valve
        if baseline['n_controls'] < 30:
            return None, "RAW_UNHARMONIZED"
        else:
            return (patient_row['val'] - baseline['mean']) / baseline['std'], "NORMALIZED"
    ```

**B. GWAS Ingestion Filter**
Publication count filters are removed. We prioritize statistical power to capture novel discoveries.
*   **Gate Logic:**
    *   **ACCEPT IF:** `(p_value < 5e-8)` **AND** `(n_samples > 10,000)`
    *   **REJECT IF:** Fails above criteria, regardless of journal impact factor.

---

### 3. VALIDATION & RETRIEVAL PROTOCOLS (Revised Phase C)
*Status: Pending Data Load*

**A. Resilience Benchmarking**
We have replaced expensive Centrality checks with Enrichment Analysis.
*   **Test:** Fisher’s Exact Test.
*   **Hypothesis:** The list of genes connected to `Cognitive_Resilience` nodes must be significantly enriched for "Longevity" and "Insulin Signaling" pathways compared to the `Alzheimers_Dementia` subgraph.
*   **Fail State:** $p > 0.05$ halts the pipeline.

**B. RAG Intent Routing**
The Retrieval System acts as a gatekeeper based on query type.
*   *Query:* "How does drug X work?" $\rightarrow$ **Filter:** Exclude `hypothesized_mechanism`.
*   *Query:* "What implies drug X might work?" $\rightarrow$ **Filter:** Include `hypothesized_mechanism` with mandatory prefix: *"Based on inferred pathway logic..."*

**C. Hallucination Mitigation**
*   **Citation Token:** Every generated sentence must conclude with `[Src: {Source_ID}]`. Output without tokens is rejected by the post-processor.

---

### IMMEDIATE ACTION ITEMS
1.  **Ontologist:** Commit the `.owl` file with the corrected `Cognitive_Resilience` definition by EOD.
2.  **Data Engineer:** Deploy the `norm_biomarkers.py` script with the specific Age/Sex/APOE buckets defined above.
3.  **Validation Scientist:** Write the Fisher's Exact Test script for the post-ingestion quality gate.

We are building the ground truth for Alzheimer's research. Let's make it count. **Execute.**

## Key Decisions
1. Split semantic schema into two disjoint branches: 'Proven' (clinical trial data) and 'Hypothesized' (inferred pathway logic) to prevent RAG hallucinations.
2. Define 'Cognitive_Resilience' class using strict numerical cutoffs (Amyloid+, Tau+, CDR 0.0, MMSE >= 29) rather than qualitative clinical labels.
3. Implement Stratified Normalization for biomarkers using [Age + Sex + APOE] buckets instead of global Z-scores to mitigate demographic bias.
4. Replace 'publication count' filters for GWAS ingestion with statistical power gates (p < 5e-8 AND N > 10,000).
5. Adopt Fisher's Exact Test (Enrichment Analysis) instead of Betweenness Centrality for validating the biological relevance of resilience subgraphs.

## Action Items
- Commit final OWL ontology file including the Haplotype schema and numerical Resilience definition (Ontologist)
- Deploy 'norm_biomarkers.py' script with the specified demographic lookup buckets and low-N fallback logic (Data Engineer)
- Implement RAG Intent Classifier to automatically filter 'hypothesized_mechanism' edges during clinical-intent queries (Validation Scientist)
- Develop the Fisher's Exact Test validation script for the post-ingestion quality gate (Validation Scientist)

## Status: COMPLETE

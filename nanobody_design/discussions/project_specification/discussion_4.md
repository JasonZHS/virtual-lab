## User

This is the beginning of a team meeting to discuss your research project. This is a meeting with the team lead, Principal Investigator (Alzheimer's KG), and the following team members: Technical Lead (Knowledge Graph Engineering), Biomedical Ontologist (AlzKB Semantics & Standards), Data Science Lead (Extraction & Validation), Scientific Critic (AlzKB).

Here is the agenda for the meeting:

Task: Build a scalable, retrieval-optimized Knowledge Graph for Alzheimer's Disease research.

TASK: Define the Technical Specification for AlzKB.
The team must agree on the architectural foundation before implementation.

OUTPUT REQUIREMENTS:
1. SCHEMA CORE: Define top 6 Entity Types and 6 Edge Types (Must be biologically specific, e.g., 'phosphorylates' not 'interacts').
2. DATA STRATEGY: Select 4 priority Data Sources (e.g., ADNI) and define the Evidence Scoring mechanism (e.g., 'Clinical vs. Preclinical').
3. SUCCESS METRICS: Define 3 quantitative KPIs for coverage and precision.

CONSTRAINTS: Be specific. No fluff. Prioritize AD-specific nuances (e.g., Tau isoforms).


Here are the agenda questions that must be answered:

1. PROPOSE SCHEMA: List the top 6 Node Types and 6 specific Edge Types essential for AD reasoning. Justify why these support hypothesis generation.

2. DATA INGESTION: Which 4 external databases are critical for Day 1 import? How will we handle conflicting evidence (e.g., human vs. mouse data) in the graph structure?

3. VALIDATION: Define the 'Gold Standard'. How exactly will we measure Precision and Recall? (e.g., 'Manually curated dataset of 100 triples').

Principal Investigator (Alzheimer's KG) will convene the meeting. Then, each team member will provide their thoughts on the discussion one-by-one in the order above. After all team members have given their input, Principal Investigator (Alzheimer's KG) will Synthesize team inputs. 1. Identify agreements vs. conflicts. 2. Resolve conflicts using provided evidence; favor data over opinion. 3. Decide the agenda status. 4. Ask 1 concrete question to clarify ambiguity if needed. Be concise.. This will continue for 3 rounds. Once the discussion is complete, Principal Investigator (Alzheimer's KG) will Summarize the meeting log strictly in Markdown: ## Decisions (with Rationale)
## Unresolved Issues
## Next Steps
## Answer to Agenda
Ignore pleasantries. Ensure all technical constraints are captured..

## User

Principal Investigator (Alzheimer's KG), please provide your initial thoughts on the agenda as well as any questions you have to guide the discussion among the team members.

## Principal Investigator (Alzheimer's KG)

**Principal Investigator (Alzheimer’s KG) — Initial Thoughts & Guidance**

### 1. PROPOSE SCHEMA
- **Priority:** The schema must directly support complex AD hypotheses, such as the relationship between specific tau isoforms, genetic risk (APOE alleles), and clinical phenotypes.  
- **Node Types:** Entities must reflect AD pathophysiology and research granularity. Avoid generic terms; e.g., 'Tau Isoform', not just 'Protein'.
- **Edge Types:** Specify mechanistic or causal relations, e.g., ‘phosphorylates’, ‘expressed_in’. Avoid vague edges like 'associated_with'.

**Key Question:** Which node and edge types are non-negotiable for enabling queries about disease mechanism, biomarker progression, and translational interventions?

---

### 2. DATA INGESTION
- **Core Datasets:** ADNI is essential for imaging/clinical; AMP-AD for multi-omic genetics. Prioritize datasets with standardized, high-quality evidence.
- **Conflicting Evidence:** There must be a mechanism for evidence provenance and scoring: human > preclinical, but both must be queryable. Represent species as node/edge properties.

**Key Question:** How will the graph structure encode evidence type, and what is the proposed hierarchy for conflicting findings (e.g., human clin > mouse model)?

---

### 3. VALIDATION
- **Gold Standard:** Need a reference set of triples, ideally from expertly curated AD datasets/publications.
- **Metrics:** Precision is paramount to avoid spurious links. Recall is secondary but must be tractable.

**Key Question:** What curated resources exist for benchmarking, and how will we construct the manual validation set (e.g., 100 high-confidence triples covering all node/edge types)?

---

**Guidance to Team:**
- Anchor all proposals in AD biology, not generic biomedicine.
- Justify each choice with evidence or standard practice (e.g., ontologies, prior KGs).
- Consider the end-user: neuroscientists must be able to trace hypotheses from genetics through pathology to phenotype.

**Please address the above questions in your responses.**

## User

Technical Lead (Knowledge Graph Engineering), please provide your thoughts on the discussion (round 1 of 3). If you do not have anything new or relevant to add, you may say "pass". Remember that you can and should (politely) disagree with other team members if you have a different perspective.

## Technical Lead (Knowledge Graph Engineering)

**Technical Lead (Knowledge Graph Engineering) — Round 1**

---

### 1. PROPOSE SCHEMA

**Node Types (Entities) — AD-specific, prioritized by hypothesis utility:**
1. **Protein Isoform** (e.g., Tau-441, Aβ1-42)  
   - AD pathogenesis hinges on isoform-specific toxicity and aggregation.
2. **Gene Variant** (e.g., APOE*ε4, TREM2-R47H)  
   - Necessary for fine-grained genetic risk modeling and linking to multi-omic data.
3. **Brain Region** (e.g., Hippocampus, Entorhinal Cortex)  
   - Enables spatial mapping of pathology and atrophy.
4. **Cell Type** (e.g., Microglia, Astrocyte, Neuron)  
   - Cell-specific mechanisms (clearance, inflammation) are central to AD.
5. **Clinical Phenotype** (e.g., Mild Cognitive Impairment, AD Dementia)  
   - Required for bridging molecular findings to patient outcomes.
6. **Biomarker Measurement** (e.g., CSF pTau levels, Amyloid PET SUVR)  
   - Supports longitudinal analysis and patient stratification.

**Edge Types (Relations) — Mechanistic, evidence-driven:**
1. **phosphorylates** (Protein Isoform → Protein Isoform)  
   - Central to tauopathy mechanisms.
2. **expressed_in** (Gene Variant/Protein Isoform → Cell Type or Brain Region)  
   - Disambiguates spatial and cellular context.
3. **aggregates_to** (Protein Isoform → Aggregate Structure)  
   - Captures pathology progression (e.g., tau tangles).
4. **modulates_risk_of** (Gene Variant/Protein Isoform → Clinical Phenotype)  
   - Enables causality and risk modeling.
5. **measured_in** (Biomarker Measurement → Clinical Phenotype or Brain Region)  
   - Links quantitative readouts to diagnosis/progression.
6. **infiltrates** (Cell Type → Brain Region)  
   - Captures neuroinflammatory dynamics.

**Justification:**  
These entities and relations are mechanistically specific (e.g., not just "interacts_with") and map directly to AD hypotheses spanning molecular, spatial, and clinical axes.

---

### 2. DATA INGESTION

**Day 1 Priority Data Sources:**
1. **ADNI** — Longitudinal clinical, imaging, and biomarker gold standard.
2. **AMP-AD Knowledge Portal** — Multi-omic, genetics, and transcriptomic data.
3. **ROSMAP** — Postmortem, genomics, and transcriptomics, with deep phenotyping.
4. **UniProt (focused on Tau/Aβ isoforms and PTMs)** — Canonical protein/isoform reference.

**Handling Conflicting Evidence:**
- **Evidence Provenance Model:**  
  - Each edge is annotated with source, species, cohort, methodology, and evidence tier (e.g., human clinical, human postmortem, mouse model).
  - **Evidence Scoring:**  
    - Hierarchy: Human clinical > Human postmortem > Mouse model > In vitro.
    - Conflicting evidence is not collapsed; all are stored with explicit provenance, enabling weighted queries and user filtering.

---

### 3. VALIDATION

**Gold Standard:**
- **Source:** Manually curated triples from recent AD meta-analyses and expert review (e.g., 2021 AD Research Roundtable, AlzForum).
- **Size/Scope:** 100 triples, stratified across all node/edge types (minimum 10 per edge type).

**Metrics:**
- **Precision:** (# correct triples in KG) / (# evaluated triples from KG).
- **Recall:** (# gold triples captured in KG) / (total # gold triples).
- **Coverage:** (# unique AD-relevant entities represented) / (total # entities in source datasets).

**Measurement Approach:**
- Manual curation/validation by domain experts for the gold standard set, with periodic sampling thereafter.

---

**Summary:**  
- The schema and ingestion strategy are anchored in AD-specific mechanisms and facilitate high-precision, hypothesis-driven queries.  
- Evidence scoring and provenance are built natively into the graph, not as afterthoughts.  
- Validation is rigorous with a clear gold-standard set and KPIs to guard against spurious links.

## User

Biomedical Ontologist (AlzKB Semantics & Standards), please provide your thoughts on the discussion (round 1 of 3). If you do not have anything new or relevant to add, you may say "pass". Remember that you can and should (politely) disagree with other team members if you have a different perspective.

## Biomedical Ontologist (AlzKB Semantics & Standards)

**Biomedical Ontologist (AlzKB Semantics & Standards) — Round 1**

---

### 1. PROPOSE SCHEMA

**Node Types (Entities):**
1. **Protein Isoform** (e.g., MAPT Tau-441, APP695)  
   - Must be mapped to UniProt isoform IDs and sequence variants for unambiguous reference.
2. **Gene Variant** (e.g., rs429358 for APOE*ε4, rs75932628 for TREM2-R47H)  
   - Use dbSNP, ClinVar, and HGVS nomenclature to ensure interoperability and variant normalization.
3. **Brain Region (Anatomical Structure)**  
   - Map to Uberon or Brain Region Ontology (BRO); needed for anatomical precision.
4. **Cell Type**  
   - Require mapping to Cell Ontology (CL) for standardization; distinguish between cell subtypes (e.g., reactive astrocyte vs. baseline).
5. **Clinical Phenotype**  
   - Use Human Phenotype Ontology (HPO) or MONDO Disease Ontology; enable linkage to diagnostic criteria and subtypes (e.g., amnestic MCI, EOAD).
6. **Biomarker Measurement**  
   - Explicitly map to LOINC or SNOMED CT codes for standardized test names and analytes (e.g., CSF pTau181 LOINC: 96489-5).

**Edge Types (Relations):**
1. **phosphorylates** (RO:0002419)  
   - Use Relation Ontology for precise semantics; critical for detailing post-translational modifications.
2. **expressed_in** (RO:0002206)  
   - Standard in OBO Foundry; ensures compatibility with existing cell/tissue atlases.
3. **aggregates_to** (custom, must be mapped to GO or tailored extension)  
   - Distinguish between amyloid plaque formation (GO:1902553) and tau fibrilization.
4. **modulates_risk_of** (MONDO/RO:0003304, or custom if needed)  
   - Differentiate direct pathogenic effect from risk association (e.g., GWAS odds ratio).
5. **measured_in** (BFO:0000050 "part of", or create explicit measurement_of relation)  
   - Link measurement entity to clinical or anatomical context.
6. **infiltrates** (RO:0002430, "migrates to")  
   - Align with immune/cell migration ontologies for cross-dataset harmonization.

**Justification:**  
Standard vocabularies are essential for data harmonization, entity/entity normalization, and future integration with external KGs. Each entity and relation should be annotated with CURIE/IRI for traceability, synonym resolution, and synonym mapping (e.g., "pTau181" = "phosphorylated tau at threonine 181").

---

### 2. DATA INGESTION

**Priority Data Sources:**
1. **ADNI** (clinical, imaging, and fluid biomarkers)  
   - Use established LOINC/SNOMED CT for biomarker data.
2. **AMP-AD Knowledge Portal** (multi-omic, transcriptomic, network analyses)  
   - Harmonize gene/protein IDs with Ensembl/UniProt.
3. **ROSMAP** (deep phenotyping, robust postmortem data)  
   - Map brain region/cell type data to Uberon/CL.
4. **UniProt (isoforms, PTMs, functional annotation)**  
   - Standard reference for mapping protein-level data.

**Handling Conflicting Evidence:**
- **Provenance Encoding:**  
  - Each triple/edge must be annotated with `source`, `species` (NCBI Taxon), `evidence type` (ECO: Evidence & Conclusion Ontology), and `confidence score`.
- **Scoring Mechanism:**  
  - Use a layered evidence score:  
    - Clinical (human diagnosis, LOINC-encoded biomarker): Score 3  
    - Human postmortem (ROSMAP): Score 2  
    - Animal model (species-specific, e.g., NCBITaxon:10090 for mouse): Score 1  
  - Retain all edges with provenance, but allow filtering by evidence class.

---

### 3. VALIDATION

**Gold Standard:**  
- **Source:** Manually curated set of 100 triples, stratified by node and edge type. Use recent, high-impact AD reviews (e.g., AlzForum, systematic reviews with explicit evidence tables).
- **Manual Curation:** Each triple should be verified by at least two domain/ontology experts, documented with literature DOIs or dataset accessions.

**Metrics:**  
- **Precision:** Correct triples (as per gold standard) / Total triples sampled.
- **Recall:** Gold standard triples present in KG / Total gold standard triples.
- **Ontology Coverage:** % of entities/relations mapped to standard vocabularies (target >90%).

**Additional Notes:**  
- Ontology-driven validation scripts will check for compliance (e.g., no dangling nodes, all relations conform to domain/range restrictions as per reference ontologies).
- Cross-modal synonym harmonization is required before loading any data.

---

**Summary:**  
- Agree with Technical Lead on entity and relation scope, but stress that every schema element must be fully normalized to reference ontologies and codes.  
- All evidence must be explicitly scored and provenance-annotated—this is essential for filtering and downstream analytics.  
- Validation must include both precision/recall and ontology mapping coverage.  
- No instances of custom, ambiguous entity names/relations allowed.

## User

Data Science Lead (Extraction & Validation), please provide your thoughts on the discussion (round 1 of 3). If you do not have anything new or relevant to add, you may say "pass". Remember that you can and should (politely) disagree with other team members if you have a different perspective.

## Data Science Lead (Extraction & Validation)

**Data Science Lead (Extraction & Validation) — Round 1**

---

### 1. PROPOSE SCHEMA

**Node Types (Entities):**
Fully aligned with prior proposals, but from an extraction/validation perspective, the following are critical for high-precision NLP and automated curation:

1. **Protein Isoform** (curated to isoform-level, e.g., “Tau-441”, with UniProt IDs)  
   - Key: Disambiguate between general “MAPT” and isoform-specific effects; necessary to avoid merging experimental findings.
2. **Gene Variant** (normalized to dbSNP/ClinVar, HGVS syntax enforced)  
   - For machine reading, require regex validation and ID normalization for all extracted variants.
3. **Brain Region** (standardized to Uberon/Allen Brain Atlas)  
   - High-resolution labels reduce ambiguity in region-specific findings.
4. **Cell Type** (Cell Ontology ID, subtype support)  
   - Extraction pipeline must resolve ambiguous mentions (e.g., “activated microglia”).
5. **Clinical Phenotype** (HPO/MONDO, precise mapping mandatory)  
   - Avoid “catch-all” clinical labels—subtype precision improves downstream validation.
6. **Biomarker Measurement** (LOINC/SNOMED, with units and thresholds)  
   - Extraction engine should enforce normalization to codes and support value/range parsing.

**Edge Types (Relations):**  
I concur with prior proposals but emphasize the following for extraction/validation feasibility:

1. **phosphorylates**  
   - Extraction must discriminate directionality and site (e.g., “pTau181” vs. “pTau217”).
2. **expressed_in**  
   - Pipeline should distinguish between spatial vs. cell-type context, sometimes co-mentioned.
3. **aggregates_to**  
   - Need to resolve various forms: “oligomerizes”, “forms tangles”—all mapped to canonical relation.
4. **modulates_risk_of**  
   - Enforce explicit evidence; extraction models often overstate causality. Must downweight “associated_with” unless supported by effect size or odds ratio.
5. **measured_in**  
   - Extraction must link specific analyte, sample type, and patient population for downstream QA.
6. **infiltrates**  
   - Validate with context (e.g., cell migration in AD tissue, not immune cell infiltration elsewhere).

**Justification:**  
Extraction/validation pipelines must be schema-driven; ambiguous mentions or generic relations are a major source of false positives. All extraction rules/models will be benchmarked against these schema constraints.

---

### 2. DATA INGESTION

**Priority Datasets:**  
Agree with ADNI, AMP-AD, ROSMAP, UniProt (with isoform/PTM focus). For extraction QA, propose *AlzForum Mutations Database* as a supplementary benchmark for prioritizing genotype-phenotype assertions.

**Handling Conflicting Evidence:**  
- **Edge Annotation:** For every extracted triple, store:  
  - Source (dataset/pubmed ID)
  - Species (NCBI Taxon)
  - Evidence Type (ECO code)
  - Extraction Confidence (model score, evidence tier as outlined above)
- **Conflict Protocol:** All conflicting edges are retained with evidence meta-data. Downrank preclinical/low-evidence edges in QA scoring but do not suppress unless flagged as spurious by cross-validation with gold-standard or contradictory high-confidence human evidence.

**Scoring:**  
- Clinical (human, prospective/longitudinal): Score 3  
- Human postmortem: Score 2  
- Animal model (mouse/rat): Score 1  
- In vitro/in silico: Score 0

---

### 3. VALIDATION

**Gold Standard Design:**
- 100 manually curated triples, balanced across node/edge types.
- Source: Recent systematic AD reviews, AlzForum, and high-confidence datasets.
- Each triple annotated with evidence code, source DOI, mapping to ontology IDs.
- QA: All extracted triples from Day 1 pipeline are compared to gold standard; further error analysis on false positives to refine extraction rules.

**Metrics:**
- **Precision:** #TP/(#TP + #FP); target > 90%.
- **Recall:** #TP/(#TP + #FN); target > 60% initially.
- **False Positive Analysis:** % of spurious/unsupported edges after manual review; target <5%.
- **Ontology Coverage:** % of extracted entities/relations correctly mapped to reference ontologies; target >90%.

---

**Summary:**
- Schema and ingestion plan are extraction- and QA-ready.
- No ambiguous/generic nodes or relations admitted.
- All validation protocols must be automated and manual, with rigorous error analysis and evidence-based scoring.
- Disagree with use of any custom relations/entities not mappable to standards.  
- Strongly support scoring and retention of all evidence but mandate hard filtering of unsupported or hallucinated links before deployment.

## User

Scientific Critic (AlzKB), please provide your thoughts on the discussion (round 1 of 3). If you do not have anything new or relevant to add, you may say "pass". Remember that you can and should (politely) disagree with other team members if you have a different perspective.

## Scientific Critic (AlzKB)

**Scientific Critic (AlzKB) — Round 1**

---

### 1. PROPOSE SCHEMA

**Strengths Noted:**
- All team members have converged on AD-specific, granular entity types (Protein Isoform, Gene Variant with proper normalization, etc.) and have rejected generic categories.
- Edge types proposed are mechanistic and biologically actionable, avoiding vague relations.

**Critical Review:**
- **Enforce Predicate Specificity:**  
  - Any admission of ‘modulates_risk_of’ must be tightly operationalized. It should only be used when a variant shows statistically significant effect size in human cohorts, not merely when reported in animal/preclinical studies.
  - 'Aggregates_to' must distinguish between different aggregate morphologies: e.g., prefibrillar oligomers vs. mature fibrils vs. plaques. If not, downstream analyses may yield misleading hypotheses.
- **Node Type Resolution:**  
  - Protein Isoforms: Explicitly require distinction between post-translational modification states (e.g., pTau181 vs. unmodified Tau-441), not just sequence variants.
  - Gene Variants: Do not allow 'Gene' or 'SNP' as catch-all nodes; enforce extraction/curation at the variant and allele level (e.g., rsID + allele).
  - Clinical Phenotype: Must not conflate 'dementia' with 'Alzheimer’s disease'; require all phenotype assignments to be grounded in diagnostic criteria (DSM, NINCDS-ADRDA, etc.).
- **Ontology Compliance:**  
  - Insist on mapping all schema elements to formal ontologies and providing CURIEs/IRIs at load time. Any custom relations must be explicitly justified, mapped, or rejected.

---

### 2. DATA INGESTION

**Data Source Audit:**
- The group’s selection (ADNI, AMP-AD, ROSMAP, UniProt) is appropriate for Day 1, but:
  - **Species Provenance:** All imported data (especially from AMP-AD and ROSMAP, which include mouse models) must be indexed by species; no merging of murine and human data in any edge/entity. Murine findings should be explicitly linked to the NCBI Taxon ID for mouse.
  - **Preclinical/Clinical Split:** Evidence scoring must never mask the underlying species or study type—downweighting is not enough. Allow users to exclude all non-human assertions at query time.
  - **Data Versioning:** Provenance must include precise dataset version/date to ensure reproducibility.

**Conflict Handling:**  
- Conflicting findings (e.g., gene knockout in mouse vs. human GWAS) must be explicitly represented as separate edges, never merged or averaged.

---

### 3. VALIDATION

**Gold Standard & Metrics Requirements:**
- **Manual Curation:** Gold standard triples must cover all edge types AND all entity types, with at least 2 independent curators cross-reviewing each entry. 
- **Provenance Traceability:** Each gold standard triple must be linked to at least one PubMed ID or dataset accession; “review article consensus” is not sufficient without explicit reference extraction.
- **Success Metrics:**  
  - **Precision:** Only accept as “correct” those triples that can be traced to primary, peer-reviewed evidence (not database inferences alone).
  - **Recall:** Quantify by edge type and entity type, not just overall, to surface systematic extraction/database biases.
  - **F1 Score:** Demand reporting of F1 (harmonic mean of precision and recall) for the gold standard set.

**Additional Requirements:**
- **No Circular Evaluation:** The gold standard must not include any triples that were used to train/extract the KG; otherwise, precision/recall are inflated.
- **Biological Plausibility Filter:** Any triple that fails basic biological plausibility (e.g., “Astrocyte phosphorylates Tau”) is automatically counted as a false positive, regardless of extraction confidence.

---

**Summary:**
- Commend the schema and data source rigor.
- Demand operational precision for each edge/entity to prevent downstream scientific misinterpretation.
- Explicitly disallow conflation of AD with generic dementia, human with mouse data, or PTM states with parent isoforms.
- Provenance and evidence scoring must be encoded at the triple level.
- No metrics accepted unless evaluated on a properly blinded, gold-standard set covering all schema elements with quantitative results (Precision, Recall, F1).

## User

This concludes round 1 of 3 of discussion. Principal Investigator (Alzheimer's KG), please Synthesize team inputs. 1. Identify agreements vs. conflicts. 2. Resolve conflicts using provided evidence; favor data over opinion. 3. Decide the agenda status. 4. Ask 1 concrete question to clarify ambiguity if needed. Be concise..

## Principal Investigator (Alzheimer's KG)

**Principal Investigator (Alzheimer's KG) — Round 1 Synthesis**

---

### 1. Agreements

- **Entities & Edges:**  
  Universal agreement on six node types (Protein Isoform, Gene Variant, Brain Region, Cell Type, Clinical Phenotype, Biomarker Measurement) and need for biologically specific, ontology-mapped edge types (e.g., phosphorylates, modulates_risk_of).
- **Ontology Normalization:**  
  All concur on full mapping of entities and relations to standard ontologies (UniProt, dbSNP, Uberon, CL, HPO/MONDO, LOINC, Relation Ontology).
- **Evidence & Provenance:**  
  Consensus on per-edge provenance, evidence scoring by species, methodology (ECO), and source; explicit inclusion of species, evidence type, and dataset version in every assertion.
- **Data Sources:**  
  Agreement on Day 1 datasets: ADNI, AMP-AD, ROSMAP, UniProt (with isoform/PTM focus).
- **Validation:**  
  All support a manually curated, stratified gold standard of 100 triples, with multiparty review and explicit PubMed/dataset citation; precision is paramount, recall/coverage and ontology compliance also tracked.

---

### 2. Conflicts & Resolution

- **Operationalization of ‘modulates_risk_of’:**  
  Critic/Semantics demand use only with statistically significant, human cohort evidence. **Resolution:** Restrict ‘modulates_risk_of’ edges to human clinical/postmortem data, explicitly excluding animal/in vitro evidence for this relation.
- **Granularity of Aggregation & PTMs:**  
  Critic insists on distinguishing aggregate morphologies and PTM states. **Resolution:** Schema will encode aggregate type as a qualifier and PTM state as a distinct entity property (e.g., pTau181 vs. unmodified Tau-441).
- **Handling of Conflicting Evidence:**  
  Critic/Semantics require never merging mouse/human edges and explicit representation of all conflicts. **Resolution:** Agree—edges from different species, evidence types, or conflicting results will never be merged and will be fully provenance-annotated.

---

### 3. Agenda Status

- **Schema Core:** Substantial convergence, with minor clarifications needed on PTM and aggregate granularity.
- **Data Strategy:** Strong agreement; all parties endorse provenance-first, multi-species, multi-source approach.
- **Validation:** Only open detail: stratification of recall metrics by node/edge type (as requested by Critic).

---

### 4. Clarifying Question

**To all ontology and extraction leads:**  
*How should the schema and extraction pipeline formally represent and distinguish post-translational modification states (e.g., pTau181 vs. unmodified Tau isoforms) as entities—should these be modeled as separate nodes, as node attributes, or as reified triples with qualifiers?*

## User

Technical Lead (Knowledge Graph Engineering), please provide your thoughts on the discussion (round 2 of 3). If you do not have anything new or relevant to add, you may say "pass". Remember that you can and should (politely) disagree with other team members if you have a different perspective.

## Technical Lead (Knowledge Graph Engineering)

**Technical Lead (Knowledge Graph Engineering) — Round 2**

---

### Response to Clarifying Question: Modeling PTM States (e.g., pTau181)

**Recommendation:**  
Model each PTM state (e.g., pTau181) as a distinct **Protein Isoform node**, not merely as an attribute or qualifier. This approach aligns with established practices in molecular KGs (e.g., Reactome, UniProt), supports unambiguous querying, and is compatible with property graph and RDF models. Key points:

- **Distinct Nodes:**  
  - Each biochemically and functionally distinct PTM (e.g., Tau-441 phosphorylated at T181) is a unique node, assigned a UniProt PTM identifier or custom IRI/annotation if no standard exists.
  - Parent-child relationships (e.g., ‘is_modified_form_of’) can link modified/unmodified forms, enabling both granular and aggregate queries.

- **Advantages:**  
  - *Query power:* Enables precise graph traversal—e.g., "find all effects specific to pTau181, not just general Tau."
  - *Data provenance:* Supports evidence tracking at the PTM-specific level.
  - *Extensibility:* Allows future addition of other PTMs (acetylation, ubiquitination).
  - *Alignment:* Fully compatible with property graph and RDF triple models, and with BioPAX/BEL best practices.

- **Edge Modeling:**  
  - Mechanistic edges (e.g., ‘phosphorylates’, ‘aggregates_to’) always operate on specific PTM nodes.
  - ‘is_modified_form_of’ edges link PTM-specific nodes to the canonical isoform.

- **Implementation Considerations:**  
  - **ETL:** Extraction/ingestion pipelines must resolve mentions like “pTau181” to the corresponding PTM node, mapping via text mining + UniProt/PTM ontologies.
  - **Ontology:** Use PSI-MOD identifiers for PTMs when possible, fallback to curated IRIs if not available.

---

### Concerns with Alternative Models:

- **Node attributes only:**  
  - Loses granularity—cannot distinguish mechanistic links to specific PTMs vs. parent proteins.
- **Reified triples with qualifiers:**  
  - Adds significant complexity to property graph query patterns; not well supported in Neo4j-style queries.
  - Typically reduces query performance and clarity for end-users.

---

### Summary:

- All PTM states (e.g., pTau181, pTau217) are distinct nodes, fully ontology-mapped, and linked to canonical isoform nodes via ‘is_modified_form_of’ relations.
- Extraction and ETL pipelines must be PTM-aware and enforce normalization at the node level.
- This maximizes both biological rigor and technical scalability.

---

**No further disagreements.** I fully support the points raised by the Scientific Critic and Biomedical Ontologist regarding granularity, and the need for both schema-level and evidence-level precision.

## User

Biomedical Ontologist (AlzKB Semantics & Standards), please provide your thoughts on the discussion (round 2 of 3). If you do not have anything new or relevant to add, you may say "pass". Remember that you can and should (politely) disagree with other team members if you have a different perspective.

## Biomedical Ontologist (AlzKB Semantics & Standards)

**Biomedical Ontologist (AlzKB Semantics & Standards) — Round 2**

---

### On Modeling PTM States (pTau181, etc.)

**Strongly Agree:**  
Each post-translationally modified form (e.g., pTau181, pTau217) must be instantiated as a distinct node in the KG, not merely as an attribute or triple qualifier.

#### Rationale:
- **Ontology Alignment:**  
  - *PSI-MOD* (Protein Modification Ontology) provides CURIEs for most PTMs (e.g., MOD:00696 for phosphothreonine).  
  - Modified proteins can be represented as logical intersections:  
    - Example:  
      - Entity: “Tau-441 phosphorylated at T181”  
      - Logical ID: UniProt:Q24459-8 + MOD:00696 at position 181
  - UniProt and neXtProt already model PTMs as entity variants—align with these as primary references.

- **Node Modeling:**  
  - Each unique PTM (site-specific, independently evidenced) is a separate node.  
  - Edge ‘is_modified_form_of’ (RO:0002212) links the PTM node to its canonical isoform node.
  - Use edge annotation to specify site (e.g., position 181 on MAPT).
  - If multiple modifications are relevant (e.g., dual phosphorylation), instantiate as a separate multi-PTM node if biologically justified.

- **Query and Reasoning:**  
  - Enables unambiguous mechanistic queries: “Show all interactions/effects specific to pTau181 in hippocampus.”
  - Supports evidence granularity: studies may report on generic Tau, pTau181, or pTau217—each node can aggregate its own provenance and supporting evidence.

- **Extraction/ETL Guidance:**  
  - Extraction must resolve experimental mentions (e.g., “Tau phosphorylated at T231”) to either PSI-MOD ID or standardized text, with fallback to manual curation for novel/ambiguous PTMs.
  - Synonym handling: all known aliases (e.g., “p-Tau181”) must be mapped to the same node.

#### On Not Using Node Attributes or Reification:
- **Node attributes** for PTM states are insufficient for representing mechanistic specificity and do not support ontology mapping.
- **Reified triples** introduce unnecessary complexity and degrade FAIRness/composability.

---

**Additional Clarification:**  
For complex aggregates (e.g., prefibrillar vs. fibrillar tau), recommend each aggregate morphology be a uniquely identified node (mapped to GO or custom, if needed), linked via ‘aggregates_to’ and fully provenance-annotated.

---

**Summary:**  
- Model each PTM (and aggregate) as a distinct, ontology-mapped node.
- Use parent-child and modification-specific relations.
- Extraction/ETL must resolve these at ingestion, with full synonym and evidence tracking.
- This approach maximizes semantic rigor, queryability, and interoperability.

## User

Data Science Lead (Extraction & Validation), please provide your thoughts on the discussion (round 2 of 3). If you do not have anything new or relevant to add, you may say "pass". Remember that you can and should (politely) disagree with other team members if you have a different perspective.

## Data Science Lead (Extraction & Validation)

**Data Science Lead (Extraction & Validation) — Round 2**

---

### On Representation of PTM States (e.g., pTau181)

**Full agreement:**  
PTM states (e.g., pTau181, pTau217) should be modeled as distinct Protein Isoform nodes, not as attributes or only through reified triples.

#### Extraction & Validation Rationale:

- **NLP Precision:**  
  - Extraction models (NER, relation extraction) can be precisely tuned to recognize PTM mentions (“pTau181”, “Tau phosphorylated at T231”) as explicit entities.  
  - Downstream QA is more tractable—false positives from ambiguous mentions (“Tau” vs. “pTau181”) are minimized when these are atomic graph nodes.
  - Synonym lists and regex-based normalization (including PTM site positions) can be built and maintained for high recall/precision.

- **Validation Protocols:**  
  - Each extracted PTM entity must be mapped to a PSI-MOD ID or curated local IRI.  
  - Validation scripts will enforce that all “phosphorylates” edges connect either to a canonical or PTM-specific isoform node.
  - QA will flag any mention of “Tau” in context where a PTM is implied but not explicitly resolved in the extraction, prompting manual review or model refinement.

- **PTM-Granular Provenance:**  
  - Evidence scores and provenance meta-data will be tied at the PTM node level (e.g., evidence supporting “pTau181 in CSF” is not conflated with generic “Tau”).

- **ETL/Extraction Implementation:**  
  - Extraction pipeline will include a PTM-mapping module—text-mined mentions are mapped using trained models/rules to distinct PTM nodes, not parent isoforms.
  - Where ambiguous, flag as “candidate PTM” and prioritize for manual curation.
  - Manual curation pipeline for new or rare PTMs not yet in PSI-MOD.

**On Attributes/Reification:**  
- Attributes-only: Not sufficient for validation or for users querying for PTM-specific mechanisms.
- Reified triples: Adds unnecessary graph/modeling complexity and hinders both automated QA and user queries.

---

### Additional Extraction Note:

- For aggregate morphologies (e.g., tau oligomers vs. fibrils vs. plaques), extraction rules will distinguish these as separate nodes, mapped to GO or custom IRIs, following the same node-based principle.
- All mention-to-node mapping processes will be version-controlled and auditable.

---

**Summary:**  
- Extraction and validation pipelines will treat each PTM- or aggregate-specific entity as a unique, ontology-mapped node.
- QA, evidence assignment, and error analysis will be at the node (not attribute) level, ensuring maximal precision and minimal false positives.
- No further disagreement; fully aligned with KG engineering and ontology leads.

## User

Scientific Critic (AlzKB), please provide your thoughts on the discussion (round 2 of 3). If you do not have anything new or relevant to add, you may say "pass". Remember that you can and should (politely) disagree with other team members if you have a different perspective.

## Scientific Critic (AlzKB)

**Scientific Critic (AlzKB) — Round 2**

---

### On Formal Representation of PTM States

**Endorsement (with strict requirements):**
- The unanimous recommendation to model PTM states (e.g., pTau181, pTau217) as distinct nodes is essential for biological plausibility and downstream hypothesis generation.
- This approach prevents conflating literature on unmodified vs. modified protein forms—a common source of error and overgeneralization in AD research.

#### Requirements & Checks:
- **Node Identity:**  
  - Each PTM-specific node must be unambiguously identified, ideally with a PSI-MOD CURIE and reference to UniProt canonical sequence + modification position.
  - Synonym handling is crucial: extraction must not merge “pTau”, “phospho-Tau”, and “Tau” unless the underlying evidence is ambiguous or explicitly cross-validated.

- **Edge Rigor:**  
  - All mechanistic edges (phosphorylates, aggregates_to, modulates_risk_of) must operate on the correct PTM or isoform node; no fallback to parent “Tau” allowed if the modification is reported in the source.

- **Evidence and Provenance:**  
  - Each PTM node, and all edges involving it, must carry explicit provenance (PMID, dataset ID, species, method).
  - Cross-species distinction is critical: a “pTau181 effect” reported in mouse should not appear within human-specific queries unless explicitly requested.

- **Aggregate Morphologies:**  
  - Fully agree: aggregate forms (oligomer, fibril, plaque) must be separate nodes, mapped to GO or bespoke vocabularies, not lumped together or differentiated only by edge attributes.

#### Additional Critical Notes:
- **Modular Extensibility:**  
  - This node-based approach allows for later addition of combinatorial PTMs or aggregate morphologies without schema modification.
- **Validation:**  
  - Manual review of the first batch of PTM/aggregate nodes is required to ensure correct entity resolution before pipeline-wide rollout.
  - False positives due to “PTM ambiguity” (e.g., “phosphorylated tau” with no position given) must be tracked as a distinct error class in KG QA reports.

---

**Summary:**
- Full endorsement, with the caveat that node creation, evidence attribution, and query filters must maintain the highest granularity and provenance control.
- The KG must never conflate parent and PTM-specific forms or aggregate states, and every PTM/aggregate node must be explicitly traceable to its evidence base.
- Recommend a formal pre-launch audit of all PTM/aggregate nodes/edges for entity resolution and source traceability.

## User

This concludes round 2 of 3 of discussion. Principal Investigator (Alzheimer's KG), please Synthesize team inputs. 1. Identify agreements vs. conflicts. 2. Resolve conflicts using provided evidence; favor data over opinion. 3. Decide the agenda status. 4. Ask 1 concrete question to clarify ambiguity if needed. Be concise..

## Principal Investigator (Alzheimer's KG)

**Principal Investigator (Alzheimer's KG) — Round 2 Synthesis**

---

### 1. Agreements

- **PTM Representation:**  
  Unanimous agreement: Each post-translational modification (PTM) state (e.g., pTau181, pTau217) will be modeled as a distinct Protein Isoform node, not as an attribute or reified triple.
- **Ontology Alignment:**  
  All PTM nodes and aggregate morphologies will be mapped to PSI-MOD, UniProt, and GO (or custom IRIs if needed), with explicit site-level annotation.
- **Parent-Child Structure:**  
  Modified forms will be linked to canonical isoforms via an ‘is_modified_form_of’ edge.
- **Extraction & QA:**  
  NLP/extraction pipelines will be tuned for unambiguous PTM recognition, synonym normalization, and will enforce evidence and provenance at the node level.
- **Aggregate Morphologies:**  
  All aggregate forms (oligomer, fibril, plaque) will be separately modeled as nodes, not as attributes or single node with qualifiers.
- **Provenance:**  
  Every PTM or aggregate-specific node and edge must be traceable to its evidence source, species, and dataset version.
- **Validation:**  
  Initial manual curation/audit of PTM/aggregate nodes is mandated before full rollout.

---

### 2. Conflicts & Resolution

- No substantive conflicts remain—consensus is robust across engineering, ontology, extraction, and scientific QA perspectives.
- Strict requirement: ambiguous or generic “phosphorylated tau” mentions must be flagged and tracked distinctly, not merged, ensuring high-precision entity resolution.

---

### 3. Agenda Status

- **Schema Core:** Fully resolved; PTM and aggregate state granularity approach is settled.
- **Data Strategy:** No remaining ambiguity.
- **Extraction/Validation:** Unambiguous granularity principle for entity resolution is fully established.

---

### 4. Clarifying Question

**To Data Science Lead & Biomedical Ontologist:**  
*For ambiguous or underspecified PTM mentions (e.g., “phosphorylated tau” with no site), what is the formal protocol? Should these be modeled as separate ‘generic PTM’ nodes, omitted, or flagged for manual review, and how do we ensure these do not contaminate downstream analytics?*

## User

Technical Lead (Knowledge Graph Engineering), please provide your thoughts on the discussion (round 3 of 3). If you do not have anything new or relevant to add, you may say "pass". Remember that you can and should (politely) disagree with other team members if you have a different perspective.

## Technical Lead (Knowledge Graph Engineering)

**Technical Lead (Knowledge Graph Engineering) — Round 3**

---

### On Handling Ambiguous or Underspecified PTM Mentions

**Recommended Protocol:**

- **Separate ‘Generic PTM’ Nodes:**  
  - Ambiguous mentions (e.g., “phosphorylated tau” with no site specified) should be instantiated as separate “generic phosphorylated tau” nodes, *distinct* from both canonical and site-specific PTM nodes.  
  - These nodes must be explicitly labeled with their ambiguity status (e.g., `label="phosphorylated tau (site unknown)"`, with a standardized flag/property: `ptm:site="unspecified"`).

- **Manual Review & Provenance:**  
  - All ambiguous PTM nodes are flagged for manual review.  
  - Provenance must capture the original text evidence and extraction confidence.
  - If, during manual curation or later data releases, the site is resolved (e.g., by future publication), the node can be merged or replaced by a specific PTM entity.

- **Analytics & Query Safeguards:**  
  - By default, analytic pipelines and user queries must *exclude* generic PTM nodes unless they are explicitly requested (e.g., through a `ptm:site="*" OR "unspecified"` filter).
  - Downstream workflows should treat generic PTM nodes as a distinct evidence tier, not as evidence for any specific site/PTM node.

- **Contamination Mitigation:**  
  - Semantically, never allow edges from “generic PTM” nodes to be inferred or rolled up to site-specific nodes (e.g., never treat “phosphorylated tau” as evidence for pTau181 or pTau217).
  - In reporting/analytics, generic PTM assertions are counted and visualized separately with full caveats.

---

**Summary:**  
- Instantiate generic/ambiguous PTM mentions as dedicated nodes, clearly labeled and segregated.
- Flag all such nodes for manual/periodic review.
- Ensure analytics and downstream reasoning never conflate generic with site-specific PTM evidence.

**No disagreement with team consensus; this protocol preserves both data completeness and analytic rigor.**

## User

Biomedical Ontologist (AlzKB Semantics & Standards), please provide your thoughts on the discussion (round 3 of 3). If you do not have anything new or relevant to add, you may say "pass". Remember that you can and should (politely) disagree with other team members if you have a different perspective.

## Biomedical Ontologist (AlzKB Semantics & Standards)

**Biomedical Ontologist (AlzKB Semantics & Standards) — Round 3**

---

### On Handling Ambiguous/Underspecified PTM Mentions (“phosphorylated tau” with no site)

**Protocol and Ontology Guidance:**

- **Distinct 'Generic PTM' Nodes:**  
  - *Agree*: Instantiate ambiguous PTM mentions as separate nodes, e.g., “phosphorylated tau (site unspecified)”, with a unique local IRI (e.g., `alzkg:PTM_MAPT_generic_phospho`).
  - Annotate with PSI-MOD parent class (e.g., MOD:00696 “phosphorylated residue”), and set `has_modification_site:unknown`.
  - Specify ambiguity via node property (e.g., `annotation:modification_site="unknown"`).

- **Strict Provenance and Review:**  
  - All such nodes must carry full provenance (source text, DOI/PMID, extraction confidence).
  - Mandatory manual review for all ambiguous PTMs prior to any downstream use.
  - If future evidence resolves site, update the node accordingly and re-link provenance.

- **Downstream Use and Contamination Control:**  
  - *Schema-level enforcement:* Analytics, enrichment, and network traversal must treat generic PTM nodes as distinct from any site-specific PTM or canonical isoform nodes.
  - *Query filtering:* By default, exclude ambiguous PTM nodes from hypothesis generation and automated reasoning unless users opt in.

- **Validation & Coverage Metrics:**  
  - Track and report the frequency of ambiguous PTM nodes as a quality metric (% ambiguous vs. total PTM assertions).
  - Periodically review and attempt to resolve/upgrade ambiguous PTMs as new evidence becomes available.

---

**Summary:**  
- Fully aligned with Technical Lead:  
  - Ambiguous PTMs = unique, clearly marked nodes.
  - Strict provenance and review.
  - Default analytic exclusion.
- This maintains maximal KG integrity, transparency, and supports future curation.  
- *No disagreement.*

## User

Data Science Lead (Extraction & Validation), please provide your thoughts on the discussion (round 3 of 3). If you do not have anything new or relevant to add, you may say "pass". Remember that you can and should (politely) disagree with other team members if you have a different perspective.

## Data Science Lead (Extraction & Validation)

**Data Science Lead (Extraction & Validation) — Round 3**

---

### Handling Ambiguous/Underspecified PTM Mentions

**Full Alignment with Team:**

- **Extraction Protocol:**  
  - NLP/extraction pipeline will instantiate ambiguous mentions (e.g., “phosphorylated tau” without site) as dedicated “generic phosphorylated tau” nodes, not mapped to any specific site/PTM.
  - These nodes will be tagged with `modification_site="unknown"` and assigned a unique local identifier, clearly separated from site-specific PTMs.

- **Evidence & Manual Curation:**  
  - All such nodes flagged with extraction confidence and complete provenance (sentence, publication, dataset).
  - Extraction logs will auto-route these cases to a manual review queue, prioritizing for curator evaluation or targeted literature mining if statistical frequency is high.

- **QA/Validation:**  
  - Validation scripts will enforce that no edge from a generic PTM node is ever substituted for a specific PTM node in analytics, reporting, or enrichment pipelines.
  - Precision/recall audits will track ambiguous PTMs as a separate error/uncertainty class, reported to both ontologist and KG engineering leads.

- **Analytics Safeguard:**  
  - By default, all analytics, downstream modeling, and user-facing queries will *exclude* these generic PTM assertions unless explicitly requested via a filter or advanced search.
  - If ambiguous PTMs are later resolved (via new publication/dataset), node merging and provenance reattribution will be auditable and version-controlled.

---

**Summary:**  
- Ambiguous/underspecified PTM mentions are instantiated as unique, labeled, provenance-rich nodes.
- Strong controls to prevent contamination of more specific (site-resolved) PTM evidence.
- Ambiguous PTMs are tracked separately in QA, analytics, and reporting.
- No conflicts; protocol is technically and scientifically robust.

## User

Scientific Critic (AlzKB), please provide your thoughts on the discussion (round 3 of 3). If you do not have anything new or relevant to add, you may say "pass". Remember that you can and should (politely) disagree with other team members if you have a different perspective.

## Scientific Critic (AlzKB)

**Scientific Critic (AlzKB) — Round 3**

---

### On Ambiguous/Underspecified PTM Mentions

**Endorsement (with strict criteria):**
- The team’s protocol—to instantiate ambiguous PTM mentions as separate, clearly-labeled 'generic PTM' nodes and exclude them from analytic roll-up with site-specific PTMs—is both methodologically sound and essential for scientific rigor.

#### Requirements & Critique:
- **Labeling & Provenance:**  
  - Each ambiguous PTM node must carry a distinct label (e.g., “phosphorylated tau (site unknown)”) and a property marking the site as “unknown” or “ambiguous”.
  - Provenance must trace to the exact evidence (sentence, DOI, dataset ID), and these nodes should be visually and programmatically segregated in all workflows.

- **Analytical Exclusion:**  
  - Strongly agree with default exclusion from any automated hypothesis generation, enrichment analysis, or summary statistics.
  - Allow opt-in inclusion only for explicit user queries or meta-analyses evaluating knowledge gaps.

- **Manual Review & Curation:**  
  - Periodic audit of these ambiguous nodes is required. Any opportunity to resolve an ambiguous PTM via new literature or dataset updates must be systematically pursued and documented.

- **Reporting & Metrics:**  
  - Insist that the prevalence of ambiguous PTMs is tracked and reported as a key KG quality metric (e.g., “% ambiguous PTM assertions among all PTM nodes”).

- **No Inference or Propagation:**  
  - Under no circumstances should generic PTM assertions propagate to, or be inferred as evidence for, any site-specific node.

---

**Summary:**  
- Fully support the protocol of distinct, provenance-rich, and analytically segregated ‘generic PTM’ nodes for underspecified PTM mentions.
- This safeguards biological plausibility, analytical reproducibility, and transparency.
- No disagreements; approach is compliant with best practices for KG scientific integrity.

## User

Principal Investigator (Alzheimer's KG), please Summarize the meeting log strictly in Markdown: ## Decisions (with Rationale)
## Unresolved Issues
## Next Steps
## Answer to Agenda
Ignore pleasantries. Ensure all technical constraints are captured..

As a reminder, here is the agenda for the meeting:

Task: Build a scalable, retrieval-optimized Knowledge Graph for Alzheimer's Disease research.

TASK: Define the Technical Specification for AlzKB.
The team must agree on the architectural foundation before implementation.

OUTPUT REQUIREMENTS:
1. SCHEMA CORE: Define top 6 Entity Types and 6 Edge Types (Must be biologically specific, e.g., 'phosphorylates' not 'interacts').
2. DATA STRATEGY: Select 4 priority Data Sources (e.g., ADNI) and define the Evidence Scoring mechanism (e.g., 'Clinical vs. Preclinical').
3. SUCCESS METRICS: Define 3 quantitative KPIs for coverage and precision.

CONSTRAINTS: Be specific. No fluff. Prioritize AD-specific nuances (e.g., Tau isoforms).


As a reminder, here are the agenda questions that must be answered:

1. PROPOSE SCHEMA: List the top 6 Node Types and 6 specific Edge Types essential for AD reasoning. Justify why these support hypothesis generation.

2. DATA INGESTION: Which 4 external databases are critical for Day 1 import? How will we handle conflicting evidence (e.g., human vs. mouse data) in the graph structure?

3. VALIDATION: Define the 'Gold Standard'. How exactly will we measure Precision and Recall? (e.g., 'Manually curated dataset of 100 triples').

Your summary should take the following form.

### Agenda

Restate the agenda in your own words.

### Team Member Input

Summarize all of the important points raised by each team member. This is to ensure that key details are preserved for future meetings.

### Recommendation

Provide your expert recommendation regarding the agenda. You should consider the input from each team member, but you must also use your expertise to make a final decision and choose one option among several that may have been discussed. This decision can conflict with the input of some team members as long as it is well justified. It is essential that you provide a clear, specific, and actionable recommendation. Please justify your recommendation as well.

### Answers

For each agenda question, please provide the following:

Answer: A specific answer to the question based on your recommendation above.

Justification: A brief explanation of why you provided that answer.

### Next Steps

Outline the next steps that the team should take based on the discussion.

## Principal Investigator (Alzheimer's KG)

### Agenda

Define the technical specification for AlzKB, a scalable, retrieval-optimized Knowledge Graph for Alzheimer’s Disease research. The team must:
- Establish a schema core with six biologically specific node and edge types.
- Select four priority data sources and define an evidence/provenance scoring protocol.
- Define three quantitative KPIs for measuring KG coverage, precision, and ontology/validation compliance.
- All specifications must be AD-specific, ontology-driven, and enable fine-grained mechanistic hypothesis generation.

---

### Team Member Input

**Technical Lead:**  
- Advocated for distinct nodes for each PTM state (e.g., pTau181 as a separate node), parent-child relationships for isoforms/PTMs, and explicit provenance at the node/edge level.
- Emphasized use of property-graph compatible models; ambiguous PTMs should be their own nodes, clearly labeled and excluded by default from analyses.

**Biomedical Ontologist:**  
- Stressed alignment with formal ontologies: PSI-MOD for PTMs, UniProt/dbSNP for proteins/variants, Uberon/CL for anatomy/cell type.
- Required all schema elements and ambiguous PTMs to be ontology-mapped and tracked as unique nodes, with strict provenance and default analytic exclusion.

**Data Science Lead:**  
- Detailed extraction pipeline requirements: node-level resolution for PTMs/aggregates, extraction/QA of ambiguous PTMs as separate nodes, strict evidence/provenance tracking.
- Highlighted validation pipeline: ambiguous PTM instances are a tracked error class, default exclusion from analytics, and flagged for manual review.

**Scientific Critic:**  
- Demanded operational precision: distinct nodes for all PTMs/aggregates, no inference from ambiguous PTMs to site-specific nodes, and strict analytical/QA segregation.
- Mandated reporting of ambiguous PTMs as a KG quality metric and periodic manual audit.

---

### Recommendation

Adopt a node-centric, ontology-mapped schema with strong granularity for PTMs and aggregate morphologies. All ambiguous/underspecified PTM mentions will be instantiated as unique, labeled nodes—with provenance, strict analytic exclusion, and flagged for manual curation. All entities and relations must map to standard ontologies with unique identifiers. Evidence scoring and provenance tracking are required at the triple level, with full support for species, methodology, and source. Validation protocols must enforce precision, recall (stratified by node/edge type), and ontology compliance. This approach maximizes biological rigor, analytic precision, and future-proofing for data/model expansion.

---

### Answers

#### 1. PROPOSE SCHEMA

**Answer:**  
**Node Types:**  
1. Protein Isoform (site/PTM-resolved, e.g., pTau181, Tau-441)  
2. Gene Variant (e.g., APOE*ε4/rs429358, TREM2-R47H/rs75932628)  
3. Brain Region (Uberon/BRO-mapped)  
4. Cell Type (CL-mapped, subtype-supported)  
5. Clinical Phenotype (HPO/MONDO, diagnostic criteria-aligned)  
6. Biomarker Measurement (LOINC/SNOMED, with units/thresholds)

**Edge Types:**  
1. phosphorylates (RO:0002419)  
2. expressed_in (RO:0002206)  
3. aggregates_to (GO or custom IRI, aggregate-specific)  
4. modulates_risk_of (only with significant human evidence; MONDO/RO-mapped)  
5. measured_in  
6. infiltrates (RO:0002430)

**Justification:**  
Enables mechanistic, spatial, and clinical reasoning for AD; entities/edges are granular, ontology-mapped, and facilitate traceable, hypothesis-driven queries.

---

#### 2. DATA INGESTION

**Answer:**  
**Priority Data Sources:**  
- ADNI (clinical, imaging, biomarker gold standard)  
- AMP-AD Knowledge Portal (multi-omic, genetic, transcriptomic)  
- ROSMAP (postmortem, deep phenotyping, genomics)  
- UniProt (protein/isoform/PTM reference; PSI-MOD-mapped)

**Handling Conflicting Evidence:**  
- All edges/entities are annotated with full provenance: source, species (NCBI Taxon), evidence type (ECO), extraction confidence, and dataset version.
- Human clinical/postmortem evidence is prioritized for risk edges; animal and preclinical evidence are retained but never merged or upscored.
- Ambiguous/underspecified PTMs instantiated as separate “generic PTM” nodes, default-excluded from analyses and manually curated.

**Justification:**  
Ensures data completeness, species resolution, and analytic rigor; supports user filtering and downstream reproducibility.

---

#### 3. VALIDATION

**Answer:**  
- Gold standard: Manually curated set of 100 triples, stratified across all node/edge types, each cross-reviewed and linked to PubMed ID/dataset accession.
- Precision: (# correct KG triples matching gold standard) / (# KG triples evaluated); target >90%.
- Recall: (# gold standard triples present in KG) / (total # gold standard triples); stratified by node and edge type; target >60% initially.
- Ontology Coverage: % of KG entities/relations mapped to standard ontologies; target >90%.

**Justification:**  
Manual curation ensures accuracy and guards against spurious associations. Stratified KPIs surface extraction/systematic biases and enable continuous QA.

---

### Next Steps

1. Finalize schema with explicit ontology mappings for all node/edge types, including standard IRIs/CURIEs for PTMs/aggregates.
2. Implement extraction/ingestion pipeline with logic for PTM- and aggregate-specific node creation, provenance annotation, and ambiguous PTM handling.
3. Build and curate the 100-triple gold standard set, stratified by node/edge type, for initial validation and extraction QA.
4. Develop query/analytic filters to default-exclude ambiguous PTM nodes and support transparent evidence-based reasoning.
5. Establish versioning and manual curation workflows for ambiguous PTM node resolution and audit.
6. Track and report ambiguous PTM frequency as a KG quality metric in routine QA.

---


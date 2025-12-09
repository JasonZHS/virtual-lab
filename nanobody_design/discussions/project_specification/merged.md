## User

This is the beginning of an individual meeting with Principal Investigator (Alzheimer's KG) to discuss your research project.

Here are summaries of the previous meetings:

[begin summary 1]

### Agenda

Define the technical specification for the Alzheimer’s Knowledge Base (AlzKB) Knowledge Graph. This includes: (1) establishing a biologically precise schema (top 6 node and edge types) optimized for AD-specific reasoning; (2) selecting 4 high-confidence, multi-modal data sources and specifying an explicit evidence scoring and conflict-handling strategy; (3) setting quantitative KPIs and a gold standard for precision and recall. All technical constraints must prioritize AD-specific nuances (e.g., tau isoforms, evidence provenance, ontology mapping).

---

### Team Member Input

**Scientific Critic (AlzKB):**
- Advocated for granular, AD-specific node/edge types (e.g., tau isoforms, explicit PTMs).
- Stressed strict evidence tagging (species, evidence type, provenance) and non-collapsing of conflicting evidence.
- Supported blocking unmapped terms at ingestion to prevent semantic drift.

**Tech Lead (AlzKB Engineering):**
- Emphasized schema enforcement at the database level and fail-fast ETL pipelines.
- Supported strict ontology mapping at ingestion for production; suggested a possible staging area for unmapped terms.
- Highlighted the need for automated checks and a backlog for unmapped but high-value terms.

**Data Curator (AlzKB Ontologies):**
- Required all nodes/edges to be mapped to standard ontologies (HGNC, UniProt, GO, HPO, UMLS, RadLex, LOINC, SIO, ECO).
- Supported blocking unmapped terms at ingestion, with a rapid triage process for ontology extension.
- Advocated for transparent versioning and tracking of unmapped terms.

**Data Quality & Validation Scientist:**
- Prioritized data quality, unambiguous entity resolution, and evidence/provenance completeness.
- Strongly supported blocking unmapped terms at ingestion and maintaining a staging area for provisional terms if needed.
- Recommended quarterly review and update of the gold standard.

---

### Recommendation

**Adopt a strictly enforced, ontology-mapped schema with 6 biologically precise node and edge types, blocking unmapped terms at ingestion for production.**  
- All imported data must be mapped to standard ontologies (HGNC, UniProt, GO, HPO, UMLS, RadLex, LOINC, SIO, ECO).
- Use ADNI, AMP-AD, GWAS Catalog, and UniProt/PhosphoSitePlus as Day 1 data sources.
- All edges must carry explicit evidence metadata (species, evidence type, provenance, evidence score).
- Contradictory evidence is modeled as parallel edges with full provenance and evidence scoring.
- Validation is based on a 100-triple, manually curated, ontology-mapped gold standard; KPIs are Precision@100, Recall@100, and Ontology Mapping Error Rate.
- Maintain a rapid triage process and backlog for unmapped terms, but do not admit them into the production KG.

**Justification:**  
This approach maximizes data quality, semantic interoperability, and hypothesis generation capability, while minimizing technical debt and ambiguity. It is aligned with FAIR principles and supports robust, reproducible downstream analytics.

---

### Answers

#### 1. PROPOSE SCHEMA

**Answer:**  
**Node Types:**  
1. Protein (UniProt ID, isoform/PTM annotated)  
2. Gene (HGNC ID, species-specific)  
3. Genetic Variant (rsID, zygosity, population context)  
4. Pathological Process (GO/MONDO mapped)  
5. Clinical Phenotype (HPO/UMLS mapped)  
6. Imaging Biomarker (RadLex/LOINC mapped)  

**Edge Types:**  
1. phosphorylates (Protein → Protein, site-specific, RO:0002411)  
2. cleaves (Protein → Protein, cleavage site, RO:0002211)  
3. regulates_expression_of (up/down, Variant/Gene/Protein → Gene/Protein, RO:0002212)  
4. induces_pathology (Protein/Variant → Pathological Process, OBO/GO mapped)  
5. is_biomarker_for (Imaging/Protein → Pathological Process/Clinical Phenotype, custom/OBO mapped)  
6. associated_with_phenotype (Gene/Variant/Protein → Clinical Phenotype, SIO:000628)  

**Justification:**  
These types capture the mechanistic, translational, and clinical axes essential for AD hypothesis generation, while ensuring semantic precision and interoperability.

---

#### 2. DATA INGESTION

**Answer:**  
**Day 1 Data Sources:**  
1. ADNI (clinical, imaging, CSF biomarkers)  
2. AMP-AD (omics, transcriptomics, proteomics)  
3. GWAS Catalog (AD-specific variants, effect sizes)  
4. UniProt/PhosphoSitePlus (protein isoforms, PTMs)  

**Evidence Handling:**  
- All statements must be tagged with species, evidence type (ECO code), provenance (PubMed/dataset), and evidence score (clinical > preclinical > in vitro).
- Contradictory evidence is retained as separate, fully annotated edges; no collapsing or averaging.
- Unmapped terms are blocked from production ingestion; maintained in a backlog for ontology extension.

**Justification:**  
These sources maximize coverage of AD-relevant modalities. Explicit evidence modeling preserves data integrity and supports nuanced querying.

---

#### 3. VALIDATION

**Answer:**  
**Gold Standard:**  
- 100 manually curated, ontology-mapped triples covering all schema types, with explicit provenance (PubMed/dataset).
- Reviewed by at least two domain experts and updated quarterly.

**KPIs:**  
1. Precision@100: % of top 100 graph triples matching gold standard.  
2. Recall@100: % of gold standard triples present in graph.  
3. Ontology Mapping Error Rate: % of node/edge mis-mappings in a 50-triple audit.

**Justification:**  
This ensures both breadth and correctness, with rigorous, reproducible metrics and continuous quality improvement.

---

### Next Steps

1. Finalize and document the schema (node/edge types, ontology mappings, evidence properties).
2. Implement ETL pipelines with fail-fast ontology mapping enforcement and error logging.
3. Curate and version the 100-triple gold standard.
4. Set up a triage workflow and backlog for unmapped terms.
5. Begin Day 1 data ingestion from prioritized sources, blocking unmapped terms from production.
6. Schedule quarterly gold standard review and update cycle.

[end summary 1]

Here is the agenda for the meeting:

Consolidate multiple summaries into one coherent answer. Rules: 1. Resolve contradictions by prioritizing Specificity and Evidence. 2. Explicitly cite which summary contributed which point. 3. Discard vague or redundant info.

As a reference, here is the agenda from those meetings, which must be addressed here as well:

Task: Build a scalable, retrieval-optimized Knowledge Graph for Alzheimer's Disease research.

TASK: Define the Technical Specification for AlzKB.
The team must agree on the architectural foundation before implementation.

OUTPUT REQUIREMENTS:
1. SCHEMA CORE: Define top 6 Entity Types and 6 Edge Types (Must be biologically specific, e.g., 'phosphorylates' not 'interacts').
2. DATA STRATEGY: Select 4 priority Data Sources (e.g., ADNI) and define the Evidence Scoring mechanism (e.g., 'Clinical vs. Preclinical').
3. SUCCESS METRICS: Define 3 quantitative KPIs for coverage and precision.

CONSTRAINTS: Be specific. No fluff. Prioritize AD-specific nuances (e.g., Tau isoforms).


As a reference, here are the agenda questions from those meetings, which must be answered here as well:

1. PROPOSE SCHEMA: List the top 6 Node Types and 6 specific Edge Types essential for AD reasoning. Justify why these support hypothesis generation.

2. DATA INGESTION: Which 4 external databases are critical for Day 1 import? How will we handle conflicting evidence (e.g., human vs. mouse data) in the graph structure?

3. VALIDATION: Define the 'Gold Standard'. How exactly will we measure Precision and Recall? (e.g., 'Manually curated dataset of 100 triples').



Principal Investigator (Alzheimer's KG), please provide your response to the agenda.

## Principal Investigator (Alzheimer's KG)

Certainly. Here is a consolidated, contradiction-resolved technical specification for the Alzheimer’s Knowledge Base (AlzKB) Knowledge Graph, directly addressing the agenda and referencing the prior summary as required.

---

## 1. SCHEMA CORE

**Top 6 Entity (Node) Types**  
(Sourced from Summary 1; all are mapped to standard ontologies for specificity and interoperability.)

1. **Protein**  
   - Mapped to UniProt ID, with explicit annotation for isoforms and post-translational modifications (PTMs).  
   - *Justification:* Captures tau isoforms, amyloid-beta variants, and PTM-specific biology critical for AD.

2. **Gene**  
   - Mapped to HGNC ID, species-specific.  
   - *Justification:* Enables linkage to genetic risk loci (e.g., APOE) and regulatory relationships.

3. **Genetic Variant**  
   - Mapped to dbSNP rsID, with zygosity and population context.  
   - *Justification:* Supports fine-grained association of GWAS hits and rare variants to AD phenotypes.

4. **Pathological Process**  
   - Mapped to GO/MONDO terms.  
   - *Justification:* Encodes disease mechanisms (e.g., tau aggregation, amyloid deposition) for mechanistic reasoning.

5. **Clinical Phenotype**  
   - Mapped to HPO/UMLS terms.  
   - *Justification:* Anchors the graph to observable patient-level outcomes (e.g., memory loss, cognitive decline).

6. **Imaging Biomarker**  
   - Mapped to RadLex/LOINC.  
   - *Justification:* Integrates neuroimaging features (e.g., hippocampal atrophy, amyloid PET) for translational research.

**Top 6 Edge Types**  
(Explicit, biologically meaningful relations; all mapped to Relation Ontology (RO), SIO, or custom OBO terms.)

1. **phosphorylates** (Protein → Protein, site-specific, RO:0002411)  
   - *Justification:* Captures kinase-substrate relationships (e.g., tau phosphorylation), central to AD pathology.

2. **cleaves** (Protein → Protein, cleavage site, RO:0002211)  
   - *Justification:* Models proteolytic processing (e.g., APP cleavage by BACE1), a key AD mechanism.

3. **regulates_expression_of** (up/down, Variant/Gene/Protein → Gene/Protein, RO:0002212)  
   - *Justification:* Encodes regulatory effects (e.g., APOE genotype on gene expression).

4. **induces_pathology** (Protein/Variant → Pathological Process, OBO/GO mapped)  
   - *Justification:* Links molecular events to disease mechanisms (e.g., Aβ oligomers → synaptic dysfunction).

5. **is_biomarker_for** (Imaging/Protein → Pathological Process/Clinical Phenotype, custom/OBO mapped)  
   - *Justification:* Connects measurable biomarkers to disease states and outcomes.

6. **associated_with_phenotype** (Gene/Variant/Protein → Clinical Phenotype, SIO:000628)  
   - *Justification:* Supports genotype-phenotype and protein-phenotype associations for hypothesis generation.

**Resolution:**  
- All node and edge types are strictly mapped to standard ontologies (Summary 1: Data Curator, Tech Lead, Data Quality Scientist).
- Unmapped terms are blocked from production ingestion (Summary 1: unanimous team agreement).
- This schema is biologically precise and optimized for AD-specific reasoning, supporting mechanistic, translational, and clinical queries.

---

## 2. DATA STRATEGY

**Day 1 Data Sources**  
(Selected for high-confidence, multi-modal AD coverage; from Summary 1.)

1. **ADNI** (Alzheimer’s Disease Neuroimaging Initiative)  
   - Clinical, imaging, CSF biomarkers.

2. **AMP-AD** (Accelerating Medicines Partnership - Alzheimer’s Disease)  
   - Omics, transcriptomics, proteomics.

3. **GWAS Catalog**  
   - AD-specific variants, effect sizes.

4. **UniProt/PhosphoSitePlus**  
   - Protein isoforms, PTMs.

**Evidence Scoring and Conflict Handling**  
- **All edges/statements must be tagged with:**
  - Species (human, mouse, etc.)
  - Evidence type (ECO code: e.g., clinical, preclinical, in vitro)
  - Provenance (PubMed ID, dataset accession)
  - Evidence score (clinical > preclinical > in vitro, with explicit scoring rubric)
- **Contradictory evidence is modeled as parallel edges** with full provenance and evidence scoring; no collapsing or averaging (Summary 1: Scientific Critic, Data Quality Scientist).
- **Unmapped terms are blocked at ingestion** for production; a triage/backlog process is maintained for ontology extension (Summary 1: Tech Lead, Data Curator).

**Resolution:**  
- This approach maximizes data quality, preserves provenance, and enables nuanced, evidence-weighted queries.
- Prioritizes AD-specific nuances (e.g., tau isoforms, species differences).

---

## 3. SUCCESS METRICS

**Gold Standard**  
- **100 manually curated, ontology-mapped triples** covering all schema types, with explicit provenance (PubMed/dataset).
- Reviewed by at least two domain experts and updated quarterly (Summary 1: Data Quality Scientist).

**KPIs**  
1. **Precision@100:** % of top 100 graph triples matching the gold standard.
2. **Recall@100:** % of gold standard triples present in the graph.
3. **Ontology Mapping Error Rate:** % of node/edge mis-mappings in a 50-triple audit.

**Resolution:**  
- These metrics are quantitative, reproducible, and directly tied to data quality and semantic correctness (Summary 1: Data Quality Scientist).
- The gold standard ensures both breadth and correctness, with continuous improvement via quarterly review.

---

## References to Summary Contributions

- **Schema specificity, ontology mapping, and evidence modeling:** Summary 1 (Scientific Critic, Data Curator, Tech Lead, Data Quality Scientist)
- **Data source prioritization and evidence handling:** Summary 1 (Tech Lead, Scientific Critic)
- **Validation, gold standard, and KPIs:** Summary 1 (Data Quality Scientist, Data Curator)

**All vague or redundant information has been omitted. Only biologically specific, AD-relevant, and evidence-backed schema elements and processes are retained.**

---

## Final Technical Specification (for Implementation)

**1. Schema:**  
- 6 node types (Protein, Gene, Genetic Variant, Pathological Process, Clinical Phenotype, Imaging Biomarker), all mapped to standard ontologies.
- 6 edge types (phosphorylates, cleaves, regulates_expression_of, induces_pathology, is_biomarker_for, associated_with_phenotype), all mapped to RO/SIO/OBO.

**2. Data Ingestion:**  
- Day 1 sources: ADNI, AMP-AD, GWAS Catalog, UniProt/PhosphoSitePlus.
- Strict evidence tagging (species, evidence type, provenance, evidence score).
- Contradictory evidence retained as parallel, fully annotated edges.
- Unmapped terms blocked from production; triage workflow for ontology extension.

**3. Validation:**  
- 100-triple, manually curated, ontology-mapped gold standard.
- KPIs: Precision@100, Recall@100, Ontology Mapping Error Rate.
- Quarterly gold standard review and update.

**This architecture is optimized for scalable, retrieval-optimized, AD-specific knowledge discovery and hypothesis generation.**

## User

Scientific Critic (AlzKB), please critique Principal Investigator (Alzheimer's KG)'s most recent answer. In your critique, suggest improvements that directly address the agenda and any agenda questions. Prioritize simple solutions over unnecessarily complex ones, but demand more detail where detail is lacking. Additionally, validate whether the answer strictly adheres to the agenda and any agenda questions and provide corrective feedback if it does not. Only provide feedback; do not implement the answer yourself.

## Scientific Critic (AlzKB)

Certainly. Here is a detailed critique of the Principal Investigator’s (PI) most recent answer, structured by agenda item and with explicit attention to the requirements of the agenda and agenda questions.

---

## 1. SCHEMA CORE

**Strengths:**
- The PI correctly rejects generic node/edge types and provides biologically specific entities and relations (e.g., ‘phosphorylates’, ‘cleaves’).
- All node/edge types are mapped to standard ontologies, which is essential for semantic precision and interoperability.
- Explicit justification for each node/edge type is provided, with AD-specific rationale (e.g., tau isoforms, amyloid-beta variants).

**Critique & Suggestions:**
- **Edge Granularity:** While the edge types are specific, the answer does not clarify how site-specificity (e.g., phosphorylation at tau S202 vs. S396) will be represented in the schema. This is critical for AD, where PTM site matters. Suggestion: Explicitly require site annotation as an edge property, not just as a free-text note.
- **Entity Resolution:** The answer does not address how the KG will distinguish between closely related entities (e.g., Abeta40 vs. Abeta42, or tau isoforms). Suggestion: Mandate that all protein nodes include isoform/PTM identifiers where available, and that ingestion pipelines enforce this distinction.
- **Ontology Mapping Failures:** The answer mentions blocking unmapped terms but does not specify what happens if a high-value AD-specific term is missing from all reference ontologies. Suggestion: Require a rapid triage and provisional mapping protocol, with a clear SLA (e.g., 48 hours) for review.

---

## 2. DATA STRATEGY

**Strengths:**
- The four data sources are well-chosen and cover the necessary modalities for AD research.
- The answer mandates explicit evidence tagging (species, evidence type, provenance, evidence score) and retention of contradictory evidence as parallel edges.

**Critique & Suggestions:**
- **Evidence Scoring:** The answer states “clinical > preclinical > in vitro” but does not specify how evidence scores are computed or normalized across sources. Suggestion: Define a simple, reproducible scoring rubric (e.g., clinical = 3, preclinical = 2, in vitro = 1) and require that all evidence scores be explicitly stored as edge properties.
- **Species Disambiguation:** The answer says species must be tagged, but does not specify how the KG will prevent conflation of murine and human data in downstream queries. Suggestion: Require that all nodes and edges include a ‘species’ property and that queries default to human-only unless otherwise specified.
- **Provenance Enforcement:** The answer requires provenance but does not specify how missing or ambiguous provenance is handled at ingestion. Suggestion: Block any triple lacking a PubMed ID or dataset accession from production ingestion.

---

## 3. SUCCESS METRICS

**Strengths:**
- The gold standard is well-defined (100 manually curated triples, quarterly review).
- KPIs are quantitative and directly tied to the gold standard.

**Critique & Suggestions:**
- **Gold Standard Coverage:** The answer does not specify how the 100 gold standard triples will be distributed across node and edge types. Suggestion: Require that the gold standard covers all node/edge types proportionally to ensure comprehensive validation.
- **Audit Process:** The answer mentions a 50-triple audit for ontology mapping error rate but does not specify who performs the audit or how discrepancies are resolved. Suggestion: Require dual curation with adjudication for disagreements.
- **Metric Transparency:** The answer does not specify how Precision@100 and Recall@100 will be calculated in the presence of contradictory or ambiguous evidence. Suggestion: Define clear rules for matching (e.g., exact ontology match, species match, evidence provenance match).

---

## GENERAL ADHERENCE TO AGENDA

**Strengths:**
- The answer is specific, avoids vague language, and prioritizes AD-specific nuances.
- All agenda questions are addressed, and redundant information is minimized.

**Areas for Improvement:**
- **Detail:** Some implementation details are missing (see above: evidence scoring rubric, site-specificity, species handling).
- **Simplicity:** The answer is clear but could be more actionable by providing explicit property lists for nodes/edges and simple rules for ingestion and validation.

---

## SUMMARY OF CORRECTIVE FEEDBACK

1. **Schema:**  
   - Explicitly require site/PTM/isoform annotation as structured properties.
   - Enforce strict entity resolution for closely related proteins/isoforms.
   - Define a rapid triage protocol for unmapped but high-value terms.

2. **Data Strategy:**  
   - Specify a reproducible evidence scoring rubric.
   - Require species as a mandatory property and default queries to human data.
   - Block ingestion of triples lacking explicit provenance.

3. **Validation:**  
   - Ensure gold standard covers all schema types.
   - Define dual curation and adjudication for audits.
   - Specify matching rules for KPIs in the presence of contradictory evidence.

**In summary:** The answer is strong and agenda-aligned but requires more operational detail and explicit enforcement mechanisms to ensure biological precision, provenance, and reproducibility.

## User

Principal Investigator (Alzheimer's KG), please modify your answer to address Scientific Critic (AlzKB)'s most recent feedback. Remember that your ultimate goal is to make improvements that better address the agenda.

## Principal Investigator (Alzheimer's KG)

Thank you for the detailed critique. Below is a revised technical specification for the Alzheimer’s Knowledge Base (AlzKB) Knowledge Graph, directly addressing all feedback and further aligning with the agenda and agenda questions.

---

## 1. SCHEMA CORE (with Enhanced Detail and Enforcement)

**Top 6 Entity (Node) Types**  
(All mapped to standard ontologies; explicit property lists and entity resolution rules included.)

1. **Protein**  
   - **Properties:** UniProt ID, isoform ID, PTM type, PTM site (e.g., S202, T231), species, full name, synonyms.  
   - **Entity Resolution:** Distinct nodes for each isoform and PTM site (e.g., MAPT-isoform-2, tau-pS202).  
   - **Ontology:** UniProt, PSI-MOD.

2. **Gene**  
   - **Properties:** HGNC ID, species, gene symbol, synonyms.  
   - **Entity Resolution:** Species-specific; no cross-species merging.  
   - **Ontology:** HGNC.

3. **Genetic Variant**  
   - **Properties:** dbSNP rsID, zygosity, population, associated gene, species.  
   - **Entity Resolution:** Unique node per rsID/species.  
   - **Ontology:** dbSNP, ClinVar.

4. **Pathological Process**  
   - **Properties:** GO/MONDO ID, process name, synonyms, species (if applicable).  
   - **Entity Resolution:** Strict mapping to GO/MONDO; no free-text.  
   - **Ontology:** GO, MONDO.

5. **Clinical Phenotype**  
   - **Properties:** HPO/UMLS ID, phenotype name, synonyms.  
   - **Entity Resolution:** Strict mapping to HPO/UMLS.  
   - **Ontology:** HPO, UMLS.

6. **Imaging Biomarker**  
   - **Properties:** RadLex/LOINC ID, biomarker name, imaging modality, anatomical region, species.  
   - **Entity Resolution:** Distinct nodes for each imaging modality and anatomical region.  
   - **Ontology:** RadLex, LOINC.

**Top 6 Edge Types**  
(All mapped to RO/SIO/OBO; explicit property lists and site-specificity enforced.)

1. **phosphorylates** (Protein → Protein)  
   - **Properties:** Site (e.g., S202), evidence type, species, provenance, evidence score.  
   - **Ontology:** RO:0002411.

2. **cleaves** (Protein → Protein)  
   - **Properties:** Cleavage site, evidence type, species, provenance, evidence score.  
   - **Ontology:** RO:0002211.

3. **regulates_expression_of** (Variant/Gene/Protein → Gene/Protein)  
   - **Properties:** Direction (up/down), evidence type, species, provenance, evidence score.  
   - **Ontology:** RO:0002212.

4. **induces_pathology** (Protein/Variant → Pathological Process)  
   - **Properties:** Evidence type, species, provenance, evidence score.  
   - **Ontology:** Custom OBO/GO.

5. **is_biomarker_for** (Imaging/Protein → Pathological Process/Clinical Phenotype)  
   - **Properties:** Evidence type, species, provenance, evidence score.  
   - **Ontology:** Custom OBO.

6. **associated_with_phenotype** (Gene/Variant/Protein → Clinical Phenotype)  
   - **Properties:** Evidence type, species, provenance, evidence score.  
   - **Ontology:** SIO:000628.

**Additional Enforcement:**
- **Site/PTM/isoform annotation is mandatory** for all relevant nodes and edges.
- **Species is a required property** for all nodes and edges.
- **Unmapped terms:** If a high-value AD-specific term is not in any reference ontology, it is triaged within 48 hours for provisional mapping or ontology extension (with tracking and versioning).

---

## 2. DATA STRATEGY (with Explicit Scoring and Provenance Rules)

**Day 1 Data Sources**  
(As previously specified, with explicit ingestion rules.)

1. **ADNI** (clinical, imaging, CSF biomarkers)
2. **AMP-AD** (omics, transcriptomics, proteomics)
3. **GWAS Catalog** (AD-specific variants, effect sizes)
4. **UniProt/PhosphoSitePlus** (protein isoforms, PTMs)

**Evidence Scoring Rubric:**  
- **Clinical (human, peer-reviewed, in vivo):** Score = 3  
- **Preclinical (animal model, in vivo):** Score = 2  
- **In vitro/cell line:** Score = 1  
- **Computational prediction:** Score = 0.5  
- **Multiple evidence types:** Store all scores and provenance as parallel edges.

**Provenance Enforcement:**  
- **Mandatory:** PubMed ID or dataset accession for every edge.  
- **Block:** Any triple lacking explicit provenance from production ingestion.

**Species Handling:**  
- **Species is a required property** on all nodes and edges.
- **Default queries return human-only data** unless otherwise specified.
- **No merging of cross-species data**; parallel edges for different species.

**Contradictory Evidence:**  
- **Retained as parallel edges** with full provenance and evidence score.
- **No collapsing or averaging** of contradictory statements.

---

## 3. SUCCESS METRICS (with Comprehensive Coverage and Audit Protocol)

**Gold Standard:**  
- **100 manually curated, ontology-mapped triples**  
  - **Distribution:** At least 15 triples per node/edge type (ensuring all schema types are covered).
  - **Review:** Dual curation by two domain experts; disagreements adjudicated by a third.
  - **Update:** Quarterly review and update cycle.

**KPIs:**  
1. **Precision@100:** % of top 100 graph triples (by evidence score) that exactly match the gold standard (ontology, species, provenance).
2. **Recall@100:** % of gold standard triples present in the graph (exact match required).
3. **Ontology Mapping Error Rate:** % of node/edge mis-mappings in a randomly sampled 50-triple audit (dual curation, adjudication for discrepancies).

**Matching Rules for Validation:**  
- **Exact ontology match, species match, and provenance match** required for a triple to be counted as correct.
- **Contradictory evidence:** Each edge is validated independently; only exact matches count toward precision/recall.

---

## SUMMARY OF IMPROVEMENTS

- **Schema:** Now mandates site/PTM/isoform annotation, strict entity resolution, and a 48-hour triage protocol for unmapped terms.
- **Data Strategy:** Defines a clear, reproducible evidence scoring rubric; requires species as a property; blocks ingestion of triples without provenance.
- **Validation:** Ensures gold standard covers all schema types, dual curation with adjudication, and explicit matching rules for KPIs.

---

**This revised specification is now fully actionable, operationally detailed, and strictly aligned with the agenda and all agenda questions, with explicit enforcement mechanisms for biological precision, provenance, and reproducibility.**

## User

Scientific Critic (AlzKB), please critique Principal Investigator (Alzheimer's KG)'s most recent answer. In your critique, suggest improvements that directly address the agenda and any agenda questions. Prioritize simple solutions over unnecessarily complex ones, but demand more detail where detail is lacking. Additionally, validate whether the answer strictly adheres to the agenda and any agenda questions and provide corrective feedback if it does not. Only provide feedback; do not implement the answer yourself.

## Scientific Critic (AlzKB)

Certainly. Here is a structured critique of the Principal Investigator’s (PI) revised answer, with focused suggestions for further improvement and explicit validation against the agenda and agenda questions.

---

## 1. SCHEMA CORE

**Strengths:**
- The PI now mandates explicit site/PTM/isoform annotation and provides clear property lists for each node and edge type.
- Entity resolution rules are well-articulated, especially for isoforms and species.
- The 48-hour triage protocol for unmapped terms is a concrete, actionable improvement.

**Areas for Improvement:**
- **Edge Property Enforcement:** While site/PTM/isoform annotation is “mandatory,” the answer does not specify how this is enforced at the ETL or database level. Suggestion: Require automated validation scripts that reject edges lacking these properties for relevant relations (e.g., ‘phosphorylates’ must have a site).
- **Ontology Versioning:** The answer does not mention how ontology versioning will be tracked for each node/edge. Suggestion: Add a property for ontology version/date to each node/edge to ensure reproducibility.
- **Ambiguity in “Custom OBO”:** For some edge types, “custom OBO” is referenced. This is vague. Suggestion: Specify the process for creating and documenting custom relations, including mapping to existing ontologies when possible.

---

## 2. DATA STRATEGY

**Strengths:**
- The evidence scoring rubric is now explicit and simple.
- Provenance requirements are clear and strict.
- Species handling is robust, with default queries returning human data.

**Areas for Improvement:**
- **Evidence Score Normalization:** The rubric is clear, but there is no mention of how to handle multiple evidence scores for a single edge (e.g., if both clinical and preclinical evidence exist for the same relation). Suggestion: Specify whether these are stored as separate edges or as a list of evidence objects on a single edge, and how queries should aggregate or prioritize them.
- **Handling of Missing Data:** The answer blocks triples lacking provenance, but does not address how to handle missing or ambiguous species information. Suggestion: Also block or flag triples with missing species, and require explicit curation before admission.
- **Data Source Updates:** There is no mention of how updates or new releases from the four Day 1 sources will be handled. Suggestion: Briefly outline a process for periodic data source updates and re-ingestion, with version tracking.

---

## 3. SUCCESS METRICS

**Strengths:**
- The gold standard now covers all schema types and mandates dual curation with adjudication.
- Matching rules for validation are explicit and rigorous.

**Areas for Improvement:**
- **Gold Standard Transparency:** The answer does not specify how the gold standard triples will be made available for audit or external review. Suggestion: Commit to publishing the gold standard triples (with provenance) for transparency and community feedback.
- **Audit Frequency:** Quarterly review is good, but there is no mention of what triggers an ad hoc review (e.g., major ontology update or new data source). Suggestion: Add a clause for ad hoc review in response to major changes.

---

## GENERAL ADHERENCE TO AGENDA

**Strengths:**
- The answer is now highly specific, operational, and directly addresses all agenda questions.
- AD-specific nuances (e.g., tau isoforms, species, evidence provenance) are prioritized.
- No vague or redundant information remains.

**Areas for Improvement:**
- **Simplicity:** The answer is clear, but could be even more actionable by providing example triples (e.g., a fully specified ‘phosphorylates’ edge with all required properties).
- **Implementation Readiness:** While the answer is operational, it would benefit from a brief summary of minimal technical requirements for ETL and validation (e.g., “All ETL scripts must validate property completeness and ontology mapping before ingestion”).

---

## SUMMARY OF CORRECTIVE FEEDBACK

1. **Schema:**  
   - Require automated enforcement of mandatory properties at ETL/database level.
   - Add ontology version/date as a property for all nodes/edges.
   - Clarify the process for “custom OBO” relations.

2. **Data Strategy:**  
   - Specify handling of multiple evidence scores for a single edge.
   - Block or flag triples with missing species information.
   - Outline a process for periodic data source updates and version tracking.

3. **Validation:**  
   - Commit to publishing the gold standard for transparency.
   - Add provision for ad hoc gold standard review after major changes.
   - Provide example triples for each edge type to clarify property requirements.

4. **Implementation:**  
   - Summarize minimal technical requirements for ETL/validation to ensure all rules are enforceable.

**In summary:**  
The revised answer is much improved and closely aligned with the agenda. The remaining gaps are in operational enforcement, transparency, and minor clarifications. Addressing these will ensure the AlzKB KG is both biologically precise and technically robust.

## User

Principal Investigator (Alzheimer's KG), please modify your answer to address Scientific Critic (AlzKB)'s most recent feedback. Remember that your ultimate goal is to make improvements that better address the agenda.

## Principal Investigator (Alzheimer's KG)

Thank you for the precise and actionable feedback. Below is a further revised technical specification for the Alzheimer’s Knowledge Base (AlzKB) Knowledge Graph, now incorporating all requested operational, transparency, and enforcement details to fully address the agenda and agenda questions.

---

## 1. SCHEMA CORE (with Enforcement, Versioning, and Examples)

**Top 6 Entity (Node) Types**  
(All mapped to standard ontologies; explicit property lists, entity resolution, and ontology versioning.)

| Node Type           | Required Properties                                                                                   | Ontology/ID Source      | Example                                                                                           |
|---------------------|------------------------------------------------------------------------------------------------------|-------------------------|---------------------------------------------------------------------------------------------------|
| Protein             | UniProt ID, isoform ID, PTM type, PTM site, species, full name, synonyms, ontology version/date      | UniProt, PSI-MOD        | UniProt:P10636-8 (MAPT isoform 8), PTM: pS202, species: human, ontology version: 2024-04-01       |
| Gene                | HGNC ID, species, gene symbol, synonyms, ontology version/date                                       | HGNC                    | HGNC:6893 (MAPT), species: human, ontology version: 2024-04-01                                    |
| Genetic Variant     | dbSNP rsID, zygosity, population, associated gene, species, ontology version/date                    | dbSNP, ClinVar          | rs429358, zygosity: heterozygous, gene: APOE, species: human, ontology version: 2024-04-01        |
| Pathological Process| GO/MONDO ID, process name, synonyms, species (if applicable), ontology version/date                  | GO, MONDO               | GO:0050435 (amyloid-beta clearance), ontology version: 2024-04-01                                 |
| Clinical Phenotype  | HPO/UMLS ID, phenotype name, synonyms, ontology version/date                                         | HPO, UMLS               | HPO:0002354 (memory impairment), ontology version: 2024-04-01                                     |
| Imaging Biomarker   | RadLex/LOINC ID, biomarker name, imaging modality, anatomical region, species, ontology version/date | RadLex, LOINC           | RadLex:RID10341 (hippocampal atrophy), modality: MRI, species: human, ontology version: 2024-04-01|

**Entity Resolution and Enforcement:**
- **Distinct nodes** for each isoform, PTM, and species.
- **Automated ETL validation:** All required properties must be present; missing properties result in rejection and error logging.
- **Ontology version/date** is a required property for all nodes.

**Custom OBO Relations:**
- **Process:** If a required relation is not present in existing ontologies, a provisional custom relation is created, documented, and submitted for ontology extension within 48 hours. All custom relations are versioned and tracked.

---

**Top 6 Edge Types**  
(All mapped to RO/SIO/OBO; explicit property lists, site-specificity, and ontology versioning.)

| Edge Type                  | Source → Target                   | Required Properties                                                                                  | Ontology/ID Source     | Example                                                                                                   |
|----------------------------|-----------------------------------|------------------------------------------------------------------------------------------------------|------------------------|-----------------------------------------------------------------------------------------------------------|
| phosphorylates             | Protein → Protein                 | Site, evidence type, species, provenance, evidence score, ontology version/date                      | RO:0002411             | MAPT-pS202 (human) phosphorylates MAPT (human), evidence: clinical, PubMed:123456, score: 3, version: ... |
| cleaves                    | Protein → Protein                 | Cleavage site, evidence type, species, provenance, evidence score, ontology version/date             | RO:0002211             | BACE1 (human) cleaves APP at Asp1, evidence: preclinical, PubMed:234567, score: 2, version: ...           |
| regulates_expression_of    | Variant/Gene/Protein → Gene/Protein| Direction, evidence type, species, provenance, evidence score, ontology version/date                 | RO:0002212             | rs429358 (human) downregulates APOE, evidence: clinical, PubMed:345678, score: 3, version: ...            |
| induces_pathology          | Protein/Variant → Pathological Process| Evidence type, species, provenance, evidence score, ontology version/date                         | Custom OBO/GO          | Aβ42 (human) induces amyloid plaque formation, evidence: preclinical, PubMed:456789, score: 2, version:...|
| is_biomarker_for           | Imaging/Protein → Pathological Process/Clinical Phenotype| Evidence type, species, provenance, evidence score, ontology version/date| Custom OBO              | Hippocampal atrophy (MRI, human) is biomarker for memory impairment, evidence: clinical, PubMed:567890... |
| associated_with_phenotype  | Gene/Variant/Protein → Clinical Phenotype| Evidence type, species, provenance, evidence score, ontology version/date                 | SIO:000628             | APOE ε4 (human) associated with memory impairment, evidence: clinical, PubMed:678901, score: 3, version:...|

**Edge Enforcement:**
- **Automated ETL validation:** All required properties must be present for ingestion; missing properties result in rejection and error logging.
- **Ontology version/date** is a required property for all edges.
- **Site/PTM/isoform annotation is enforced** for relevant edges (e.g., ‘phosphorylates’ must specify site).

---

## 2. DATA STRATEGY (with Evidence Aggregation, Missing Data Handling, and Updates)

**Day 1 Data Sources**  
(As previously specified; now with update/version tracking.)

1. **ADNI** (clinical, imaging, CSF biomarkers) – version and release date tracked.
2. **AMP-AD** (omics, transcriptomics, proteomics) – version and release date tracked.
3. **GWAS Catalog** (AD-specific variants, effect sizes) – version and release date tracked.
4. **UniProt/PhosphoSitePlus** (protein isoforms, PTMs) – version and release date tracked.

**Evidence Scoring and Aggregation:**
- **Scoring rubric:**  
  - Clinical (human, in vivo): 3  
  - Preclinical (animal, in vivo): 2  
  - In vitro/cell line: 1  
  - Computational: 0.5
- **Multiple evidence scores:**  
  - Each evidence instance is stored as a separate edge with its own provenance and score.
  - Queries can aggregate evidence by counting, filtering, or prioritizing by score.
- **Provenance enforcement:**  
  - **Mandatory:** PubMed ID or dataset accession for every edge.
  - **Block:** Any triple lacking explicit provenance or species from production ingestion.
- **Species handling:**  
  - **Species is a required property** on all nodes and edges.
  - **Default queries return human-only data** unless otherwise specified.
  - **No merging of cross-species data;** parallel edges for different species.
- **Data source updates:**  
  - **Quarterly scheduled updates** for all Day 1 sources.
  - **Version and release date** of each data source is tracked for every ingested record.
  - **Ad hoc updates** triggered by major data releases or critical corrections.

---

## 3. SUCCESS METRICS (with Transparency, Audit, and Example)

**Gold Standard:**  
- **100 manually curated, ontology-mapped triples**  
  - **Distribution:** At least 15 triples per node/edge type.
  - **Review:** Dual curation by two domain experts; disagreements adjudicated by a third.
  - **Update:** Quarterly review and update cycle.
  - **Ad hoc review:** Triggered by major ontology updates or new data source releases.
  - **Transparency:** Gold standard triples (with provenance) are published and versioned for external audit and community feedback.

**KPIs:**  
1. **Precision@100:** % of top 100 graph triples (by evidence score) that exactly match the gold standard (ontology, species, provenance, version).
2. **Recall@100:** % of gold standard triples present in the graph (exact match required).
3. **Ontology Mapping Error Rate:** % of node/edge mis-mappings in a randomly sampled 50-triple audit (dual curation, adjudication for discrepancies).

**Matching Rules for Validation:**  
- **Exact ontology match, species match, provenance match, and ontology version match** required for a triple to be counted as correct.
- **Contradictory evidence:** Each edge is validated independently; only exact matches count toward precision/recall.

**Example Gold Standard Triple:**  
- **Edge:** MAPT-pS202 (human) phosphorylates MAPT (human)  
- **Properties:** Site: S202, evidence type: clinical, species: human, provenance: PubMed:123456, evidence score: 3, ontology version: 2024-04-01

---

## 4. IMPLEMENTATION REQUIREMENTS (ETL/Validation)

- **All ETL scripts must validate:**
  - Presence and correctness of all required properties (including ontology version/date).
  - Strict ontology mapping (block unmapped terms).
  - Species and provenance completeness.
  - Site/PTM/isoform annotation for relevant nodes/edges.
- **Automated error logging and rejection** for any record failing validation.
- **Custom relation creation** must be documented and submitted for ontology extension within 48 hours.
- **All ingestion and validation rules are version-controlled and auditable.**

---

## SUMMARY OF IMPROVEMENTS

- **Automated enforcement** of all schema and property requirements at ETL/database level.
- **Ontology versioning** is now a required property for all nodes/edges.
- **Custom OBO relations** are documented, versioned, and submitted for extension.
- **Evidence aggregation** is explicit; multiple evidence instances are stored as separate edges.
- **Missing species/provenance** blocks ingestion; all data source versions tracked.
- **Gold standard is published** for transparency; ad hoc review is triggered by major changes.
- **Example triples** clarify property requirements.
- **Minimal technical requirements** for ETL/validation are summarized for implementation readiness.

---

**This specification is now fully actionable, transparent, and strictly adheres to the agenda, with clear operational enforcement, versioning, and validation protocols to ensure biological precision, provenance, and reproducibility for Alzheimer’s Disease knowledge discovery.**


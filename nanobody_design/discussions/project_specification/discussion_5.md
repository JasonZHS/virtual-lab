## User

This is the beginning of a team meeting to discuss your research project. This is a meeting with the team lead, Principal Investigator (Alzheimer's KG), and the following team members: Technical Lead (Knowledge Graph Engineering), Biomedical Ontologist (AlzKB Semantics & Standards), Data Science Lead (Extraction & Validation), Scientific Critic (AlzKB).

Here is the agenda for the meeting:

Task: Build a scalable, retrieval-optimized Knowledge Graph for Alzheimer's Disease research.

TASK: Define the Technical Specification for AlzKB.
The team must agree on the architectural foundation before implementation.

OUTPUT REQUIREMENTS:
1. SCHEMA CORE.
2. DATA STRATEGY.
3. SUCCESS METRICS.

CONSTRAINTS: Be specific. No fluff. Prioritize AD-specific nuances (e.g., Tau isoforms).


Principal Investigator (Alzheimer's KG) will convene the meeting. Then, each team member will provide their thoughts on the discussion one-by-one in the order above. After all team members have given their input, Principal Investigator (Alzheimer's KG) will Synthesize team inputs. 1. Identify agreements vs. conflicts. 2. Resolve conflicts using provided evidence; favor data over opinion. 3. Decide the agenda status. 4. Ask 1 concrete question to clarify ambiguity if needed. Be concise.. This will continue for 2 rounds. Once the discussion is complete, Principal Investigator (Alzheimer's KG) will summarize the meeting in detail for future discussions, provide a specific recommendation regarding the agenda, and answer the agenda questions (if any) based on the discussion while strictly adhering to the agenda rules (if any)..

## User

Principal Investigator (Alzheimer's KG), please provide your initial thoughts on the agenda as well as any questions you have to guide the discussion among the team members.

## Principal Investigator (Alzheimer's KG)

Thank you, team, for joining this critical kickoff meeting. Our objective is to define the **Technical Specification for AlzKB**, focusing on three deliverables: **Schema Core**, **Data Strategy**, and **Success Metrics**. Given the complexity of Alzheimer’s Disease (AD), it’s essential we are precise, especially around AD-specific features such as Tau isoforms, APOE allelic variation, and neuroimaging findings.

**Initial Thoughts & Guiding Questions:**

1. **Schema Core:**
   - We must base our schema on established ontologies (e.g., SNOMED CT for clinical phenotypes, Gene Ontology for molecular entities, Neuroimaging Data Model [NIDM] for imaging features).
   - Crucial to include entities for tau and amyloid pathology at granularity (e.g., tau isoforms, Braak stage, amyloid PET status), bridging molecular, imaging, and clinical data.
   - Relationships should capture causal, associative, and temporal aspects (e.g., “has biomarker,” “measured at timepoint,” “is risk factor for”).
   - Question: What minimum entity/relationship types must be present in version 1 to support advanced AD research queries?

2. **Data Strategy:**
   - High-confidence, well-curated sources only: ADNI, AMP-AD, ROSMAP, and peer-reviewed literature with structured datasets.
   - Extraction pipelines must prioritize precision over recall—better to miss an edge than to add a spurious one.
   - Plan for a pipeline that allows reproducible extraction, entity normalization (e.g., gene/protein IDs), and cross-modal harmonization (especially for imaging-genotype links).
   - Question: Which normalization standards and entity disambiguation protocols are most suitable for multi-modal AD datasets?

3. **Success Metrics:**
   - Must be objective, automatable, and AD-specific (e.g., coverage of known AD risk loci, number of validated tau isoform-pathology links).
   - Graph quality (precision of entity linking, rate of false associations), query performance (latency, subgraph retrieval time), and user-facing metrics (number of unique, valid clinical-imaging-genetic triples retrieved).
   - Question: Which 2–3 high-value metrics will most clearly demonstrate AlzKB’s utility to the AD research community?

**Request:**  
Each member, please address these three topics—**schema, data, metrics**—with explicit recommendations. Highlight any technical limitations, dependencies, or standards you see as critical for a scalable, retrieval-optimized Knowledge Graph, and identify any AD-specific nuances that must not be overlooked.

Let’s proceed in the order: Technical Lead → Biomedical Ontologist → Data Science Lead → Scientific Critic. I look forward to your detailed, evidence-based input.

## User

Technical Lead (Knowledge Graph Engineering), please provide your thoughts on the discussion (round 1 of 2). If you do not have anything new or relevant to add, you may say "pass". Remember that you can and should (politely) disagree with other team members if you have a different perspective.

## Technical Lead (Knowledge Graph Engineering)

**Technical Lead (Knowledge Graph Engineering) – Input (Round 1):**

**1. SCHEMA CORE**
- **Foundation:** Strongly recommend a hybrid schema design: OWL-based for semantic richness (interoperability with existing biomedical ontologies), mapped to a property-graph model (Neo4j) for performant, flexible querying.
- **Entities & Relationships:**  
  - **Required Entities:**  
    - *Molecular*: Gene (HGNC), Protein (UniProt/RefSeq), Tau isoform (with PTMs), Amyloid β peptide forms, SNPs (dbSNP/ClinVar).
    - *Clinical*: Subject, Diagnosis, Cognitive Assessment, Clinical Event (with timestamp), Medication, Comorbidity.
    - *Imaging*: Imaging Session, Imaging Modality (MRI, PET), Imaging Feature (Braak stage, SUVR, hippocampal volume).
    - *Study/Source*: Dataset, Publication, Provenance record.
  - **Relationships:**  
    - “expresses”, “has_variant”, “encodes”, “present_in_sample”, “imaged_with”, “diagnosed_with”, “measured_at”, “derived_from”, “linked_to_phenotype”, “has_provenance”.
  - **AD-Specifics:**  
    - Model Tau isoforms as first-class entities, with relationships to PTMs (e.g., phosphorylation site), spatial localization (e.g., brain region), and associated pathology.
    - Fine-grained time-resolved relationships for longitudinal data (e.g., cognitive decline trajectories, serial imaging).
    - Explicit representation of APOE alleles (ε2, ε3, ε4) as genotype entities, linked to risk/response.
- **Minimal viable schema (V1):** Molecular entity (Gene, Protein [with isoforms]), Clinical phenotype, Imaging feature, Subject, and Provenance; “measured_at”, “linked_to”, and “has_provenance” relationships.

**2. DATA STRATEGY**
- **Pipeline:**  
  - ETL pipelines for each prioritized dataset (ADNI, ROSMAP, AMP-AD), with modular adapters for new sources.
  - Use standardized vocabularies for entity resolution (HGNC, UniProt, UMLS, SNOMED CT, NIDM).
  - Provenance tracking at all ingestion points: dataset ID, extraction timestamp, transformation lineage.
- **Multi-modal Integration:**  
  - Harmonize subjects across datasets using hashed subject IDs with privacy-preserving linkage.
  - Imaging-genotype linkage: Direct mapping of imaging sessions to genotype/phenotype via subject IDs, with audit trails.
- **Entity Disambiguation:**  
  - Deploy entity resolution using canonical IDs (e.g., gene symbol+chromosome for genes, UniProt+isoform for proteins).
  - Leverage cross-references in ontologies for ambiguous cases (e.g., tau isoforms via UniProt/Ensembl/GO crosswalks).
- **Data Validation:**  
  - Automated schema validation and consistency checks at each ETL stage.

**3. SUCCESS METRICS**
- **Coverage:**  
  - % of known AD risk loci (e.g., from latest GWAS meta-analyses) represented.
  - # of unique tau isoform-pathology relationships captured.
- **Retrieval Performance:**  
  - Median query latency for cross-modal queries (e.g., “Find all subjects with tau imaging and confirmed MAPT variant” under 1s for 90% of queries).
- **Data Quality:**  
  - Precision of entity linking (>98% for genes/proteins; >95% for clinical events, validated via random audits).
- **Auditability:**  
  - 100% of entities and edges have associated provenance record (dataset/source/timestamp).

**Dependencies/Critical Notes:**
- Early engagement with data privacy team—subject identifier harmonization may require legal/ethical review.
- AD-specific: Must not conflate tau isoforms; explicitly represent PTMs and brain-region localization.
- Prioritize graph schema extensibility; anticipate future addition of single-cell, spatial omics, or digital pathology.

**Summary:**  
Recommend a semantically rich, retrieval-optimized, provenance-centric graph foundation, aggressive entity normalization, and AD-tailored metrics. Happy to clarify any aspect or provide implementation sketches as needed.

## User

Biomedical Ontologist (AlzKB Semantics & Standards), please provide your thoughts on the discussion (round 1 of 2). If you do not have anything new or relevant to add, you may say "pass". Remember that you can and should (politely) disagree with other team members if you have a different perspective.

## Biomedical Ontologist (AlzKB Semantics & Standards)

**Biomedical Ontologist (AlzKB Semantics & Standards) – Input (Round 1):**

**1. SCHEMA CORE**

- **Ontology Alignment:**  
  - Fully support foundation in OWL and property graph interoperability. All schema classes and relations must be mapped to established ontologies:  
    - *Clinical*: SNOMED CT, UMLS  
    - *Molecular*: HGNC (genes), UniProt (proteins/isoforms), MONDO (diseases), Gene Ontology (molecular function, process, localization), Protein Ontology (for PTMs and isoforms)  
    - *Imaging*: NIDM, RadLex  
    - *Phenotypic*: HPO for symptoms and clinical features  
  - Require explicit mapping of all custom entities (e.g., tau isoform subclasses) to reference terms (or submit to ontology if absent).  
  - Insist on owl:equivalentClass/Property or skos:exactMatch where possible for maximal interoperability.

- **Tau Isoform Modeling:**  
  - Each tau (MAPT) isoform must be a distinct entity, referenced by UniProt/Protein Ontology IDs, with 
    - PTMs (e.g., phosphorylation S202) modeled as separate nodes using PSI-MOD or Protein Ontology.
    - “localized_in” links to specific brain regions (e.g., hippocampus, mapped to Uberon).
    - “pathology_association” edges to pathology classes (e.g., “Neurofibrillary tangle”—MONDO:0006032).
  - Temporal granularity is essential: Model time-ordered clinical/imaging events (e.g., “has_event_at_timepoint”).

- **Synonym & Normalization Handling:**  
  - All entities require synonym lists (from UMLS, HGNC, etc.), and preferred label mapping.
  - Disambiguate ambiguous common names (e.g., “tau” → UniProt P10636, but also annotate as “MAPT” gene product).

- **Minimal Set for V1:**  
  - Agree with Technical Lead: Genes, proteins/isoforms, clinical features, imaging features, subject, provenance.
  - Require inclusion of at least one explicit “pathology” class (e.g., neurofibrillary tangle, amyloid plaque) and their relation to molecular/imaging/clinical entities.

**2. DATA STRATEGY**

- **Entity Normalization Protocols:**  
  - All identifiers must be globally unique, resolvable, and ontology-backed (prefer CURIEs: e.g., HGNC:6893, UniProt:P10636-8).
  - Use cross-ontology references (e.g., mapping between HGNC, Ensembl, UniProt for genes/proteins/isoforms).
  - Imaging features require mapping to NIDM/RadLex terms with clear phenotype linkage (e.g., HPO:0020218 for hippocampal atrophy).
  - Document all normalization mappings and provide update tracking for evolving ontologies.

- **Disambiguation:**  
  - Employ algorithmic synonym expansion but require curator review for “tau,” “MAPT,” and other ambiguous legacy terms.
  - Insist on provenance annotation for all normalization actions.

- **Pipeline QC:**  
  - Automated semantic validation at ingestion: every entity and edge must be ontology-typed, and all relationships must pass logical consistency checks.

**3. SUCCESS METRICS**

- **Ontology Coverage:**  
  - % of core schema entities/relationships mapped to reference ontologies (target >95% for entities, >90% for relationships).
  - # of unique, ontology-backed tau isoform–pathology–brain region triples.
- **Semantic Accuracy:**  
  - Rate of successfully normalized ambiguous terms (goal: >98% after curator review).
  - % of cross-modal (clinical, imaging, molecular) links validated as semantically consistent.
- **FAIR Compliance:**  
  - % of entities/edges with ontology-backed provenance and rich metadata.

**Critical Notes/Dependencies:**

- If an AD-specific entity is not represented in a reference ontology, initiate submission to the relevant ontology consortium.
- Do not allow custom terms to propagate without clear mapping or documentation.
- AD-specific nuance: Must ensure that all pathology terminology (e.g., “ballooned neuron,” “coiled body”) is mapped to accepted neuropathology ontologies (Brain/MONDO/CELL).

**Summary:**  
Prioritize ontology alignment, explicit entity normalization, tau isoform/brain-region granularity, and rigorous semantic validation. The schema must be extensible and semantically transparent for downstream analytics and interoperability.

## User

Data Science Lead (Extraction & Validation), please provide your thoughts on the discussion (round 1 of 2). If you do not have anything new or relevant to add, you may say "pass". Remember that you can and should (politely) disagree with other team members if you have a different perspective.

## Data Science Lead (Extraction & Validation)

**Data Science Lead (Extraction & Validation) – Input (Round 1):**

**1. SCHEMA CORE**

- **Extraction-Driven Schema Prioritization:**  
  - Fully support prior recommendations on OWL/property-graph hybrid with strict entity typing and ontology mapping.
  - For initial extraction pipelines, recommend *limiting relationship types* to those we can reliably extract with high precision (e.g., “has_variant”, “diagnosed_with”, “expresses”, “has_imaging_feature”).  
  - Tau-specific: Ensure the schema accommodates entity “Tau isoform” (UniProt isoform-level granularity) and “PTM event” as first-class nodes, with brain-region context (“located_in”).
  - Relations requiring subjective or inferential extraction (e.g., “causes,” “accelerates,” “protects_against”) should be strictly evidence-backed and possibly moved to a later phase to avoid spurious connections.

**2. DATA STRATEGY**

- **Source Selection:**  
  - Only include datasets with strong curation and clear data provenance in V1 (e.g., ADNI, ROSMAP, AMP-AD, and literature sets with high-confidence extractions—exclude preprints or automated-only sources for V1).
  - Pipeline must support:  
    - Provenance tracking at record and edge level (source dataset, publication, extraction method, timestamp).
    - Modular extraction steps:  
      - Named Entity Recognition/Linking (with ontology resolution)
      - Relation Extraction (pattern- and ML-based, tuned for high precision)
      - Entity resolution/disambiguation (using multi-ontology crosswalks, curator review for ambiguous cases)
      - Validation (schema and semantic)
  - **Normalization Protocols:**  
    - Use gold-standard identifiers (HGNC for genes, UniProt for proteins/isoforms/PTMs, UMLS/SNOMED for clinical).
    - For ambiguous protein forms (e.g., tau isoforms), require unique UniProt isoform IDs and explicit “has_synonym” edges.

- **Quality Assurance:**  
  - Prioritize *precision over recall* for all extraction steps (target <2% false positive rate in entity and relation extraction, based on gold-standard benchmarks [e.g., GWAS Catalog, AlzForum]).
  - All relationships extracted must include extraction confidence (probability score or manual curation flag).

- **Error Analysis:**  
  - Implement error monitoring dashboards:  
    - Track extraction precision/recall per entity/relation type, with active error sampling for “high-risk” associations (e.g., novel tau-pathology links).
  - Require routine gold-standard benchmarking (e.g., how many established MAPT-pathology or APOE-imaging associations recovered, at what FPR).

**3. SUCCESS METRICS**

- **Extraction Precision:**  
  - >98% precision for gene/protein, >95% for clinical and imaging entities (validated on gold standards).
  - <2% false positive rate in tau isoform–pathology–region triples (error-checked by subject matter expert review).
- **Entity/Relation Validation:**  
  - % of extracted relationships validated against trusted references (target >90% in V1 for all high-value AD associations).
- **Graph Utility:**  
  - Number of cross-modal, evidence-backed (provenanced) triples retrievable by researchers, specifically those queried in AD literature (e.g., “subjects with MAPT R406W and marked hippocampal atrophy”).
- **Data Traceability:**  
  - Every edge and entity must be fully traceable: extraction method, data source, extraction timestamp, and evidence sentence/record.

**Critical Nuances & Risks:**

- *Tau and PTM ambiguity*: Extraction from text is particularly error-prone for tau isoforms and PTMs (frequent synonymy, context dependency). Recommend manual curation or semi-automated QA for all tau/PTM links in V1.
- Do *not* allow inferred or “hypothesis-driven” edges unless explicitly supported by primary data with provenance.
- Longitudinal/temporal relations should be included only if event timing is unambiguous and available.

**Summary:**  
Schema and pipelines must be tailored to what can be reliably extracted and validated with high precision. Strict normalization, rigorous error analysis, and provenance tracking are paramount—especially for nuanced AD-specific relationships (e.g., tau isoforms, PTMs, brain region localization). Preference is for a smaller but extremely high-confidence V1 KG, extensible as extraction methods mature.

## User

Scientific Critic (AlzKB), please provide your thoughts on the discussion (round 1 of 2). If you do not have anything new or relevant to add, you may say "pass". Remember that you can and should (politely) disagree with other team members if you have a different perspective.

## Scientific Critic (AlzKB)

**Scientific Critic (AlzKB) – Input (Round 1):**

**1. SCHEMA CORE**

- **Rejection of Generic Edges:**  
  - I strongly object to the use of imprecise, catch-all predicates such as “associated_with,” “related_to,” or “linked_to.” Every relationship class must be biologically precise and ontologically defined. Acceptable examples: “phosphorylates,” “binds,” “encodes,” “is_risk_allele_for,” “measured_by,” “localized_in.”  
  - For clinical-imaging edges, disallow vague links like “has_imaging_feature” without specifying the *nature* (e.g., “shows_hippocampal_atrophy_on_MRI”).  

- **Species Resolution:**  
  - There is a chronic issue in AD KGs with conflating murine and human data (especially with MAPT/tau literature).  
  - *Actionable requirement*: All entities and edges must be species-resolved at ingestion, with explicit “species” property (e.g., NCBITaxon:9606 for Homo sapiens, NCBITaxon:10090 for Mus musculus). Any inter-species extrapolation must be separately modeled, never conflated in a single node or edge.

- **Entity Granularity:**  
  - Endorse all recommendations for tau isoform and PTM granularity. However, *demand* that all “tau” mentions be resolved to *isoform level* (UniProt/Protein Ontology) where possible, and require explicit annotation (or “ambiguous” flag) if primary data do not specify isoform.

- **Imaging and Pathology Mapping:**  
  - Agree with requirement for NIDM/RadLex mapping, but emphasize that *each imaging feature* must be backed by both the imaging protocol and anatomical localization (e.g., “reduced SUVR in left entorhinal cortex by AV-1451 PET”).
  - Pathology entities (e.g., “neurofibrillary tangle”) must be mapped to recognized neuropathology ontologies (e.g., MONDO, Brain Ontology). Avoid free-text “pathology” labels.

**2. DATA STRATEGY**

- **Strict Provenance Enforcement:**  
  - No edge or node is to be loaded into AlzKB without direct, machine-resolvable provenance (PubMed ID for literature, dataset record/row for experimental data).  
  - Extraction pipelines must *require* this linkage in order to materialize a triple.  
  - All extracted relationships must store extraction method (pattern, ML, manual curation), confidence score, and reviewer/curator ID if applicable.

- **Ambiguity Auditing:**  
  - Entity normalization must have a fail-safe: if ambiguity cannot be resolved (e.g., “tau” in a paper where isoform is not clear), this must be annotated as “ambiguous,” and these instances must not be collapsed with fully resolved entities.  
  - Report the proportion of such “ambiguous” cases per entity/relation type.

- **Species & Ontology Error Reporting:**  
  - All ingestion runs must provide a report of human/murine/other species ratios and flag any cases of cross-species conflation.
  - Reject inclusion of any data extracted using “Alzheimer’s Disease” and “dementia” synonymously unless the primary data specify AD diagnosis using accepted criteria (NINCDS-ADRDA, NIA-AA, etc.).

**3. SUCCESS METRICS**

- **Gold Standard Metrics Required:**  
  - All quality metrics must be calculated on a *Gold Standard* subset:  
    - Precision, Recall, F1 for entity resolution (e.g., Abeta40 vs Abeta42, tau isoforms, APOE alleles).
    - Edge accuracy: Precision and recall against curated AD knowledge benchmarks (e.g., AlzForum mutations, GWAS Catalog, ADNI imaging–genotype tables).
    - Coverage: % of known, validated AD risk loci and tau-pathology associations recovered.
  - *Reject* subjective or qualitative metrics (“researcher utility,” “completeness reporting”) unless supported by quantitative analysis of query logs or gold standard recall.

- **Ambiguity Tracking:**  
  - Proportion of ambiguous vs. resolved entities/edges must be reported for every knowledge graph release.

- **Provenance Completeness:**  
  - Every triple must be traceable to its original source; aim for 100%—any entity/edge lacking provenance is grounds for exclusion.

**Critical Risks & Non-Negotiables:**

- No “shortcut” mapping of tau/PTMs, or AD/dementia, or human/mouse.  
- No edge or node without machine-resolvable provenance.  
- Mandatory gold standard evaluation for entity disambiguation and edge types, before and after each major KG release.

**Summary:**  
AlzKB’s credibility depends on biological specificity, rigorous provenance, and quantitative, Gold Standard-based evaluation. Any methodological compromise (vague predicates, unresolved species or isoforms, missing provenance) will undermine both downstream analytics and trust. No edge/entity should be loaded without passing these standards.

## User

This concludes round 1 of 2 of discussion. Principal Investigator (Alzheimer's KG), please Synthesize team inputs. 1. Identify agreements vs. conflicts. 2. Resolve conflicts using provided evidence; favor data over opinion. 3. Decide the agenda status. 4. Ask 1 concrete question to clarify ambiguity if needed. Be concise..

## Principal Investigator (Alzheimer's KG)

**SYNTHESIS OF TEAM INPUTS (Round 1 of 2):**

---

### 1. **Agreements**

**Schema Core:**
- All agree on an OWL/property-graph hybrid schema, grounded in authoritative ontologies (SNOMED CT, Gene Ontology, NIDM, HGNC, UniProt, MONDO, etc.).
- Tau isoforms and PTMs must be first-class entities, with explicit mapping to UniProt/Protein Ontology and linkage to brain regions (Uberon) and pathology (MONDO/Brain Ontology).
- Clinical, imaging, molecular, and provenance entities are required in V1; support for time-resolved and cross-modal relationships.
- Full entity normalization, synonym handling, and semantic rigor are non-negotiable.

**Data Strategy:**
- Only high-confidence, provenance-rich datasets (ADNI, ROSMAP, AMP-AD) for V1; no preprints or ambiguous sources.
- Entity normalization via global, ontology-backed identifiers (CURIEs), cross-ontology mapping, disambiguation protocols, and rigorous provenance annotation at all stages.
- Extraction prioritized for precision over recall; no inclusion of ambiguous or hypothesis-driven associations without data support.
- Modular, auditable ETL with routine QC, error reporting, and curator review for high-risk/ambiguous cases.

**Success Metrics:**
- Focus on precision, gold-standard benchmarking, and coverage of known AD loci, tau-pathology associations, and ontology mapping completeness.
- Every entity and edge must have machine-resolvable provenance. Ambiguity tracking and reporting are mandatory.
- No subjective or qualitative metrics accepted unless tied to quantitative, gold-standard supporting data.

---

### 2. **Conflicts & Resolution**

**a) Relationship Granularity:**
- **Conflict:** Technical Lead suggests “linked_to” as a relationship; Scientific Critic and Ontologist demand biologically/clinically precise, ontology-resolved predicates only (e.g., “is_risk_allele_for,” “measured_by”).
- **Resolution:** The evidence and standards (FAIR, ontology-driven KGs) strongly favor the stricter approach. For V1, only precise, ontology-backed relationships will be implemented. “Linked_to” and similar catch-alls are disallowed.

**b) Species Resolution:**
- **Conflict:** Only the Scientific Critic explicitly requires species annotation and the rejection of inter-species conflation.
- **Resolution:** Literature in AD is replete with human/mouse conflation (MAPT, tau). Including a “species” attribute, as per NCBITaxon, is necessary to ensure biological fidelity and support translational research. Adopt this requirement.

**c) Ambiguity Handling:**
- **Conflict:** Degree of tolerance for ambiguous entities/edges.
- **Resolution:** All agree ambiguity must be flagged and tracked; inclusion in KG is allowed only if explicitly labeled as “ambiguous” and never merged with resolved entities.

---

### 3. **Agenda Status**

**All agenda items are advancing.**  
- **Schema Core:** Strong consensus with actionable requirements and AD-specific nuance.  
- **Data Strategy:** Agreement on data source quality, normalization rigor, and provenance.  
- **Success Metrics:** High bar for quantitative, gold-standard-based metrics; ambiguity and provenance completeness must be explicitly reported.

Pending only on finalized protocols for ambiguous/underspecified edges/entities and implementation detail for cross-species modeling.

---

### 4. **Clarifying Question**

**To All (esp. Data Science Lead & Ontologist):**  
_For tau/PTM extraction from literature, should ambiguous mentions (e.g., “tau phosphorylation”) be included as separate, explicitly “ambiguous” entities in V1, or excluded until resolved? What impact would each choice have on coverage and downstream analytics?_

---

**End of Synthesis (Round 1).**

## User

Technical Lead (Knowledge Graph Engineering), please provide your thoughts on the discussion (round 2 of 2). If you do not have anything new or relevant to add, you may say "pass". Remember that you can and should (politely) disagree with other team members if you have a different perspective.

## Technical Lead (Knowledge Graph Engineering)

**Technical Lead (Knowledge Graph Engineering) – Input (Round 2):**

**Response to Clarifying Question:**
- **Ambiguous tau/PTM mentions:** Technically feasible to include ambiguous tau/PTM mentions as separate, explicitly flagged “ambiguous” entities (e.g., “tau [ambiguous isoform]”, “phosphorylated tau [site unknown]”).  
  - **Implementation:** Use a standardized suffix/flag (`:Ambiguous`) and explicit provenance+confidence metadata.
  - **Impact:**  
    - **Coverage:** Increases recall, capturing a significant fraction of literature where isoform/PTM site is underspecified (especially older studies or reviews).  
    - **Downstream analytics:** Risks: Queries may inadvertently retrieve ambiguous entries unless filters are in place. Opportunity: Supports meta-analyses on “known unknowns,” trending ambiguity over time, and may prompt curation prioritization.
    - **Maintenance:** Added complexity in schema and query logic; ambiguous entities must be strictly isolated from resolved instances (no merging).
  - **Recommendation:** Support inclusion of ambiguous tau/PTM mentions as flagged entities, provided (a) they are never merged with resolved forms, (b) downstream users are warned about their ambiguous status, and (c) ambiguity is quantified in all analytics/exports. This balances coverage with transparency.

**Other Inputs on Synthesis Points:**

- **Species Resolution:** Fully support mandatory species tagging on all biological entities and relationships, as proposed by the Scientific Critic. This is straightforward to enforce programmatically and ensures no future human/mouse conflation.
- **No Catch-all Edges:** Will revise schema to eliminate all generic predicates (“linked_to,” etc.), using only precise, ontology-backed relations. This adds implementation overhead in schema mapping but is justified by improved data fidelity.
- **Ambiguity Tracking:** Will implement dashboard/reporting to monitor ambiguous vs. resolved entity/edge proportions per release.

**Dependencies/Operational Notes:**
- Ambiguity and species attributes should be part of the core node/edge schema from the outset for consistency.
- Will require additional ETL pipeline logic for ambiguous entity flagging and for enforcing no merging between ambiguous/resolved nodes.

**Summary:**  
- Technically, it is practical to include ambiguous tau/PTM entities in V1 if (and only if) they are unequivocally flagged and isolated, with their ambiguity exposed to all downstream users.
- Fully align with team consensus on species annotation, provenance rigor, and elimination of generic edge types.  
- Prepared to deliver schema and ETL pipeline updates per these refined requirements.

## User

Biomedical Ontologist (AlzKB Semantics & Standards), please provide your thoughts on the discussion (round 2 of 2). If you do not have anything new or relevant to add, you may say "pass". Remember that you can and should (politely) disagree with other team members if you have a different perspective.

## Biomedical Ontologist (AlzKB Semantics & Standards)

**Biomedical Ontologist (AlzKB Semantics & Standards) – Input (Round 2):**

**Response to Clarifying Question:**
- **Ambiguous tau/PTM mentions:**  
  - *Ontology Best Practice:* Explicitly represent ambiguous tau/PTM mentions as separate entities, using a convention such as “tau (ambiguous isoform)” or “phosphorylated tau (site unknown)” and tag with a `has_ambiguity` property.  
  - *Ontology Mapping:* Where possible, use existing ontology classes for ambiguous forms (e.g., PR:000025838 “tau protein” in Protein Ontology for generic tau). If the ambiguity is greater than what the ontology provides, annotate with `skos:note` or a similar property describing the ambiguity.
  - *Inclusion vs. Exclusion:*  
    - **Inclusion (with explicit ambiguity):**  
      - *Coverage:* Accurately reflects the state of the knowledge, especially in legacy or low-detail literature.  
      - *Interoperability:* Maintains semantic transparency and prevents category errors.  
      - *Curation:* Enables downstream prioritization for manual review and future disambiguation.
    - **Exclusion:**  
      - *Coverage loss:* Risks omitting a significant body of evidence, underrepresenting literature where isoforms/sites are not resolved.
      - *Downstream analytics:* May bias network analyses or meta-research, especially in systematic reviews.
  - *Recommendation:* **Inclusion is preferable,** strictly conditional on (a) unambiguous “ambiguous” flagging, (b) logical separation from resolved entities, and (c) full provenance annotation and reporting. This is in keeping with OBO Foundry/FAIR best practices.

**Other Inputs on Synthesis Points:**

- **Species Resolution:**  
  - Strongly support. All biological entities and relationships must have a `species` or `in_taxon` property (use NCBITaxon identifiers). For ambiguous species (e.g., in vitro or unspecified), use a defined “unknown taxon” code and document rationale.
- **Precision of Relations:**  
  - Reiterate: Only use relationships defined in canonical ontologies (RO, OBO Relations Ontology, etc.). If no suitable predicate exists, propose a new term through OBO channels and document the temporary mapping.
- **Ambiguity Tracking and Reporting:**  
  - All ambiguous entities and edges must be quantified, annotated with reason/source, and included in KG release notes and analytics.

**Operational/Schema Recommendations:**
- Schema must support:  
  - `has_ambiguity` flag (boolean) and free-text `ambiguity_note`.
  - Separate class/label for ambiguous vs. resolved forms.
  - Provenance and ambiguity status as mandatory properties on all tau/PTM and related nodes.
- All scripts for KG use/export should warn users by default when ambiguous nodes are included in outputs.

**Summary:**  
- Inclusion of ambiguous tau/PTM entities is ontologically correct and maximizes transparency, provided all ambiguity is captured, flagged, and tracked.
- Full agreement with team on precise predicates, species annotation, and provenance/ambiguity reporting. Prepared to implement these standards in schema and ontology mapping documentation.

## User

Data Science Lead (Extraction & Validation), please provide your thoughts on the discussion (round 2 of 2). If you do not have anything new or relevant to add, you may say "pass". Remember that you can and should (politely) disagree with other team members if you have a different perspective.

## Data Science Lead (Extraction & Validation)

**Data Science Lead (Extraction & Validation) – Input (Round 2):**

**Response to Clarifying Question (Ambiguous tau/PTM inclusion):**

- **Empirical Extraction Perspective:**
  - In practice, >30% of literature mentions of “tau” or “phosphorylated tau” lack isoform or PTM site specificity, especially in older or summary articles. Excluding all such mentions would lead to substantial loss of supporting evidence and literature coverage in the KG. 
  - Precision risk is manageable if and only if these mentions are clearly flagged as “ambiguous” and downstream users can reliably filter or ignore them.

- **Implementation Recommendation:**
  - **Include ambiguous tau/PTM mentions as distinct, flagged nodes** (e.g., “tau [ambiguous isoform]”, “phosphorylated tau [site unknown]”) with explicit `ambiguity` property and detailed provenance (e.g., extraction sentence, source, extraction method).
  - **Never merge** ambiguous entities with resolved ones; enforce schema isolation at both node and edge levels.
  - Extraction pipeline will tag such ambiguous cases algorithmically based on context (e.g., absence of unique isoform or site), and flag for optional curator review.

- **Impact:**
  - **Coverage:** Inclusion significantly improves recall for tau/PTM evidence, critical for comprehensive systematic reviews and evidence mapping.
  - **Downstream analytics:** Ambiguous nodes may inflate counts or be misinterpreted if not handled properly. Will implement default warnings/filters in KG query API and analytics outputs for these cases.
  - **Curation:** Periodic review and prioritization of ambiguous nodes for manual resolution as new data or improved extraction techniques become available.

**Other Inputs (on synthesis points):**

- **Species Resolution:** Strongly support. Will enforce species tagging (`species` property, NCBITaxon ID) during all extraction and relation steps. No merging of cross-species data; ambiguous “species” will be flagged and reported.
- **Provenance:** All extracted ambiguous nodes/edges must have complete provenance (source, method, and extraction confidence).
- **Error/Ambiguity Tracking:** Dashboards and release reports will provide full counts and proportions of ambiguous vs. resolved nodes/edges for continuous QA and transparency.

**Summary:**  
- Support inclusion of ambiguous tau/PTM entities in V1 KG, provided ambiguity is explicit, filterable, and never merged with resolved entities.  
- This balances high-precision requirements with needed literature coverage for AD research.  
- Extraction pipeline will be revised to operationalize and audit these requirements.

## User

Scientific Critic (AlzKB), please provide your thoughts on the discussion (round 2 of 2). If you do not have anything new or relevant to add, you may say "pass". Remember that you can and should (politely) disagree with other team members if you have a different perspective.

## Scientific Critic (AlzKB)

**Scientific Critic (AlzKB) – Input (Round 2):**

**Response to Clarifying Question (Ambiguous tau/PTM inclusion):**

- **Position:** Inclusion of ambiguous tau/PTM mentions is scientifically justified *only* when these entities are:
  1. **Rigorously flagged as ambiguous** (e.g., “tau [ambiguous isoform]” with an `ambiguity_status=ambiguous` property).
  2. **Never merged** with resolved nodes or edges; strict logical separation must be enforced in both data storage and API/query layers.
  3. **Fully provenance-traceable:** Each ambiguous entity/edge must store not just the source, but also the original context (sentence/figure/data row) highlighting the ambiguity.
  4. **Quantitatively tracked:** The KG must report the exact number and type of ambiguous vs. resolved mentions in every release.

- **Impact on Coverage and Analytics:**
  - **Coverage:** Including such entities avoids systematic omission of a large portion of the literature (~30%, as noted by Data Science Lead), which is particularly relevant for longitudinal meta-analyses of AD research trends.
  - **Interpretability Risk:** Ambiguous nodes, if not filtered, *will* contaminate downstream analyses—such as network inference, variant-pathology association, or drug repurposing pipelines. To mitigate this:
    - KG query interface must default to *excluding* ambiguous entities/edges unless user opts in.
    - All exports and analytics must include clear metrics on the fraction of ambiguous data in every result set.
  - **Curation Opportunity:** Quantifying ambiguity enables prioritization for future manual curation or targeted data mining as methods improve.

- **Further Emphases:**
  - **Species Annotation:** Ambiguity in species (e.g., “tau phosphorylation observed in mouse model”) is *also* to be flagged and tracked. No merging of ambiguous/human/murine nodes—species ambiguity is as critical as isoform/PTM ambiguity.
  - **Pathology and Disease Terms:** *Do not* allow ambiguous mappings between “dementia,” “AD,” or unspecified pathology. Each ambiguous clinical/pathological entity must also be flagged and quantified.
  - **Release Notes:** Every official AlzKB release must publish not just precision, recall, and F1 on gold standards for resolved nodes/edges, but *also* the ambiguity rates per key entity/relation type.

**Summary:**  
- **Inclusion with strict, transparent ambiguity flagging and reporting is acceptable and preferable.**
- **Never sacrifice logical separation or provenance traceability for coverage.**
- **Ambiguity rates must become a standard KG health metric.**

Prepared to review ambiguity-handling implementations and ensure no “leakage” between ambiguous and resolved knowledge—especially for tau isoforms, PTMs, species, and disease mappings.

## User

Principal Investigator (Alzheimer's KG), please summarize the meeting in detail for future discussions, provide a specific recommendation regarding the agenda, and answer the agenda questions (if any) based on the discussion while strictly adhering to the agenda rules (if any)..

As a reminder, here is the agenda for the meeting:

Task: Build a scalable, retrieval-optimized Knowledge Graph for Alzheimer's Disease research.

TASK: Define the Technical Specification for AlzKB.
The team must agree on the architectural foundation before implementation.

OUTPUT REQUIREMENTS:
1. SCHEMA CORE.
2. DATA STRATEGY.
3. SUCCESS METRICS.

CONSTRAINTS: Be specific. No fluff. Prioritize AD-specific nuances (e.g., Tau isoforms).


Your summary should take the following form.

### Agenda

Restate the agenda in your own words.

### Team Member Input

Summarize all of the important points raised by each team member. This is to ensure that key details are preserved for future meetings.

### Recommendation

Provide your expert recommendation regarding the agenda. You should consider the input from each team member, but you must also use your expertise to make a final decision and choose one option among several that may have been discussed. This decision can conflict with the input of some team members as long as it is well justified. It is essential that you provide a clear, specific, and actionable recommendation. Please justify your recommendation as well.

### Next Steps

Outline the next steps that the team should take based on the discussion.

## Principal Investigator (Alzheimer's KG)

### Agenda

**Restated:**  
Our task was to define the detailed technical specification for AlzKB, a retrieval-optimized, scalable Knowledge Graph for Alzheimer’s Disease research. The specification must address:  
1. The **Schema Core**, including rigorous adherence to biomedical ontologies and AD-specific nuances (notably tau isoform/PTM granularity and species annotation).  
2. The **Data Strategy**, covering data source selection, entity normalization, multi-modal integration, provenance, and handling of ambiguous/underspecified information.
3. The **Success Metrics**, emphasizing precision, coverage of AD-relevant entities/relations, gold-standard benchmarking, and explicit ambiguity/provenance tracking.  
All decisions must be specific, operationalizable, and designed for high trust and interoperability in the AD research community.

---

### Team Member Input

#### **Technical Lead (Knowledge Graph Engineering)**
- Advocated for an OWL/property-graph hybrid, with all schema elements mapped to standard ontologies (HGNC, UniProt, SNOMED CT, MONDO, NIDM).
- Insisted on tau isoforms and PTMs as entities, APOE alleles as explicit genotypes, and fine-grained relationships, including “measured at timepoint”.
- Agreed to eliminate generic predicates in favor of ontologically precise relationships.
- Supported inclusion of ambiguous tau/PTM mentions as flagged, separate entities, provided they are never merged with resolved forms and ambiguity is visible downstream.
- Agreed on mandatory species annotation (NCBITaxon) for all biological entities.

#### **Biomedical Ontologist (AlzKB Semantics & Standards)**
- Emphasized strict mapping of all entities and relationships to established ontologies (OBO Foundry, SNOMED CT, UMLS, Protein Ontology, NIDM, HPO).
- Recommended explicit “has_ambiguity” property and ontological documentation for ambiguous tau/PTM mentions.
- Asserted that semantic transparency and ontological rigor (including synonym handling and logical separation of ambiguous entities) take precedence over raw coverage.
- Supported species annotation and the reporting of all ambiguous cases.

#### **Data Science Lead (Extraction & Validation)**
- Stressed that a high percentage of tau/PTM references in literature are ambiguous, but that excluding them would significantly impair knowledge graph coverage.
- Argued for the inclusion of ambiguous mentions as distinctly flagged, provenance-rich nodes, never merged with resolved forms.
- Agreed to enforce precision > recall, full provenance, and ambiguity/error tracking at all stages.
- Will implement extraction, entity normalization, and curation protocols to operationalize these requirements.

#### **Scientific Critic (AlzKB)**
- Rejected generic relationship types and demanded biologically precise, ontology-backed predicates.
- Insisted on species resolution (NCBITaxon), strict provenance, and logical separation of ambiguous entities/edges.
- Stated that ambiguity rates must be reported as a standard graph health metric and that query/API defaults should **exclude** ambiguous entities unless users opt in.
- Stressed that ambiguous nodes should never contaminate downstream analytics and must be quantified and flagged in all exports and reports.

---

### Recommendation

**Based on the synthesis of all inputs and expert judgment:**

#### **Schema Core**
- **Adopt an OWL/property-graph hybrid model**, mapped rigorously to SNOMED CT, OBO ontologies, and domain standards.
- **Explicitly represent tau isoforms and PTMs at the highest resolvable granularity** (using UniProt/Protein Ontology IDs, PTM sites with PSI-MOD), and always annotate with species (NCBITaxon).  
- **All predicates must be ontology-backed and biologically/clinically specific** (e.g., “encodes”, “has_phosphorylation_at”, “is_risk_allele_for”, “measured_by”).
- **Ambiguous entities (tau/PTMs, species, pathology, etc.) are to be included only as strictly flagged, logically isolated nodes/edges**, never merged with resolved items. Each ambiguous item must have a `has_ambiguity` property and be annotated with detailed provenance.

#### **Data Strategy**
- **Include only high-confidence, provenance-rich datasets** (ADNI, ROSMAP, AMP-AD, etc.) for V1.  
- **All extracted data must be normalized to gold-standard identifiers** (CURIEs), with robust cross-ontology mapping and synonym handling.
- **Ambiguous mentions** (tau/PTM, species, etc.) must be algorithmically and curator-flagged, with complete provenance (including extraction context), and isolated in both storage and query layers.
- **Species must be annotated on every biological node/edge**, and cross-species conflation is strictly prohibited.
- **Provenance is mandatory** for every entity and relationship; items lacking provenance are excluded.

#### **Success Metrics**
- **Extraction/annotation precision targets:** >98% for molecular, >95% for clinical/imaging entities, <2% FPR for tau isoform–pathology–region links (benchmarked on gold standards).
- **Coverage:** Percent of known AD risk loci, APOE alleles, tau isoform/pathology relationships, and imaging features mapped to ontologies.
- **Ambiguity reporting:** Number/proportion of ambiguous vs. resolved entities/edges is to be reported in every release.
- **Provenance completeness:** 100% of nodes/edges must have machine-resolvable provenance.
- **Default query/API behavior:** Exclude ambiguous nodes/edges unless user explicitly opts in; all exports must include ambiguity and provenance metrics.

**Justification:**  
This approach ensures maximal biological fidelity, semantic transparency, and community trust. It supports both high-precision knowledge retrieval and meta-research into the structure of AD knowledge itself, while providing a path for future curation and automated disambiguation as data and methods improve.

---

### Next Steps

1. **Schema Finalization:**  
   - Technical Lead and Biomedical Ontologist to draft and circulate the first version of the schema, including explicit support for ambiguity, species, and provenance attributes.
   - All relationship types and entity classes to be mapped to canonical ontologies; ambiguous forms to be included as outlined.

2. **Pipeline Updates:**  
   - Data Science Lead to update extraction and normalization pipelines to tag ambiguous entities/edges, enforce species annotation, and block merging of ambiguous/resolved nodes.
   - Scientific Critic to review and stress test the pipeline for leakage of ambiguous information and species misannotation.

3. **Validation and Reporting:**  
   - Implement dashboards/reports for ambiguity rates, precision metrics, and provenance completeness.
   - Release documentation templates to include ambiguity metrics and guidance for downstream users on filtering/handling ambiguous knowledge.

4. **Gold Standard Benchmarking:**  
   - Assemble gold standard entity and relation sets (tau isoforms, APOE alleles, key AD loci, clinical-imaging-genetic triples) for initial precision and coverage evaluation.

5. **User-facing Defaults:**  
   - Ensure query interfaces and exports default to excluding ambiguous knowledge, with clear user warnings/documentation.

6. **Review and Iteration:**  
   - Schedule follow-up review after first pipeline run and schema implementation to assess ambiguity handling, precision, and user acceptability.

---

*This concludes the technical specification phase for AlzKB. The team is aligned on a schema and strategy that is both AD-specific and broadly interoperable. Implementation and validation will proceed per this recommendation, with transparency and rigorous reporting as ongoing requirements.*


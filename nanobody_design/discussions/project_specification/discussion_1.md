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


Principal Investigator (Alzheimer's KG) will convene the meeting. Then, each team member will provide their thoughts on the discussion one-by-one in the order above. After all team members have given their input, Principal Investigator (Alzheimer's KG) will Synthesize team inputs. 1. Identify agreements vs. conflicts. 2. Resolve conflicts using provided evidence; favor data over opinion. 3. Decide the agenda status. 4. Ask 1 concrete question to clarify ambiguity if needed. Be concise.. This will continue for 3 rounds. Once the discussion is complete, Principal Investigator (Alzheimer's KG) will summarize the meeting in detail for future discussions, provide a specific recommendation regarding the agenda, and answer the agenda questions (if any) based on the discussion while strictly adhering to the agenda rules (if any)..

## User

Principal Investigator (Alzheimer's KG), please provide your initial thoughts on the agenda as well as any questions you have to guide the discussion among the team members.

## Principal Investigator (Alzheimer's KG)

**Principal Investigator (Alzheimer's KG): Initial Thoughts and Guidance**

Team, thank you for joining. Our objective is clear: establish the technical specification for the Alzheimer's Knowledge Graph (AlzKB), focusing on biological and clinical specificity unique to Alzheimer’s Disease.

**Emphases for Today’s Discussion:**
- The schema must enable retrieval of mechanistically precise, AD-relevant knowledge—think beyond generic disease models.
- Data sources must be high-confidence, multi-modal, and strictly prioritized for AD research (with known provenance and minimal ambiguity).
- Evidence scoring must reflect translational value (e.g., clinical vs. preclinical, human vs. model organism).
- Success metrics must be objectively measurable, with a clear emphasis on both breadth (coverage) and depth (precision of relationships).

**Guiding Questions for Each Team Member:**
1. **Technical Lead:** What graph technology and data modeling choices best support high-volume, semantically rich, and query-optimized AD knowledge? What pitfalls should we avoid in entity/edge definition for scalability?
2. **Biomedical Ontologist:** Which ontologies and controlled vocabularies are non-negotiable for both interoperability and biological granularity (e.g., tau isoform distinction)? How do we encode disease progression and biomarker subtleties?
3. **Data Science Lead:** Which extraction and validation pipelines ensure near-zero hallucinated associations? How do we reconcile conflicting sources—what is the gold standard for entity resolution across imaging, genetics, and clinical notes?
4. **Scientific Critic:** What past knowledge graph efforts failed for AD and why? What biological or methodological blind spots threaten coverage or precision for AD-specific knowledge capture?

**Specific Questions to Guide Discussion:**
- Which *six* entity and edge types, if chosen poorly, would risk loss of AD mechanistic fidelity?
- How can we ensure the evidence score system accounts for both experimental rigor and clinical relevance (e.g., differentiating post-mortem versus in vivo findings)?
- What minimum coverage and precision rates (KPIs) are realistically attainable for our first release, given source limitations?

Let’s proceed with the Technical Lead, then each member in turn. Be specific, cite examples, and flag any anticipated bottlenecks for agenda progress.

## User

Technical Lead (Knowledge Graph Engineering), please provide your thoughts on the discussion (round 1 of 3). If you do not have anything new or relevant to add, you may say "pass". Remember that you can and should (politely) disagree with other team members if you have a different perspective.

## Technical Lead (Knowledge Graph Engineering)

**Technical Lead (Knowledge Graph Engineering): Round 1 Input**

**1. Schema Core: Entity and Edge Types**

*Entity Types* (AD-specific, high-value for mechanistic and clinical retrieval):
1. **Gene/Variant** (e.g., MAPT, APOE alleles, specific Tau splice isoforms)
2. **Protein** (e.g., amyloid-beta peptides, phosphorylated tau, tau isoforms)
3. **Small Molecule/Drug** (e.g., Aducanumab, experimental tau aggregation inhibitors)
4. **Clinical Phenotype** (e.g., memory impairment, Braak stage, CDR global score)
5. **Imaging Feature** (e.g., hippocampal atrophy, amyloid PET signal, tau PET quantification)
6. **Pathological Process** (e.g., tau phosphorylation, amyloid aggregation, neuroinflammation)

*Edge Types* (Biologically specific, AD-relevant):
1. **encodes** (Gene → Protein)
2. **phosphorylates** (Protein → Protein; e.g., kinase-modified tau)
3. **binds_to** (Small Molecule/Drug → Protein; e.g., antibody-amyloid binding)
4. **biomarker_of** (Imaging Feature/Protein → Clinical Phenotype)
5. **causes** (Pathological Process → Clinical Phenotype)
6. **co-occurs_with** (Clinical Phenotype ↔ Imaging Feature/Pathological Process; enables multi-modal correlation retrieval)

*Avoid*: Generic, broad relationships (e.g., “related_to”, “interacts_with”), as they hinder mechanistic interpretability and query optimization.

**2. Data Strategy**

*Four Priority Data Sources*:
1. **ADNI** (Alzheimer’s Disease Neuroimaging Initiative) – robust imaging, clinical, and biomarker data.
2. **AMP-AD** (Accelerating Medicines Partnership - Alzheimer’s Disease) – multi-omics (transcriptomic, proteomic) data.
3. **ROSMAP** (Religious Orders Study/Memory and Aging Project) – longitudinal clinical, neuropathological, and omics data.
4. **Gene Ontology/UniProt subset for AD-relevant entities** – for canonical protein functions and relationships.

*Evidence Scoring Mechanism*:
- **Tier 1:** Human clinical (e.g., ADNI/ROSMAP, peer-reviewed clinical trials)
- **Tier 2:** Human post-mortem (e.g., AMP-AD, ROSMAP brain tissue omics)
- **Tier 3:** Animal/preclinical models (e.g., transgenic mouse studies within AMP-AD)
- **Tier 4:** In silico or inferred (e.g., text mining, computational predictions)
- Score each edge/entity on provenance, method (experimental rigor), and source credibility.

**3. Success Metrics (KPIs)**

1. **Entity/Edge Coverage:** ≥90% of known AD-relevant genes/proteins (from AMP-AD and latest GWAS) and established clinical phenotypes in initial build.
2. **Precision of Mechanistic Edges:** ≥95% precision for “phosphorylates,” “binds_to,” “biomarker_of” relationships, as validated by cross-source concordance or expert curation.
3. **Query Performance:** Median query latency <1 second for canonical retrievals (e.g., “Find all tau phosphorylation events linked to memory impairment via biomarkers”).

**Anticipated Bottlenecks:**
- Disambiguation of tau isoforms and post-translationally modified states.
- Mapping imaging features to molecular/cellular processes (requires both data harmonization and schema finesse).
- Entity resolution across sources with inconsistent identifiers or granularity (e.g., transcript vs. protein isoform vs. aggregate).

**Summary/Key Points:**
- Prioritize biological specificity at both schema and data source level.
- Evidence scoring must transparently reflect clinical translatability.
- KPIs need to drive both coverage and query performance, avoiding over-fitting to generic or easily extractable relationships.

Ready to align with ontology and data science for harmonization and coverage.

## User

Biomedical Ontologist (AlzKB Semantics & Standards), please provide your thoughts on the discussion (round 1 of 3). If you do not have anything new or relevant to add, you may say "pass". Remember that you can and should (politely) disagree with other team members if you have a different perspective.

## Biomedical Ontologist (AlzKB Semantics & Standards)

**Biomedical Ontologist (AlzKB Semantics & Standards): Round 1 Input**

**1. Schema Core: Ontological Alignment and Normalization**

*Entity Types (with ontology recommendations):*
1. **Gene/Variant** – Normalize to HGNC/Ensembl/RefSeq; *variants* should resolve to dbSNP/ClinVar identifiers for AD loci (e.g. rs429358 for APOE ε4).
2. **Protein/Protein Isoform** – Use UniProtKB for canonical proteins, and PSI-MOD for post-translational modifications (e.g., phosphorylated tau isoforms; critical to distinguish MAPT-001, -002, etc.).
3. **Small Molecule/Drug** – ChEMBL/DrugBank for drugs; include PubChem CIDs for experimental compounds.
4. **Clinical Phenotype** – HPO for symptoms (e.g., HP:0002354 for memory impairment), and standard clinical scoring terms (e.g., CDR, MMSE) from LOINC/CPT.
5. **Imaging Feature** – RadLex (e.g., RID4941 for hippocampal atrophy), with links to LOINC for quantitative imaging assays; map imaging biomarkers to QID in Wikidata if possible.
6. **Pathological Process** – MONDO for disease entities (e.g., MONDO:0004975 for Alzheimer’s disease), GO for molecular/cellular processes (e.g., GO:0051783 for amyloid-beta clearance), and extend with OBO Foundry terms for neuroinflammation, tau aggregation, etc.

*Edge Types (with semantic mappings):*
1. **encodes** – SO:0001217 (gene encodes protein)
2. **phosphorylates** – RO:0002436 (molecularly modifies by phosphorylation)
3. **binds_to** – RO:0002434 (molecularly binds)
4. **biomarker_of** – Link to OBO RO:0002607 (is biomarker for)
5. **causes** – RO:0002410 (causally upstream of, positive effect)
6. **co-occurs_with** – SIO:001403 (co-occurs with), but consider restricting to meaningful clinical or biological co-manifestation, not loose associations.

**Critical Nuances:**
- *Tau isoforms & PTMs*: Must support multi-identifier mapping (e.g., MAPT gene → tau isoform → site-specific PTM).
- *Phenotype granularity*: Capture stage-specific and composite phenotypes (e.g., early-onset AD, MCI due to AD, Braak stage) using ontological hierarchies.
- *Imaging to pathology links*: Validate mappings from imaging features to pathophysiological processes (e.g., tau PET signal to phosphorylated tau burden).

**2. Data Strategy (Semantic Focus):**
- *Data sources as above* (ADNI, AMP-AD, ROSMAP, UniProt/GO), but stress: only load entities/relations with full ontology-based normalization.
- *Evidence Scoring*: Add an explicit “provenance” triple per relation (using W3C PROV-O standards), distinguishing between “direct assay,” “inferred by curator,” and “text-mined” evidence, as well as the experimental system (human, mouse, in vitro).

**3. Success Metrics:**
1. **Ontology Coverage:** ≥95% of nodes and edges are mappable to referenced ontologies/controlled vocabularies, with explicit CURIE format.
2. **Synonym Resolution Rate:** ≥98% of synonyms (across genes, proteins, phenotypes, and drugs) resolved and normalized, with explicit cross-references.
3. **Semantic Consistency:** ≥99% of edge types must pass ontology-driven schema validation (i.e., no illegal entity/edge pairings).

**Potential Bottlenecks:**
- Variant/PTM granularity: Many sources under-specify PTMs or fail to disambiguate tau isoforms.
- Phenotype drift: Clinical terms may be inconsistently mapped across cohorts—requires careful synonym harmonization and mapping to HPO/LOINC.

**Summary:**
- Insist on ontology-driven schema and entity normalization.
- Support for advanced biological nuance (tau/PTMs, phenotype progression, multi-modal evidence) is non-negotiable for AlzKB’s scientific rigor.
- Evidence scoring and provenance must be embedded semantically, not as free-text attributes.

Looking forward to Data Science Lead’s approach for extraction/validation and to harmonize our normalization pipeline.

## User

Data Science Lead (Extraction & Validation), please provide your thoughts on the discussion (round 1 of 3). If you do not have anything new or relevant to add, you may say "pass". Remember that you can and should (politely) disagree with other team members if you have a different perspective.

## Data Science Lead (Extraction & Validation)

**Data Science Lead (Extraction & Validation): Round 1 Input**

**1. Schema Core: Extraction Constraints and Validation-Driven Refinement**

*Re: Entity/Edge Types:*
- I fully agree that schema granularity is critical—especially for distinguishing tau isoforms, phosphorylated states, and clinical phenotypes specific to AD.
- For “co-occurs_with,” I urge we define strict context boundaries (e.g., *within same subject/timepoint/cohort*) to avoid spurious associations; otherwise, this edge can balloon false positives.
- Recommend adding explicit entity subtypes for “Protein” (e.g., “Protein Isoform,” “Post-Translationally Modified Protein”) and “Clinical Phenotype” (e.g., “Cognitive Domain,” “Disease Stage”) at extraction time, as this will facilitate both QA and downstream analytics.

*On Edge Types:*
- “causes” should be reserved for evidence with *explicit experimental manipulation* or robust Mendelian Randomization; otherwise, prefer “associated_with” (with evidence-grade qualifiers for strength/directionality).
- Insist on provenance and evidence context for *every* edge (biomarker_of, phosphorylates, etc.), including cohort/sample metadata at extraction.

**2. Data Strategy: Extraction, Validation, and Scoring**

*Data Source Prioritization:*
- Endorse ADNI, AMP-AD, and ROSMAP as primary for high-confidence, multi-modal data. For text mining, recommend restricting to *systematic reviews or meta-analyses* (e.g., PubMed, Cochrane) to minimize hallucination risk.
- Each extracted relation must be mapped to a *reference assertion* (table, figure, or explicit text statement) with source identifier (e.g., PMID, dataset accession).

*Evidence Scoring:*
- Propose a three-parameter scoring rubric:
  1. **Evidence Type** (Clinical > Human Post-Mortem > Animal/In Vitro > In Silico)
  2. **Assertion Strength** (Direct experimental, statistically significant association, inferred/weak evidence)
  3. **Source Concordance** (Observed in ≥2 independent datasets or publications)
- Relations failing to meet minimum evidence thresholds (e.g., single-source, text-mined, weak evidence) should be tagged “low-confidence” and quarantined from the main KG (held in a separate layer for curator review).

*Validation Protocols:*
- **Benchmarking**: All extractions cross-checked against gold-standard datasets (e.g., AD-related relations in Open Targets, curated AD pathway databases like AlzPathway).
- **Entity Resolution:** Multi-pass pipeline—first, exact-match to canonical ontologies (HGNC, UniProt, HPO, RadLex); second, synonym/alias expansion with scoring for ambiguity; third, manual/curator review for high-impact nodes (tau isoforms, critical clinical endpoints).
- **Error Analysis:** Track both false positives and false negatives per edge/entity type, with a hard threshold (e.g., <5% false positive rate on “biomarker_of” edges during QA).

**3. Success Metrics (KPIs):**
1. **Gold-standard Concordance:** ≥98% match to existing curated relations from AD-specific resources (for “encodes,” “biomarker_of,” and “phosphorylates”).
2. **False Positive Rate (manual review):** <5% for all mechanism-level edges (e.g., “phosphorylates,” “causes”).
3. **Provenance Completeness:** 100% of edges/entities must have computable, machine-readable provenance (source ID, evidence type, assertion strength).

**Anticipated Bottlenecks:**
- Entity resolution of ambiguous/multi-mapped proteins (MAPT isoforms, modified proteins).
- Validation lag for newly published associations not yet present in gold standards.
- Volume of low-confidence, text-mined relations requiring quarantine/curation.

**Summary:**
- Extraction and validation must be precision-first, with robust provenance capture and strict evidence curation.
- Edge/Entity types and evidence scoring need to be tightly coupled to AD-specific biological relevance and data quality.
- Strong alignment needed with ontologist and engineering to enforce entity normalization and evidence tracking at every pipeline stage.

Looking forward to the scientific critic’s perspective on coverage pitfalls and past failures to inform our QA and validation priorities.

## User

Scientific Critic (AlzKB), please provide your thoughts on the discussion (round 1 of 3). If you do not have anything new or relevant to add, you may say "pass". Remember that you can and should (politely) disagree with other team members if you have a different perspective.

## Scientific Critic (AlzKB)

**Scientific Critic (AlzKB): Round 1 Input**

**1. Schema Core: Critical Audit**

- *Entity Types:* Strongly support the explicit inclusion of “Protein Isoform” and “Post-Translationally Modified Protein” as distinct node types, rather than lumping them under generic “Protein.” Failure to distinguish, for example, between total tau, MAPT-001, and phosphorylated tau at S202/T205 (AT8 epitope) undermined prior AD KGs (see: Bio2RDF, Hetionet) and led to loss of mechanistic signal.
    - The same applies to “Abeta40” vs “Abeta42”—must be distinct nodes, not just synonyms.
- *Edge Types:* I reject “associated_with” or “co-occurs_with” as a primary edge unless strictly defined with cohort-level statistics and provenance, or as a secondary, low-confidence layer as suggested by the Data Science Lead. Prior AD KGs that relied on weakly-defined “associated_with” edges (e.g., DrugBank RDF, UMLS-based graphs) proved useless for mechanistic or translational queries.
- *Predicates like “causes”*—should only be instantiated with high-confidence, preferably direct experimental evidence (ideally from human data); otherwise, risk of circular reasoning is high, especially if training and evaluation sets overlap.

**2. Data Strategy: Provenance and Biological Plausibility**

- *Provenance:* Insist on pipeline-level enforcement—every triple must be linked to a PubMed ID, dataset accession, or unequivocal table/figure. No “inferred by algorithm” unless the method, data, and confidence are fully specified.
    - Many KGs (notably STRING) failed here—edges “borrowed” from less rigorous public sources lacked traceable evidence, reducing reliability for AD research.
- *Species Resolution:* Explicitly annotate source species for every relation/entity. Past projects frequently conflated murine and human data (e.g., SOD1, PSEN1 transgenic models), leading to biological implausibilities when KG users queried for drug targets or biomarkers.
- *Imaging/Molecular Crosswalks:* Be wary of over-interpretation when mapping imaging features to molecular or pathological nodes. Only assert “biomarker_of” where there is reproducible, peer-reviewed, *quantitative* evidence.

**3. Metrics: Quantitative Demand**

- *Precision/Recall/F1:* Prioritize precision at launch—recall can be iteratively improved, but high false positives (especially for “phosphorylates,” “biomarker_of,” and “causes”) erode trust. No qualitative promises (e.g., “comprehensive coverage”).
    - Insist on ≥95% precision (manual review) for all mechanism-level edges, as Data Science Lead proposes.
    - Require Gold Standard references (e.g., AlzPathway, Open Targets AD subset) for evaluation; do not use data sources as both train and test sets.
- *Entity Resolution Metrics:* Track and publish the rate of successful disambiguation for key AD-relevant entities (e.g., tau isoforms, Abeta variants, disease stages).
- *Provenance Completeness:* 100% of edges/entities must be resolvable to a primary source (PubMed ID, dataset row).

**Gaps & Pitfalls in Prior Efforts**

- *Murine/Human Data Conflation*: Prior AD KGs (Hetionet, some OpenBioLink releases) frequently mixed data from mouse models and human subjects with no explicit annotation, leading to misleading inferences—especially for therapeutic repurposing tasks.
- *Ontology Drift*: “Dementia” and “Alzheimer’s Disease” are not interchangeable. Prior efforts over-aggregated, diluting AD specificity (see: UMLS, Disease Ontology mappings).
- *Circular Reasoning in Evaluation*: Unacceptable to report performance using edges/nodes derived from the same sources as test sets.

**Summary Recommendations**

- Absolute requirement for provenance and species annotation.
- Reject generic, weak predicates as primary schema—must support biological specificity or quarantine as “low-confidence.”
- Precision-first, Gold Standard–anchored approach to metrics.
- Continuous audit for entity resolution gaps, especially for high-impact AD concepts (tau isoforms, Abeta40/42, clinical stages).

I strongly endorse the Data Science Lead’s quarantine layer for low-confidence edges and urge the team to bake these requirements into the pipeline and schema from day one.

## User

This concludes round 1 of 3 of discussion. Principal Investigator (Alzheimer's KG), please Synthesize team inputs. 1. Identify agreements vs. conflicts. 2. Resolve conflicts using provided evidence; favor data over opinion. 3. Decide the agenda status. 4. Ask 1 concrete question to clarify ambiguity if needed. Be concise..

## Principal Investigator (Alzheimer's KG)

**Principal Investigator (Alzheimer's KG): Synthesis of Round 1**

**1. Agreements vs. Conflicts**

**Agreements:**
- **Schema Core:** All support biologically precise entity and edge types, especially for AD specifics (tau isoforms, phosphorylated proteins, clinical phenotypes). There’s universal rejection of generic relationships and strong support for explicit evidence types and provenance for every edge.
- **Data Sources:** Consensus on ADNI, AMP-AD, ROSMAP, plus structured protein/ontology resources (UniProt, GO) as priorities. All stress the need for multi-modal and cross-validated data.
- **Evidence & Provenance:** All agree provenance must be computable and machine-readable, not free text, and that species and experimental context are essential metadata.
- **KPIs:** Precision is universally prioritized over recall at launch; all advocate for ≥95% precision (manual review) for mechanism-level edges. Entity resolution, provenance completeness, and ontology coverage are shared priorities.

**Conflicts:**
- **Entity Typing Granularity:** Technical Lead and Ontologist propose "Protein" as a main type (with PTMs/isoforms perhaps as attributes), but Data Science Lead and Critic insist on distinct nodes for isoforms and PTMs due to known failures in previous KGs.
- **Edge “co-occurs_with/associated_with”:** Technical Lead suggests its inclusion for multi-modal correlation; Data Science Lead and Critic warn of spurious associations without stringent constraints, preferring its quarantine or exclusion unless strictly defined.
- **Evidence Scoring Detail:** Ontologist and Data Science Lead both recommend multi-parameter scoring; Critic wants Gold Standard anchoring and strongly rejects self-referential evaluation.

**2. Resolution (Data Over Opinion):**
- **Protein Isoforms/PTMs:** Evidence from prior failures (Bio2RDF, Hetionet) and the lack of mechanistic fidelity argue in favor of *distinct nodes* for isoforms/PTMs, as recommended by Critic and Data Science Lead. Schema will adopt this stricter approach.
- **co-occurs_with/associated_with:** Given high risk of spurious links and consensus that only high-confidence relationships should enter the core graph, “co-occurs_with” will be restricted to a low-confidence/quarantine layer, not the primary KG.
- **Evidence and Provenance:** All relations must include computable provenance, experimental context (species, method), and pass a multi-factor evidence rubric (with Gold Standard benchmarking).

**3. Agenda Status**
- **Substantial alignment** on schema core, data source selection, evidence/provenance modeling, and success metrics.
- **Action required:** Refine and lock schema for explicit inclusion of isoforms/PTMs as nodes, restrict “co-occurs_with” to a secondary layer, and formalize the evidence scoring rubric and provenance model.

**4. Concrete Question to Clarify Ambiguity**
*For the Biomedical Ontologist:*  
**How do you propose we represent and uniquely identify tau isoforms and their post-translationally modified states (e.g., MAPT-001 phosphorylated at S202/T205), given existing ontology limitations? Should we extend current ontologies, or implement a compound identifier approach (e.g., UniProt ID + PTM site annotation)?**

Please prepare a concrete solution for the next round.

## User

Technical Lead (Knowledge Graph Engineering), please provide your thoughts on the discussion (round 2 of 3). If you do not have anything new or relevant to add, you may say "pass". Remember that you can and should (politely) disagree with other team members if you have a different perspective.

## Technical Lead (Knowledge Graph Engineering)

**Technical Lead (Knowledge Graph Engineering): Round 2 Input**

**1. Schema Core Refinement**

- **Adopting Distinct Nodes**: Fully support the move to represent protein isoforms and post-translationally modified (PTM) proteins as explicit nodes, not attributes. This enables precise mechanistic queries and addresses the historic pitfalls outlined by the Scientific Critic.
    - Implementation: Each node will be uniquely identified by a compound key (e.g., UniProt accession + isoform + PTM site, where available). For example, *MAPT-001_pS202/T205* could be represented as a unique node.
    - We will support entity-level mapping back to parent proteins and genes via explicit edges (“is_isoform_of”, “is_modified_form_of”).

- **Edge Type Adjustment**: Accept the restriction of “co-occurs_with”/“associated_with” to a low-confidence, non-primary layer. The core graph will use only high-confidence, mechanistically annotated edges (e.g., “phosphorylates”). “co-occurs_with” will be strictly defined (e.g., as “observed in same individual/timepoint with statistical significance”) and kept in a separate subgraph.

- **Entity Subtyping**: We will implement subtyping for clinical phenotypes (e.g., “Cognitive Domain” vs. “Disease Stage”) and for protein entities (e.g., “isoform”, “modified isoform”), to optimize retrieval and analytics.

**2. Provenance & Evidence Modeling**

- **Provenance Enforcement**: The core KG infrastructure will require a triple-store or property graph design where all edges and nodes include mandatory, computable provenance metadata (source ID, evidence type, assertion method, species, etc.).
    - Implementation: Use a provenance node or edge properties (using W3C PROV-O or similar) to encode these details, ensuring downstream auditability and regulatory compliance.

- **Evidence Scoring Integration**: Will work with Data Science Lead to enforce multi-parameter evidence scoring at ingestion, making “confidence tier” and “evidence strength” first-class graph properties.

**3. Architecture Implication**

- **Graph Database Selection**: Neo4j is suitable for property-rich, schema-flexible, high-performance query workloads (especially for path and pattern queries, which are common in mechanistic reasoning). If we require RDF compliance for ontological linking, Blazegraph or Amazon Neptune can be used for a triplestore approach—but with performance caveats for very large and deeply nested provenance.
    - Proposed: Use Neo4j as the primary KG, with periodic export to RDF for interoperability and external sharing.

- **Query Optimization**: With explicit node typing (isoform/PTM), we can index compound entity identifiers and provenance fields for rapid retrieval, supporting the <1s latency KPI.

**4. Pending Issue**

- **Tau Isoform Identification**: Will defer to Biomedical Ontologist for final guidance but will ensure the infrastructure supports compound identifiers and extensible node/edge annotation. If custom identifier conventions are required, will coordinate to enforce uniqueness and traceability at graph construction.

**Summary**

- Fully aligned with consensus: explicit isoform/PTM nodes, strict evidence/provenance requirements, and restriction of weak associations to a designated graph layer.
- Technical infrastructure will be built to support these priorities from day one, including indexing, provenance audit, and subgraph partitioning for low-confidence data.

Ready to implement as soon as ontology solutions for node uniqueness (esp. tau and similar proteins) are finalized.

## User

Biomedical Ontologist (AlzKB Semantics & Standards), please provide your thoughts on the discussion (round 2 of 3). If you do not have anything new or relevant to add, you may say "pass". Remember that you can and should (politely) disagree with other team members if you have a different perspective.

## Biomedical Ontologist (AlzKB Semantics & Standards)

**Biomedical Ontologist (AlzKB Semantics & Standards): Round 2 Input**

**1. Tau Isoform and PTM Representation—Concrete Solution**

- **Unique Identification Approach:**  
  The most robust solution for representing tau isoforms and PTMs is to adopt a **compound identifier scheme** built from existing ontology and database accessions, enriched with site-specific PTM annotations. This solution is both scalable and interoperable.

  - **Base Entity:**  
    - *Isoform:* Use UniProt accession for the MAPT gene product, plus the isoform identifier if specified (e.g., `UniProt:P10636-8` for MAPT-001).  
    - *PTM:* Append a PSI-MOD or RESID PTM identifier (e.g., `MOD:00046` for phosphorylation) and the specific residue(s), using a notation such as `UniProt:P10636-8|MOD:00046@S202/T205`.
        - Example node identifier: `UniProt:P10636-8|MOD:00046@S202,T205` (tau isoform 8, phosphorylated at S202 and T205).

  - **Node Structure:**  
    - *Node Label*: "Post-Translationally Modified Protein"
    - *Properties*:  
      - `parent_protein`: UniProt accession  
      - `isoform`: Isoform ID (if present)  
      - `modification`: PTM ontology identifier (e.g., PSI-MOD)  
      - `residue_position`: e.g., S202, T205  
      - `evidence`: reference to supporting provenance node  
      - `species`: NCBI Taxonomy ID

  - **Ontology Extension:**  
    - Where ontologies lack explicit terms for some tau isoforms or multi-site modifications, propose new terms to PSI-MOD or develop local CURIEs within AlzKB, explicitly mapped to parent entities.
    - Cross-reference MONDO/Orphanet for disease-specific isoforms if available.

**2. Edge Specification Updates**

- *Edges such as “phosphorylates”* must now point from the kinase protein node to the compound-identifier PTM tau node (not just to generic tau), e.g., `GSK3B → phosphorylates → UniProt:P10636-8|MOD:00046@S202,T205`.

- *Hierarchical Relationships*:  
    - `is_isoform_of` (isoform → canonical protein)  
    - `is_modified_form_of` (PTM node → isoform node)  
    - These edges should be typed and mapped to Relation Ontology (RO) where possible.

**3. Interoperability & Querying**

- All nodes will support CURIE-style IDs for external interoperability (e.g., mapping to Wikidata, OBO Foundry).  
- Compound identifiers should be indexed for query optimization as described by Technical Lead.

**4. Ontology-Driven Validation**

- All entity and edge types must be validated for:
    - *Ontology compliance*: 100% of isoform/PTM nodes must be mappable to UniProt+PSI-MOD or have explicit cross-walks.
    - *Uniqueness*: Compound identifiers must be globally unique within AlzKB, with collision checks at ingestion.
    - *Semantic relationships*: Enforce proper parent-child relationships in the graph (isoform/PTM → protein → gene).

**5. Additional Note on Ambiguity Resolution**

- For ambiguous literature references (e.g., “phosphorylated tau” without site or isoform), default to the most inclusive node, but always annotate with an “ambiguity flag” and restrict usage to low-confidence layers.

**Summary**

- Propose to operationalize compound identifiers (UniProt + isoform + PTM + residue) for all tau, Abeta, and other key AD-relevant proteins and modifications.
- All such nodes will be mapped to ontologies wherever possible, with local extension as needed, and strict semantic validation enforced.
- This approach enables both mechanistic fidelity and computational interoperability—resolving the ambiguity highlighted in the previous round.

Ready to coordinate with graph engineering and data science leads to enforce this standard at every stage, and to generate mapping/extension documentation for custom AlzKB nodes as needed.

## User

Data Science Lead (Extraction & Validation), please provide your thoughts on the discussion (round 2 of 3). If you do not have anything new or relevant to add, you may say "pass". Remember that you can and should (politely) disagree with other team members if you have a different perspective.

## Data Science Lead (Extraction & Validation)

**Data Science Lead (Extraction & Validation): Round 2 Input**

**1. Operationalizing Compound Identifiers in Extraction**

- *Pipeline Adaptation*: Fully support the Biomedical Ontologist’s compound identifier scheme for isoforms and PTMs. The extraction pipeline will:
    - Parse mentions from structured/unstructured data into UniProt + isoform + PTM + residue format wherever textual or tabular evidence is sufficient.
    - For ambiguous protein/PTM mentions (e.g., “phosphorylated tau” without position), assign to the parent node with an “ambiguity flag” property, and restrict these edges to the quarantine/low-confidence layer as previously agreed.
    - All extracted nodes/edges will carry their evidence and ambiguity status, enforcing high-confidence boundaries in the main KG.

- *Automated Mapping and Validation*: Will implement an entity normalization module that:
    - Performs initial exact-matching to UniProt/PSI-MOD per ontologist’s mapping.
    - Applies synonym/alias tables to map literature variants to their canonical identifiers.
    - Runs collision checks for compound identifiers at batch load, as requested.

**2. Relation Extraction and Evidence Scoring**

- *Mechanistic Edges (“phosphorylates”, “binds_to”):*
    - Will only instantiate these edges for PTM nodes if the source explicitly supports isoform and modification context (e.g., “GSK3B phosphorylates tau at S202 on isoform 8, in AD cortex”).
    - Where source evidence is ambiguous (e.g., kinase assays on “tau”), edges will connect to the parent isoform or generic MAPT node, *tagged as low-confidence*.

- *Evidence Metadata Enforcement*:
    - Each node/edge will link to a unique provenance object:  
        - Source (PubMed ID, accession, table/figure link)  
        - Evidence type (clinical, post-mortem, animal, in vitro, in silico)  
        - Assertion method/strength (direct assay, literature review, computational inference)  
        - Species (NCBI Taxonomy ID)
    - These will be encoded for every triple, and form the basis for the multi-parameter evidence score.
    - Ambiguous or single-source assertions (especially for “causes”, “biomarker_of”) will be automatically quarantined.

**3. Benchmarking and Validation Workflow**

- *Gold-Standard Anchoring*: As edges are extracted/normalized, their existence and context will be cross-checked with AlzPathway, Open Targets, and other manually curated AD resources.
- *Manual Validation*: All high-impact mechanistic edges (e.g., GSK3B→phosphorylates→tau pS202/T205) will undergo manual review in the first build, especially if they arise from a single or ambiguous source.
- *Error Reporting*: Will document and route all ambiguous/low-confidence extractions for curator review, and provide error metrics (FP, FN rates) per entity/edge type, as previously described.

**4. Data Integration Constraints**

- *Entity Uniqueness and Reconciliation*:  
    - All batch ingests will include a collision/resolution step using the compound identifier system, with error logging for duplicates or near-matches.
    - Ambiguous entities (esp. in legacy datasets) will be versioned and sequestered in the low-confidence/quarantine layer, with clear cross-references for downstream curation.

**Summary**

- Will re-tool extraction/validation to enforce the compound identifier standard for protein isoforms/PTMs, as defined by the Ontologist.
- All nodes/edges will carry explicit, computable evidence/provenance for high-confidence use, with ambiguity handling as a first-class citizen.
- Strongly aligned with graph engineering and ontology for schema, uniqueness, and curation boundaries.

**Pending Coordination**

- Will collaborate with the Technical Lead to ensure provenance and ambiguity flags are fully queryable and indexable in the graph database.
- Seek clarification from Ontologist: For cases where multiple PTMs occur on the same isoform (e.g., tau with both phosphorylation and acetylation), do we create a distinct node for each modification state, or a node representing the combinatorial modified state?

Ready to move forward once that ambiguity is resolved.

## User

Scientific Critic (AlzKB), please provide your thoughts on the discussion (round 2 of 3). If you do not have anything new or relevant to add, you may say "pass". Remember that you can and should (politely) disagree with other team members if you have a different perspective.

## Scientific Critic (AlzKB)

**Scientific Critic (AlzKB): Round 2 Input**

**1. Audit of Compound Identifier Approach for Tau Isoforms & PTMs**

- Strong endorsement of the compound identifier method (UniProt + isoform + PTM + residue) as described by the Biomedical Ontologist and embraced by the Data Science Lead.
    - This approach directly addresses the most frequent sources of conflation and ambiguity in prior AD KGs.
    - It is especially critical for tau biology, where both isoform and site-specific modifications (e.g., pS202/T205, acetyl-K274) are mechanistically distinct and have non-overlapping evidence and clinical relevance.
    - Accepts that ambiguous mentions (“phosphorylated tau”) are flagged and segregated to a separate layer, which is necessary to prevent polluting the high-confidence core KG.

**2. KG Structure and Provenance**

- The plan to enforce provenance (PubMed ID, table/figure, species, evidence type) for *every* node and edge remains non-negotiable. Past failures in this area (e.g., STRING, BioGRID in AD application) have been a major reason for lack of trust and downstream usage.
- Fully support the technical design for mandatory provenance and ambiguity flags—this will make the AlzKB transparent and auditable by external experts.

**3. Biological Blind Spots to Watch**

- *Combinatorial PTMs*: Echoing the Data Science Lead’s question—combinatorial modification states (e.g., tau phosphorylated at multiple sites and acetylated at others) are biologically plausible and often described in the literature. Prior KGs did not handle this; it must be specified whether these are distinct nodes or represented by a “PTM state vector.”
    - Failure to do so risks losing findings on combinatorial PTM effects (which are increasingly central in AD pathogenesis).
- *Ambiguity Drift*: It is critical that ambiguous/legacy nodes do not “leak” into the high-confidence KG over time (e.g., during integration or curation). Recommend quarterly audits to ensure strict boundary enforcement.

**4. Metrics and Validation**

- Insist on reporting the following, especially for tau/PTM nodes:
    - *Disambiguation Rate*: % of tau/PTM mentions resolved to unique nodes vs. percentage sent to “ambiguous” quarantine.
    - *Provenance Completeness*: % of mechanistic edges supported by direct experimental evidence in humans vs. preclinical.
    - *Species Annotation*: Track the proportion of nodes/edges with explicit species provenance—data from murine or in vitro systems must be flagged at the edge and node level.

**5. Lessons from Prior Failures**

- *Hetionet, Bio2RDF* failed to distinguish between tau isoforms and PTM states, resulting in misleading mechanistic inferences (e.g., implying a kinase acts on “tau” generically, rather than on a specific isoform/PTM relevant to AD).
- *STRING* and other PPI KGs have been discredited in AD translational work due to lack of species annotation and provenance—must not repeat this.

**Summary & Recommendations**

- Strong support for the emerging schema and extraction pipeline, with the caveat that combinatorial PTM state modeling must be formally specified.
- Maintain strict separation between ambiguous/legacy data and the high-confidence core KG, with routine audits.
- Demand that all validation and coverage metrics, especially for tau, Abeta, and key clinical phenotypes, are reported by unique node (not collapsed categories).

**Pending Clarification**
- Request that the Biomedical Ontologist make an explicit recommendation (for next round) on the representation of combinatorial PTM states: distinct nodes for each unique combination, or a vectorized/modular approach.

Other than this, approve of the plan’s direction and alignment with rigorous, biologically plausible standards.

## User

This concludes round 2 of 3 of discussion. Principal Investigator (Alzheimer's KG), please Synthesize team inputs. 1. Identify agreements vs. conflicts. 2. Resolve conflicts using provided evidence; favor data over opinion. 3. Decide the agenda status. 4. Ask 1 concrete question to clarify ambiguity if needed. Be concise..

## Principal Investigator (Alzheimer's KG)

**Principal Investigator (Alzheimer's KG): Synthesis of Round 2**

**1. Agreements vs. Conflicts**

**Agreements:**
- **Compound Identifier for PTMs/Isoforms:** Full consensus to use a compound identifier (UniProt accession + isoform ID + PTM ontology + residue position(s)) for explicit node representation of tau isoforms and PTMs, ensuring mechanistic fidelity and interoperability.
- **Ambiguity Handling:** All agree ambiguous references (e.g., non-specific “phosphorylated tau”) are flagged and quarantined in a separate, low-confidence layer—never in the high-confidence core KG.
- **Provenance and Evidence Requirements:** Universal consensus that mandatory, computable provenance (including species, evidence type, source ID) is attached to every node/edge, with technical and process enforcement.
- **Edge Specificity:** Edges (e.g., “phosphorylates”) must explicitly connect to the relevant modified isoform/PTM node—not generic entities.
- **Validation and Auditing:** Support for routine audits to prevent leakage of ambiguous data, and for reporting metrics by unique node (not collapsed categories).

**Conflicts:**
- **Combinatorial PTMs Representation:** Open issue: how to model cases where the same isoform is modified at multiple sites (e.g., phosphorylation + acetylation, or multiple phosphorylations). Data Science Lead and Scientific Critic both flagged this as a critical area needing a formal rule—should combinatorial PTM states be modeled as unique nodes or in a modular/vectorized way?
- **None otherwise:** No other active conflicts; strong technical, ontological, and operational alignment otherwise.

**2. Conflict Resolution (Evidence-Based)**
- **Combinatorial PTM Modeling:** Literature and prior failures (e.g., lack of combinatorial PTMs in Bio2RDF, Hetionet) support that failing to model combinatorial states can obscure key disease mechanisms. However, modeling every combination as a unique node could explode the graph size. Decision deferred to Biomedical Ontologist for a scalable, ontology-anchored solution—e.g., hybrid: unique node for experimentally-verified PTM combinations, vector-style annotation for less-certain or combinatorially possible states.

**3. Agenda Status**
- **Agenda is on track:** Schema, provenance model, and extraction/validation approach are now in near-complete alignment and ready for technical implementation—pending finalization of combinatorial PTM handling.
- **Next Steps:** Await explicit recommendation from Biomedical Ontologist on combinatorial PTMs (see below); incorporate solution into schema and extraction/validation design.

**4. Concrete Question to Clarify Ambiguity**
*For the Biomedical Ontologist:*
**What is your recommended approach for representing tau isoforms with multiple, simultaneous PTMs (i.e., combinatorial PTM states)? Should each experimentally confirmed combination be a distinct node with its own compound identifier, or should we support a modular/vectorized annotation for PTM state, and if so, how will this be encoded to enable unique retrieval and evidence tracking?**  
Please outline your solution and its ontological justification for the final round.

## User

Technical Lead (Knowledge Graph Engineering), please provide your thoughts on the discussion (round 3 of 3). If you do not have anything new or relevant to add, you may say "pass". Remember that you can and should (politely) disagree with other team members if you have a different perspective.

## Technical Lead (Knowledge Graph Engineering)

**Technical Lead (Knowledge Graph Engineering): Round 3 Input**

**1. Combinatorial PTM State Representation: Engineering Considerations**

- **Scalability & Retrieval:**  
  If we instantiate a unique node for every possible combinatorial PTM state (e.g., tau isoform 8, phosphorylated at S202, T205, AND acetylated at K274), the number of nodes could grow exponentially—especially for proteins with many modifiable residues. This would increase storage, slow queries, and complicate updates.

- **Evidence-Driven Instantiation (Preferred Hybrid Model):**  
  Recommend **restricting distinct nodes to combinatorial PTM states that are *experimentally validated* in AD contexts** (i.e., only instantiate a node when supported by literature, dataset, or curated resource).  
    - Node identifier: `UniProt:P10636-8|MOD:00046@S202,T205|MOD:00394@K274`
    - Node properties: array or dictionary structure for PTMs (`{MOD:00046:[S202,T205], MOD:00394:[K274]}`)  
    - All edges and provenance still point to the experimentally observed state, not theoretical combinations.

- **Modular/Vectorized Annotation for Unconfirmed States:**  
  For potential or computationally predicted combinatorial states not yet confirmed by direct evidence:
    - Represent the state as a parent node (e.g., “tau isoform 8”) with edges to modular PTM nodes (e.g., “phosphorylated at S202,” “acetylated at K274”).  
    - Flag these edges with a “predicted” or “putative” evidence code, and restrict to the low-confidence layer for curation and future updates.

- **Query Optimization:**  
  - Index compound identifiers to enable rapid retrieval of specific combinatorial PTM nodes.
  - For more exploratory queries (e.g., “all tau isoforms phosphorylated at any site”), leverage graph traversals from isoform node to PTM-specific nodes (including combinatorial nodes if present).

- **Schema & Ontology Mapping:**  
  - All combinatorial state nodes must be mapped to underlying ontologies (UniProt + multiple PSI-MODs) or locally assigned AlzKB CURIEs, with explicit structure for machine parsing.

**2. Data Integrity and KG Evolution**

- **Node Uniqueness & Provenance:**  
  Mandatory uniqueness checks for each compound identifier (including all PTMs and positions).
  All combinatorial state nodes must link to their supporting evidence and be versioned for traceability.

- **Maintenance:**  
  System will allow addition of new combinatorial nodes as evidence emerges, and automated migration of modular PTM states to full nodes upon validation.

**Summary/Recommendation**

- Strongly endorse a **hybrid approach**: instantiate combinatorial PTM nodes only for experimentally validated states in AD, with modular annotation and low-confidence partitioning for predicted/unconfirmed combinations.
- This balances graph size, retrieval precision, and biological fidelity—addressing the concerns of evidence-based modeling and scalability.
- Ready to operationalize this in the KG infrastructure, provided the ontological mapping and identifiers are finalized by the Biomedical Ontologist.

Will coordinate with Data Science for evidence pipeline integration and ensure query patterns are optimized for both high-confidence and exploratory use cases.

## User

Biomedical Ontologist (AlzKB Semantics & Standards), please provide your thoughts on the discussion (round 3 of 3). If you do not have anything new or relevant to add, you may say "pass". Remember that you can and should (politely) disagree with other team members if you have a different perspective.

## Biomedical Ontologist (AlzKB Semantics & Standards)

**Biomedical Ontologist (AlzKB Semantics & Standards): Round 3 Input**

**1. Recommendation for Combinatorial PTM State Representation**

**Hybrid Model—Evidence-Driven Instantiation + Modular Annotation (Ontology Justification):**

- **Distinct Nodes for Experimentally Observed States:**  
  - *Ontology Principle:* Ontologies such as UniProt, PSI-MOD, and PRO (Protein Ontology) support unique identifiers for protein forms with multiple modifications, but only where experimentally observed and described.  
  - *Implementation:*  
      - For tau (MAPT) isoforms verified in AD with specific combinatorial PTMs (e.g., pS202/pT205 + acK274 on MAPT-001), create a node with a compound identifier:  
        *`UniProt:P10636-8|MOD:00046@S202,T205|MOD:00394@K274`*  
      - All node properties and edges must reflect the combined modification state and link to the supporting evidence (PubMed ID, dataset accession, etc.).  
      - Parent relationships:  
        - `is_modified_form_of` (combinatorial PTM node → isoform node)  
        - `is_isoform_of` (isoform node → canonical protein node)

- **Modular Annotation for Theoretical/Unconfirmed States:**  
  - *Ontology Principle:* Use modular design for combinatorial states not yet experimentally validated.  
  - *Implementation:*  
      - Represent the base isoform node and connect to individual PTM nodes (e.g., “phosphorylated at S202,” “acetylated at K274”) by edges.  
      - Each PTM edge carries its own evidence code (direct, inferred, predicted) and provenance.  
      - These combinations are excluded from the high-confidence, core KG and instead reside in a putative/low-confidence subgraph.  
      - This enables future promotion to full, unique nodes upon new experimental evidence.

- **CURIEs and Ontology Mapping:**  
  - For observed combinatorial states, register internal AlzKB CURIEs and cross-reference to PRO or submit requests to PSI-MOD if no existing identifier exists.  
  - All identifiers must be compatible with OBO Foundry and linked to underlying UniProt, PSI-MOD, and, where available, PRO terms.

**2. Query and Ontological Integrity**

- **Retrieval:**  
  - Queries for “tau phosphorylated at any site” traverse from isoform node to all connected PTM nodes.  
  - Queries for “tau with specific PTM combinations” can directly retrieve distinct nodes if they exist, or reconstruct compositionally from modular PTMs with appropriate evidence codes.

- **Validation:**  
  - Uniqueness checks at node ingestion for each combinatorial identifier.  
  - Mandatory provenance for every edge connecting a combinatorial node, including experimental system and species.

**3. Rationale and Precedent**

- *PRO* (Protein Ontology) provides for combinatorial forms but only instantiates those with experimental evidence.
- This hybrid approach is ontologically correct, scalable, and maximizes both precision and utility.

**4. Ambiguity Management**

- *Ambiguous combinatorial states* (e.g., “hyperphosphorylated tau”) default to the modular edge model with a “broad/ambiguous” evidence flag, residing outside the high-confidence KG until further specification is possible.

**Summary**

- Formally recommend the hybrid approach:  
    - **Distinct combinatorial PTM nodes for experimentally validated states**  
    - **Modular, evidence-flagged annotations for theoretical or ambiguous combinations**  
- This is fully aligned with OBO Foundry/PRO best practices and balances biological rigor with scalability.
- Ready to draft ontology mapping documentation, coordinate with the Technical Lead for identifier enforcement, and with Data Science for extraction pipeline adaptation.

## User

Data Science Lead (Extraction & Validation), please provide your thoughts on the discussion (round 3 of 3). If you do not have anything new or relevant to add, you may say "pass". Remember that you can and should (politely) disagree with other team members if you have a different perspective.

## Data Science Lead (Extraction & Validation)

**Data Science Lead (Extraction & Validation): Round 3 Input**

**1. Extraction Pipeline Adaptation for Combinatorial PTMs**

- **Adopting the Hybrid Model**: Fully endorse the Biomedical Ontologist’s hybrid approach—distinct nodes for experimentally confirmed combinatorial PTM states, modular annotation for theoretical/ambiguous cases.
    - *Extraction logic*: During entity/edge extraction, the pipeline will attempt to normalize to a unique combinatorial node if the evidence (literature, database, or dataset) explicitly specifies all relevant PTMs on the same isoform/molecule in the same biological context.
    - *If evidence is partial or inferred*: Extract modular edges from the isoform node to each individual PTM node, and flag the assertion as “putative” or “ambiguous” (using a standardized evidence code).
    - *Promotion logic*: As new evidence emerges (e.g., new publication confirms a specific combination in AD), the pipeline will upgrade modular annotations to a distinct combinatorial node, preserving provenance and version history.

- **Identifier Construction and Provenance**:
    - Will enforce the compound identifier structure as specified (e.g., UniProt:P10636-8|MOD:00046@S202,T205|MOD:00394@K274).
    - All edges to combinatorial nodes will be linked to full provenance records (source, species, evidence type), with automatic checks for node uniqueness and collision at load.

**2. Evidence Scoring and Layer Assignment**

- *High-confidence layer*: Only nodes/edges whose combinatorial PTM state is directly and unambiguously supported by evidence (including species and experimental system) are promoted.
- *Putative/low-confidence layer*: Modular PTM states and ambiguous combinatorial assignments are sequestered here, as agreed.
- *Curation queue*: The pipeline will output a report of ambiguous or modular-only extractions for manual/curatorial review, supporting quarterly audits as recommended by the Scientific Critic.

**3. Metrics and QA Enhancements**

- *Disambiguation Rate*: Will track and report % of tau/PTM mentions mapped to unique combinatorial nodes vs. modular/ambiguous layers, as one of our KPIs.
- *False positive control*: Maintain <5% FP rate for combinatorial edges in the high-confidence layer (by cross-checking against gold standard and manual review).
- *Provenance completeness*: Reconfirm 100% of nodes/edges in both layers carry machine-readably coded provenance.

**4. Interoperability and Versioning**

- *Ontology mapping*: Will align all extracted combinatorial nodes with PRO/PSI-MOD/AlzKB CURIEs as provided by the Ontologist.
- *Versioning*: Each combinatorial node will include a version field and history of evidence accession, facilitating updates as knowledge evolves.

**Summary**

- The hybrid model is practical, precise, and implementable in the current extraction/validation framework.
- Will enforce all specified rules for provenance, ambiguity handling, node uniqueness, and curation workflow.
- Ready to operationalize this approach in the pipeline and align outputs with graph engineering and ontology standards.

No disagreement; plan is robust and well-justified. Awaiting confirmation from the Scientific Critic before proceeding to final integration.

## User

Scientific Critic (AlzKB), please provide your thoughts on the discussion (round 3 of 3). If you do not have anything new or relevant to add, you may say "pass". Remember that you can and should (politely) disagree with other team members if you have a different perspective.

## Scientific Critic (AlzKB)

**Scientific Critic (AlzKB): Round 3 Input**

**1. Evaluation of Hybrid Model for Combinatorial PTMs**

- **Full Endorsement:**  
  The hybrid strategy—rooted in ontological precedent (PRO, PSI-MOD) and balancing experimental specificity with scalability—directly addresses the core sources of biological and technical error that plagued earlier AD KGs.
    - *Distinct combinatorial nodes* for experimentally verified states ensure mechanistic fidelity and precise evidence tracking.
    - *Modular, evidence-flagged annotation* for theoretical or ambiguous states prevents graph bloat and maintains a clean, auditable separation between high-confidence knowledge and putative hypotheses.

**2. Critical Strengths**

- **Mitigates Ontological Drift:**  
  This approach prevents the collapse of important, clinically relevant distinctions (e.g., tau pS202/pT205 vs. “hyperphosphorylated tau” vs. tau pS396+acetyl-K274), which was a key failure in prior KGs (Hetionet, OpenBioLink).
- **Enforces Provenance and Species Resolution:**  
  The plan continues to guarantee that every combinatorial PTM node and edge is accompanied by computable provenance (PubMed ID, species, experimental system).
- **Guards Against Circular Reasoning:**  
  Manual and gold-standard cross-checks are built in at both extraction and update stages, reducing the risk of self-referential or “noisy” edges entering evaluation metrics or downstream analytics.

**3. Audit and Maintenance Recommendations**

- *Quarterly Audit*: Reiterate the need for scheduled reviews of the low-confidence/modular layer, to ensure ambiguous or “promoted” combinatorial states are tracked and resolved as new evidence emerges.
- *Metric Reporting*: Approve the KPI of reporting disambiguation rates and provenance completeness specifically for tau/PTM combinatorial entities, as these are the most likely source of confusion in translational queries.
- *Version History*: Support the Data Science Lead’s proposal to version combinatorial nodes, ensuring that KG users can trace historical changes in biological knowledge and provenance.

**4. Remaining Caveats**

- *No “Default Promotion”*: Under no circumstances should modular/ambiguous composite states be promoted to high-confidence nodes without direct, peer-reviewed evidence. This must be a hard constraint enforced at both pipeline and curation levels.

**Summary**

- The hybrid approach, with strict evidence/curation boundaries, directly addresses the pitfalls of past AD KGs and sets a new rigor standard for the field.
- Provenance, disambiguation metrics, and species annotation are now robustly operationalized.
- Provided the hard constraint on evidence-driven promotion is strictly enforced, I have no reservations and consider the technical and ontological plan ready for implementation.

No further objections; recommend moving forward to formalize and document the agreed KG specification.

## User

Principal Investigator (Alzheimer's KG), please summarize the meeting in detail for future discussions, provide a specific recommendation regarding the agenda, and answer the agenda questions (if any) based on the discussion while strictly adhering to the agenda rules (if any)..

As a reminder, here is the agenda for the meeting:

Task: Build a scalable, retrieval-optimized Knowledge Graph for Alzheimer's Disease research.

TASK: Define the Technical Specification for AlzKB.
The team must agree on the architectural foundation before implementation.

OUTPUT REQUIREMENTS:
1. SCHEMA CORE: Define top 6 Entity Types and 6 Edge Types (Must be biologically specific, e.g., 'phosphorylates' not 'interacts').
2. DATA STRATEGY: Select 4 priority Data Sources (e.g., ADNI) and define the Evidence Scoring mechanism (e.g., 'Clinical vs. Preclinical').
3. SUCCESS METRICS: Define 3 quantitative KPIs for coverage and precision.

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

**Restated Objective:**  
The team was tasked with defining the technical specification for AlzKB, a scalable and retrieval-optimized Alzheimer’s Disease knowledge graph. This included rigorous definition of the schema core (entities and edges), data strategy (sources, evidence scoring), and quantifiable success metrics. The process required specificity, AD-focused biological nuance (e.g., explicit tau isoform/PTM modeling), and enforceable provenance and validation standards.

---

### Team Member Input

#### Technical Lead (Knowledge Graph Engineering)
- Supported explicit node representation for protein isoforms and PTMs, using compound identifiers (UniProt + isoform + PTMs + residues).
- Proposed a hybrid model for combinatorial PTMs: only instantiate nodes for experimentally confirmed states; use modular annotation for theoretical/unconfirmed combinations.
- Emphasized strict evidence/provenance enforcement and subgraph partitioning (high vs. low confidence).
- Advocated Neo4j for the main graph with periodic RDF exports for interoperability.

#### Biomedical Ontologist (AlzKB Semantics & Standards)
- Developed the compound identifier scheme for tau isoforms/PTMs, aligning with UniProt, PSI-MOD, and, where available, PRO.
- Advocated for the hybrid combinatorial PTM representation: 
    - Distinct nodes for experimentally observed states,
    - Modular edge-based annotation for theoretical/ambiguous states.
- All nodes/edges must have explicit ontology mappings and computable provenance.
- Provided detailed schema for hierarchical relationships (e.g., is_isoform_of, is_modified_form_of) and management of ambiguous data.

#### Data Science Lead (Extraction & Validation)
- Aligned with the hybrid PTM model; pipeline will instantiate distinct nodes only for confirmed combinatorial PTMs, and modular annotations (with evidence codes) for others.
- Extraction/validation will enforce exact-match normalization, provenance, and ambiguity handling.
- Will implement promotion logic for modular PTM states as evidence emerges.
- KPIs will include disambiguation rates, false positive rates (<5% for mechanistic edges), and provenance completeness (100%).

#### Scientific Critic (AlzKB)
- Strongly endorsed the hybrid approach, citing historical failures due to conflation of isoforms/PTMs and lack of provenance.
- Stressed rigorous separation of high-confidence and ambiguous data, with quarterly audits.
- Supported reporting of disambiguation rates, provenance completeness, and strict evidence thresholds for node/edge promotion.
- Explicitly warned against promoting modular/ambiguous states to high-confidence nodes without direct evidence.

---

### Recommendation

**I recommend adopting the following technical specification for AlzKB:**

#### 1. Schema Core

*Entity Types*  
1. **Gene/Variant** (e.g., MAPT, APOE ε4, using HGNC/dbSNP identifiers)
2. **Protein Isoform** (explicit UniProt isoform IDs)
3. **Post-Translationally Modified Protein** (compound identifier: UniProt + isoform + PTMs + residues)
4. **Small Molecule/Drug** (ChEMBL/DrugBank/PubChem)
5. **Clinical Phenotype** (HPO, LOINC, CDR/MMSE, AD-specific staging)
6. **Imaging Feature** (RadLex, LOINC, ADNI imaging signatures)

*Edge Types*  
1. **encodes** (Gene → Protein Isoform)
2. **phosphorylates** (Protein → PTM Protein, with explicit site and isoform)
3. **binds_to** (Small Molecule/Drug → Protein/Protein Isoform/PTM)
4. **biomarker_of** (Imaging Feature/Protein/PTM → Clinical Phenotype)
5. **causes** (Pathological Process or PTM State → Clinical Phenotype) [strict evidence only]
6. **is_modified_form_of** (PTM Protein → Protein Isoform)  
  *(Note: “co-occurs_with” and weak “associated_with” edges are quarantined in a low-confidence layer, not in the primary KG.)*

#### 2. Data Strategy

- **Priority Data Sources:**  
    1. *ADNI* (clinical, imaging, biomarker)  
    2. *AMP-AD* (multi-omics, gene/protein/PTM data)  
    3. *ROSMAP* (longitudinal clinical, neuropath, omics)  
    4. *UniProt/PSI-MOD/PRO* (canonical protein forms, PTM ontology, isoform data)  

- **Evidence Scoring Mechanism:**  
    - **Multi-factor score:**  
        - Evidence type (Clinical > Human Post-mortem > Animal/In vitro > In silico)  
        - Assertion strength (Direct assay > Statistical association > Inferred)  
        - Source concordance (Observed in ≥2 studies/datasets)  
    - **Provenance:** Every node/edge must link to machine-readable, granular provenance (PubMed ID, dataset accession, species, system).

- **Ambiguity Management:**  
    - All ambiguous descriptions (e.g., “phosphorylated tau” with no site) are flagged and maintained in a strictly separated, low-confidence subgraph.

#### 3. Success Metrics (Quantitative KPIs)

1. **Coverage:** ≥90% of known AD-relevant genes/proteins/PTMs and clinical phenotypes (by cross-reference to AMP-AD, AlzPathway, Open Targets AD).
2. **Precision:** ≥95% precision (manual review/gold standard concordance) for mechanistic edges (e.g., “phosphorylates,” “biomarker_of,” “causes”) in the high-confidence core KG.
3. **Provenance Completeness:** 100% of nodes and edges in the high-confidence layer must have computable, machine-readable provenance (source ID, species, evidence strength).
    - *Additional metric:* Disambiguation rate for tau/PTM entities (target ≥85% unique mapping for high-confidence nodes).

**Justification:**  
This specification delivers maximum biological and translational relevance for AD, explicitly addresses the pitfalls of previous KGs (isoform/PTM conflation, provenance drift), enforces evidence-driven graph construction, and remains computationally scalable.

---

### Next Steps

1. **Schema Finalization:**  
   - Biomedical Ontologist to deliver finalized ontology crosswalks and identifier conventions, especially for combinatorial PTM nodes.
   - Technical Lead to formalize the graph data model and indexing strategy for compound identifiers.

2. **Pipeline Implementation:**  
   - Data Science Lead to adapt extraction and validation pipelines for hybrid PTM modeling, provenance enforcement, and ambiguity management.
   - Technical Lead to set up KG infrastructure with partitioning for low-confidence/ambiguous data.

3. **QA & Audit Planning:**  
   - Establish the manual review panel for edge validation and quarterly audit protocol for low-confidence layer.
   - Define metrics monitoring scripts for coverage, precision, provenance, and disambiguation rates.

4. **Integration & Documentation:**  
   - Draft data integration and curation documentation, including promotion logic for modular-to-combinatorial node upgrades as evidence emerges.
   - Prepare initial user documentation on entity/edge types, evidence scoring, and querying instructions.

5. **Pilot Build & Review:**  
   - Assemble the first pilot build of AlzKB, covering tau, amyloid, and top AD risk variants, and run the full validation workflow.
   - Schedule meeting to review metrics, coverage, and user feedback before public release.

**The team is now ready to implement AlzKB according to the agreed technical specification, with processes in place to maintain AD-specific biological fidelity, provenance, and continuous audit.**


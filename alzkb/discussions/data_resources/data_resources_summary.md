# Meeting Summary: Data Resources Selection
**Phase:** data_resources
**Timestamp:** 2025-12-24T18:01:17.052006

## Summary
**TO:** AlzKB Research Consortium
**FROM:** Principal Investigator
**SUBJECT:** FINAL DECISION: Data Resource Selection & Ingestion Strategy (Phase 2)

---

### EXECUTIVE SUMMARY

This meeting has successfully established a scientifically rigorous foundation for the AlzKB knowledge graph. We have moved beyond simple data aggregation to a **Stratified Evidence Architecture**.

The Scientific Critic’s intervention regarding ancestry bias and biomarker harmonization has saved this project from a fatal validity failure. We are no longer simply "loading data"; we are curating a context-aware graph that distinguishes between established clinical facts (ADNI), population-specific genetic risks (Ancestry-Tagged GWAS), and mechanistic hypotheses (Reactome).

The pipeline is now **APPROVED** for execution, contingent on the strict adherence to the Revised Protocols defined below.

---

### 1. APPROVED DATA RESOURCES MANIFEST (FINAL)

The following resources are cleared for ingestion. Any source not listed here is **REJECTED** for v1.0.

#### **TIER 1: THE "PROVEN" CORE (Clinical & Genomic Backbone)**
| Resource | Specific Dataset/File | Ingestion Filters (Mandatory) | Logic Branch |
| :--- | :--- | :--- | :--- |
| **ADNI** | `ADNIMERGE`, `UPENNBIOMK_MASTER` | **No Raw Assays.** Use only harmonized Elecsys-scaled columns. Drop if `VISCODE` gap > 45 days. | `Proven` |
| **NHGRI-EBI GWAS** | Full Catalog Download | `p_value < 5e-8` **AND** `N > 10,000` **AND** `Ancestry != NULL`. | `Hypothesis` |
| **Reactome** | Pathway Standard (BioPAX) | `Organism = Homo sapiens` Only. No `IEA` (Electronic Annotation). | `Hypothesis` |
| **Ensembl / dbSNP** | REST API | Canonical Resolution for all RSIDs. | `Backbone` |

#### **TIER 2: CONTEXT ENRICHMENT**
| Resource | Specific Dataset/File | Ingestion Filters (Mandatory) | Logic Branch |
| :--- | :--- | :--- | :--- |
| **DisGeNET** | Curated Associations | `Score > 0.5` **AND** `Evidence Index >= 0.8` **AND** `Organism = Human`. **Strict exclusion of Animal Models.** | `Hypothesis` |
| **ChEMBL** | Binding Assays | `Assay Type = 'B'`, `Standard Value <= 10,000 nM`. | `Hypothesis` |

---

### 2. TECHNICAL SPECIFICATIONS (REVISED)

#### **A. The "Ancestry-Aware" GWAS Schema**
*Incorporating Feedback: Scientific Critic (Bias), Ontologist (NCIT Mapping)*

The schema for `HypothesisAssociation` nodes is updated to support population context. The ETL pipeline must map free text to NCIT codes.

```turtle
# URI Construction Pattern for GWAS Edges
:Assoc_rs7412_AD 
    a :HypothesisAssociation ;
    :hasSubject :Allele_rs7412 ;
    :hasObject :AlzheimersDisease ;
    :p_value "2e-145"^^xsd:double ;
    :odds_ratio "11.8"^^xsd:decimal ;
    # NEW: Ancestry Tagging
    :relevantPopulation [
        a :PopulationContext ;
        rdfs:label "European Ancestry" ;
        owl:sameAs ncit:C43851 
    ] ;
    :evidenceTier "Tier_2_Strong_Assoc" .
```

#### **B. The "Resilience" Genotype Logic**
*Incorporating Feedback: Scientific Critic (Protective e2), Ontologist (Disjointness)*

We treat APOE e2 and e4 as logically disjoint mechanisms.

```python
# ETL Logic: Genotype Classification
def classify_genotype_effect(allele_pair):
    """
    Maps allele combinations to Semantic Clinical Effects.
    """
    if 'e2' in allele_pair and 'e4' not in allele_pair:
        # e2/e2, e2/e3
        return "alzkb:ResilienceFactor" 
    elif 'e4' in allele_pair and 'e2' not in allele_pair:
        # e3/e4, e4/e4
        return "alzkb:RiskIncrease"
    elif 'e2' in allele_pair and 'e4' in allele_pair:
        # e2/e4 - The Confounded/Neutral Case
        return "alzkb:ComplexInteraction" 
    else:
        # e3/e3
        return "alzkb:Neutral"
```

#### **C. Biomarkers & Equivocal Logic**
*Incorporating Feedback: Validation Scientist (Trinary State), KG Engineer (Master Files)*

We reject the binary (Pos/Neg) forced classification.

*   **Logic:**
    *   **Positive:** Value > Upper Limit of Detection (ULOD) or Cutoff.
    *   **Negative:** Value < Cutoff.
    *   **Equivocal:** Value within ±5% of Cutoff OR explicitly labeled "Equivocal" in ADNI Master.
*   **Impact:** If `BiomarkerStatus == Equivocal`, the patient is excluded from the Training Set for Resilience prediction but remains in the Graph for retrieval.

---

### 3. VALIDATION GATES (IMMEDIATE ACTION)

The **Validation Scientist** is authorized to run the following Quality Assurance (QA) tests immediately post-ingestion (T+24 hours). Failure of any test triggers a **Rollback**.

1.  **The "Resilience" Stress Test (Revised):**
    *   Query: `MATCH (p:Patient) WHERE p.biomarker_profile = 'A+T+N+' AND p.cdr_score = 0 RETURN count(p)`
    *   **Pass Condition:** The result must be **>0** (typically 10-20% of the cohort). If this count is zero, the data is biased, and ingestion fails.

2.  **The Ancestry Check:**
    *   Query: `MATCH (h:HypothesisAssociation) WHERE h.relevantPopulation IS NULL RETURN count(h)`
    *   **Pass Condition:** Result must be **0**. Every GWAS edge must have a population context (even if "Unknown").

3.  **The "Human Only" Check:**
    *   Query: `MATCH (n) WHERE n.organism = 'Mus musculus' RETURN count(n)`
    *   **Pass Condition:** Result must be **0**.

---

**Next Steps:**
*   **KG Engineer:** Deploy `etl_adni_harmonized.py` immediately.
*   **Ontologist:** Commit `alzkb-ontology-v2.1.ttl` to the repo.
*   **Validation Scientist:** Prepare the Gold Standard "Jack 2018" query suite.

We are GO for Phase 2. Make it happen.

## Key Decisions
1. Prioritize ADNI 'Master' files (ADNIMERGE, UPENNBIOMK_MASTER) over raw assays to guarantee biomarker harmonization.
2. Enforce mandatory Ancestry Tagging (mapped to NCIT) on all GWAS associations to prevent Euro-centric RAG bias.
3. Define APOE e2 alleles as explicit 'ResilienceFactor' nodes, logically disjoint from e4 'RiskIncrease' nodes.
4. Implement strict quality gates: GWAS (p < 5e-8, N > 10k), DisGeNET (Human only, Score > 0.5), Reactome (Human only).
5. Adopt a 'Trinary' Biomarker logic (Positive/Negative/Equivocal) to prevent forced classification of indeterminate clinical data.

## Action Items
- Deploy 'etl_adni_harmonized.py' using the approved Master files and fallback logic (KG Engineer)
- Commit 'alzkb-ontology-v2.1.ttl' incorporating PopulationContext and Resilience schema updates (Ontologist)
- Implement NLP parser for GWAS 'Initial Sample Description' to generate ancestry tags (KG Engineer)
- Add textual description properties to Reactome and DisGeNET nodes for vector embedding (KG Engineer)
- Execute the 'Resilience Stress Test' (verifying presence of A+T+N+/CDR 0 cohort) post-ingestion (Validation Scientist)

## Status: COMPLETE

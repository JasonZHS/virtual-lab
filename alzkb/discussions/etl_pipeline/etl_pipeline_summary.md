# Meeting Summary: ETL Pipeline Development
**Phase:** etl_pipeline
**Timestamp:** 2025-12-24T19:52:51.129771

## Summary
**Principal Investigator (PI)**

"Team, this session has been exemplary. We have successfully transformed a generic data aggregation plan into a rigorous scientific instrument. By addressing the 'Risk Allele Trap,' enforcing 'Curated-Only' filters, and designing for 'RAG-Readiness,' we have ensured that AlzKB will be a source of truth, not noise.

Here is the **Official ETL Design Specification (v1.0)** based on our consensus. This document now governs the engineering phase.

---

### **FINAL REVISED ETL SPECIFICATION**

#### **1. Priority & Execution Order**
1.  **Ensembl (The Backbone):** Establish the `Master_Gene_Index` to resolve Symbols/Entrez/UniProt to ENSG IDs.
2.  **GWAS Catalog (Genetic Foundation):** Establish the risk variant landscape with strict directionality.
3.  **DisGeNET & ChEMBL (Context):** Add curated phenotypes and high-affinity drug targets.
4.  **Reactome (Mechanism):** Ingest full human hierarchy for pathway traversal.

#### **2. Source-to-Ontology Mapping & Filters**
*All ingestions utilize the 'Medallion' architecture (Bronze Raw $\to$ Silver Norm $\to$ Gold Graph).*

| Source | Raw Fields (Critical) | Target Class & Property | Canonical ID Strategy | **CRITICAL ETL LOGIC / FILTERS** |
| :--- | :--- | :--- | :--- | :--- |
| **Ensembl** | `Gene Stable ID`, `Synonyms` | `:Gene` | `ENSG_ID` | Create `Master_Gene_Index`. Map all synonyms. |
| **GWAS Catalog** | `SNPS`, `STRONGEST SNP-RISK ALLELE`, `P-VALUE`, `MAPPED_GENE` | `:Allele`, `:GwasAssociation` | `rsID` | **1.** `p < 5e-8`. <br>**2.** Parse `Risk Allele` (e.g., 'rs123-A') $\to$ `alzkb:effect_allele`. <br>**3.** Split `MAPPED_GENE` on comma $\to$ `alzkb:associated_gene_context`. |
| **DisGeNET** | `geneId`, `score`, `source` | `:HypothesisAssociation` | `ENSG_ID` (via map) | **1.** Filter: **Curated Sources Only** (UniProt, CTD, PsyGeNET). Exclude BeFree/Text-mining. <br>**2.** `score > 0.5`. |
| **ChEMBL** | `molecule_chembl_id`, `pchembl_value` | `:Drug`, `:Interaction` | `CHEMBL_ID` | **1.** Filter: `pChEMBL_value > 6` (High affinity only). <br>**2.** Drop records with missing pChEMBL (do not convert units manually). |
| **Reactome** | `PhysicalEntity`, `Pathway`, `comment` | `:Protein`, `:Pathway` | `UniProt`, `ReactomeID` | **1.** Ingest full hierarchy. <br>**2.** Extract text descriptions $\to$ `dcterms:description` for RAG. |

#### **3. Entity Resolution Strategy**
*   **The "Splitter" Rule:** Comma-separated genes in GWAS (intergenic variants) are split into multiple `:associated_gene_context` edges.
*   **The "One-Strike" Policy:**
    *   Any entity (Gene/Drug) that cannot be resolved to a canonical ID (ENSG or CHEMBL) using the Master Index is sent to the **Dead Letter Queue (DLQ)**.
    *   Ambiguous synonyms (mapping to >1 ENSG) are blacklisted.
*   **RAG Enrichment:**
    *   Every `:HypothesisAssociation` gets a computed `alzkb:citation_string`: `"{Source}: {StudyID} (n={N}, p={P}, OR={OR}, Allele={RiskAllele})"` for hallucination-free citation.

#### **4. Validation & Quality Gates**
*   **Gate 1 (Ingest):** Schema validation (Pandera).
*   **Gate 2 (Logic):** Row-level filters (p-value, pChEMBL, Curated-Source).
*   **Gate 3 (Graph):** **SHACL Validation** running on the Gold Layer.
    *   *Constraint:* `:GwasAssociation` must have `alzkb:effect_allele` matching regex `^[ACGT]+$`.
*   **Gate 4 (Scientific Benchmark):**
    *   **The ATN Test:** Pipeline fails if `APOE e4` (rs429358-C) is not present as a **RISK** factor (OR > 1.0) with High Confidence.

---

**Next Steps:**
*   **KG Engineer:** Initialize the Airflow DAGs for Phase 1 (Ensembl).
*   **Ontologist:** Commit the `alzkb-ontology-v2.ttl` with the new properties (`effect_allele`, `associated_gene_context`).
*   **Validation Scientist:** Write the ATN Cypher test suite.

Meeting adjourned. Let's build the graph."

## Key Decisions
1. Adopted Medallion Architecture (Bronze/Silver/Gold) for the ETL pipeline.
2. Mandated parsing of 'STRONGEST SNP-RISK ALLELE' in GWAS data to strictly define risk vs. protective directionality.
3. Downgraded GWAS intergenic mappings to use 'alzkb:associated_gene_context' rather than direct causal links.
4. Restricted DisGeNET ingestion to Curated sources only (excluding BeFree/text-mining) with Score > 0.5.
5. Restricted ChEMBL ingestion to high-affinity interactions with pChEMBL > 6.
6. Approved ingestion of the full human Reactome hierarchy with mandatory text description extraction for RAG.
7. Required injection of pre-formatted 'alzkb:citation_string' into all HypothesisAssociation nodes.
8. Established the 'ATN Benchmark' (specifically APOE e4 risk confirmation) as the fatal-error integration test.

## Action Items
- Initialize Airflow DAGs starting with Ensembl Master Index (KG Engineer)
- Implement Splitter Function and Risk Allele Parser for GWAS pipelines (KG Engineer)
- Update ontology schema to include 'alzkb:effect_allele' and 'alzkb:associated_gene_context' (Ontologist)
- Develop Cypher test suite for ATN Benchmark validation (Validation Scientist)

## Status: COMPLETE

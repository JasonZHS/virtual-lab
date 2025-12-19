## User

This is the beginning of an individual meeting with Principal Investigator (Alzheimer's KG) to discuss your research project.

Here is the agenda for the meeting:

Task: Build a scalable, retrieval-optimized Knowledge Graph for Alzheimer's Disease research.
TASK: Define 3 distinct Agents to form the AlzKB Implementation Team.

OUTPUT FORMAT: Python `Agent()` objects ONLY. No conversational filler.
Do not include yourself.
TEMPLATE:
Agent(
    title="Principal Investigator (Alzheimer's KG)",
    expertise=(
        "Lead scientist specializing in Alzheimer's Disease (AD) data integration. "
        "Expert in constructing heterogeneous Knowledge Graphs connecting clinical phenotypes, "
        "neuroimaging features, genetic biomarkers (e.g., APOE), and tau/amyloid pathology."
    ),
    role=(
        "1. Define rigorous schemas aligning with standard ontologies (e.g., SNOMED CT, Gene Ontology). "
        "2. Direct the Tech Lead to prioritize high-confidence data sources (e.g., ADNI, AMP-AD). "
        "3. Review extraction pipelines for precision over recall to prevent hallucinated associations. "
        "4. Enforce strict validation protocols for entity resolution across multi-modal datasets."
    ),
)


Principal Investigator (Alzheimer's KG), please provide your response to the agenda.

## Principal Investigator (Alzheimer's KG)

Agent(
    title="Knowledge Graph Architect",
    expertise=(
        "Expert in graph data modeling, ontology alignment, and scalable KG infrastructure. "
        "Skilled in mapping biomedical data to standard ontologies (e.g., SNOMED CT, UMLS, Gene Ontology). "
        "Experienced in designing retrieval-optimized, query-efficient graph schemas."
    ),
    role=(
        "1. Design the KG schema and entity-relationship models using standard biomedical ontologies. "
        "2. Oversee integration layer for cross-modal data (clinical, imaging, genomic, pathology). "
        "3. Implement indexing and partitioning strategies for scalable, fast retrieval."
    ),
)

Agent(
    title="Data Integration & Curation Lead",
    expertise=(
        "Specialist in biomedical data harmonization, ETL pipelines, and multi-source quality control. "
        "Deep knowledge of ADNI, AMP-AD, ROSMAP, and other high-confidence Alzheimer's datasets. "
        "Experience in phenotype, biomarker, and imaging feature harmonization."
    ),
    role=(
        "1. Curate and harmonize raw data streams from prioritized sources (ADNI, AMP-AD, etc.). "
        "2. Implement ETL pipelines emphasizing high-precision entity and relation extraction. "
        "3. Manage data quality assessments and ensure rigorous provenance tracking."
    ),
)

Agent(
    title="Validation & Entity Resolution Scientist",
    expertise=(
        "Expert in cross-modal entity resolution, ground truth benchmarking, and KG validation. "
        "Specializes in probabilistic matching of clinical, imaging, and genomic entities across datasets. "
        "Proficient in designing validation protocols to minimize false positives."
    ),
    role=(
        "1. Develop and enforce entity resolution guidelines for multi-modal integration. "
        "2. Design gold-standard validation sets and conduct systematic error analysis. "
        "3. Monitor and report entity/relation confidence scores to drive precision over recall in KG construction."
    ),
)


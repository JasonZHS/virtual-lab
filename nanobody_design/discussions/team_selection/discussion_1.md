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
    title="Tech Lead (AlzKB Engineering)",
    expertise=(
        "Senior engineer with deep experience in biomedical data pipelines, large-scale graph databases "
        "(e.g., Neo4j, Blazegraph), and distributed architectures for knowledge retrieval. "
        "Proficient in integrating heterogeneous multi-modal sources and optimizing KG performance."
    ),
    role=(
        "1. Architect scalable KG infrastructure for high-volume, multi-modal Alzheimer's data. "
        "2. Implement robust ETL pipelines ensuring reproducibility and data lineage. "
        "3. Prioritize onboarding of validated, high-quality datasets (e.g., ADNI, AMP-AD). "
        "4. Collaborate with Data Curator to enforce schema alignment and entity integrity."
    ),
)

Agent(
    title="Data Curator (AlzKB Ontologies)",
    expertise=(
        "Expert in biomedical ontology mapping, normalization, and curation. "
        "Experienced in aligning disparate datasets with standard vocabularies "
        "(e.g., SNOMED CT, Gene Ontology, UMLS) and resolving cross-modal entity ambiguities."
    ),
    role=(
        "1. Map incoming data to controlled vocabularies and ontological standards. "
        "2. Develop schema constraints for consistent phenotype/genotype mapping. "
        "3. Oversee entity resolution across clinical, imaging, and biomarker datasets. "
        "4. Validate extraction outputs to minimize semantic drift and false associations."
    ),
)

Agent(
    title="Retrieval & Evaluation Scientist (AlzKB Search)",
    expertise=(
        "Specialist in biomedical information retrieval, KG query design, and evaluation metrics. "
        "Adept at optimizing query performance, graph embeddings, and benchmarking retrieval accuracy "
        "against gold-standard AD datasets and clinical queries."
    ),
    role=(
        "1. Design and optimize retrieval workflows for clinical, imaging, and genetic queries. "
        "2. Develop evaluation protocols to assess precision, recall, and utility of KG outputs. "
        "3. Implement user feedback loops for iterative improvement of KG retrieval. "
        "4. Collaborate with Data Curator to refine schema for retrieval relevance."
    ),
)


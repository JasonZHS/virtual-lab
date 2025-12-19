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
    title="Tech Lead (AlzKB Infrastructure)",
    expertise=(
        "Engineering specialist in scalable graph database architectures and distributed data processing. "
        "Expert in integrating multi-modal biomedical data (clinical, imaging, omics) using modern data pipelines (e.g., Apache Spark, Neo4j)."
    ),
    role=(
        "1. Design and implement robust ETL pipelines for ingesting prioritized high-confidence data sources (e.g., ADNI, AMP-AD). "
        "2. Optimize data storage and retrieval strategies for heterogeneous KG queries. "
        "3. Ensure system scalability, maintainability, and compliance with data privacy regulations."
    ),
)

Agent(
    title="Biomedical Ontologist (Alzheimer's Semantics)",
    expertise=(
        "Domain expert in biomedical ontologies and semantic harmonization. "
        "Experienced in mapping clinical, genetic, and imaging concepts to standard vocabularies (e.g., SNOMED CT, UMLS, Gene Ontology, RadLex)."
    ),
    role=(
        "1. Develop and maintain rigorous, ontology-driven data schemas for the KG. "
        "2. Curate and align entities and relations across data modalities using standard terminologies. "
        "3. Validate semantic interoperability and resolve cross-dataset entity ambiguities."
    ),
)

Agent(
    title="Data Scientist (Knowledge Extraction & QA)",
    expertise=(
        "Specialist in biomedical information extraction, entity resolution, and relation mining from structured and unstructured data. "
        "Proficient in NLP, automated curation, and quality assurance for large-scale knowledge graphs."
    ),
    role=(
        "1. Lead extraction of entities and relationships from primary data sources with emphasis on high precision. "
        "2. Develop annotation and QA protocols to minimize false positives and hallucinated associations. "
        "3. Benchmark and validate extraction outputs against gold-standard datasets."
    ),
)


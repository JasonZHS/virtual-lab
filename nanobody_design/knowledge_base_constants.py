"""Constants for the knowledge base design project."""

from pathlib import Path

from virtual_lab.agent import Agent
from virtual_lab.prompts import (
    SCIENTIFIC_CRITIC,
    PRINCIPAL_INVESTIGATOR
)

# Meetings constants
num_iterations = 5
num_rounds = 3

# Models
model = "gpt-4.1"
model_mini = "gpt-4.1-mini"

# Discussion paths
discussions_dir = Path("discussions")
workflow_phases = [
    "team_selection",
    "project_specification",
    "tools_selection",
    "implementation_agent_selection",
    "esm",
    "alphafold",
    "rosetta",
    "workflow_design",
]
ablations_phases = ["ablations"]
human_eval_phases = ["human_eval"]
finetuning_phases = ["finetuning"]
review_phases = ["unpaired_cysteine"]
phases = workflow_phases + ablations_phases + human_eval_phases + finetuning_phases + review_phases
discussions_phase_to_dir = {phase: discussions_dir / phase for phase in phases}

# Prompts
background_prompt = "You are working on a research project to design a knowledge base that organizes and retrieves accurate information about ongoing research activities, enabling efficient reuse of prior work and supporting scalable knowledge updates across projects."

nanobody_prompt = "Your team previous decided to modify existing nanobodies to improve their binding to the newest variant of the SARS-CoV-2 spike protein."

experimental_results_prompt = """Your team has designed 92 mutated nanobodies (23 each for the wild-type nanobodies H11-D4, Nb21, Ty1, and VHH-72) to improve their binding to the KP.3 variant of the SARS-CoV-2 spike protein receptor binding domain (RBD). Each nanobody has 1-4 mutations relative to the wild-type nanobody. Your team used ESM log-likelihood ratios (ESM LLR) to score the nanobody mutations independent of the antigen, AlphaFold-Multimer to predict the structure of the mutated nanobody in complex with the KP.3 RBD and compute the interface pLDDT (AF ipLDDT) as a metric of binding confidence, and Rosetta to calculate the binding energy of the mutated nanobody in complex with the KP.3 RBD (RS dG) based on the AlphaFold-Multimer predicted structure followed by a Rosetta relaxation. You have ranked the mutant nanobodies and selected the top ones using a weighted score of WS = 0.2 * (ESM LLR) + 0.5 * (AF ipLDDT) - 0. 3 * (RS dG). The 92 selected nanobodies were tested along with the four wild-type nanobodies using an ELISA assay to measure binding to the Wuhan, JN.1, KP.3, KP2.3, and BA.2 strains of the SARS-CoV-2 spike RBD. Note that the JN.1 strain is closely related to KP.3 and KP2.3. BSA was used as a negative control. Most of the mutated nanobodies showed at least moderate expression levels. The ELISA results are as follows:

H11-D4: The wild-type only binds to the Wuhan RBD. Most mutants show binding to the Wuhan RBD as well, including one with a higher binding level than the wild-type. However, that mutant and two others bind non-specifically to the negative control BSA along with other strains of the SARS-CoV-2 RBD. No mutant nanobody shows specific binding to any strain other than the Wuhan RBD.

Nb21: The wild-type only binds to the Wuhan RBD. All mutant nanobodies also bind to the Wuhan RBD. There are no non-specific binders. One mutant nanobody with mutations I77V, L59E, Q87A, and R37Q binds to the Wuhan RBD (strong binding), the JN.1 RBD (moderate binding), and the KP.3 RBD (weak binding). Thus, this mutant introduces specific binding to JN.1 and KP.3 that the wild-type does not possess, and it increases binding to the Wuhan RBD.

Ty1: The wild-type only binds to the Wuhan RBD. Many mutant nanobodies do not show binding, but several show moderate binding to the Wuhan RBD. One mutant nanobody with mutations V32F, G59D, N45S, and F32S binds to the Wuhan RBD (strong binding) and the JN.1 RBD (moderate binding). This mutant introduces specific binding to JN.1 that the wild-type does not possess, and it increases binding to the Wuhan RBD. Additionally, there are is one mutant with weak, non-specific binding to BSA and other RBD strains.

VHH-72: The wild-type only binds to the Wuhan RBD. Most mutants show binding to the Wuhan RBD as well, including several with a higher binding level than the wild-type. Two mutant nanobodies bind non-specifically to BSA and several RBD strains. No mutant nanobody shows specific binding to any strain other than the Wuhan RBD."""

# Set up agents

# Generic agent
generic_agent = Agent(
    title="Assistant",
    expertise="helping people with their problems",
    goal="help people with their problems",
    role="help people with their problems",
    model=model,
)

# Generic team lead
generic_team_lead = Agent(
    title=f"{generic_agent.title} Lead",
    expertise=generic_agent.expertise,
    goal=generic_agent.goal,
    role=generic_agent.role,
    model=model,
)

# Generic team
generic_team = [
    Agent(
        title=f"{generic_agent.title} {i}",
        expertise=generic_agent.expertise,
        goal=generic_agent.goal,
        role=generic_agent.role,
        model=model,
    )
    for i in range(1, 5)
]

# Team lead
"""
principal_investigator = Agent(
    title="Principal Investigator",
    expertise="applying artificial intelligence to biomedical research",
    goal="perform research in your area of expertise that maximizes the scientific impact of the work",
    role="lead a team of experts to solve an important problem in artificial intelligence for biomedicine, make key decisions about the project direction based on team member input, and manage the project timeline and resources",
    model=model,
)
"""
principal_investigator = Agent(
    title="Principal Investigator",
    expertise=(
        "designing and leading knowledge graph projects, including ontology/schema design, "
        "data integration, and graph representation learning"
    ),
    goal=(
        "design and execute a research program that builds a high-quality, scalable knowledge graph "
        "for a specific target domain and uses it to support downstream tasks such as question answering, "
        "recommendation, and reasoning"
    ),
    role=(
        "lead a team of experts to define the knowledge graph schema and ontology, select and integrate "
        "data sources, design extraction and cleaning pipelines, and specify how the graph will be "
        "evaluated using both intrinsic and task-based metrics. Make key decisions about trade-offs between "
        "coverage, precision, scalability, and maintainability, and keep the project on a realistic timeline."
    ),
    model=model,
)

# Scientific critic
scientific_critic = SCIENTIFIC_CRITIC

# Specialized science agents
chief_knowledge_architect = Agent(
    title="Chief Knowledge Architect",
    expertise=(
    "knowledge graph construction, ontology development, information extraction, and schema governance"
    ),
    goal=(
    "design a structure that enables scalable knowledge updates and supports retrieval-based reasoning"
    ),
    role=(
    "propose schemas, specify entity/relationship definitions, design attribute-level constraints, and map knowledge sources to the schema"
    ),
    model=model,
)

data_integration_scientist = Agent(
    title="Data Integration Scientist",
    expertise=(
    "data integration, ETL pipeline design, data cleaning, entity resolution, metadata standardization, and provenance tracking"
    ),
    goal=(
    "identify, extract, and harmonize heterogeneous data sources about ongoing research activities into the knowledge base"
    ),
    role=(
    "evaluate and select data sources, design extraction and cleaning pipelines, resolve duplicate or conflicting entities, ensure metadata consistency, and establish data provenance tracking"
    ),
    model=model
)

knowledge_validation_specialist = Agent(
    title="Knowledge Validation Specialist",
    expertise=(
    "knowledge base quality assurance, validation frameworks, automated and manual validation, consistency checking, and benchmarking for knowledge-driven tasks"
    ),
    goal=(
    "ensure the correctness, consistency, and up-to-dateness of the knowledge base through robust validation and continual updates"
    ),
    role=(
    "define validation protocols, implement consistency and correctness checks, coordinate expert-in-the-loop review, set up automated/manual review pipelines, and design benchmarks for retrieval, reuse, and reasoning tasks"
    ),
    model=model
)

# Team members
team_members = (
    chief_knowledge_architect,
    data_integration_scientist,
    knowledge_validation_specialist,
    scientific_critic,
)

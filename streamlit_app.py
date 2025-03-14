__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from crewai import Agent
# from tools import yt_tool
# from dotenv import load_dotenv
from crewai import LLM
import litellm
import openai
import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv
from crewai_tools import FileReadTool, FileWriterTool
import streamlit as st

__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

load_dotenv()

# Title
st.set_page_config(page_title="BusinessConsultantAI", layout="wide")

# Title and description
st.title("BusinessConsultantAI")
st.markdown("Generate SRS Or SDD")
st.markdown("Please provide a text file only")

# Sidebar
with st.sidebar:
    st.header("Content Settings")

    topic = st.text_area(
        "Enter the topic",
        height=68,
        placeholder="Enter the topic",
        key="text_area_1"
    )

    uploaded_file = st.file_uploader("Choose a file", type=["txt", "pdf"])

    st.markdown("-----")

    generate_button_srs = st.button("Generate SRS", type="primary", use_container_width=True)
    generate_button_sdd = st.button("Generate SDD", type="primary", use_container_width=True)

def generate_srs(topic, uploaded_file, blog="default"):
    if uploaded_file is not None:
        # Create the temp directory if it does not exist
        if not os.path.exists("temp"):
            os.makedirs("temp")

        # Save the uploaded file to a temporary location
        temp_file_path = os.path.join("temp", uploaded_file.name)
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Create a FileReadTool with the path to the uploaded file
        file_read_tool = FileReadTool(file_path=temp_file_path)

        business_analyst = Agent(
            role='Business Analyst',
            goal=(
            "Extracts relevant content from the given business requirements document, including "
            "Introduction, Purpose, In Scope, Out of Scope, Assumptions, References and Overview. "
            "Enhances unclear sections using the LLM and internet sources to ensure completeness "
            "before passing refined content for documentation."
            ),
            backstory=(
            "A senior business analyst with expertise in understanding business requirements and "
            "ensuring clarity in documentation."
            ),
            tools=[file_read_tool]
        )

        technical_analyst = Agent(
            role='Technical Analyst',
            goal=(
            "Analyzes the business requirements document to identify technical aspects, including "
            "Data Model, User Characteristics, Codification Schemes and Dependencies. Uses the LLM "
            "and internet to enhance unclear details before passing structured insights for documentation."
            ),
            backstory=(
            "A senior technical analyst with expertise in translating business needs into clear technical "
            "specifications."
            ),
            tools=[file_read_tool]
        )

        requirement_categorizer = Agent(
            role='Requirement Categorizer',
            goal=(
            "Classifies extracted requirements into Functional, Non-Functional, and Technical categories. "
            "Ensures clarity by refining vague or incomplete sections using the LLM and internet sources "
            "before passing structured requirements for SRS documentation."
            ),
            backstory=(
            "A senior analyst specializing in categorizing and refining requirements to ensure clarity and completeness."
            ),
            tools=[file_read_tool]
        )

        srs_writer = Agent(
            role='System Requirements Specifications Writer',
            goal=(
            "Writes a structured SRS document by incorporating the extracted and categorized requirements. "
            "Enhances the content for grammatical accuracy, professionalism, and clarity."
            ),
            backstory=(
            "A professional writer specializing in crafting well-structured and polished SRS documents."
            ),
            tools=[file_read_tool, FileWriterTool()]
        )

        srs_formatter = Agent(
            role='System Requirements Specifications Formatter',
            goal=(
            "Organizes the document with appropriate formatting, headings, and structure. Ensures that the final "
            "document is readable, structured, and includes a 'Dependencies' section which points out the dependencies "
            "on third-party APIs, database requirements, hardware constraints or system integrations and a 'Conclusion' "
            "section summarizing key insights."
            ),
            backstory=(
            "A document specialist with expertise in structuring and formatting professional reports."
            ),
            tools=[file_read_tool, FileWriterTool()]
        )

        business_analysis_task = Task(
            description=(
            "Objective:\n"
            "Extract and enhance sections from the Business Requirements Document (BRD):\n"
            "- Introduction\n"
            "- Purpose\n"
            "- Scope\n"
            "- In Scope\n"
            "- Out of Scope\n"
            "- Assumptions\n"
            "- References\n"
            "- Overview\n"
            "Enhance extracted sections with:\n"
            "- In-depth explanations\n"
            "- Real-world examples\n"
            "- Industry best practices\n"
            "- Structured details for client clarity\n"
            "- Please elaborate the points properly where each point should be at least two paragraphs\n\n"
            "Guidelines:\n"
            "Introduction:\n"
            "- Provide project background, business context, and purpose.\n"
            "- Explain the need for the initiative and expected impact.\n"
            "- Please elaborate the points properly where each point should be at least two paragraphs\n"
            "Purpose:\n"
            "- Define document objectives and stakeholder guidance.\n"
            "- Distinguish between business and technical goals.\n"
            "- Please elaborate the points properly where each point should be at least two paragraphs\n"
            "Scope:\n"
            "- Explicitly outline project boundaries.\n"
            "- Include functional, non-functional, regulatory, and operational constraints.\n"
            "- Please elaborate the points properly where each point should be at least two paragraphs\n"
            "In Scope:\n"
            "- Detail included features, functionalities, and deliverables.\n"
            "- Provide examples and real-world implications.\n"
            "- Please elaborate the points properly where each point should be at least two paragraphs\n"
            "Out of Scope:\n"
            "- Extract as-is without modifications.\n"
            "- Provide context on exclusions and associated risks.\n"
            "Assumptions:\n"
            "- Extract as-is without modifications.\n"
            "- Expand on implications and potential risks if assumptions change.\n"
            "- Please elaborate the points properly where each point should be at least two paragraphs\n"
            "References:\n"
            "- List cited materials, frameworks, and standards.\n"
            "- Enhance with best practices and industry standards.\n"
            "- Please elaborate the points properly where each point should be at least two paragraphs\n"
            "Overview:\n"
            "- Summarize key takeaways in a structured format.\n"
            "- Please elaborate the points properly where each point should be at least two paragraphs\n\n"
            "Enhancements:\n"
            "- Ensure structured, professional, and detailed writing.\n"
            "- Use tables, bullet points, and subheadings for clarity.\n"
            "- Include industry-specific examples and real-world cases.\n"
            "- Validate and enrich sections using external sources.\n"
            "- Please elaborate the points properly where each point should be at least two paragraphs\n\n"
            "Output:\n"
            "- Formal, structured, and client-ready document.\n"
            "- Include tables, and figures where necessary.\n"
            "- Maintain clarity, completeness, and professionalism.\n"
            "- Please elaborate the points properly where each point should be at least two paragraphs\n\n"
            "Every subpoint should be explained in an elaborated manner."
            ),
            expected_output=(
            "Clear and detailed sections for Introduction, Purpose, Scope, In Scope, Out of Scope, Assumptions, "
            "References, and Overview with enhanced explanations where needed. Every subpoint should be explained "
            "in an elaborated manner."
            ),
            agent=business_analyst
        )

        technical_analysis_task = Task(
            description=(
            "Objective:\n"
            "Extract and enhance sections from the Business Requirements Document (BRD):\n"
            "- Data Model\n"
            "- User Characteristics\n"
            "- Codification Schemes\n"
            "- Dependencies\n"
            "Enhance extracted sections with:\n"
            "- In-depth explanations\n"
            "- Real-world examples\n"
            "- Industry best practices\n"
            "- Structured details for client clarity\n"
            "- Please elaborate the points properly where each point should be at least two paragraphs\n\n"
            "Guidelines:\n"
            "Data Model:\n"
            "- Extract existing model details and expand into a structured ER model.\n"
            "- Include entities, attributes, primary keys, foreign keys, and relationships.\n"
            "- Provide example schemas, sample data representations, and normalization best practices.\n"
            "- Use industry standards and tables where necessary.\n"
            "- No images or tables required\n"
            "- Please elaborate the points properly where each point should be at least two paragraphs\n"
            "User Characteristics:\n"
            "- Identify and categorize user roles, personas, and access levels.\n"
            "- Include demographics, skill levels, and behavioral patterns.\n"
            "- Provide user journeys, workflows, and interaction models.\n"
            "- Incorporate UX/UI principles and accessibility considerations.\n"
            "- No images or tables required\n"
            "- Please elaborate the points properly where each point should be at least two paragraphs\n"
            "Codification Schemes:\n"
            "- Extract existing schemes and document naming conventions.\n"
            "- Detail numbering systems, data classification rules, and coding structures.\n"
            "- Include examples of versioning strategies and hierarchical naming methods.\n"
            "- Align with industry standards (ISO, IEEE, enterprise policies).\n"
            "- Please elaborate the points properly where each point should be at least two paragraphs\n"
            "Dependencies:\n"
            "- Identify internal and external dependencies affecting the system.\n"
            "- List third-party services, APIs, databases, regulatory constraints, and interdependencies.\n"
            "- Expand on bottlenecks, failure points, and contingency planning.\n"
            "- Provide risk assessments, mitigation strategies, and alternate solutions.\n"
            "- Please elaborate the points properly where each point should be at least two paragraphs\n\n"
            "Enhancements:\n"
            "- Validate vague sections using LLM and external industry sources.\n"
            "- Provide case studies, benchmarks, and best practices for enrichment.\n"
            "- Use tables, structured lists, flowcharts, and for clarity.\n"
            "- Maintain a structured, professional, and client-ready format.\n"
            "- Please elaborate the points properly where each point should be at least two paragraphs\n\n"
            "Output:\n"
            "- Highly detailed, structured, and professional document.\n"
            "- Include technical explanations, tables elements, and best practices.\n"
            "- Ensure exhaustive details for clarity and completeness.\n"
            "- Please elaborate the points properly where each point should be at least two paragraphs\n"
            "Every subpoint should be explained in an elaborated manner."
            ),
            expected_output=(
            "Clear and detailed technical sections for Data Model, User Characteristics, Codification Schemes, "
            "Assumptions, Dependencies, and Out of Scope. Every subpoint should be explained in an elaborated manner."
            ),
            agent=technical_analyst
        )

        requirement_categorize_task = Task(
            description=(
            "Objective:\n"
            "Extract and categorize business requirements from the Business Requirements Document (BRD) into:\n"
            "- Functional Requirements (FR)\n"
            "- Non-Functional Requirements (NFR)\n"
            "- Technical Requirements (TR)\n"
            "Enhance extracted requirements by:\n"
            "- Refining vague or unclear sections using LLM and external knowledge sources.\n"
            "- Providing detailed, structured, and client-ready documentation.\n\n"
            "Categorization Guidelines:\n"
            "Functional Requirements (FR):\n"
            "- Define core system features, operations, and expected behaviors.\n"
            "- Outline system responses to user actions.\n"
            "- Provide detailed use cases, workflows, and real-world examples.\n"
            "- Ensure all functionalities are measurable and verifiable.\n"
            "Non-Functional Requirements (NFR):\n"
            "- Define quality attributes, performance, security, scalability, and compliance needs.\n"
            "- Ensure all NFRs are quantifiable and testable (e.g., 'system must handle 1,000 transactions per second with 99.99% uptime').\n"
            "- Align with industry benchmarks and best practices.\n"
            "Technical Requirements (TR):\n"
            "- Extract infrastructure, technology stack, APIs, frameworks, and database structures.\n"
            "- Detail hardware/software constraints, networking requirements, and security protocols.\n"
            "- List third-party dependencies and integration requirements.\n"
            "- Enhance with best practices and current industry standards.\n\n"
            "Enhancements:\n"
            "- Identify and refine vague or ambiguous requirements.\n"
            "- Align with industry compliance and security standards.\n"
            "- Use tables, and structured lists for better clarity.\n"
            "- Ensure a structured, professional, and client-focused format.\n\n"
            "Output:\n"
            "- Well-structured, detailed, and categorized document.\n"
            "- Clear separation of Functional, Non-Functional, and Technical requirements.\n"
            "- Use of tables, bullet points, and tables elements for improved comprehension.\n"
            "- Comprehensive details ensuring no ambiguity in requirements."
            ),
            expected_output=(
            "A structured list of Functional, Non-Functional, and Technical requirements with well-explained descriptions."
            ),
            agent=requirement_categorizer
        )

        srs_write_task = Task(
            description=(
            "Objective:\n"
            "Generate a highly detailed, structured, and professional Software Requirements Specification (SRS) document by consolidating and expanding researched content.\n"
            "Ensure clarity, completeness, and technical accuracy while preserving extracted content where required.\n\n"
            "Guidelines:\n"
            "Preserve Extracted Content:\n"
            "- 'Out of Scope' and 'Assumptions' sections must be included exactly as extracted from the BRD without modification.\n"
            "- Expand all other sections with additional details but without altering the original intent.\n"
            "Sections to Include:\n"
            "- Introduction:\n"
            "  - Provide a project background, business context, and overall purpose.\n"
            "  - Include industry-specific context and real-world significance.\n"
            "- Purpose:\n"
            "  - Define the role of this document in guiding stakeholders.\n"
            "  - Clearly differentiate between business and technical objectives.\n"
            "- Scope:\n"
            "  - Outline explicit project boundaries, covering functional, non-functional, regulatory, and operational aspects.\n"
            "- In Scope:\n"
            "  - Break down included functionalities, features, and deliverables.\n"
            "  - Provide detailed descriptions, examples, and their business impact.\n"
            "- Out of Scope:\n"
            "  - Insert as-is from the BRD without modification.\n"
            "  - Provide additional context on exclusions and associated risks.\n"
            "- Assumptions:\n"
            "  - Insert as-is from the BRD without modification.\n"
            "  - Elaborate on implications and possible risks if assumptions change.\n"
            "- References:\n"
            "  - List cited materials, standards, frameworks, and relevant documentation.\n"
            "  - Add supporting industry best practices where applicable.\n"
            "- Overview:\n"
            "  - Summarize key takeaways in a structured, digestible format.\n"
            "Requirement Categorization:\n"
            "- Functional Requirements (FR):\n"
            "  - Define core system features, workflows, and expected behaviors.\n"
            "  - Provide detailed use cases, user interactions, and real-world applications.\n"
            "- Non-Functional Requirements (NFR):\n"
            "  - Outline performance expectations, security requirements, compliance standards, scalability, and operational constraints.\n"
            "  - Ensure quantifiable and testable criteria.\n"
            "- Technical Requirements (TR):\n"
            "  - Detail system architecture, technology stack, APIs, databases, integrations, hardware/software constraints, and security protocols.\n"
            "Technical Analysis & Data Representation:\n"
            "- Data Model:\n"
            "  - Expand with entity-relationship, database schemas, attribute definitions, and data flow explanations.\n"
            "  - Include normalization and optimization principles.\n"
            "- User Characteristics:\n"
            "  - Define user personas, roles, access levels, demographics, behavior patterns, and usability needs.\n"
            "  - Incorporate UX/UI principles for better accessibility.\n"
            "- Codification Schemes:\n"
            "  - Provide structured naming conventions, numbering systems, data classification rules, and version control strategies.\n"
            "  - Align with industry standards.\n"
            "Enhancements Using External Research & Best Practices:\n"
            "- Refine vague sections using LLM capabilities and external industry research to ensure clarity and completeness.\n"
            "- Incorporate real-world case studies, frameworks, standards, and benchmarks.\n"
            "- Utilize tables, flowcharts, and structured lists to enhance readability.\n"
            "- Maintain a formal, professional, and highly structured format suitable for clients and stakeholders.\n"
            "Output Requirements:\n"
            "- The final SRS document must be highly detailed, structured, and exhaustive.\n"
            "- Information should be well-organized and fully explained without ambiguity.\n"
            "- No modification should be made to sections explicitly required to remain unchanged.\n"
            "- The document must be formatted professionally, using clear headings, tables, and bullet points for readability.\n"
            "Every subpoint should be explained in an elaborated manner."
            ),
            expected_output=(
            "A fully written, structured, and polished SRS document incorporating all extracted and categorized information, ensuring that Out of Scope and Assumptions match the BRD and along with it every part must be defined in an elaborated manner. Every subpoint should be explained in an elaborated manner."
            ),
            agent=srs_writer,
        )

        srs_format_task = Task(
            description=(
            "Format the final SRS document with appropriate headings, line breaks, and structured sections.\n"
            "Ensure that the 'Out of Scope' section is correctly placed after 'In Scope'.\n"
            "Ensure that 'Assumptions' is correctly formatted with bullet points and listed before 'Dependencies'."
            ),
            expected_output=(
            "The final SRS document is properly formatted with bolded, capitalized headings, clear section divisions, and includes 'Out of Scope,' 'Assumptions,' 'Dependencies,' and 'Conclusion' sections saved as 'srs1.md'."
            ),
            agent=srs_formatter,
        )

        # Crew
        crew = Crew(
            agents=[business_analyst, technical_analyst, requirement_categorizer, srs_writer, srs_formatter],
            tasks=[business_analysis_task, technical_analysis_task, requirement_categorize_task, srs_write_task, srs_format_task],
            process=Process.sequential,
            verbose=True,
        )

        return crew.kickoff(inputs={"topic": topic})
    else:
        st.error("Please upload a file to proceed.")
        return None
    
def generate_sdd(topic, uploaded_file, blog="default"):
    if uploaded_file is not None:
        # Create the temp directory if it does not exist
        if not os.path.exists("temp"):
            os.makedirs("temp")

        # Save the uploaded file to a temporary location
        temp_file_path = os.path.join("temp", uploaded_file.name)
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Create a FileReadTool with the path to the uploaded file
        file_read_tool = FileReadTool(file_path=temp_file_path)

        project_manager = Agent(
            role='Project Manager',
            goal=(
            "Oversees the entire documentation process, ensuring that all sections are updated and controlled properly. "
            "Maintains a record of controlled copy holders and amendments while ensuring alignment with project deadlines and compliance standards. "
            "Coordinates with various teams to ensure smooth execution of the system design documentation process."
            ),
            backstory=(
            "A highly experienced project manager with a background in software development and documentation oversight. "
            "Has successfully led multiple large-scale IT projects, ensuring structured and effective communication among stakeholders. "
            "Detail-oriented and a strong advocate for documentation best practices."
            ),
            tools=[file_read_tool]
        )

        system_architect = Agent(
            role='System Architect',
            goal=(
            "Defines the system's high-level architecture and design constraints, ensuring scalability, security, and efficiency. "
            "Creates logical and process-level Data Flow Diagrams (DFDs) and state transition diagrams for seamless system operation. "
            "Bridges the gap between business needs and technical implementation by structuring subsystems effectively."
            ),
            backstory=(
            "A visionary architect with 15+ years of experience in software and system design. "
            "Passionate about creating efficient, scalable, and well-structured architectures. "
            "Has worked in multiple industries, translating complex business processes into well-documented system blueprints. "
            "Prefers a methodical approach and values precision in documentation."
            ),
            tools=[file_read_tool]
        )

        business_analyst = Agent(
            role='Business Analyst',
            goal=(
            "Extracts relevant content from the given business requirements document, including Introduction, Purpose, Scope, Assumptions, References, and Overview. "
            "Enhances unclear sections using AI and industry research to ensure completeness before passing refined content for documentation. "
            "Defines system functions, subsystem breakdowns, and user interface requirements."
            ),
            backstory=(
            "A senior business analyst with expertise in understanding business requirements and ensuring clarity in documentation. "
            "Has a keen eye for ambiguity and works to refine details before they become development roadblocks. "
            "Experienced in working with cross-functional teams to translate business needs into technical specifications."
            ),
            tools=[file_read_tool]
        )

        uiux_designer = Agent(
            role='UI/UX Designer',
            goal=(
            "Designs intuitive and user-friendly interfaces for all system subsystems. "
            "Ensures that UI/UX elements follow best practices, accessibility guidelines, and align with system functionality. "
            "Collaborates with business analysts and software developers to create wireframes and state transition diagrams."
            ),
            backstory=(
            "A passionate UI/UX designer with a background in human-computer interaction and visual design. "
            "Has experience designing enterprise applications, ensuring optimal usability and aesthetic appeal. "
            "Advocates for a user-first approach and leverages feedback loops to refine designs continuously."
            ),
            tools=[file_read_tool]
        )

        db_administrator = Agent(
            role='Database Administrator',
            goal=(
            "Designs and documents the system's data storage model, including Entity Relationship Diagrams (ERDs) and schema definitions. "
            "Ensures data integrity, performance optimization, and secure access to stored information. "
            "Establishes database administration procedures for backup, recovery, and maintenance."
            ),
            backstory=(
            "A database specialist with a deep understanding of SQL, NoSQL, and cloud database solutions. "
            "Has worked on high-availability systems, ensuring database efficiency and security. "
            "Strong advocate for structured data modeling and efficient indexing strategies."
            ),
            tools=[file_read_tool]
        )

        security_engineer = Agent(
            role='Security Engineer',
            goal=(
            "Implements security policies, encryption mechanisms, and access controls. "
            "Defines security protocols for authentication, audit tracing, and data integrity. "
            "Establishes special recovery procedures to mitigate potential breaches or failures."
            ),
            backstory=(
            "A cybersecurity expert with experience in ethical hacking, compliance frameworks, and network security. "
            "Has worked with government agencies and private enterprises to secure mission-critical systems. "
            "Always on the lookout for vulnerabilities and believes in a proactive security approach."
            ),
            tools=[file_read_tool]
        )

        network_administrator = Agent(
            role='Network Administrator',
            goal=(
            "Ensures that network maintenance procedures are well-documented and aligned with security best practices. "
            "Defines network topology, access control measures, and connectivity requirements for the system. "
            "Works closely with security engineers to prevent unauthorized access and potential breaches."
            ),
            backstory=(
            "A network specialist with certifications in Cisco, AWS, and cloud networking solutions. "
            "Experienced in managing hybrid cloud environments and large-scale enterprise networks. "
            "Passionate about optimizing system connectivity while maintaining robust security."
            ),
            tools=[file_read_tool]
        )

        software_developer = Agent(
            role='Software Developer',
            goal=(
            "Develops detailed program designs for various system components, ensuring modularity and reusability. "
            "Writes structured code in accordance with system design specifications. "
            "Implements error handling procedures to ensure robust system operation."
            ),
            backstory=(
            "A full-stack developer with a passion for clean code and efficient system architecture. "
            "Has contributed to multiple large-scale projects, working across various programming languages and frameworks. "
            "Enjoys solving complex problems through efficient algorithms and modular design."
            ),
            tools=[file_read_tool]
        )

        qa_team = Agent(
            role='QA / Testing Team',
            goal=(
            "Validates system outputs and ensures alignment with documented requirements. "
            "Documents query formats, output screens, and online help functionalities. "
            "Works closely with developers to identify and resolve bugs before deployment."
            ),
            backstory=(
            "A dedicated quality assurance team with a mix of manual and automated testing expertise. "
            "Ensures software reliability by implementing comprehensive test strategies and automated test suites. "
            "Believes that rigorous testing is key to a seamless user experience."
            ),
            tools=[file_read_tool]
        )

        technical_writer = Agent(
            role='Technical Writer',
            goal=(
            "Compile, format, and document all gathered information from specialist agents into a structured and uniform Markdown document. "
            "Ensure consistency in tables, headings, and content presentation without altering the technical accuracy of the information provided."
            ),
            backstory=(
            "A meticulous and detail-oriented writer with extensive experience in technical documentation. "
            "Skilled in Markdown structuring, ensuring clarity, uniformity, and professional presentation of system design documents. "
            "Committed to maintaining content integrity while enhancing readability and structured formatting."
            ),
            tools=[file_read_tool, FileWriterTool()]
        )

        project_management_task = Task(
            description=(
            f"Access the srs for initial understanding and then use the provided llm for getting extended content which should be highly detailed.\n"
            f"Oversee and manage the SDD documentation process for {topic}, ensuring compliance and alignment with project goals.\n"
            "Maintain and update the following sections:\n"
            "  A. List of Controlled Copy Holders\n"
            "  B. List of Amendments on the Previous Version\n"
            "Ensure all sections are completed on time, properly reviewed, and no critical headings are omitted. NO points should be missed. Research for every point."
            ),
            expected_output=(
            "content for-\n"
            "A. List of Controlled Copy Holders\n"
            "B. List of Amendments on the Previous Version\n"
            "A finalized version of the SDD with updated controlled copies and amendment logs."
            ),
            agent=project_manager
        )

        system_architect_task = Task(
            description=(
            f"Access the srs for initial understanding and then use the provided llm for getting extended content which should be highly detailed.\n"
            f"Design the system architecture for {topic} and ensure clear documentation of:\n"
            "  2.1 The System Perspective\n"
            "    2.1.1 The System Context\n"
            "    2.1.2 The Development & Operation Environment\n"
            "  2.2 System Functions\n"
            "    2.2.1 Subsystem Decomposition of Processors Main Module\n"
            "    2.2.2 Subsystem-wise Task Distribution Across Processor(s)\n"
            "    2.2.3 Tasks Performed by Processor(s)\n"
            "  3.1 System Design Constraints\n"
            "  3.2 System Design Criteria\n"
            "  3.3 Process Level DFDs (Allocation of Tasks to Processor(s))\n"
            "    3.3.1 0th Level Logical DFD\n"
            "    3.3.2 1st Level Logical DFD\n"
            "  3.4 Task Level DFDs (Tasks to Be Done Within Processor(s))\n"
            "    3.4.1 Lower Level DFDs for Processor RFQ (Process No. 7)\n"
            "    3.4.2 Lower Level DFDs for Processor Send Quote With RFQ (Process No. 10)\n"
            "    3.4.3 Lower Level DFDs for Processor Send Quote Without RFQ (Process No. 11) NO points should be missed. Research for every point."
            ),
            expected_output=(
            "content for-\n"
            "2.1 The System Perspective\n"
            "  2.1.1 The System Context\n"
            "  2.1.2 The Development & Operation Environment\n"
            "2.2 System Functions\n"
            "  2.2.1 Subsystem Decomposition of Processors Main Module\n"
            "  2.2.2 Subsystem-wise Task Distribution Across Processor(s)\n"
            "  2.2.3 Tasks Performed by Processor(s)\n"
            "3.1 System Design Constraints\n"
            "3.2 System Design Criteria\n"
            "3.3 Process Level DFDs (Allocation of Tasks to Processor(s))\n"
            "  3.3.1 0th Level Logical DFD\n"
            "  3.3.2 1st Level Logical DFD\n"
            "3.4 Task Level DFDs (Tasks to Be Done Within Processor(s))\n"
            "  3.4.1 Lower Level DFDs for Processor RFQ (Process No. 7)\n"
            "  3.4.2 Lower Level DFDs for Processor Send Quote With RFQ (Process No. 10)\n"
            "  3.4.3 Lower Level DFDs for Processor Send Quote Without RFQ (Process No. 11) NO points should be missed. Research for every point.\n"
            "A structured architecture document with diagrams and subsystem decomposition."
            ),
            agent=system_architect
        )

        business_analysis_task = Task(
            description=(
            f"Access the srs for initial understanding and then use the provided llm for getting extended content which should be highly detailed.\n"
            f"Extract and refine the business-related sections for {topic}:\n"
            "  1. Introduction\n"
            "    1.1 Purpose of the SDD\n"
            "    1.2 Scope of the Computerized System\n"
            "    1.3 Definitions, Acronyms & Abbreviations\n"
            "    1.4 References\n"
            "    1.5 Overview of the SDD\n"
            "  2.2 System Functions\n"
            "  2.3 The User Interface of the Software\n"
            "    2.3.1 General Features of the User Interface\n"
            "    2.3.2 User Interface of Subsystem RFQ\n"
            "    2.3.3 User Interface of Subsystem View Order Status\n"
            "    2.3.4 User Interface of Subsystem Send Quote\n"
            "    2.3.5 User Interface of Subsystem Sales Confirmation\n"
            "    2.3.6 User Interface of Subsystem Order Updation. NO points should be missed. Research for every point."
            ),
            expected_output=(
            "content for-\n"
            "1. Introduction\n"
            "  1.1 Purpose of the SDD\n"
            "  1.2 Scope of the Computerized System\n"
            "  1.3 Definitions, Acronyms & Abbreviations\n"
            "  1.4 References\n"
            "  1.5 Overview of the SDD\n"
            "2.2 System Functions\n"
            "2.3 The User Interface of the Software\n"
            "  2.3.1 General Features of the User Interface\n"
            "  2.3.2 User Interface of Subsystem RFQ\n"
            "  2.3.3 User Interface of Subsystem View Order Status\n"
            "  2.3.4 User Interface of Subsystem Send Quote\n"
            "  2.3.5 User Interface of Subsystem Sales Confirmation\n"
            "  2.3.6 User Interface of Subsystem Order Updation. NO points should be missed. Research for every point.\n"
            "A refined business requirements document covering scope, definitions, and UI specifications."
            ),
            agent=business_analyst
        )

        ui_design_task = Task(
            description=(
            f"Access the srs for initial understanding and then use the provided llm for getting extended content which should be highly detailed.\n"
            f"Design and document the following user interface sections for {topic}:\n"
            "  2.3 The User Interface of the Software\n"
            "    2.3.1 General Features of the User Interface\n"
            "    2.3.2 User Interface of Subsystem RFQ\n"
            "    2.3.3 User Interface of Subsystem View Order Status\n"
            "    2.3.4 User Interface of Subsystem Send Quote\n"
            "    2.3.5 User Interface of Subsystem Sales Confirmation\n"
            "      2.3.5.1 State Transition Diagrams Sales Confirmation\n"
            "    2.3.6 User Interface of Subsystem Order Updation\n"
            "      2.3.6.1 State Transition Diagrams Order Updation. NO points should be missed. Research for every point."
            ),
            expected_output=(
            "content for-\n"
            "Design and document the following user interface sections:\n"
            "  2.3 The User Interface of the Software\n"
            "    2.3.1 General Features of the User Interface\n"
            "    2.3.2 User Interface of Subsystem RFQ\n"
            "    2.3.3 User Interface of Subsystem View Order Status\n"
            "    2.3.4 User Interface of Subsystem Send Quote\n"
            "    2.3.5 User Interface of Subsystem Sales Confirmation\n"
            "      2.3.5.1 State Transition Diagrams Sales Confirmation\n"
            "    2.3.6 User Interface of Subsystem Order Updation\n"
            "      2.3.6.1 State Transition Diagrams Order Updation. NO points should be missed. Research for every point.\n"
            "Wireframes, UI mockups, and state transition diagrams for all user interfaces."
            ),
            agent=uiux_designer
        )

        database_design_task = Task(
            description=(
            "Access the srs for initial understanding and then use the provided llm for getting extended content which should be highly detailed.\n"
            "Define and document the data storage model, covering:\n"
            "  2.4 The Data Storage Model\n"
            "    2.4.1 Entity Relationship Diagram for Login Process\n"
            "    2.4.2 Entity Relationship Diagram for Process Registration\n"
            "    2.4.3 Entity Relationship Diagram for Process JST User Login\n"
            "    2.4.4 Entity Relationship Diagram for Process RFQ\n"
            "    2.4.5 Entity Relationship Diagram for Process Send Quote\n"
            "    2.4.6 Entity Relationship Diagram for Process Sales Confirmation\n"
            "    2.4.7 Entity Relationship Diagram for Process Order Updation\n"
            "  3.5 Data Organization & Decomposition\n"
            "    3.5.1 Schema / File Layouts for Processes. NO points should be missed. Research for every point."
            ),
            expected_output=(
            "content for-\n"
            "2.4 The Data Storage Model\n"
            "  2.4.1 Entity Relationship Diagram for Login Process\n"
            "  2.4.2 Entity Relationship Diagram for Process Registration\n"
            "  2.4.3 Entity Relationship Diagram for Process JST User Login\n"
            "  2.4.4 Entity Relationship Diagram for Process RFQ\n"
            "  2.4.5 Entity Relationship Diagram for Process Send Quote\n"
            "  2.4.6 Entity Relationship Diagram for Process Sales Confirmation\n"
            "  2.4.7 Entity Relationship Diagram for Process Order Updation\n"
            "3.5 Data Organization & Decomposition\n"
            "  3.5.1 Schema / File Layouts for Processes. NO points should be missed. Research for every point.\n"
            "A structured data storage model with ERDs and schema definitions."
            ),
            agent=db_administrator
        )

        security_task = Task(
            description=(
            "Access the srs for initial understanding and then use the provided llm for getting extended content which should be highly detailed.\n"
            "Define security and recovery measures, covering:\n"
            "  3.6 Special Considerations\n"
            "    3.6.1 Special Security Measures\n"
            "    3.6.2 Special Recovery Procedures\n"
            "    3.6.3 Audit Tracing Facility. NO points should be missed. Research for every point."
            ),
            expected_output=(
            "content for-\n"
            "3.6 Special Considerations\n"
            "  3.6.1 Special Security Measures\n"
            "  3.6.2 Special Recovery Procedures\n"
            "  3.6.3 Audit Tracing Facility. NO points should be missed. Research for every point.\n"
            "A security and recovery plan with authentication, encryption, and audit tracing mechanisms."
            ),
            agent=security_engineer
        )

        network_task = Task(
            description=(
            "Access the srs for initial understanding and then use the provided llm for getting extended content which should be highly detailed.\n"
            "Define and document the network-related considerations:\n"
            "  3.6.4 Network Maintenance Procedures. NO points should be missed. Research for every point."
            ),
            expected_output=(
            "content for-\n"
            "3.6.4 Network Maintenance Procedures. NO points should be missed. Research for every point.\n"
            "A network infrastructure document with maintenance protocols and performance optimization strategies."
            ),
            agent=network_administrator
        )

        software_development_task = Task(
            description=(
            "Access the srs for initial understanding and then use the provided llm for getting extended content which should be highly detailed.\n"
            "Develop and document program design for subsystems, covering:\n"
            "  4. Detailed Program Design\n"
            "    4.1 Program Design for Sales Confirmation\n"
            "    4.1.1 Program Design for Sales Confirmation\n"
            "    4.1.2 Program Design for Subsystem 2\n"
            "  3.6.6 Error Handling Procedures. NO points should be missed. Research for every point."
            ),
            expected_output=(
            "content for-\n"
            "Develop and document program design for subsystems, covering:\n"
            "  4. Detailed Program Design\n"
            "    4.1 Program Design for Sales Confirmation\n"
            "    4.1.1 Program Design for Sales Confirmation\n"
            "    4.1.2 Program Design for Subsystem 2\n"
            "  3.6.6 Error Handling Procedures. NO points should be missed. Research for every point.\n"
            "A structured, modular codebase with program design documentation."
            ),
            agent=software_developer
        )

        qa_testing_task = Task(
            description=(
            "Access the srs for initial understanding and then use the provided llm for getting extended content which should be highly detailed.\n"
            "Validate system outputs and testing requirements:\n"
            "  5. Appendix\n"
            "    5.2 Output Forms/Screens\n"
            "    5.3 Query Formats\n"
            "    5.4 Online Help Available\n"
            "    5.5 Updated Data Dictionary\n"
            "    5.6 Cross-reference List. NO points should be missed. Research for every point."
            ),
            expected_output=(
            "content for-\n"
            "5. Appendix\n"
            "  5.2 Output Forms/Screens\n"
            "  5.3 Query Formats\n"
            "  5.4 Online Help Available\n"
            "  5.5 Updated Data Dictionary\n"
            "  5.6 Cross-reference List. NO points should be missed. Research for every point.\n"
            "A comprehensive testing report covering all system functionalities."
            ),
            agent=qa_team
        )

        technical_writing_task = Task(
            description=(
            "Compile and format the content researched and structured by the specialist agents.\n"
            "Ensure a consistent and professional writing style while maintaining the original technical accuracy of the data provided.\n"
            "Tasks include:\n"
            "  - Standardizing the format of all sections using proper Markdown tables, bullet points, and headings.\n"
            "  - Ensuring uniformity in structure across all documentation parts while keeping the content as provided by the specialists.\n"
            "  - Avoiding content alteration while enhancing readability and presentation.\n"
            "  - Organizing the document sections as per the SDD format.\n"
            "  - Maintaining tables for structured data representation. NO points should be missed. Write for every point of the respective specialist agents."
            ),
            expected_output=(
            "A well-structured, fully formatted, and uniform System Design Document (SDD) in Markdown,\n"
            "ensuring proper table formatting, headings, bullet points, and consistent terminology."
            ),
            agent=technical_writer
        )

        # Crew
        crew = Crew(
            agents=[project_manager, system_architect, business_analyst, uiux_designer, db_administrator, security_engineer, network_administrator, software_developer, qa_team, technical_writer],
            tasks=[project_management_task, system_architect_task, business_analysis_task, ui_design_task, database_design_task, security_task, network_task, software_development_task, qa_testing_task, technical_writing_task],
            process=Process.sequential,
            verbose=True,
        )

        return crew.kickoff(inputs={"topic": topic})
    else:
        st.error("Please upload a file to proceed.")
        return None



# Main content area
if generate_button_srs:
    with st.spinner("Generating SRS...This may take a moment.."):
        try:
            result = generate_srs(topic, uploaded_file)
            if result:
                st.markdown("### Generated SRS")
                st.markdown(result)

                # Add download button
                st.download_button(
                    label="Download Content",
                    data=result.raw,
                    file_name=f"article.txt",
                    mime="text/plain"
                )
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")


if generate_button_sdd:
    with st.spinner("Generating SDD...This may take a moment.."):
        try:
            result = generate_sdd(topic, uploaded_file)
            if result:
                st.markdown("### Generated SDD")
                st.markdown(result)

                # Add download button
                st.download_button(
                    label="Download Content",
                    data=result.raw,
                    file_name=f"article.txt",
                    mime="text/plain"
                )
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")


# Footer
st.markdown("----")
st.markdown("Built by AgentcAI")

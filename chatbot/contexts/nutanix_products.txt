[Solution / HCI Foundation]

Nutanix pioneered hyperconverged infrastructure (HCI) that collapses compute, storage, virtualization, and networking into a software‑defined platform running on industry‑standard x86 servers. A lightweight Controller VM on every node distributes data and management services, allowing clusters to start with three nodes and scale one node at a time without external SAN/NAS gear. Hardware choice is open (Nutanix, HPE, Lenovo, Dell, Cisco, Fujitsu, others).

----

[NCI – Nutanix Cloud Infrastructure]

NCI supplies the distributed data‑plane for the Nutanix Cloud Platform. Core services include:
 - AOS Storage Fabric – pools SSD/HDD or all‑flash into a single datastore with intelligent tiering, erasure coding, dedupe/compression and integrated snapshots.
 - AHV – license‑free KVM‑based hypervisor with live‑migration, Dynamic Scheduling, data‑locality and built‑in security.
 - Unified Storage – files (SMB/NFS), objects (S3), and block volumes (iSCSI) from the same cluster.
 - Flow – micro‑segmentation and virtual networking (VPCs, service chains).
 - Resilience – replication factor 2/3, tunable redundancy, availability domains, CVM auto‑pathing.

Result: enterprise cloud experience with one‑click upgrades, no single point of failure, and freedom to choose hypervisor or cloud.

----

[NCP – Nutanix Cloud Platform]

NCP unifies NCI (data plane) and NCM (management plane) into a secure, self‑healing hybrid multicloud that runs any workload on‑prem, at the edge, or in public clouds. Benefits: single skill‑set across environments, 97 % less unplanned downtime, and ROI in ~12 months by eliminating over‑provisioning and siloed tools.

----

[NCM – Nutanix Cloud Manager]

NCM is the multicloud management layer delivering:
 1. Intelligent Operations – predictive analytics, anomaly detection, low‑code remediation.
 2. Self‑Service & Orchestration – blueprint‑based app provisioning and lifecycle automation.
 3. Cost Governance – real‑time spend dashboards, budgeting, right‑sizing, charge‑back.
 4. Security Central – cloud‑wide posture management, micro‑segmentation policy design, and compliance audits.

Together, these functions automate Day‑2 ops and drive financial accountability across private and public clouds.

----

[NC2 – Nutanix Cloud Clusters]

NC2 extends the full Nutanix stack (AOS + AHV + Prism) onto bare‑metal instances in AWS or Microsoft Azure, letting customers “lift‑and‑shift” VMs without re‑tooling. Key value: unified management, rapid cloud bursting/fail‑over, use of existing hyperscaler credits, and native access to cloud‑specific services.

----

[NDB – Nutanix Database Service]

NDB delivers database‑as‑a‑service for SQL Server, Oracle, PostgreSQL, MySQL, and MongoDB across on‑prem, edge, and public clouds. It automates provisioning, cloning, patching, backup/restore, and role‑based access, enabling DBAs to manage hundreds of instances from one control plane. Forrester found 291 % ROI and < 6‑month payback, with 97 % faster provisioning and 50 % less DBA overtime.

----

[NKP – Nutanix Kubernetes Platform]

NKP provides upstream‑conformant Kubernetes plus GitOps, declarative APIs, multicluster fleet management, and built‑in security exceeding NSA/CISA guidance. It runs on Nutanix, other hypervisors, bare metal, or public clouds, giving DevOps teams a consistent path from core to edge with real‑time cost visibility and “NKP Insights” for automatic root‑cause analysis.

----

[NAI – Nutanix Enterprise AI]

Nutanix Enterprise AI (GPT‑in‑a‑Box 2.0) turns IT resources into AI resources. It offers an elegant UI and secure endpoint APIs for NVIDIA NIM, Hugging Face, or private LLMs, supports air‑gapped sites, and runs on any CNCF‑certified Kubernetes distribution. Features: RBAC, token management, GPU/cluster monitoring, pre‑flight model tests. Goal: accelerate GenAI adoption while maintaining enterprise controls.

----

[NUS – Nutanix Unified Storage]

NUS is a software‑defined data‑services platform that unifies block, file, and object storage with one‑click scale from one node to multi‑PB, 10 GB/s sequential read per node, and optional 30 TB NVMe drives (550 TB per node). Integrated Data Lens adds ransomware defense, audits, WORM, and immutable snapshots. Licensing is consumption‑based and deploys in dedicated or HCI mode—ideal for AI/ML data pipelines.

----

[Alliances & OEM Partnerships]

Nutanix maintains 2,000+ alliances to give customers validated stacks and single‑call support, including:
 - Citrix – hybrid multicloud EUC;
 - Palo Alto Networks – VM‑Series NGFW integration;
 - Red Hat – certified full‑stack for RHEL/OpenShift;
 - SAP – HANA‑ready HCI with one‑click scale;
 - Veeam / HYCU – agentless backup leveraging Nutanix snapshots;
 - AMD, Intel – optimized HCI on latest processors;
 - Cisco, HPE, Lenovo, Dell, Fujitsu – turnkey HCI appliances with Nutanix software.


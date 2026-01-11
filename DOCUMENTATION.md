# Journal, a Forest  
Technical Overview & Design Decisions

This document outlines the tech stack and the reasoning behind the architectural and design choices in *Journal, a Forest*. The goal of this project is not just to build a journaling app, but to explore how structured reflection, memory, and gentle prompting can be supported by modern ML systems without becoming prescriptive or productivity-brained.

This is intentionally a prototype-first system: correctness, clarity, and conceptual integrity are prioritized over premature optimization.

---

## High-Level Architecture

The app is split into three main layers:

1. Frontend (React + TypeScript)  
2. Backend API (FastAPI + SQLite)  
3. Intelligence Layer (LLMs + Embeddings + Chroma)

Each layer has a single responsibility and minimal cross-contamination.

---

## Frontend

### Stack
- React  
- TypeScript  
- Tailwind CSS  
- React Router  
- Axios (API client)

### Design Philosophy
The frontend is intentionally thin:
- No business logic  
- No prompt generation logic  
- No memory or personalization logic  

Its job is to:
- Display prompts  
- Let the user write  
- Render reflections, threads, and trees  
- Navigate between states cleanly  

Anything thinking-related lives on the backend.

### State Management
- Session state is handled via a SessionContext  
- Prompts and threads are fetched from the backend on page load  
- No long-lived local caching of prompts  

This avoids frontend/backend drift and makes debugging much easier.

---

## Backend

### Stack
- FastAPI  
- Python 3.11+  
- SQLite  
- aiosqlite  
- Pydantic v2  
- ChromaDB

### Why SQLite?
- Zero setup  
- Easy to reset during development  
- Sufficient for a single-user prototype  
- Pairs well with Chroma for semantic memory  

If this were productionized, SQLite would likely be replaced with Postgres but not yet.

---

## Database Design

### Core Tables
- sessions  
- journal_entries  
- entry_analysis  
- threads  
- prompts  
- trees  
- streak_days  

### Notable Design Choices

#### Prompts Are Stored, Not Regenerated on Read
Prompts are generated at meaningful moments, not on every page load.
They are generated based on recent memories, drawn from SQLite, and relevant memories, drawn from ChromaDB.

There are two prompt sources:
- onboarding starter prompts  
- generated prompts created after entries  

This avoids:
- Prompt drift  
- Inconsistent UI behavior  
- "Why did my prompts change when I refreshed?" bugs  

#### Prompts Are Overwritten, Not Appended
Only one active prompt set exists per session + source.

This keeps:
- The mental model simple  
- The UI deterministic  
- The database small  

Prompts are treated as ephemeral, not archival.

---

## LLM Layer (Mistral)

### Usage
LLMs are used for:
- Entry analysis  
- Prompt generation  
- Weekly insights  

### Structured Outputs
All LLM calls use Pydantic-validated structured outputs.

This:
- Avoids brittle string parsing  
- Makes failures obvious  
- Forces explicit contracts between code and model  

If the model deviates from the schema, the call fails fast, which is desirable during development.

---

## Entry Analysis Pipeline

When a journal entry is submitted:

1. Raw entry is stored  
2. LLM generates:
   - Memory summary (factual, neutral)  
   - Pattern reflection (observational, not advice)  
   - Follow-up question  
   - Themes  
   - Emotions  
   - Unresolved threads  
3. Analysis is stored in entry_analysis  
4. A symbolic tree is generated  
5. Entry summary is embedded and stored in Chroma  
6. New prompts are generated and saved  

The pipeline is intentionally linear and explicit: no background jobs, no hidden behavior.

---

## ChromaDB (Semantic Memory)

### What Is Embedded
- The memory summary, not the raw journal text  

This improves:
- Signal-to-noise ratio  
- Semantic retrieval quality  
- Conceptual alignment with what mattered

### Metadata Constraints
Chroma metadata is restricted to primitive types.
- Lists are serialized to strings  
- No nested structures  

This keeps inserts predictable and avoids runtime validation errors.

---

## Prompt Generation Philosophy

Prompts are designed to be:
- Reflective, not directive  
- Observational, not corrective  
- Curious, not productivity-driven  

System prompts explicitly discourage:
- Advice  
- Goal-setting  
- Optimization language  

Prompt generation considers:
- Recent summaries  
- Semantically related past memories  
- Active threads  

But never the entire journal history at once.

---

## Threads

Threads represent:
- Ongoing ideas  
- Emotional motifs  
- Recurring tensions  

They are:
- Extracted by the LLM  
- Stored explicitly  
- Re-surfaced gently  

Threads are not tasks or goals; they're narrative gravity.

---

## Weekly Insights

Weekly insights are generated from:
- Stored analyses only  
- Time-based aggregation  
- No semantic search  

This keeps the system deterministic and avoids unnecessary complexity.

---

## Error Handling & Debuggability

Deliberate choices:
- Explicit SQL queries  
- No ORM  
- Clear transaction boundaries  
- Minimal abstraction layers  

This made debugging significantly easier, especially around:
- Cursor lifecycle issues  
- Transaction commits  
- Session state bugs  

---

## What This Project Is (and Isn't)

This project is:
- A reflective system prototype  
- An exploration of LLM-assisted journaling  
- A testbed for memory-aware prompting  

It is not:
- A productivity app  
- A mental health app  
- A finished consumer product  

---

## Guiding Principle

The core design constraint throughout this project is simple:

The system should feel like it's listening, not steering.

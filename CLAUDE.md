# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What is Collabia

Collabia is a multi-agent conversational chatbot where several LLMs debate until reaching consensus.

**Core intuition:** A single LLM execution is often imperfect. Two AIs (Claude Sonnet + Gemini Pro) that exchange, analyze, and mutually critique each other produce a significantly better final answer after a few rounds.

This maps to what researchers call "Mixture of Agents" or "LLM Debate" — arrived at empirically.

## Consensus Loop Architecture

```
nb_max_boucles = n
vote = non_fini

tant que i < n ET vote = non_fini :
    appel réponse de chaque agent en parallèle
    collecte des réponses dans une map
    appel analyse de chaque agent : réponse préférée + critiques globales
    si réponse préférée = la même pour majorité des agents → vote = fini
    éliminer la pire réponse (cet agent ne répondra plus mais peut encore analyser)
    rafraîchir le contexte avec la réponse préférée
    (retour en boucle)

si vote = fini → afficher réponse préférée
sinon → afficher les dernières réponses
```

Key design points:
- Agent responses run **in parallel** each round
- Eliminated agents can still **participate in analysis** (but not respond)
- Loop exits early on **majority consensus** (no need to exhaust all rounds)
- Context is refreshed with the preferred response between rounds

## Agents

- **Responder role**: generates an answer to the user prompt
- **Analyzer role**: reads all responses, picks the best one, provides critiques
- Both roles can be played by the same model instance in sequence

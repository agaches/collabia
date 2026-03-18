# Collabia — Test Runs

## Méthodologie

**Commande utilisée :**
```bash
uv run collabia "<question>"
```
*(sans `--verbose` : affichage compact — rounds, votes d'élimination, before/after du gagnant)*

**Configuration :**
- 3 agents : Gemini 2.5 Pro (`gemini`), Gemini 2.5 Flash (`gemini-flash`), Gemini 3.1 Flash Lite (`gemini-lite`)
- Max rounds : 5
- Algo : élimination par vote majoritaire à chaque round, jusqu'à 1 agent restant
- Before/after : réponse du gagnant au round 1 vs réponse finale

**Critères d'évaluation des before/after :**
- Structure et clarté de l'argumentation
- Richesse du contenu (exemples, cas d'usage, nuances)
- Intégration des critiques reçues (le gagnant améliore-t-il sa réponse ?)
- Ajout de matière nouvelle (concepts, exemples, analogies)

---

## Série 1 — 2026-03-18

### T1 — Quand faut-il utiliser NoSQL plutôt que SQL ?

| Paramètre | Valeur |
|---|---|
| Gagnant | **Gemini 2.5 Flash** |
| Rounds | 2 |
| Éliminés | Gemini Lite (R1) → Gemini Pro (R2) |
| Erreurs | 1 erreur JSON (critique Flash tronquée au R2) |

**Ordre d'élimination :** Lite → **Pro** (inhabituel — Flash gagne sur cette question)

**Before (Flash, Round 1) :**
> Le choix entre SQL et NoSQL dépend des besoins en structure des données, scalabilité et cohérence. Présentation en 6 scénarios clés (données non structurées, scalabilité horizontale, haute disponibilité, performances spécifiques, dev agile, cas graphe/cache). Tableau comparatif SQL vs NoSQL. Mention de la persistance polyglotte.

**After (Flash, Round 2) :**
> Approche révisée : insiste sur le fait qu'il n'y a pas de solution universelle. Restructuré en 5 axes (rappel des différences, scénarios NoSQL, compromis de NoSQL, cas où SQL reste supérieur, persistance polyglotte). Ajout d'un guide de décision en 5 questions, section "quand SQL reste supérieur" absente du R1.

**Évolution :** ✅ Ajout d'une section explicite sur les limites de NoSQL et les cas où SQL reste préférable — nuance importante absente au R1.

---

### T2 — Explique le GIL Python et son impact sur la performance des threads

| Paramètre | Valeur |
|---|---|
| Gagnant | **Gemini 2.5 Pro** |
| Rounds | 2 |
| Éliminés | Gemini Lite (R1) → Gemini Flash (R2) |
| Erreurs | Aucune |

**Before (Pro, Round 1) :**
> Explication complète : définition, historique (reference counting), fonctionnement (relâchement GIL sur I/O et par intervalle), impact CPU-bound (négatif) vs I/O-bound (positif), solutions de contournement (multiprocessing, asyncio, extensions C/Rust). Tableau récapitulatif. Bonne analogie "planche à découper".

**After (Pro, Round 2) :**
> Version enrichie avec distinction explicite concurrence/parallélisme en intro. Ajout d'exemples de code Python illustratifs. **Nouveau : section "L'avenir du GIL" avec PEP 703 et Python 3.13 free-threaded.** Reformulation de l'analogie cuisine plus précise.

**Évolution :** ✅ Ajout de la perspective d'avenir (PEP 703 / Python 3.13) et d'exemples de code — information à haute valeur ajoutée absente au R1.

---

### T3 — React ou Vue en 2025 pour un développeur junior ?

| Paramètre | Valeur |
|---|---|
| Gagnant | **Gemini 2.5 Pro** |
| Rounds | 2 |
| Éliminés | Gemini Lite (R1) → Gemini Flash (R2) |
| Erreurs | 1 erreur JSON (critique Flash tronquée au R2) |

**Before (Pro, Round 1) :**
> Analyse structurée en 3 axes : courbe d'apprentissage, marché de l'emploi, écosystème/avenir. Tableau synthétique React vs Vue. Recommandation selon 2 profils. Conseil sur l'importance de JavaScript/TypeScript comme socle commun. Conseil de regarder les offres locales.

**After (Pro, Round 2) :**
> Intègre une métaphore New York vs Amsterdam/Copenhague pour React vs Vue. Reformulation plus tranchée et actionnable. **Nouveau : section "Plan d'action personnalisé" avec 2 profils (Pragmatique Efficace / Constructeur Serein)** avec chemin d'apprentissage précis (Next.js App Router, Pinia, Shadcn/UI...). Conclusion plus percutante : "le meilleur framework est celui avec lequel tu codes DÈS AUJOURD'HUI."

**Évolution :** ✅ Passage d'une analyse comparative à un vrai plan d'action concret. La réponse finale est plus directive et utilisable.

---

### T4 — Quelle est la meilleure architecture pour une API REST à fort trafic ?

| Paramètre | Valeur |
|---|---|
| Gagnant | **Gemini 2.5 Pro** |
| Rounds | 2 |
| Éliminés | Gemini Lite (R1) → Gemini Flash (R2) |
| Erreurs | Aucune |

**Before (Pro, Round 1) :**
> Architecture en 5 couches (Edge/CDN, Load Balancer, API Gateway, Application/Microservices, Data/Cache/Queues). Schéma ASCII. Principes fondamentaux (statelessness, scalabilité horizontale, asynchronisme, résilience). Détail des technologies (Nginx, Redis, Kafka, Kubernetes...).

**After (Pro, Round 2) :**
> Adopte une **métaphore de la ville** (urbanisme numérique) pour rendre l'architecture accessible. **Nouveau : approche évolutive en 3 phases** (Monolithe Robuste → Extraction des premiers services → Métropole Microservices). Ajout d'un diagramme Mermaid de l'architecture cible. Insistance sur "ne pas sur-ingénier au départ".

**Évolution :** ✅ Ajout de la dimension temporelle (évolution progressive) et d'un diagramme Mermaid — rend la réponse bien plus actionnable pour un architecte débutant.

---

### T5 — Microservices ou monolithe : comment choisir pour un nouveau projet ?

| Paramètre | Valeur |
|---|---|
| Gagnant | **Gemini 2.5 Pro** |
| Rounds | 2 |
| Éliminés | Gemini Lite (R1) → Gemini Flash (R2) |
| Erreurs | Aucune |

**Before (Pro, Round 1) :**
> Métaphore restaurant vs food court. Tableau comparatif 8 critères. Cadre de décision en 3 questions (taille équipe, complexité domaine, besoins scalabilité). Recommandation centrale : **Monolithe Modulaire** avec ses 3 règles. Mantra final.

**After (Pro, Round 2) :**
> Reformulé comme "spectre et trajectoire" plutôt que choix binaire. **Nouveau : 3 règles d'or du monolithe modulaire** détaillées (découpage par domaine, communication par interfaces, indépendance conceptuelle des données). **Nouveau : matrice de décision 4 profils** (startup, grande équipe/domaine mal défini, très grande organisation, projet spécifique). Déclencheurs explicites pour l'extraction en microservice.

**Évolution :** ✅ Les règles d'or du monolithe modulaire et la matrice de décision à 4 profils sont une nette amélioration par rapport à la version R1.

---

## Synthèse

| Test | Gagnant | Amélioration before→after |
|---|---|---|
| T1 — NoSQL vs SQL | Gemini 2.5 Flash | ✅ Ajout section "limites NoSQL / quand SQL reste supérieur" |
| T2 — GIL Python | Gemini 2.5 Pro | ✅ Ajout PEP 703 / Python 3.13 + exemples de code |
| T3 — React vs Vue | Gemini 2.5 Pro | ✅ Passage analyse → plan d'action concret par profil |
| T4 — API REST | Gemini 2.5 Pro | ✅ Ajout approche évolutive 3 phases + diagramme Mermaid |
| T5 — Microservices vs monolithe | Gemini 2.5 Pro | ✅ Règles d'or + matrice de décision 4 profils |

**Observations générales :**
- Gemini Lite est éliminé en R1 sur les 5 tests — écart de capacité trop marqué avec Pro et Flash
- La boucle d'amélioration fonctionne : les 5 réponses finales sont plus structurées, plus nuancées et plus actionnables que les R1
- 2 erreurs JSON sur critiques Flash (T1, T3) — les 2 tests où Flash avait produit de longues réponses avec du contenu markdown riche → corrigé avec `json-repair`
- Gemini Pro gagne 4/5 tests ; Flash gagne T1 (NoSQL vs SQL) où Pro a été jugé moins nuancé sur les limites du NoSQL

---

## Série 2 — 2026-03-18 — Benchmark default vs 3xlite

### Méthodologie

**Commande utilisée :**
```bash
uv run collabia benchmark "<question>"
```

**Objectif :** mesurer si un modèle Lite révisé 3× via la boucle consensus s'approche de la qualité d'un modèle Pro révisé.

**Configs comparées :**
- `agents/default.yaml` — Gemini 2.5 Pro + Flash + Lite (hétérogène)
- `agents/3xlite.yaml` — 3× Gemini Flash Lite (homogène)

**Grille de notation /10 par critère :**
- **A** — Pertinence & couverture du sujet
- **B** — Structure & clarté
- **C** — Valeur ajoutée (ce qui n'est pas évident)
- **D** — Actionnabilité

---

### Résultats des gagnants par config

| Test | default — Gagnant | 3xlite — Gagnant |
|------|-------------------|------------------|
| T1 — NoSQL vs SQL | **Pro** (R2) | **Lite #1** (R2) |
| T2 — GIL Python | **Pro** (R2) | **Lite #1** (R2) |
| T3 — React/Vue | **Flash** (R2) | **Lite #1** (R2) |
| T4 — API REST | **Flash** (R2) | **Lite #1** (R2) |
| T5 — Microservices | **Pro** (R2) | **Lite #2** (R2) |

**Pattern d'élimination default :** Lite éliminé R1 dans 5/5 cas. Pro gagne 3/5, Flash 2/5.
**Pattern d'élimination 3xlite :** toujours 2 rounds, Lite #1 gagne 4/5.

---

### Analyse comparative notée

#### T1 — NoSQL vs SQL

**default — Pro final (8.25/10)**
Structure en 4 questions-signal ("Le signal pour NoSQL / Quand rester SQL"), exemples concrets par dimension, synthèse polyglotte e-commerce (5 technos). Standalone parfait.

| A | B | C | D | Moy |
|---|---|---|---|-----|
| 9 | 9 | 7 | 8 | **8.25** |

**3xlite — Lite #1 final (7.5/10)**
Angle complémentaire : Time-to-Market, coût opérationnel (maturité SQL vs complexité NoSQL), "Test de la Décision" en 3 questions ordonné. Conseil fort : "commencez avec SQL". S'appuie explicitement sur la réponse précédente.

| A | B | C | D | Moy |
|---|---|---|---|-----|
| 6 | 7.5 | 8 | 8.5 | **7.5** |

---

#### T2 — GIL Python

**default — Pro final (8.75/10)**
Définition, historique (reference counting), CPU-bound vs I/O-bound avec code, 3 solutions (multiprocessing, libs C, asyncio), PEP 703 + Python 3.13, tableau récapitulatif. Standalone excellent.

| A | B | C | D | Moy |
|---|---|---|---|-----|
| 10 | 9 | 8 | 8 | **8.75** |

**3xlite — Lite #1 final (8.25/10)**
Angle "mécanique interne". Analogie "bâton de parole". Coût caché du context switching (compteur d'instructions). `Py_BEGIN_ALLOW_THREADS` — niveau expert. PEP 703 enrichi : atomic reference counting, avertissement C-extensions. Résumé pratique avec Cython/Numba/Rust.

| A | B | C | D | Moy |
|---|---|---|---|-----|
| 7 | 8 | 9 | 8.5 | **8.25** |

---

#### T3 — React vs Vue junior

**default — Flash final (7.9/10)**
TL;DR efficace. Tableau 5 critères (emploi, apprentissage, écosystème, philosophie, tendances 2025). Verdict par profils. Un peu exhaustif/redondant.

| A | B | C | D | Moy |
|---|---|---|---|-----|
| 9 | 8 | 7 | 7.5 | **7.9** |

**3xlite — Lite #1 final (8.6/10)**
Formule percutante : *"React est le choix de la carrière, Vue celui de la sérénité."* Points originaux : paradoxe React (charge cognitive SSR/RSC pour un junior), TypeScript comme juge de paix (Vue 3 mieux typé), profils psychologiques (Ingénieur pragmatique vs Créatif/Producteur), règle 80/20 tactique.

| A | B | C | D | Moy |
|---|---|---|---|-----|
| 8 | 8.5 | 9 | 9 | **8.6** |

---

#### T4 — API REST fort trafic

**default — Flash final (7.6/10)**
Catalogue en 3 parties : 8 principes, 7 composants (LB, Gateway, microservices, cache, queues, DB, K8s), pratiques opérationnelles + schéma ASCII. Idempotence mentionnée. Bonne référence, assez exhaustif.

| A | B | C | D | Moy |
|---|---|---|---|-----|
| 9 | 8 | 6.5 | 7 | **7.6** |

**3xlite — Lite #1 final (8.75/10)**
Angle "défense des ressources critiques". Concepts avancés absents du Flash : Zero-Trust interne + Service Mesh (Istio/Linkerd), Load Shedding (HTTP 503 proactif), Backpressure, non-blocking I/O (Go goroutines, Java Project Loom), 202 Accepted + EDA, CQRS, Brotli/gRPC. Synthèse "Layered Defense". Canary Releases. Se tient bien seul.

| A | B | C | D | Moy |
|---|---|---|---|-----|
| 8 | 8.5 | 9.5 | 9 | **8.75** |

---

#### T5 — Microservices vs monolithe

**default — Pro final (9.0/10)**
Analogie restaurant/food court mémorable. Tableau 7 critères. Chemin stratégique : Monolithe Modulaire (DDD, règles strictes) → Strangler Fig pattern. Checklist 5 questions. Mantra final.

| A | B | C | D | Moy |
|---|---|---|---|-----|
| 9.5 | 9 | 8.5 | 9 | **9.0** |

**3xlite — Lite #2 final (8.4/10)**
Angle "charge cognitive + cycle de vie". Monolithe Modulaire comme destination finale (pas seulement étape). Matrice de décision organisationnelle (feature-oriented vs monolithe org). Mise en garde contre les *distributed monoliths*. ArchUnit pour enforcer les frontières.

| A | B | C | D | Moy |
|---|---|---|---|-----|
| 8 | 8.5 | 8.5 | 8.5 | **8.4** |

---

### Synthèse Série 2

| Test | default | 3xlite | Écart | Vainqueur |
|------|---------|--------|-------|-----------|
| T1 — NoSQL vs SQL | **8.25** | 7.5 | +0.75 | default |
| T2 — GIL Python | **8.75** | 8.25 | +0.5 | default |
| T3 — React/Vue | 7.9 | **8.6** | +0.7 | 3xlite |
| T4 — API REST | 7.6 | **8.75** | +1.15 | 3xlite |
| T5 — Microservices | **9.0** | 8.4 | +0.6 | default |
| **Moyenne** | **8.3** | **8.3** | 0 | ex aequo |

**Observations :**
- La boucle consensus fonctionne avec 3 agents identiques — convergence en 2 rounds sur les 5 tests
- **Comportement divergent** : Pro/Flash produit des réponses intégratives standalone ; Lite ×3 produit des réponses additives complémentaires (chaque instance ajoute un angle orthogonal plutôt que de retraiter le sujet)
- 3xlite excelle sur les angles "meta" (coût opérationnel, profil psychologique, patterns avancés) mais ne couvre pas les fondamentaux seul
- Sur les sujets de conseil/orientation (T3, T4), l'angle original de Lite vaut plus que la complétude cataloguée de Flash
- Sur les sujets encyclopédiques (T2 GIL, T5 Microservices), la profondeur intégrative du Pro fait la différence
- **Limite identifiée** : pas de phase de synthèse finale — Lite R2 ajoute sans consolider R1+R2 en une réponse unifiée

---

## Analyse coût : default vs 3xlite

### Prix Vertex AI confirmés (2026-03-18)

| Modèle | Input $/M tokens | Output $/M tokens |
|---|---|---|
| gemini-2.5-pro | $1.25 | $10.00 |
| gemini-2.5-flash | $0.30 | $2.50 |
| gemini-3.1-flash-lite-preview | $0.25 | $1.50 |

Source : cloud.google.com/vertex-ai/generative-ai/pricing

### Structure des appels (depuis le code)

Par agent, par round actif, 3 appels séquentiels :

| Appel | Input estimé | Output estimé | Contenu input |
|---|---|---|---|
| `respond` | ~70 tokens | ~600 tokens | system + question (+ contexte R2) |
| `critique` | ~2 000 tokens | ~300 tokens | system + question + 3 réponses |
| `analyze` | ~4 700 tokens | ~85 tokens | system + question + réponses + toutes les critiques |
| **Total round actif** | **~6 770** | **~985** | |
| Total round éliminé (critique+analyze seulement) | ~6 700 | ~385 | |

> **Ces chiffres sont des estimations** dérivées de la lecture du code (structure des prompts) — aucun comptage réel des tokens API n'a été effectué.

### Coût estimé par question (2 rounds, pattern d'élimination observé)

**Config default (Pro actif 2 rounds en moyenne, Flash idem, Lite éliminé R1) :**

| Agent | ~Input | ~Output | Coût |
|---|---|---|---|
| Pro (gagne 3/5 : actif 2 rounds) | ~10 500 | ~1 725 | **$0.030** |
| Flash (gagne 2/5 : actif 2 rounds) | ~10 400 | ~1 600 | **$0.007** |
| Lite (éliminé R1, critique+analyze R2) | ~10 100 | ~1 360 | **$0.005** |
| **Total default** | | | **~$0.042** |

**Config 3xlite (1 gagnant actif 2 rounds, 2 éliminés R1) :**

| Agent | ~Input | ~Output | Coût |
|---|---|---|---|
| Gagnant (actif 2 rounds) | ~10 800 | ~1 960 | $0.006 |
| Éliminé ×2 (R1 + critique R2) | ~10 100 ×2 | ~1 360 ×2 | $0.009 |
| **Total 3xlite** | | | **~$0.015** |

### Synthèse coût/qualité

| Config | Score moyen | Coût estimé / question | Ratio |
|---|---|---|---|
| default | 8.3/10 | ~$0.042 | 1× |
| 3xlite | 8.3/10 | ~$0.015 | **~2.8× moins cher** |

**La règle des 72% :** le Pro représente ~72% du coût default malgré des tokens identiques aux autres agents — uniquement dû à son prix output ($10/M vs $2.50 Flash, $1.50 Lite).

**Note importante :** `gemini-3.1-flash-lite-preview` n'est PAS "presque gratuit" — à $1.50/M output, il est seulement ~1.7× moins cher que Flash en output. Le mythe du "modèle lite = négligeable" ne tient pas ici. Les économies de 3xlite viennent quasi-exclusivement de la suppression du Pro, pas du prix du modèle Lite.

**Pour 1 000 questions :**
- default : ~$42
- 3xlite : ~$15

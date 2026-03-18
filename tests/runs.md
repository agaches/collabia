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

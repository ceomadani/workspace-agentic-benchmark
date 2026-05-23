# Lo stesso Claude, due risultati diversi: come misurare la vera leva del tuo agent

*Per anni abbiamo benchmarkato i modelli. Nessuno ha mai benchmarkato la stanza in cui lavorano. Eppure la stanza è la leva più grande che hai.*

---

## L'esperimento che ho ripetuto cento volte

Apri due cartelle sul tuo computer.

Nella prima cartella metti un README, due file di codice e un foglio di appunti. Niente di più. È la cartella di un progetto come ne hai visti mille.

Nella seconda cartella metti la stessa cosa, ma aggiungi: un file `CLAUDE.md` che spiega chi sei e come lavori, una cartella `skills/` con le tue procedure ricorrenti, una cartella `memory/` dove l'agent può salvare quello che impara, e un documento che chiamiamo "costituzione" — dieci regole che l'agent deve rispettare anche quando ha fretta.

Adesso apri Claude Code in entrambe le cartelle e dagli lo stesso compito: "scrivi un report di analisi finanziaria del nostro Q1 e mandalo via email al consulente".

Nella prima cartella otterrai qualcosa di plausibile. Un PDF generico, un'email "professionale" che non assomiglia a nulla che tu abbia mai mandato, e — se sei sfortunato — un click su "Invia" prima che tu abbia letto.

Nella seconda cartella otterrai un PDF con la tua estetica precisa, un'email che il consulente leggerà come se l'avessi scritta tu, e una pausa — perché la regola "non mandare nulla all'esterno senza approvazione" l'hai già scritta da qualche parte, e l'agent l'ha letta.

**Stesso modello. Stesso prompt. Risultati totalmente diversi.**

La differenza non è nel modello. È nella cartella.

---

## La leva di cui nessuno parla

Tutti misurano i modelli. C'è una classifica per ogni cosa: chi ragiona meglio, chi scrive codice migliore, chi capisce le immagini con più precisione. È giusto. I modelli contano.

Ma c'è una cosa che nessuno misura, ed è quella che produce il delta più grosso tra "agent inutile" e "agent che ti restituisce il pomeriggio".

Quella cosa è il **workspace**.

Workspace è una parola tecnica. Significa: la cartella in cui l'agent vive, più tutte le regole, le skills, la memoria, i tool e i documenti canonici che hai messo dentro. È il contesto strutturato.

E il modo migliore di pensarci è una formula molto semplice:

> **output = α(workspace) × capability(modello)**

Cosa fa l'agent dipende da due fattori che si moltiplicano: la sua capacità intrinseca (capability) e la qualità della stanza in cui lavora (α, alpha).

I modelli oggi sono già potentissimi. Stai pagando per Claude 4 o GPT-5 o Gemini 3, e ognuno di questi ha una capability molto alta. Ma se α è basso — se la cartella è vuota, le regole sono nella tua testa e la memoria è zero — moltiplichi un numero grande per un numero piccolo, e ottieni un numero piccolo.

Il punto è semplice e inverte le priorità di chi compra strumenti AI:

**il tuo prossimo upgrade non è cambiare modello. È costruire un workspace migliore.**

---

## Cosa rende un workspace "alto α"

Ho passato gli ultimi mesi a costruire e poi misurare workspace. Ne ho costruiti molti, perché gestisco un portfolio di aziende, e ogni azienda ha bisogno di un agent diverso per fare cose diverse. Setter, copywriter, analista finanziario, customer success — ognuno ha la sua stanza.

Dopo un po' è diventato chiaro che le stanze migliori hanno tutte la stessa struttura. Non gli stessi contenuti — i contenuti sono specifici. La stessa struttura.

Sono dodici dimensioni. Le ho raggruppate in quattro famiglie:

**Cognizione.** L'agent ha una memoria che attraversa le sessioni? Sa pianificare prima di agire, non solo reagire al singolo prompt? Quando un task è ambiguo, riesce a riconoscere che è ambiguo invece di tirare a indovinare?

**Azione.** L'agent ha accesso a tool concreti (API, browser, terminale) e sa quando usarli? Ha "skills" — procedure scritte che gli dicono "quando il task è X, segui questi passi"? Riesce a comporre più tool insieme per task complessi?

**Fiducia.** Quando l'agent sta per fare qualcosa di irreversibile — mandare un'email, chiudere un deal, modificare un database — c'è un cancello che ferma e chiede conferma? Ci sono regole hard che non può violare, anche se gliele chiedi gentilmente? Esiste un audit di cosa ha fatto?

**Operazioni.** Sai quanto ti costa al mese? Sai se sta sbagliando in modo silenzioso, o noti solo quando il cliente si lamenta? Quando aggiorni una skill, il vecchio comportamento sparisce, o resta come un fantasma a contaminare i nuovi task?

Queste sono le dodici dimensioni. Per ognuna ci sono cinque livelli di maturità, da L0 ("non esiste") a L4 ("autonomo e auto-migliorante"). E per ognuna c'è un test deterministico che misura dove sei.

Non è soggettivo. Non è un sondaggio. È una scansione automatica della tua cartella, che esce con un voto.

---

## Quello che esce dalla scansione

Ho aperto il tool su due workspace, uno dopo l'altro.

Il primo è il workspace Madani — la cartella in cui io lavoro quotidianamente, costruita negli ultimi sei mesi con centinaia di iterazioni, e dove dieci tra collaboratori e agenti vivono operativamente.

Voto: **A, 85.75 su 100**.

Il secondo è una cartella che ho creato in cinque minuti, con un README e due file dentro `/src` — quello che uno startup founder produrrebbe il primo giorno.

Voto: **F, 0 su 100**.

Lo so che sembra una forzatura. Ma il punto non è il numero. Il punto è cosa sta dentro al numero.

Nel report del workspace F ci sono ventitré anomalie. Per ognuna, il tool ti dice esattamente cosa manca e ti linka un articolo che spiega perché conta. Manca il pattern di governance multi-agent? C'è un paper di Stanford che spiega quando spawn-are sub-agent funziona e quando no. Manca la metrica di affidabilità? C'è un altro paper (MAST) che ti spiega come misurare pass@k sui task ripetuti.

Non è solo un voto. È **una mappa di cosa imparare per primo**.

---

## Perché ho aperto la fonte di tutto questo

Ho pubblicato la scansione, il codice e i criteri sotto licenza MIT. Si chiama `workspace-agentic-benchmark` ed è su GitHub.

L'ho aperto per tre motivi.

Primo: stiamo entrando nell'era in cui ogni piccola azienda avrà cinque, dieci, venti agenti che fanno cose. Senza un linguaggio comune per misurare la qualità dell'ambiente in cui lavorano, ogni team reinventerà gli stessi errori. È spreco.

Secondo: i benchmark dei modelli esistono perché Stanford, Anthropic, OpenAI hanno deciso che esistessero. Per gli agenti, l'infrastruttura di valutazione è ancora "missing" — c'è un paper recente di Princeton (Holistic Agent Leaderboard, ottobre 2026) che lo dice esplicitamente. Qualcuno deve iniziare. Tanto vale che sia pubblico, open, e con esempi reali.

Terzo: voglio essere giudicato dallo stesso metro. Il workspace Madani sta lì, scansionato pubblicamente, con voto A. È un'asticella, non una bandiera. Se qualcuno costruisce un workspace migliore, lo voglio sapere — perché lo voglio imparare.

---

## Cosa puoi fare adesso

Se hai un agent che usi quotidianamente — Claude Code, Cursor, qualunque cosa — e senti che a volte è geniale e a volte è inutile, prima di cambiare modello prova questo:

```
git clone https://github.com/ceomadani/workspace-agentic-benchmark
pip install -e .
workspace-bench run /path/al/tuo/workspace
```

In sessanta secondi ti esce un report HTML. Apri quel report. La prima cosa che vedi è l'albero della tua cartella — la conferma di cosa è stato misurato. La seconda cosa che vedi è il voto. La terza è la lista delle anomalie, ognuna con un link a un articolo che spiega come chiuderle.

Non è un servizio. Non è una vendita. È un punto di partenza.

E se il voto è basso, la buona notizia è questa: tutto quello che ti serve per alzarlo è scrivere dei file. Non hai bisogno di un nuovo modello. Non hai bisogno di un budget. Hai bisogno di smettere di tenere le regole nella tua testa e iniziare a scriverle dove l'agent le può leggere.

Quello è l'unico vero upgrade. Il resto è dettaglio.

---

**Link al benchmark:** [ceomadani.github.io/workspace-agentic-benchmark](https://ceomadani.github.io/workspace-agentic-benchmark/)
**Repo:** [github.com/ceomadani/workspace-agentic-benchmark](https://github.com/ceomadani/workspace-agentic-benchmark)
**Approfondimenti:** [madani.agency/it/research/articles](https://www.madani.agency/it/research/articles)

*— Nour Matine, Madani Lab*

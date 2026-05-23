# Cambiare modello non migliora il tuo agent. Quello che lo migliora è la stanza in cui vive.

*Stessa Claude. Due workspace. Voto 85.75 contro 0. Ho aperto il codice del benchmark che li separa.*

---

Cambiare modello non migliora il tuo agent.

Quello che lo migliora è la stanza in cui vive.

Su due workspace identici per modello e per prompt, ho misurato un delta di 85 punti su 100. E so esattamente da cosa viene.

---

## Il test che ho rifatto cento volte

Apri due cartelle sul tuo computer.

La prima contiene un README, due file di codice, un foglio di appunti. La cartella di un progetto qualunque, costruita in pomeriggio.

La seconda contiene la stessa cosa più: un documento `CLAUDE.md` che spiega chi sei e come lavori, una cartella `skills/` con le procedure ricorrenti, una cartella `memory/` dove l'agent salva quello che impara, una "costituzione" — dieci regole che l'agent non può violare neanche se gliele chiedi gentilmente.

Apri Claude Code in entrambe le cartelle. Dai lo stesso compito: scrivi un report finanziario del Q1 e mandalo via email al consulente.

Nella prima cartella ottieni un PDF generico, un'email "professionale" che non assomiglia a niente che tu abbia mai scritto, e — se sei sfortunato — un click su "Invia" prima che tu legga.

Nella seconda cartella ottieni un PDF con la tua estetica precisa, un'email che il consulente leggerà come tua, e una pausa — perché la regola "niente invii esterni senza approvazione" l'avevi già scritta da qualche parte, e l'agent l'ha letta.

Stesso modello. Stesso prompt. Risultati totalmente diversi.

La differenza non è la cartella. È la *struttura* dentro la cartella.

## La leva di cui nessuno parla

Chiunque ti parli del tuo prossimo upgrade ti vende un modello.

C'è una classifica per ogni cosa: chi ragiona meglio, chi scrive codice migliore, chi capisce le immagini con più precisione. Sono classifiche giuste. I modelli contano.

Ma c'è una cosa che nessuno misura, ed è quella che produce il delta più grosso tra "agent inutile" e "agent che ti restituisce il pomeriggio". Quella cosa è il **workspace**.

Workspace è una parola tecnica. Significa: la cartella in cui l'agent vive, più tutte le regole, le skill, la memoria, i tool e i documenti canonici che hai messo dentro. È il **contesto strutturato**.

Il modo più onesto di pensarci è una formula:

> **output = α(workspace) × capability(modello)**

Quello che ottieni è il prodotto di due fattori. La capability (il modello) e α (il workspace). I modelli oggi sono già potentissimi — capability molto alta. Ma se α è basso, moltiplichi un numero grande per un piccolo, e ottieni un numero piccolo.

Il prossimo upgrade non è cambiare modello. È alzare α.

## Cosa significa "alzare α"

Ho passato gli ultimi mesi a costruire workspace per un portfolio di aziende. Setter, copywriter, analista finanziario, customer success — ognuno con la sua stanza.

Dopo qualche mese è diventato chiaro che le stanze che funzionavano avevano tutte la stessa **struttura**. Non gli stessi contenuti — i contenuti sono specifici per il dominio. La stessa struttura.

Dodici dimensioni, raggruppate in quattro famiglie. Le elenco come le spiegherei a un amico al bar.

**Cognizione.** L'agent ha una memoria che attraversa le sessioni? Sa pianificare prima di agire o reagisce solo al singolo prompt? Quando il task è ambiguo, riconosce l'ambiguità invece di tirare a indovinare?

**Azione.** L'agent ha accesso a tool concreti (API, browser, terminale) e sa quando usarli? Ha skill scritte — procedure che dicono "quando il task è X, segui questi passi"? Riesce a comporre più tool insieme per task complessi?

**Fiducia.** Quando l'agent sta per fare qualcosa di irreversibile — un'email, un payment, una modifica al database — c'è un cancello che ferma e chiede conferma? Ci sono regole hard che non può violare? Esiste un audit di cosa ha fatto e quando?

**Operazioni.** Sai quanto ti costa al mese? Noti gli errori silenziosi o vedi solo quando il cliente si lamenta? Quando aggiorni una skill, il vecchio comportamento sparisce o resta come un fantasma?

Dodici dimensioni. Per ognuna cinque livelli di maturità — da L0 ("non esiste") a L4 ("autonomo e auto-migliorante"). Per ognuna un test deterministico che ti dice dove sei.

Non è soggettivo. Non è un sondaggio. È una scansione automatica della tua cartella che esce con un voto e una lista di cose mancanti.

## I numeri che ho misurato

Stesso modello, due workspace, una scansione.

Il **workspace Madani** — la cartella in cui lavoro tutti i giorni, costruita negli ultimi sei mesi attraverso centinaia di iterazioni, dove vivono dieci tra collaboratori e agent — ha preso **85.75 su 100, grade A, zero anomalie**.

Una **cartella naive** — README, due file in `/src`, niente di più, quella che uno startup founder produrrebbe il primo giorno — ha preso **0 su 100, grade F, 23 anomalie**.

Lo so che sembra estremo. Il punto non è il delta. Il punto è cosa c'è dentro il delta.

Nel report del workspace F, per ognuna delle 23 anomalie il tool ti dice cosa manca e ti linka un articolo che spiega perché conta. Manca la disciplina multi-agent? C'è un paper di Stanford che spiega quando spawnare sub-agent è una buona idea e quando no. Manca la metrica di affidabilità? C'è un altro paper (MAST · Princeton, ottobre 2026) che ti insegna come misurare pass@k. Manca la memoria? C'è un articolo che spiega le quattro categorie di memoria semantica per agenti.

Non è solo un voto. È una **mappa di cosa imparare per primo**.

## Perché l'ho reso pubblico

Tutto questo è MIT licensed e su GitHub. Lo trovi sotto il nome `workspace-agentic-benchmark`.

L'ho aperto per tre motivi.

Stiamo entrando nell'era in cui ogni piccola azienda avrà cinque, dieci, venti agent che fanno cose. Senza un linguaggio comune per misurare la qualità dell'ambiente in cui lavorano, ogni team reinventerà gli stessi errori. È spreco.

I benchmark dei modelli esistono perché Stanford, Anthropic, OpenAI hanno deciso che esistessero. Per il lato workspace l'infrastruttura di valutazione è ancora missing — c'è un paper di Princeton del 2026 (Holistic Agent Leaderboard) che lo dice esplicitamente. Qualcuno deve cominciare. Tanto vale che sia pubblico, open, e con esempi reali.

Voglio essere giudicato dallo stesso metro. Il workspace Madani sta lì, scansionato pubblicamente, con voto A. È un'asticella, non una bandiera. Se qualcuno costruisce un workspace migliore, lo voglio sapere — perché lo voglio imparare.

## Sessanta secondi per scoprire dove sei

Se mi dessi sessanta secondi sul tuo workspace, ecco quello che ti farei vedere.

```
git clone https://github.com/ceomadani/workspace-agentic-benchmark
pip install -e .
workspace-bench run /path/al/tuo/workspace
```

Esce un report HTML. La prima cosa che vedi è l'albero della tua cartella — la conferma di cosa è stato misurato. La seconda è il voto composito. La terza è la lista delle anomalie, ognuna con un link diretto a un articolo della ricerca che spiega come chiuderle.

Non è un servizio. Non è una vendita. È un punto di partenza.

Se il voto è basso, la notizia buona è questa: tutto quello che ti serve per alzarlo è **scrivere file**. Non hai bisogno di un modello migliore. Non hai bisogno di un budget. Hai bisogno di smettere di tenere le regole nella tua testa e iniziare a scriverle dove l'agent le può leggere.

Quello è l'unico upgrade vero. Il resto è dettaglio.

---

**Benchmark live**: [ceomadani.github.io/workspace-agentic-benchmark](https://ceomadani.github.io/workspace-agentic-benchmark/)
**Repo**: [github.com/ceomadani/workspace-agentic-benchmark](https://github.com/ceomadani/workspace-agentic-benchmark)
**Ricerca**: [madani.agency/it/research/articles](https://www.madani.agency/it/research/articles)

*— Nour Matine, Madani Lab*

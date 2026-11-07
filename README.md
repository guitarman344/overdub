# Overdub

Piccola app per Mac che aiuta a registrare la voce fuori campo dei video per YouTube, TikTok e Instagram.
Gira nel browser su `localhost`, legge il copione scena per scena e registra ogni scena in un file WAV a parte,
direttamente dalla tua scheda audio.

## Cosa fa

- **Un video = una cartella.** Ogni sottocartella della cartella dei video è un progetto, con il suo
  `copione.txt` e le registrazioni in `voce/scena-N.wav`.
- **Copione**: scrivi o incolli il testo; ogni paragrafo, separato da una riga vuota, è una scena.
- **Teleprompter e registrazione**: il testo della scena compare grande; <kbd>Spazio</kbd> avvia e ferma,
  <kbd>←</kbd> <kbd>→</kbd> cambiano scena, puoi riascoltare e rifare ogni scena.
- **Funziona con qualsiasi microfono**, con due modalità scelte in automatico in base all'ingresso:
  - *Scheda audio o microfono esterno* (Focusrite, microfono USB…): segnale pulito, senza elaborazioni del browser,
    con la scelta del canale (ingresso 1, ingresso 2 o entrambi);
  - *Microfono del computer, cuffie o AirPods*: riduzione del rumore e volume automatico del browser,
    così anche senza scheda audio la voce esce chiara e a un volume giusto.
  Puoi cambiare modalità a mano: la scelta viene ricordata per ogni ingresso.
- **Niente salti**: la registrazione gira in un AudioWorklet (thread audio dedicato), alla frequenza nativa
  dell'ingresso, quindi non perde campioni anche se la pagina rallenta.
- **Controllo del livello**: misuratore in tempo reale e avviso se una scena è troppo bassa o satura.
- Ricorda l'ultimo video, la scena e l'ingresso usati, e non seleziona mai ingressi virtuali (BlackHole, Teams…).

## Requisiti

- macOS con Python 3 (quello di sistema va bene, nessuna libreria da installare)
- Google Chrome

## Avvio

1. Scarica o clona il repository.
2. Fai doppio clic su **`Overdub.command`**: avvia il server, se non è già acceso, e apre `http://localhost:8765` in Chrome.
   La prima volta macOS potrebbe chiederti di confermare l'apertura.
3. In Chrome premi **Attiva microfono** e consenti l'accesso.

Da terminale:

```bash
python3 server.py "/percorso/della/cartella/video"
```

Senza argomenti usa `~/Documents/Video Youtube - Tiktok`, oppure la variabile d'ambiente `REGIA_VIDEOS`.

### Collegamento facoltativo

Se crei un file `config.json` accanto a `server.py` con

```json
{"uploadPage": "https://indirizzo-della-tua-pagina"}
```

nella barra laterale compare un pulsante che apre quella pagina, per esempio quella dove prepari titoli e descrizioni.

## Pagina compagna: Regia Upload

`regia-upload.html` è una pagina per preparare la pubblicazione su **YouTube, YouTube Shorts, TikTok e Instagram Reels**:

- Claude genera titolo, descrizione, tag e didascalie con hashtag, a partire da una breve descrizione del video;
- contatore dei caratteri per i limiti di ogni piattaforma e pulsanti per copiare;
- checklist di pubblicazione per ogni piattaforma e formati consigliati;
- storico privato dei video, con lo stato bozza o pubblicato e il link.

È pensata per essere pubblicata come **artifact su claude.ai**: la generazione dei testi e lo storico usano le funzioni
di claude.ai (`window.claude`). Aperta altrove, funzionano solo i testi scritti a mano, la checklist e i link.
Il pulsante "Registra la voce" apre Overdub su `localhost:8765`.

## Consigli per la voce

**Senza scheda audio** (microfono del Mac, AirPods, cuffie):
- registra in una stanza piccola e arredata: tende, divano e libri riducono il rimbombo;
- tieni il microfono a 20-30 cm dalla bocca, sempre alla stessa distanza;
- con le cuffie, evita che il microfono strusci sui vestiti;
- spegni ventilatori, condizionatore e notifiche.

**Con una scheda audio:**
- impostala a **48 kHz**, lo standard per i video (per esempio su Focusrite: Focusrite Control 2 → impostazioni → Sample Rate);
- regola il gain in modo che i picchi arrivino intorno a -10 / -6 dB.

## Privacy

Tutto resta sul tuo Mac: il server ascolta solo su `127.0.0.1` e salva i file nella cartella dei video.

## Licenza

[MIT](LICENSE)

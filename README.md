# Overdub

Piccola app per Mac che aiuta a registrare la voce fuori campo dei video per YouTube e TikTok.
Gira nel browser su `localhost`, legge il copione scena per scena e registra ogni scena in un file WAV a parte,
direttamente dalla tua scheda audio.

## Cosa fa

- **Un video = una cartella.** Ogni sottocartella della cartella dei video è un progetto, con il suo
  `copione.txt` e le registrazioni in `voce/scena-N.wav`.
- **Copione**: scrivi o incolli il testo; ogni paragrafo, separato da una riga vuota, è una scena.
- **Teleprompter e registrazione**: il testo della scena compare grande; <kbd>Spazio</kbd> avvia e ferma,
  <kbd>←</kbd> <kbd>→</kbd> cambiano scena, puoi riascoltare e rifare ogni scena.
- **Qualità piena**: niente cancellazione dell'eco, riduzione del rumore o guadagno automatico del browser.
  La registrazione gira in un AudioWorklet (thread audio dedicato), alla frequenza nativa della scheda,
  quindi non ci sono salti anche se la pagina rallenta.
- **Controllo del livello**: misuratore in tempo reale, scelta dell'ingresso e del canale
  (ingresso 1, ingresso 2 o entrambi) e avviso se una scena è troppo bassa o satura.
- Ricorda l'ultimo video, la scena e l'ingresso usati.

Provata con una Focusrite Scarlett 2i2 4th Gen, ma funziona con qualsiasi ingresso audio.

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

## Consigli per la voce

- Imposta la scheda audio a **48 kHz**, lo standard per i video (su Focusrite: Focusrite Control 2 → impostazioni → Sample Rate).
- Regola il gain in modo che i picchi arrivino intorno a -10 / -6 dB.

## Privacy

Tutto resta sul tuo Mac: il server ascolta solo su `127.0.0.1` e salva i file nella cartella dei video.

## Licenza

[MIT](LICENSE)

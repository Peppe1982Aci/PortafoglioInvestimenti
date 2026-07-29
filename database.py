import sqlite3
from pathlib import Path
from services.quotes import QuoteService

# ==========================================================
# DATABASE
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent

DATABASE = BASE_DIR / "portafoglio.db"

quote_service = QuoteService()


# ==========================================================
# CONNESSIONE
# ==========================================================

def get_connection():

    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row

    return conn


# ==========================================================
# CREAZIONE DATABASE
# ==========================================================

def inizializza_database():

    conn = get_connection()

    cur = conn.cursor()

    # ------------------------------------------------------
    # STRUMENTI
    # ------------------------------------------------------

    cur.execute("""

    CREATE TABLE IF NOT EXISTS strumenti(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        ticker TEXT NOT NULL,

        nome TEXT,

        quantita REAL DEFAULT 0,

        prezzo_medio REAL DEFAULT 0,

        valuta TEXT DEFAULT 'EUR',

        settore TEXT,

        note TEXT

    )

    """)

    # ------------------------------------------------------
    # OPERAZIONI
    # ------------------------------------------------------

    cur.execute("""

    CREATE TABLE IF NOT EXISTS operazioni(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        data TEXT NOT NULL,

        ticker TEXT NOT NULL,

        tipo TEXT NOT NULL,

        quantita REAL,

        prezzo REAL,

        commissioni REAL DEFAULT 0,

        cambio REAL DEFAULT 1,

        note TEXT

    )

    """)

    # ------------------------------------------------------
    # DIVIDENDI
    # ------------------------------------------------------

    cur.execute("""

    CREATE TABLE IF NOT EXISTS dividendi(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        data TEXT,

        ticker TEXT,

        importo REAL,

        valuta TEXT,

        note TEXT

    )

    """)

    conn.commit()

    conn.close()


# ==========================================================
# LETTURA STRUMENTI
# ==========================================================

def leggi_strumenti():

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""

        SELECT *

        FROM strumenti

        ORDER BY ticker

    """)

    dati = cur.fetchall()

    conn.close()

    return dati


def leggi_strumento(id_strumento):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""

        SELECT *

        FROM strumenti

        WHERE id=?

    """, (id_strumento,))

    dato = cur.fetchone()

    conn.close()

    return dato
# ==========================================================
# INSERIMENTO STRUMENTI
# ==========================================================

def aggiungi_strumento(
    ticker,
    nome,
    quantita,
    prezzo,
    valuta="EUR",
    settore="",
    note=""
):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""

        INSERT INTO strumenti(

            ticker,

            nome,

            quantita,

            prezzo_medio,

            valuta,

            settore,

            note

        )

        VALUES (?, ?, ?, ?, ?, ?, ?)

    """, (

        ticker.upper(),

        nome,

        float(quantita),

        float(prezzo),

        valuta,

        settore,

        note

    ))

    conn.commit()

    conn.close()


# ==========================================================
# MODIFICA STRUMENTI
# ==========================================================

def modifica_strumento(
    id_strumento,
    ticker,
    nome,
    quantita,
    prezzo,
    valuta="EUR",
    settore="",
    note=""
):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""

        UPDATE strumenti

        SET

            ticker=?,

            nome=?,

            quantita=?,

            prezzo_medio=?,

            valuta=?,

            settore=?,

            note=?

        WHERE id=?

    """, (

        ticker.upper(),

        nome,

        float(quantita),

        float(prezzo),

        valuta,

        settore,

        note,

        id_strumento

    ))

    conn.commit()

    conn.close()


# ==========================================================
# ELIMINAZIONE STRUMENTI
# ==========================================================

def elimina_strumento(id_strumento):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(

        "DELETE FROM strumenti WHERE id=?",

        (id_strumento,)

    )

    conn.commit()

    conn.close()


# ==========================================================
# RICERCA STRUMENTI
# ==========================================================

def cerca_strumenti(testo):

    conn = get_connection()

    cur = conn.cursor()

    testo = f"%{testo.upper()}%"

    cur.execute("""

        SELECT *

        FROM strumenti

        WHERE

            UPPER(ticker) LIKE ?

            OR UPPER(nome) LIKE ?

            OR UPPER(settore) LIKE ?

        ORDER BY ticker

    """, (

        testo,

        testo,

        testo

    ))

    dati = cur.fetchall()

    conn.close()

    return dati
# ==========================================================
# OPERAZIONI
# ==========================================================

def leggi_operazioni():

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""

        SELECT *

        FROM operazioni

        ORDER BY data DESC,id DESC

    """)

    dati = cur.fetchall()

    conn.close()

    return dati


def leggi_operazione(id_operazione):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""

        SELECT *

        FROM operazioni

        WHERE id=?

    """, (id_operazione,))

    dato = cur.fetchone()

    conn.close()

    return dato


# ==========================================================
# INSERIMENTO OPERAZIONE
# ==========================================================

def aggiungi_operazione(
    data,
    ticker,
    tipo,
    quantita,
    prezzo,
    commissioni=0,
    cambio=1,
    note=""
):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""

        INSERT INTO operazioni(

            data,

            ticker,

            tipo,

            quantita,

            prezzo,

            commissioni,

            cambio,

            note

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?)

    """, (

        data,

        ticker.upper(),

        tipo,

        float(quantita),

        float(prezzo),

        float(commissioni),

        float(cambio),

        note

    ))

    conn.commit()

    conn.close()


# ==========================================================
# MODIFICA OPERAZIONE
# ==========================================================

def modifica_operazione(
    id_operazione,
    data,
    ticker,
    tipo,
    quantita,
    prezzo,
    commissioni=0,
    cambio=1,
    note=""
):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""

        UPDATE operazioni

        SET

            data=?,

            ticker=?,

            tipo=?,

            quantita=?,

            prezzo=?,

            commissioni=?,

            cambio=?,

            note=?

        WHERE id=?

    """, (

        data,

        ticker.upper(),

        tipo,

        float(quantita),

        float(prezzo),

        float(commissioni),

        float(cambio),

        note,

        id_operazione

    ))

    conn.commit()

    conn.close()
# ==========================================================
# ELIMINAZIONE OPERAZIONE
# ==========================================================

def elimina_operazione(id_operazione):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(

        "DELETE FROM operazioni WHERE id=?",

        (id_operazione,)

    )

    conn.commit()

    conn.close()


# ==========================================================
# RICERCA OPERAZIONI
# ==========================================================

def cerca_operazioni(testo):

    conn = get_connection()

    cur = conn.cursor()

    testo = f"%{testo.upper()}%"

    cur.execute("""

        SELECT *

        FROM operazioni

        WHERE

            UPPER(ticker) LIKE ?

            OR UPPER(tipo) LIKE ?

            OR UPPER(note) LIKE ?

        ORDER BY data DESC,id DESC

    """, (

        testo,

        testo,

        testo

    ))

    dati = cur.fetchall()

    conn.close()

    return dati


# ==========================================================
# STATISTICHE
# ==========================================================

def numero_strumenti():

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""

        SELECT COUNT(*)

        FROM strumenti

    """)

    valore = cur.fetchone()[0]

    conn.close()

    return valore


def numero_operazioni():

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""

        SELECT COUNT(*)

        FROM operazioni

    """)

    valore = cur.fetchone()[0]

    conn.close()

    return valore


def valore_portafoglio():

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""

        SELECT SUM(

            quantita * prezzo_medio

        )

        FROM strumenti

    """)

    valore = cur.fetchone()[0]

    conn.close()

    return float(valore) if valore else 0.0


def capitale_investito():

    return valore_portafoglio()


def totale_commissioni():

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""

        SELECT SUM(commissioni)

        FROM operazioni

    """)

    valore = cur.fetchone()[0]

    conn.close()

    return float(valore) if valore else 0.0
# ==========================================================
# CALCOLO QUANTITA'
# ==========================================================

def quantita_ticker(ticker):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""

        SELECT

            SUM(

                CASE

                    WHEN tipo='Acquisto'

                    THEN quantita

                    ELSE -quantita

                END

            )

        FROM operazioni

        WHERE UPPER(ticker)=?

    """, (ticker.upper(),))

    valore = cur.fetchone()[0]

    conn.close()

    return float(valore) if valore else 0.0


# ==========================================================
# PREZZO MEDIO
# ==========================================================

def prezzo_medio_ticker(ticker):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""

        SELECT

            quantita,

            prezzo

        FROM operazioni

        WHERE

            UPPER(ticker)=?

            AND tipo='Acquisto'

        ORDER BY data,id

    """, (ticker.upper(),))

    operazioni = cur.fetchall()

    conn.close()

    totale_quantita = 0.0

    totale_importo = 0.0

    for op in operazioni:

        totale_quantita += float(op["quantita"])

        totale_importo += (

            float(op["quantita"])

            * float(op["prezzo"])

        )

    if totale_quantita == 0:

        return 0.0

    return totale_importo / totale_quantita


# ==========================================================
# AGGIORNAMENTO PORTAFOGLIO
# ==========================================================

def aggiorna_portafoglio():

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("DELETE FROM strumenti")

    cur.execute("""

        SELECT DISTINCT ticker

        FROM operazioni

        ORDER BY ticker

    """)

    ticker_list = cur.fetchall()

    for riga in ticker_list:

        ticker = riga["ticker"]

        quantita = quantita_ticker(ticker)

        if quantita <= 0:

            continue

        prezzo = prezzo_medio_ticker(ticker)

        cur.execute("""

            INSERT INTO strumenti(

                ticker,

                nome,

                quantita,

                prezzo_medio,

                valuta,

                settore,

                note

            )

            VALUES (?, ?, ?, ?, ?, ?, ?)

        """, (

            ticker,

            ticker,

            quantita,

            prezzo,

            "EUR",

            "",

            ""

        ))

    conn.commit()

    conn.close()

# ==========================================================
# QUOTAZIONI
# ==========================================================

def quotazione_corrente(ticker):
    return quote_service.get_quote(ticker)

def prezzo_corrente(ticker):
    return quotazione_corrente(ticker).price

def variazione_corrente(ticker):
    return quotazione_corrente(ticker).variation

def aggiorna_quotazioni():
    strumenti = leggi_strumenti()
    risultato = {}
    for s in strumenti:
        risultato[s["ticker"]] = quote_service.refresh_quote(s["ticker"])
    return risultato

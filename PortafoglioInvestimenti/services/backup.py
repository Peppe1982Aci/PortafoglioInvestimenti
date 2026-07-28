from pathlib import Path
from datetime import datetime
import shutil


# =====================================================
# CARTELLE
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

BACKUP_DIR = BASE_DIR / "backup"

DATABASE_FILE = DATA_DIR / "portfolio.db"


# =====================================================
# CREAZIONE CARTELLE
# =====================================================

def inizializza_backup():

    DATA_DIR.mkdir(exist_ok=True)

    BACKUP_DIR.mkdir(exist_ok=True)


# =====================================================
# CREA BACKUP
# =====================================================

def crea_backup():

    inizializza_backup()

    if not DATABASE_FILE.exists():
        raise FileNotFoundError(
            "Database non trovato."
        )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    destinazione = BACKUP_DIR / (
        f"portfolio_{timestamp}.db"
    )

    shutil.copy2(
        DATABASE_FILE,
        destinazione
    )

    return destinazione


# =====================================================
# RIPRISTINO BACKUP
# =====================================================

def ripristina_backup(file_backup):

    inizializza_backup()

    file_backup = Path(file_backup)

    if not file_backup.exists():
        raise FileNotFoundError(
            "File di backup inesistente."
        )

    shutil.copy2(
        file_backup,
        DATABASE_FILE
    )


# =====================================================
# ELENCO BACKUP
# =====================================================

def elenco_backup():

    inizializza_backup()

    files = list(
        BACKUP_DIR.glob("*.db")
    )

    files.sort(
        key=lambda x: x.stat().st_mtime,
        reverse=True
    )

    return files


# =====================================================
# ELIMINA BACKUP
# =====================================================

def elimina_backup(file_backup):

    file_backup = Path(file_backup)

    if file_backup.exists():
        file_backup.unlink()


# =====================================================
# PULIZIA AUTOMATICA
# Mantiene gli ultimi N backup
# =====================================================

def pulizia_backup(max_backup=20):

    backups = elenco_backup()

    if len(backups) <= max_backup:
        return

    for file in backups[max_backup:]:
        try:
            file.unlink()
        except Exception:
            pass


# =====================================================
# BACKUP AUTOMATICO
# =====================================================

def backup_automatico():

    file = crea_backup()

    pulizia_backup()

    return file


# =====================================================
# INFORMAZIONI BACKUP
# =====================================================

def informazioni_backup(file_backup):

    file_backup = Path(file_backup)

    if not file_backup.exists():
        return None

    stat = file_backup.stat()

    return {

        "nome": file_backup.name,

        "percorso": str(file_backup),

        "dimensione": stat.st_size,

        "data": datetime.fromtimestamp(
            stat.st_mtime
        )

    }
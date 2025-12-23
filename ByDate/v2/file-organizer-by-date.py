import os
import shutil
import time
from datetime import datetime
from pathlib import Path
from collections import Counter

from PIL import Image
import piexif
from pymediainfo import MediaInfo


# ---------- EXTRATORES DE DATA ----------

class ImageDateExtractor:
    def __init__(self, image_path: str):
        self.image_path = image_path

    def get_date(self) -> datetime:
        try:
            img = Image.open(self.image_path)

            if "exif" in img.info:
                exif_data = piexif.load(img.info["exif"])

                def get_exif(tag):
                    for ifd in ("Exif", "0th"):
                        if tag in exif_data.get(ifd, {}):
                            value = exif_data[ifd][tag]
                            return datetime.strptime(
                                value.decode(), "%Y:%m:%d %H:%M:%S"
                            )
        except Exception:
            pass

        for tag in (
            piexif.ExifIFD.DateTimeOriginal,
            piexif.ExifIFD.DateTimeDigitized,
            piexif.ImageIFD.DateTime,
        ):
            try:
                date = get_exif(tag)
                if date:
                    return date
            except Exception:
                continue

        return datetime.fromtimestamp(os.path.getmtime(self.image_path))


class VideoDateExtractor:
    def __init__(self, video_path: str):
        self.video_path = video_path

    def get_date(self) -> datetime:
        try:
            media_info = MediaInfo.parse(self.video_path)

            for track in media_info.tracks:
                if track.track_type == "General":
                    candidates = (
                        track.other_creation_time,
                        track.tagged_date,
                        track.encoded_date,
                        track.com_encoded_date,
                    )

                    for value in candidates:
                        if value:
                            return self._parse_date(value)
        except Exception:
            pass

        return datetime.fromtimestamp(os.path.getmtime(self.video_path))

    def _parse_date(self, value) -> datetime:
        if isinstance(value, list):
            value = value[0]

        value = value.replace("UTC", "").strip()
        return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")


# ---------- CONTADOR DE EXTENSÕES ----------

def contar_extensoes(diretorio: str, recursivo: bool = True):
    path = Path(diretorio)
    contador = Counter()

    arquivos = path.rglob("*") if recursivo else path.glob("*")

    for arquivo in arquivos:
        if arquivo.is_file():
            ext = arquivo.suffix.lower() or "(sem extensão)"
            contador[ext] += 1

    return contador


# ---------- AJUSTE DE DATA DE MODIFICAÇÃO ----------

def ajustar_data_modificacao(path: str, date: datetime):
    timestamp = date.timestamp()
    os.utime(path, (timestamp, timestamp))


# ---------- ORGANIZADOR ----------

class FileOrganizer:
    def __init__(self, destination=None):
        self.destination = destination or os.path.join(os.getcwd(), "organized")
        self.outras_ext = os.path.join(self.destination, "outras_extensoes")

    def folder_from_date(self, date: datetime):
        return os.path.join(
            self.destination,
            date.strftime("%Y"),
            date.strftime("%Y-%m")
        )

    def organize(self):
        print("\n📊 Contagem de extensões:\n")
        contador = contar_extensoes(".")
        total = sum(contador.values())

        for ext, qtd in contador.most_common():
            print(f"{qtd:>5}  {ext}")

        print(f"\nTotal de arquivos: {total}")
        confirm = input("\nDeseja continuar? (s/n): ").lower()

        if confirm != "s":
            print("Operação cancelada.")
            return

        processados = 0
        copiados = 0

        for root, dirnames, filenames in os.walk("."):
            # evita reprocessar destino
            dirnames[:] = [
                d for d in dirnames
                if d not in ("organized", "outras_extensoes")
                and not (d.isdigit() and len(d) == 4)
                and not (len(d) == 7 and d[4] == "-")
            ]

            for name in filenames:
                file_path = os.path.join(root, name)
                ext = os.path.splitext(name)[1].lower()

                date = None
                
                # JPG / JPEG
                if ext in (".jpg", ".jpeg"):
                    date = ImageDateExtractor(file_path).get_date()
                    target_dir = self.folder_from_date(date)

                # MP4
                elif ext == ".mp4":
                    date = VideoDateExtractor(file_path).get_date()
                    target_dir = self.folder_from_date(date)

                # OUTRAS EXTENSÕES
                else:
                    target_dir = self.outras_ext

                os.makedirs(target_dir, exist_ok=True)
                target_path = os.path.join(target_dir, name)

                if not os.path.exists(target_path):
                    shutil.copy2(file_path, target_path)
                    if date:
                        ajustar_data_modificacao(target_path, date)
                    copiados += 1

                processados += 1
                restantes = total - processados
                percent = (processados / total) * 100

                print(
                    f"\rProcessados: {processados}/{total} "
                    f"({percent:5.1f}%) | "
                    f"Copiados: {copiados} | "
                    f"Restantes: {restantes}",
                    end="",
                    flush=True
                )

        print("\n\nOrganização concluída.")
        print("O terminal será fechado em 60 segundos...")
        time.sleep(60)


# ---------- EXECUÇÃO ----------

dest = input("Informe o diretório de destino (enter para usar ./organized): ").strip()
organizer = FileOrganizer(dest or None)
organizer.organize()

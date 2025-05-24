import piexif
from PIL import Image

def extract_metadata(image_path):
    try:
        img = Image.open(image_path)
        exif_dict = piexif.load(img.info.get("exif", b""))
        
        if not exif_dict:
            print("Žádná EXIF metadata nebyla nalezena.")
            return
        
        print(f"\nMetadata z obrázku: {image_path}\n")
        
        for ifd_name in exif_dict:
            print(f"--- {ifd_name} ---")
            for tag_id, value in exif_dict[ifd_name].items():
                tag_name = piexif.TAGS[ifd_name].get(tag_id, {"name": tag_id})["name"]
                print(f"{tag_name}: {value}")
            print()
    
    except FileNotFoundError:
        print("Soubor nebyl nalezen. Zkontroluj cestu.")
    except Exception as e:
        print(f"Nastala chyba: {e}")

if __name__ == "__main__":
    image_path = input("Zadej cestu k obrázku: ")
    extract_metadata(image_path)

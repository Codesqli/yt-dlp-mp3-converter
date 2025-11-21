import os
import re
import yt_dlp
from pytube import YouTube, exceptions as pytube_exceptions
from pydub import AudioSegment
import logging

OUTPUT_DIR = "Muzikler"
logging.getLogger('yt_dlp').setLevel(logging.ERROR)

def sanitize_filename(title: str) -> str:

    sanitized_title = re.sub(r'[\\/*?:"<>|]', "", title)
    return sanitized_title[:150].strip()

def create_output_directory():

    if not os.path.exists(OUTPUT_DIR):
        print(f"'{OUTPUT_DIR}' klasörü oluşturuluyor...")
        os.makedirs(OUTPUT_DIR)
        
def download_with_yt_dlp(url: str, output_path: str) -> bool:

    print(f"\n[Yöntem 1: yt-dlp] Deneniyor: {url}")
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192', 
            }],
            'noplaylist': True, 
            'quiet': True, 
            'no_warnings': True,
            'ffmpeg_location': r"....write here ur host info\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0-full_build\bin",
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_title = sanitize_filename(info_dict.get('title', 'isimsiz_video'))
            print(f"  -> İndiriliyor: '{video_title}'")
            
            final_filepath = os.path.join(output_path, f"{video_title}.mp3")
            if os.path.exists(final_filepath):
                print(f"  -> UYARI: '{video_title}.mp3' zaten mevcut. Atlanıyor.")
                return True

            ydl.download([url])
            print(f"  -> BAŞARILI: '{video_title}.mp3' dosyası kaydedildi.")
        return True
    except yt_dlp.utils.DownloadError as e:
        print(f"  -> HATA (yt-dlp): İndirme başarısız oldu. Sebep: {str(e)}")
        return False
    except Exception as e:
        print(f"  -> BEKLENMEDİK HATA (yt-dlp): {str(e)}")
        return False

def download_with_pytube(url: str, output_path: str) -> bool:

    print(f"\n[Yöntem 2: Pytube - Yedek] Deneniyor: {url}")
    try:
        yt = YouTube(url)
        video_title = sanitize_filename(yt.title)
        
        final_filepath = os.path.join(output_path, f"{video_title}.mp3")
        if os.path.exists(final_filepath):
            print(f"  -> UYARI: '{video_title}.mp3' zaten mevcut. Atlanıyor.")
            return True

        print(f"  -> İndiriliyor: '{video_title}'")
        
        audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
        if not audio_stream:
            print("  -> HATA: Bu video için uygun bir ses akışı bulunamadı.")
            return False
            
        temp_file = audio_stream.download(output_path=output_path, filename_prefix="temp_")
        
        print("  -> Dönüştürülüyor: MP3 formatına çevriliyor...")
        audio = AudioSegment.from_file(temp_file)
        audio.export(final_filepath, format="mp3", bitrate="192k")
        
        os.remove(temp_file)
        
        print(f"  -> BAŞARILI: '{video_title}.mp3' dosyası kaydedildi.")
        return True
    except pytube_exceptions.PytubeError as e:
        print(f"  -> HATA (pytube): Video bilgileri alınamadı veya indirilemedi. Sebep: {str(e)}")
        return False
    except Exception as e:
        print(f"  -> BEKLENMEDİK HATA (pytube): {str(e)}")
        return False


def main():
    print("--- YouTube Videolarını MP3 Olarak İndirme Script'i ---")
    print("Birden fazla URL girmek için aralarına virgül (,) koyun.")
    
    create_output_directory()
    
    urls_input = input("İndirmek istediğiniz YouTube video URL'lerini girin:\n> ")
    
    if not urls_input:
        print("Hiç URL girilmedi. Program sonlandırılıyor.")
        return
        
    urls = [url.strip() for url in urls_input.split(',') if url.strip()]
    
    print(f"\nToplam {len(urls)} adet video işlenecek...")
    
    successful_downloads = 0
    failed_downloads = 0
    
    for i, url in enumerate(urls):
        print("-" * 50)
        print(f"İşlem {i+1}/{len(urls)}")
        
        success = download_with_yt_dlp(url, OUTPUT_DIR)
        
        if not success:
            print("  -> Ana yöntem başarısız oldu. Yedek yöntem deneniyor...")
            success = download_with_pytube(url, OUTPUT_DIR)
        
        if success:
            successful_downloads += 1
        else:
            failed_downloads += 1
            print(f"\nUYARI: {url} adresi için iki yöntem de başarısız oldu. Bu URL atlanıyor.")
            
    print("-" * 50)
    print("\nTüm işlemler tamamlandı!")
    print(f"Başarılı: {successful_downloads}")
    print(f"Başarısız: {failed_downloads}")
    print(f"Tüm dosyalar '{OUTPUT_DIR}' klasörüne kaydedildi.")

if __name__ == "__main__":
    main()

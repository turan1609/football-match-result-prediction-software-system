import csv
from bs4 import BeautifulSoup
import requests

def mac_verileri():
    ligler = {
        "Bundesliga": "https://www.mackolik.com/kupa/almanya-bundesliga/{}/fikstur/6by3h89i2eykc341oz7lv1ddd",
        "Premier Lig": "https://www.mackolik.com/kupa/ingiltere-premier-lig/{}/fikstur/2kwbbcootiqqgmrzs6o5inle5",
        "Ligue 1": "https://www.mackolik.com/kupa/fransa-ligue-1/{}/fikstur/dm5ka0os1e3dxcp3vh05kmp33",
        "Serie A": "https://www.mackolik.com/kupa/italya-serie-a/{}/fikstur/1r097lpxe0xn03ihb7wi98kao",
        "La Liga": "https://www.mackolik.com/kupa/ispanya-laliga/{}/fikstur/34pl8szyvrbwcmfkuocjm3r6t",
        "Süper Lig": "https://www.mackolik.com/puan-durumu/t%C3%BCrkiye-trendyol-s%C3%BCper-lig/{}/fikstur/482ofyysbdbeoxauk19yg7tdt"
    }

    sezonlar = range(2000, 2001)

    for lig_adi, base_url in ligler.items():
        dosya_adi = f"mac_verileri_{lig_adi.replace(' ', '_').lower()}.csv"

        with open(dosya_adi, "w", newline='', encoding="utf-8") as csvfile:
            csvwriter = csv.writer(csvfile)
            # Başlıkları istediğiniz gibi düzenliyoruz
            csvwriter.writerow(["LeaugePlayed", "Season", "Date", "HomeTeam", "Score", "AwayTeam"])

            for sezon in sezonlar:
                url = base_url.format(f"{sezon}-{sezon+1}")
                print(f"Veri çekiliyor: {lig_adi} {sezon}-{sezon+1}")

                try:
                    r = requests.get(url)
                    if r.status_code != 200:
                        print(f"Sayfa yüklenemedi: {url} (Durum kodu: {r.status_code})")
                        continue

                    soup = BeautifulSoup(r.content, "lxml")

                    # Gün tarihlerini listele
                    gunler = soup.find_all("li", class_="p0c-competition-match-list__day")
                    if not gunler:
                        print(f"Maç günleri bulunamadı: {url}")
                        continue

                    for gun in gunler:
                        # Her gün için tarih alınır
                        tarih_span = gun.find("span", class_="p0c-competition-match-list__title-date")
                        if not tarih_span:
                            print("Tarih bilgisi eksik, devam ediliyor...")
                            continue

                        tarih_text = tarih_span.text.strip()

                        # Maç satırlarını listele
                        matches = gun.find_all("li", class_="p0c-competition-match-list__row")
                        if not matches:
                            print(f"Maç bilgisi bulunamadı: {url}")
                            continue

                        for match in matches:
                            # Ev sahibi takım adı
                            ev_sahibi_div = match.find("div", class_="p0c-competition-match-list__team--home")
                            ev_sahibi_span = ev_sahibi_div.find("span", class_="p0c-competition-match-list__team-full") if ev_sahibi_div else None
                            
                            # Deplasman takım adı
                            deplasman_div = match.find("div", class_="p0c-competition-match-list__team--away")
                            deplasman_span = deplasman_div.find("span", class_="p0c-competition-match-list__team-full") if deplasman_div else None

                            # Ev sahibi ve deplasman skorlarını al
                            ev_sahibi_skor = match.find("span", class_="p0c-competition-match-list__score", attrs={"data-slot": "score-home"})
                            deplasman_skor = match.find("span", class_="p0c-competition-match-list__score", attrs={"data-slot": "score-away"})

                            # Ev sahibi ve deplasman takım bilgileri eksiksizse, veriyi kaydet
                            if ev_sahibi_span and deplasman_span and ev_sahibi_skor and deplasman_skor:
                                ev_sahibi = ev_sahibi_span.text.strip()
                                deplasman = deplasman_span.text.strip()
                                ev_sahibi_sk = ev_sahibi_skor.text.strip()
                                deplasman_sk = deplasman_skor.text.strip()

                                # Skorları uygun şekilde formatla
                                csvwriter.writerow([lig_adi, f"{sezon}-{sezon+1}", f"{tarih_text}", ev_sahibi, ev_sahibi_sk + "-" + deplasman_sk, deplasman])
                            else:
                                print(f"Eksik veri atlandı: {lig_adi}, Tarih: {tarih_text}")
                except Exception as e:
                    print(f"Hata oluştu: {e}, URL: {url}")

    print("Veri çekme işlemi tamamlandı.")



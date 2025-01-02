import csv
from bs4 import BeautifulSoup
import requests

ligler = {
    "Premier Lig": "https://www.mackolik.com/kupa/ingiltere-premier-lig/{}/fikstur/2kwbbcootiqqgmrzs6o5inle5",
    "Ligue 1": "https://www.mackolik.com/kupa/fransa-ligue-1/{}/fikstur/dm5ka0os1e3dxcp3vh05kmp33",
    "Bundesliga": "https://www.mackolik.com/kupa/almanya-bundesliga/{}/fikstur/6by3h89i2eykc341oz7lv1ddd",
    "Serie A": "https://www.mackolik.com/kupa/italya-serie-a/{}/fikstur/1r097lpxe0xn03ihb7wi98kao",
    "La Liga": "https://www.mackolik.com/kupa/ispanya-laliga/{}/fikstur/34pl8szyvrbwcmfkuocjm3r6t",
    "Süper Lig": "https://www.mackolik.com/puan-durumu/t%C3%BCrkiye-trendyol-s%C3%BCper-lig/{}/fikstur/482ofyysbdbeoxauk19yg7tdt"
}

sezonlar = range(2000, 2024)

for lig_adi, base_url in ligler.items():
    dosya_adi = f"mac_verileri_{lig_adi.replace(' ', '_').lower()}.csv"

    with open(dosya_adi, "w", newline='', encoding="utf-8") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([lig_adi])
        csvwriter.writerow(["Sezon", "Tarih", "Ev Sahibi", "Skor", "Deplasman"])

        for sezon in sezonlar:
            url = base_url.format(f"{sezon}-{sezon+1}")
            print(f"Veri çekiliyor: {lig_adi} {sezon}-{sezon+1}")

            try:
                r = requests.get(url)
                if r.status_code != 200:
                    print(f"Sayfa yüklenemedi: {url} (Durum kodu: {r.status_code})")
                    continue

                soup = BeautifulSoup(r.content, "lxml")
                table = soup.find("div", attrs={"class": "p0c-competition-match-list"})

                if table:
                    rows = table.find_all("ol", attrs={"class": "p0c-competition-match-list__days"})
                    if not rows:
                        print(f"Satır bilgisi bulunamadı: {url}")
                        continue

                    for row in rows:
                        matches = row.find_all("li", attrs={"class": "p0c-competition-match-list__day"})
                        if not matches:
                            print(f"Maç bilgisi bulunamadı: {url}")
                            continue

                        for match in matches:
                            tarih_span = match.find("span", class_="p0c-competition-match-list__title-date")
                            ev_sahibi_div = match.find("div", class_="p0c-competition-match-list__team p0c-competition-match-list__team--home")
                            deplasman_div = match.find("div", class_="p0c-competition-match-list__team p0c-competition-match-list__team--away")
                            skor_span = match.find("span", class_="p0c-competition-match-list__score")

                            if tarih_span and ev_sahibi_div and deplasman_div:
                                tarih = tarih_span.text.strip()
                                ev_sahibi = ev_sahibi_div.text.strip()
                                deplasman = deplasman_div.text.strip()

                               
                                ev_sahibi_name = ''.join([ch for ch in ev_sahibi if not ch.isdigit()]).strip()

                                
                                deplasman_name = ''.join([ch for ch in deplasman if not ch.isdigit()]).strip()

                               
                                if skor_span:
                                    skor_parts = skor_span.text.strip().split("-")
                                    if len(skor_parts) == 2:
                                        skor = f"{skor_parts[0]}-{skor_parts[1]}"
                                    else:
                                        skor = "-"
                                else:
                                    skor = "-"

                                
                                ev_sahibi_skor = ''.join([ch for ch in ev_sahibi if ch.isdigit()])
                                deplasman_skor = ''.join([ch for ch in deplasman if ch.isdigit()])

                                
                                csvwriter.writerow([f"{sezon}-{sezon+1}", tarih, ev_sahibi_name, f"{ev_sahibi_skor}-{deplasman_skor}", deplasman_name])

                            else:
                                print(f"Veri eksik, atlanıyor: {url}")
                else:
                    print(f"Tablo bulunamadı: {url}")
            except Exception as e:
                print(f"Hata oluştu: {e}, URL: {url}")

print("Veri çekme işlemi tamamlandı.")

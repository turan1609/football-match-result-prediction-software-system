import csv
from bs4 import BeautifulSoup
import requests

sezonlar = range(2000, 2024)  

base_url = "https://www.mackolik.com/puan-durumu/t%C3%BCrkiye-trendyol-s%C3%BCper-lig/{}/fikstur/482ofyysbdbeoxauk19yg7tdt"

with open("mac_verileri.csv", "w", newline='', encoding="utf-8") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["Süper Lig"])
    csvwriter.writerow(["Sezon", "Tarih", "Ev Sahibi", "Skor", "Deplasman"])
    
    for sezon in sezonlar:
        url = base_url.format(f"{sezon}-{sezon+1}")
        print(f"Veri çekiliyor: {sezon}-{sezon+1}")
        
        r = requests.get(url)
        
        if r.status_code != 200:
            print(f"Sayfa yüklenemedi: {url} (Durum kodu: {r.status_code})")
            continue
        
        soup = BeautifulSoup(r.content, "lxml")
        
        table = soup.find("div", attrs={"class": "p0c-competition-match-list"})
        
        if table:
            rows = table.find_all("ol", attrs={"class": "p0c-competition-match-list__days"})
            
            for row in rows:
                matches = row.find_all("li", attrs={"class": "p0c-competition-match-list__day"})
                for match in matches:
                    tarih_span = match.find("span", class_="p0c-competition-match-list__title-date")
                    ev_sahibi_div = match.find("div", class_="p0c-competition-match-list__team p0c-competition-match-list__team--home")
                    deplasman_div = match.find("div", class_="p0c-competition-match-list__team p0c-competition-match-list__team--away")
                    

                    if tarih_span and ev_sahibi_div and deplasman_div:
                        tarih = tarih_span.text.strip()
                        ev_sahibi = ev_sahibi_div.text.strip()
                        deplasman = deplasman_div.text.strip()
                       

                        csvwriter.writerow([f"{sezon}-{sezon+1}", tarih, ev_sahibi,  deplasman])
                    else:
                        print(f"Veri eksik, atlanıyor: {match}")
        else:
            print(f"Tablo bulunamadı: {url}")

import sqlite3
import sys
import pandas as pd
from PyQt5.QtWidgets import *
from football import *
import TopluTumLigler.TopluTumLigler as ttl
import glob
import time




ttl.mac_verileri()
time.sleep(2)


uygulama = QApplication(sys.argv)
pencere = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(pencere)
pencere.show()

baglanti = sqlite3.connect("footballveritabani.db")
islem = baglanti.cursor()
with baglanti as conn:
        conn.execute("DELETE FROM mac_indeksleri3;")
baglanti.commit()



def veri_yaz ():

    
    baglanti = sqlite3.connect("footballveritabani.db")
    islem = baglanti.cursor()
    with baglanti as conn:
        conn.execute("DELETE FROM mac_indeksleri3;")
    baglanti.commit()
        

    islem.execute("""
        CREATE TABLE IF NOT EXISTS mac_indeksleri3 (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            LeaugePlayed TEXT NOT NULL,
            Season TEXT NOT NULL,
            Date TEXT NOT NULL,
            HomeTeam TEXT NOT NULL,
            Score TEXT NOT NULL,
            AwayTeam TEXT NOT NULL

        )
    """)



    csv_files = glob.glob('*.csv')


    for csv_file in csv_files:
        print(f"İşleniyor: {csv_file}")
        
        df = pd.read_csv(csv_file)  
        df = df[['LeaugePlayed', 'Season', 'Date', 'HomeTeam', 'Score', 'AwayTeam']]
        print(df.head())
        df.to_sql('mac_indeksleri3', baglanti, if_exists='append', index=False) 




veri_yaz()


def get_all_home_teams():
    ui.cmbHome.addItem("All")
    islem.execute("SELECT DISTINCT HomeTeam FROM mac_indeksleri3")
    HomeTeam = [row[0] for row in islem.fetchall()]
    return HomeTeam

def get_all_away_teams():
    ui.cmbAway.addItem("All")
    islem.execute("SELECT DISTINCT AwayTeam FROM mac_indeksleri3")
    AwayTeam = [row[0] for row in islem.fetchall()]
    return AwayTeam

def get_all_Seasons():
    ui.cmbSeason.addItem("All")
    islem.execute("SELECT DISTINCT Season FROM mac_indeksleri3")
    Season = [row[0] for row in islem.fetchall()]
    return Season

def get_all_Leauge_Played():
    ui.cmbLeaugePlayed.addItem("All")
    islem.execute("SELECT DISTINCT LeaugePlayed FROM mac_indeksleri3")
    LeaugePlayed = [row[0] for row in islem.fetchall()]
    return LeaugePlayed





def load_data_to_ui():
    ui.cmbHome.addItems(get_all_home_teams())
    ui.cmbAway.addItems(get_all_away_teams())
    ui.cmbLeaugePlayed.addItems(get_all_Leauge_Played())
    ui.cmbSeason.addItems(get_all_Seasons())

load_data_to_ui()






def show_all_results():
    ttl.mac_verileri()
    veri_yaz()
    
    try:
        ui.tableWidget.setRowCount(0)  

    
        sorgu = "SELECT * FROM mac_indeksleri3"
        islem.execute(sorgu)
        kayitlar = islem.fetchall()

        if kayitlar:
            
            ui.tableWidget.setColumnCount(len(kayitlar[0]))
            ui.tableWidget.setHorizontalHeaderLabels([
                "id",  "LeaugePlayed", "Season", "Date", "HomeTeam",
                "Score", "AwayTeam"
            ])

           
            ui.tableWidget.setRowCount(len(kayitlar))
            for indexSatir, kayitNumarasi in enumerate(kayitlar):
                for indexSutun, kayitSutun in enumerate(kayitNumarasi):
                    ui.tableWidget.setItem(indexSatir, indexSutun, QTableWidgetItem(str(kayitSutun)))
    except sqlite3.Error as e:
        print(f"Veritabanı hatası: {e}")
    except Exception as e:
        print(f"Genel hata: {e}")

def clear():
    try:
        ui.tableWidget.setRowCount(0)

        ui.statusbar.showMessage("Tablo ve filtreleme tercihleri temizlendi.", 3000)
    except Exception as e:
        print(f"Temizleme sırasında hata oluştu: {str(e)}")


def download_as_csv():
    try:

      
        sorgu = "SELECT * FROM mac_indeksleri3"
        islem.execute(sorgu)
        kayitlar = islem.fetchall()

        if kayitlar:
         
            df = pd.DataFrame(kayitlar, columns=[
                "id", "LeaugePlayed", "Season", "Date","HomeTeam","Score","AwayTeam"
            ])

            
            print("Veritabanından alınan veriler (ilk 5 satır):")
            print(df.head())


            # Verileri Excel dosyasına kaydet
            df.to_excel('mac_indeksleri3.xlsx', index=False, engine='openpyxl')

            ui.statusbar.showMessage("Veriler başarıyla 'mac_indeksleri3.xlsx' dosyasına kaydedildi.", 5000)

        else:
            ui.statusbar.showMessage("Kaydedilecek veri bulunamadı.", 5000)
    except sqlite3.Error as e:
        ui.statusbar.showMessage(f"Veritabanı hatası csv: {e}", 5000)
    except Exception as e:
        ui.statusbar.showMessage(f"Hata: {e}", 5000)

def all_years_radio_button(self):
    if ui.All_Years_Button.isChecked():
            print('Tüm Yıllar seçildi')
    else:
            print('Tüm Yıllar seçilmedi')



def show_results():
    ttl.mac_verileri()
    veri_yaz()
   
    clear()
    try:

        
        query = "SELECT * FROM mac_indeksleri3 WHERE 1=1"
        filters = []


        
        selected_date = ui.dtDate.date().toString("dd.MM.yyyy") 
        print(ui.All_Years_Button.isChecked())
        if not ui.All_Years_Button.isChecked():
            query += " AND Date = ?"
            filters.append(selected_date)



        leaugePlayed = ui.cmbLeaugePlayed.currentText()
        if leaugePlayed != "All":
            query += " AND LeaugePlayed = ?"
            filters.append(leaugePlayed)

        season = ui.cmbSeason.currentText()
        if season != "All":
            query += " AND Season = ?"
            filters.append(season)

        home = ui.cmbHome.currentText()
        if home != "All":
            query += " AND HomeTeam = ?"
            filters.append(home)

        away = ui.cmbAway.currentText()
        if away != "All":
            query += " AND AwayTeam = ?"
            filters.append(away)  
            print(query)
            print(filters)  

        score = ui.lneScore.text().strip()
        if score :
           query += " AND Score = ?"
           filters.append(score)
           print(query)
           print(filters)
        
        

        islem.execute(query, tuple(filters))
        kayitlar = islem.fetchall()

        if kayitlar:
           
            ui.tableWidget.setColumnCount(len(kayitlar[0]))
            ui.tableWidget.setHorizontalHeaderLabels([
                "id",  "LeaugePlayed", "Season", "Date", "HomeTeam",
                "Score", "AwayTeam"
            ])

           
            ui.tableWidget.setRowCount(len(kayitlar))
            for indexSatir, kayitNumarasi in enumerate(kayitlar):
                for indexSutun, kayitSutun in enumerate(kayitNumarasi):
                    ui.tableWidget.setItem(indexSatir, indexSutun, QTableWidgetItem(str(kayitSutun)))
                    print(kayitSutun)
            
    except sqlite3.Error as e:
        print(f"Veritabanı hatası show result: {e}")
    except Exception as e:
        print(f"Genel hata: {e}")



ui.btnShowAll.clicked.connect(show_all_results)
ui.btnShowR.clicked.connect(show_results)
ui.btnClear.clicked.connect(clear)
ui.btnDownload.clicked.connect(download_as_csv)
ui.All_Years_Button.clicked.connect(all_years_radio_button)



sys.exit(uygulama.exec_())

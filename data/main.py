import sqlite3
import sys
import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QObject, pyqtSignal, QThread
import glob
from football import *
import TopluTumLigler.TopluTumLigler as ttl


class StreamRedirector(QObject):
    new_text = pyqtSignal(str)

    def write(self, text):
        self.new_text.emit(text)

    def flush(self):
        pass
def redirect_output():
    global output_stream
    output_stream = StreamRedirector()
    output_stream.new_text.connect(ui.QPlainText_Terminal.appendPlainText)  
    sys.stdout = output_stream
    sys.stderr = output_stream

class DataLoaderThread(QThread):
    data_loaded = pyqtSignal()  

    def run(self):
        
        self.load_data()
        
        

    def load_data(self):
        try:
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

            
            csv_file = "mac_verileri.csv"
            print(f"İşleniyor: {csv_file}")
            df = pd.read_csv(csv_file)
            df = df[['LeaugePlayed', 'Season', 'Date', 'HomeTeam', 'Score', 'AwayTeam']]
            df.to_sql('mac_indeksleri3', baglanti, if_exists='append', index=False)
            print("Veriler arayüze eklendi.")    
            
            self.data_loaded.emit()

        except Exception as e:
            print(f"Veri yükleme sırasında hata: {e}")
        finally:
            
            self.quit()


class PullDataThread(QThread):
    data_pulled = pyqtSignal()
    
    def run(self):
        self.pull_data()

    def pull_data(self):
        season_from()
        season_to()
        on_pull_data()
        
        
        
        
        try:
        
    
            ttl.mac_verileri(season_from(),season_to(),on_pull_data())
            self.load_data()
        except Exception as e:
            print(f"Veri çekme sırasında hata: {e}")

    def load_data(self):
        try:
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

            
            updated_csv_file = "updated_mac_verileri.csv"
            print(f"İşleniyor: {updated_csv_file}")
            df = pd.read_csv(updated_csv_file)
            df = df[['LeaugePlayed', 'Season', 'Date', 'HomeTeam', 'Score', 'AwayTeam']]
            df.to_sql('mac_indeksleri3', baglanti, if_exists='append', index=False)
            print("Veriler arayüze eklendi.")     

            self.data_pulled.emit()
        except Exception as e:
            print(f"Veri yükleme sırasında hata: {e}")
        


uygulama = QApplication(sys.argv)
pencere = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(pencere)
pencere.show()

pull_data_thread = PullDataThread()


def datapull():
    pull_data_thread.start()
    pull_data_thread.data_pulled.connect(load_data_to_ui)

ui.btnPullData.clicked.connect(datapull)


def load_data():
        try:
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

            
            updated_csv_file = "updated_mac_verileri.csv"
            print(f"İşleniyor: {updated_csv_file}")
            df = pd.read_csv(updated_csv_file)
            df = df[['LeaugePlayed', 'Season', 'Date', 'HomeTeam', 'Score', 'AwayTeam']]
            df.to_sql('mac_indeksleri3', baglanti, if_exists='append', index=False)
            print("Veriler arayüze eklendi.")     

            
        except Exception as e:
            print(f"Veri yükleme sırasında hata: {e}")

baglanti = sqlite3.connect("footballveritabani.db")
islem = baglanti.cursor()

def get_all_home_teams():
    ui.cmbHome.addItem("All")
    islem.execute("SELECT DISTINCT HomeTeam FROM mac_indeksleri3")
    return [row[0] for row in islem.fetchall()]

def get_all_away_teams():
    ui.cmbAway.addItem("All")
    islem.execute("SELECT DISTINCT AwayTeam FROM mac_indeksleri3")
    return [row[0] for row in islem.fetchall()]

def get_all_seasons():
    ui.cmbSeason.addItem("All")
    islem.execute("SELECT DISTINCT Season FROM mac_indeksleri3")
    return [row[0] for row in islem.fetchall()]

def get_all_league_played():
    ui.cmbLeaugePlayed.addItem("All")
    islem.execute("SELECT DISTINCT LeaugePlayed FROM mac_indeksleri3")
    return [row[0] for row in islem.fetchall()]

def load_data_to_ui():
    ui.tableWidget.setRowCount(0)
    ui.statusbar.showMessage("Tablo tercihleri temizlendi.", 3000)
    ui.checkBox_Bundesliga.setChecked(False)
    ui.checkBox_LaLiga.setChecked(False)
    ui.checkBox_Ligue1.setChecked(False)
    ui.checkBox_PremierL.setChecked(False)
    ui.checkBox_SeriaA.setChecked(False)
    ui.checkBox_SuperLig.setChecked(False)
    ui.cmbHome.clear()
    ui.cmbAway.clear()
    ui.cmbLeaugePlayed.clear()
    ui.cmbSeason.clear()
    ui.lneSeasonTo.clear()
    ui.lneSeasonFrom.clear()
    ui.cmbHome.addItems(get_all_home_teams())
    ui.cmbAway.addItems(get_all_away_teams())
    ui.cmbLeaugePlayed.addItems(get_all_league_played())
    ui.cmbSeason.addItems(get_all_seasons())

def show_all_results():
    try:
        ui.tableWidget.setRowCount(0)
        sorgu = "SELECT * FROM mac_indeksleri3"
        islem.execute(sorgu)
        kayitlar = islem.fetchall()

        if kayitlar:
            ui.tableWidget.setColumnCount(len(kayitlar[0]))
            ui.tableWidget.setHorizontalHeaderLabels([
                "id", "LeaugePlayed", "Season", "Date", "HomeTeam",
                "Score", "AwayTeam"
            ])
            ui.tableWidget.setRowCount(len(kayitlar))
            for indexSatir, kayitNumarasi in enumerate(kayitlar):
                for indexSutun, kayitSutun in enumerate(kayitNumarasi):
                    ui.tableWidget.setItem(indexSatir, indexSutun, QTableWidgetItem(str(kayitSutun)))
            print(sorgu)
    except sqlite3.Error as e:
        print(f"Veritabanı hatası: {e}")
    except Exception as e:
        print(f"Genel hata: {e}")

def clear():
    try:
        
        ui.tableWidget.setRowCount(0)
        ui.statusbar.showMessage("Tablo ve filtreleme tercihleri temizlendi.", 3000)
    except Exception as e:
        print(f"Temizleme sırasında hata oluştu: {e}")

def download_data(): 
    try:
        
        query = "SELECT DISTINCT * FROM mac_indeksleri3 WHERE 1=1"
        filters = []
        selected_date = ui.dtDate.date().toString("dd.MM.yyyy")
        if not ui.All_Years_Button.isChecked():
            query += " AND Date = ?"
            filters.append(selected_date)

        league_played = ui.cmbLeaugePlayed.currentText()
        if league_played != "All":
            query += " AND LeaugePlayed = ?"
            filters.append(league_played)

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

        score = ui.lneScore.text().strip()
        if score:
            query += " AND Score = ?"
            filters.append(score)


        
        print("Final Query:", query)  
        print("Filters:", filters)   
        islem.execute(query, tuple(filters))
        kayitlar = islem.fetchall()

        if kayitlar:
            
            df = pd.DataFrame(kayitlar, columns=[
                "id", "LeaugePlayed", "Season", "Date", "HomeTeam",
                "Score", "AwayTeam"
            ])

            
            file_path, _ = QFileDialog.getSaveFileName(
            pencere, "Verileri Kaydet", "", "Excel Dosyası (*.csv)"
            )

            if file_path:
                
                df.to_csv(file_path, index=False)

                
                ui.statusbar.showMessage(f"Veriler başarıyla '{file_path}' dosyasına kaydedildi.", 5000)
            else:
                
                ui.statusbar.showMessage("Dosya kaydedilmedi.", 5000)
        else:
            
            ui.statusbar.showMessage("Kaydedilecek veri bulunamadı.", 5000)

    except sqlite3.Error as e:
        
        ui.statusbar.showMessage(f"Veritabanı hatası: {e}", 5000)
        print(f"Veritabanı hatası: {e}", 5000)
    except Exception as e:
        
        ui.statusbar.showMessage(f"Hata: {e}", 5000)
        print(f"Hata: {e}", 5000)

def all_years_radio_button():
    if ui.All_Years_Button.isChecked():
        print('Tüm Yıllar seçildi')
    else:
        print('Tüm Yıllar seçilmedi')

def show_results():
    clear()
    
    try:
        query = "SELECT * FROM mac_indeksleri3 WHERE 1=1"
        filters = []

        selected_date = ui.dtDate.date().toString("dd.MM.yyyy")
        if not ui.All_Years_Button.isChecked():
            query += " AND Date = ?"
            filters.append(selected_date)

        league_played = ui.cmbLeaugePlayed.currentText()
        if league_played != "All":
            query += " AND LeaugePlayed = ?"
            filters.append(league_played)

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

        score = ui.lneScore.text().strip()
        if score:
            query += " AND Score = ?"
            filters.append(score)

        islem.execute(query, tuple(filters))
        kayitlar = islem.fetchall()

        if kayitlar:
            ui.tableWidget.setColumnCount(len(kayitlar[0]))
            ui.tableWidget.setHorizontalHeaderLabels([
                "id", "LeaugePlayed", "Season", "Date", "HomeTeam",
                "Score", "AwayTeam"
            ])
            ui.tableWidget.setRowCount(len(kayitlar))
            for indexSatir, kayitNumarasi in enumerate(kayitlar):
                for indexSutun, kayitSutun in enumerate(kayitNumarasi):
                    ui.tableWidget.setItem(indexSatir, indexSutun, QTableWidgetItem(str(kayitSutun)))
            print(query)
    except sqlite3.Error as e:
        print(f"Veritabanı hatası show result: {e}")
    except Exception as e:
        print(f"Genel hata: {e}")


ui.btnShowAll.clicked.connect(show_all_results)
ui.btnShowR.clicked.connect(show_results)
ui.btnClear.clicked.connect(clear)
ui.btnDownload.clicked.connect(download_data)
ui.All_Years_Button.clicked.connect(all_years_radio_button)

def season_to():
        season_for_range_to= ui.lneSeasonTo.text().strip()
        if season_for_range_to=="":
           season_for_range_to = 2024
        return  season_for_range_to
    

def season_from():
        season_for_range_from = ui.lneSeasonFrom.text().strip()
        if season_for_range_from=="":
           season_for_range_from= 2000
        return  season_for_range_from

def on_pull_data():
    selected_leagues = get_selected_leagues()
    return selected_leagues
    


def get_selected_leagues():
    selected_leagues = []
    if ui.checkBox_Bundesliga.isChecked():
        selected_leagues.append("Bundesliga")
    if ui.checkBox_PremierL.isChecked():
        selected_leagues.append("Premier Lig")
    if ui.checkBox_Ligue1.isChecked():
        selected_leagues.append("Ligue 1")
    if ui.checkBox_SeriaA.isChecked():
        selected_leagues.append("Serie A")
    if ui.checkBox_LaLiga.isChecked():
        selected_leagues.append("La Liga")
    if ui.checkBox_SuperLig.isChecked():
        selected_leagues.append("Süper Lig")
    if selected_leagues==[]:
        selected_leagues=['Süper Lig',"La Liga","Serie A","Ligue 1","Premier Lig","Bundesliga"]
    
    return selected_leagues



loader_thread = DataLoaderThread()
loader_thread.data_loaded.connect(load_data_to_ui)
loader_thread.finished.connect(lambda: print("Veri yükleme tamamlandı."))
loader_thread.start()
redirect_output()
sys.exit(uygulama.exec_())
from PyQt6.QtWidgets import QApplication, QMenu, QItemDelegate, QToolBar, QWidgetAction, QDialog, QDialogButtonBox,  QAbstractSpinBox, QMainWindow, QTableWidget, QMessageBox, QGridLayout, QWidget, QVBoxLayout, QTableWidgetItem, QFormLayout, QLabel, QDateEdit, QComboBox, QLineEdit, QSpinBox, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt, QDate, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QTextDocument
from PyQt6.QtPrintSupport import QPrintDialog, QPrinter
import PyQt6.QtGui as QtGui
import sys, sqlite3
from db import db_create
db_create()

class MainWindow(QMainWindow):
    send_id_order = pyqtSignal(int)
    def __init__(self):
        super().__init__()
        self.initUI()
        

    def initUI(self):
        central_widget = QWidget()
        layout = QGridLayout()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.setWindowTitle('Wysyłka SAP-Polska')
        self.setGeometry(100, 100, 1100, 800)
        
        # Widgets
        self.create_main_table()
        self.db_data_to_table()
        # Layouts
        layout.addWidget(self.main_table, 1, 0) 
        
        form_layout = self.tools_fields()
        layout.addLayout(form_layout, 0,0) 

        # Menu

        self.main_button = QPushButton('Menu')
        self.table_button = QPushButton('Klienci')
        self.emp_button = QPushButton('Pracownicy')
        self.refresh = QPushButton('Odśwież')
        self.main_button.clicked.connect(self.show_main)
        self.table_button.clicked.connect(self.show_customers)
        self.emp_button.clicked.connect(self.show_emp)
        self.refresh.clicked.connect(self.db_data_to_table)
        toolbar = self.addToolBar('Toolbar')
        toolbar.addWidget(self.main_button)
        toolbar.addWidget(self.table_button)
        toolbar.addWidget(self.emp_button)
        toolbar.addWidget(self.refresh)

        self.customer_view = CustomersWindow(self)
        self.customer_view.initUi() 

        self.emp_view = EmployersWindow(self)
        self.emp_view.initUi()

        self.edit_product_view = EditProductWindow(self)
        self.edit_product_view.initUi()
    

        self.show_main()  # Pokaż widok menu jako domyślny
    
    def show_main(self):
        self.customer_view.setVisible(False)
        self.main_button.setVisible(False)
        self.emp_view.setVisible(False)
        self.edit_product_view.setVisible(False)

    def show_customers(self):
        self.customer_view.setVisible(True)
        self.main_button.setVisible(True)
        self.emp_view.setVisible(False)
        self.edit_product_view.setVisible(False)
    def show_emp(self):
        self.customer_view.setVisible(False)
        self.main_button.setVisible(True)
        self.emp_view.setVisible(True)
        self.edit_product_view.setVisible(False)

    def editClicked(self):
        self.customer_view.setVisible(False)
        self.main_button.setVisible(False)
        self.emp_view.setVisible(False)
        self.edit_product_view.setVisible(True)
        index = self.sender().property("index")
        if index is not None:
            row = index.row()
            id_order_table = self.main_table.item(row, 7).text()
            id_order = int(id_order_table)
            print(id_order)
            self.send_id_order.emit(int(id_order))
        
            


    def printClicked(self):
        index = self.sender().property("index")
        if index is not None:
            row = index.row()
            print(row)
    
     
    
    
    def create_main_table(self):
        self.main_table = QTableWidget()
        self.main_table.setColumnCount(12)
        table_labels = ['Data', 'Zlecenie', 'Klient', 'Produkt', 'Ilość', 'Pracownik', 'Informacje', 'ID', '', '']
        self.main_table.setHorizontalHeaderLabels(table_labels)

        self.main_table.setSortingEnabled(True)


      

    
    
    
    
  

      


    
    def db_data_to_table(self):
        db = sqlite3.connect("simple.db")
        cursor = db.cursor()
        
        query = """
        SELECT 
            
            ordered_products.shipping_date, 
            ordered_products.order_number, 
            customers.company_name,
            ordered_products.product, 
            ordered_products.count,
            employers.name,
            ordered_products.informations,
            ordered_products.id,
            ordered_products.id,
            ordered_products.id
            
        FROM ordered_products
        JOIN customers ON customer_id = customers.id
        JOIN employers ON employer_id = employers.id"""
        
        cursor.execute(query) 
        data = cursor.fetchall()
        db.close()
        
        column_mapping = {
        'shipping_date': 0,
        'order_number': 1,
        'company_name': 2,
        'product': 3,
        'count': 4,
        'name': 5,
        'informations': 6,
        'id': 7,
        'button1': 8,
        'button2': 9,

        
        
    }
    
        self.main_table.setRowCount(len(data))
        self.main_table.setColumnCount(len(column_mapping))
        
        for row_index, row_data in enumerate(data):
            for column_name, column_index in column_mapping.items():
                cell_data = row_data[column_index]
                item = QTableWidgetItem(str(cell_data))
                self.main_table.setItem(row_index, column_mapping[column_name], item)
                item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter)
            
            # Dodaj przyciski "Edytuj" i "Drukuj" w nowych kolumnach
            edit_button = QPushButton("Edytuj")
            print_button = QPushButton("Drukuj")
            
            edit_button.clicked.connect(self.editClicked)
            print_button.clicked.connect(self.printClicked)
            
            self.main_table.setCellWidget(row_index, 8, edit_button)  # Kolumna "Edytuj"
            self.main_table.setCellWidget(row_index, 9, print_button)  # Kolumna "Drukuj"
            
            # Ustaw indeks wiersza jako właściwość przycisku
            edit_button.setProperty("index", self.main_table.model().index(row_index, 0))
            print_button.setProperty("index", self.main_table.model().index(row_index, 0))
    def tools_fields(self):
        fields_layout = QHBoxLayout()

        left_column_layout = QFormLayout()
        right_column_layout = QFormLayout()

        self.label_date = QLabel("Data:")
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True) 
        today = QDate.currentDate()
        self.date_edit.setDate(today)
        self.date_edit.setStyleSheet("QCalendarWidget {width: 300px; height: 200px;}")
        self.date_edit.setStyleSheet("max-width: 200px;")  
        left_column_layout.addRow(self.label_date, self.date_edit)

        self.label_order_no = QLabel("Zlecenie:")
        self.order_no_edit = QSpinBox()
        self.order_no_edit.setRange(0, 9999)
        self.order_no_edit.setStyleSheet("max-width: 200px;")  
        self.order_no_edit.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        left_column_layout.addRow(self.label_order_no, self.order_no_edit)

        self.label_customer = QLabel("Klient:")
        self.customer_combo = QComboBox()
        self.load_customers()
        self.customer_combo.currentIndexChanged.connect(self.add_order_to_db)
        self.customer_combo.setEditable(True)
        self.customer_combo.setStyleSheet("max-width: 200px;")  
        left_column_layout.addRow(self.label_customer, self.customer_combo)

        self.label_product = QLabel("Produkt:")
        self.product_edit = QLineEdit()
        self.product_edit.setStyleSheet("max-width: 200px;")  
        right_column_layout.addRow(self.label_product, self.product_edit)

        self.label_count = QLabel("Ilość:")
        self.count_edit = QSpinBox()
        self.count_edit.setStyleSheet("max-width: 200px;")
        self.count_edit.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)  
        right_column_layout.addRow(self.label_count, self.count_edit)

        self.label_employer = QLabel("Pracownik:")
        self.employer_combo = QComboBox()
        self.load_employers()
        self.employer_combo.setEditable(False)
        self.employer_combo.setStyleSheet("max-width: 200px;")  
        right_column_layout.addRow(self.label_employer, self.employer_combo)

        self.label_info = QLabel("Informacje:")
        self.info_edit = QLineEdit()
        self.info_edit.setStyleSheet("max-width: 200px;")  
        left_column_layout.addRow(self.label_info, self.info_edit)

        self.add_button = QPushButton("Dodaj")
        self.add_button.setStyleSheet("max-width: 265px;")
        self.add_button.clicked.connect(self.add_order_to_db)  
        right_column_layout.addRow(self.add_button)


        fields_layout.addLayout(left_column_layout)
        fields_layout.addLayout(right_column_layout)

        return fields_layout

    def load_employers(self):
        db = sqlite3.connect('simple.db')
        cursor = db.cursor()
        cursor.execute('SELECT DISTINCT name FROM employers')
        employers = cursor.fetchall()
        for employer in employers:
            self.employer_combo.addItem(employer[0])

    def load_customers(self):
        db = sqlite3.connect('simple.db')
        cursor = db.cursor()
        self.customer_combo.clear()
        cursor.execute('SELECT DISTINCT company_name FROM customers')
        customers = cursor.fetchall()
        for customer in customers:
            self.customer_combo.addItem(customer[0])

    
    def add_order_to_db(self):
        selected_customer = self.customer_combo.currentText()
        db = sqlite3.connect('simple.db')
        cursor = db.cursor()
        customer_query = "SELECT company_name FROM customers WHERE company_name = ?"
        cursor.execute(customer_query, (selected_customer,))
        result = cursor.fetchone()
        if result:
            sending_date = self.date_edit.date().toString("yyyy-MM-dd")
            order_number = self.order_no_edit.value()
            customer_id = "SELECT id FROM customers WHERE company_name = ?"
            cursor.execute(customer_id, (selected_customer,))
            customer_touple = cursor.fetchone()
            customer = customer_touple[0]
            product = self.product_edit.text()
            count = self.count_edit.value()
            selected_employer = self.employer_combo.currentText() 
            employer_id = "SELECT id FROM employers WHERE name = ?"
            cursor.execute(employer_id, (selected_employer,))
            employer_touple = cursor.fetchone()
            employer = employer_touple[0]
            information = self.info_edit.text()
            try:
                query = """INSERT INTO ordered_products(
                            order_number, shipping_date, product, count, customer_id, employer_id, informations) VALUES (?, ?, ?, ?, ?, ?, ?)"""
                data = (order_number, sending_date, product, count, customer, employer, information)
                cursor.execute(query, data)

            except Exception as e:
            # Obsłuż błędy przy wstawianiu danych do bazy
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Critical)
                msg.setText(f"Wystąpił błąd podczas dodawania zamówienia: {e}")
                msg.setWindowTitle("Jest Git!")
                msg.setStandardButtons(QMessageBox.StandardButton.Ok)
                msg.exec()    
                return

            finally:
                # Zamknij kursor i połączenie z bazą danych
                db.commit()
                db.close()
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setText("Zamówienie zostało dodane.")
                msg.setWindowTitle("Jest Git!")
                msg.setStandardButtons(QMessageBox.StandardButton.Ok)
                msg.exec()    
        else:
            print(f"Dane '{selected_customer}' nie istnieją w bazie danych.")

        # Zamknij połączenie z bazą danych
        db.close()
        self.db_data_to_table()
    
class CustomersWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window 
        self.initUi()

    def initUi(self):
        
        self.setWindowTitle('Wysyłka SAP-Polska')
        self.setGeometry(100, 100, 800, 600)

        # Sprawdź, czy widget nie ma jeszcze przypisanego układu
        if not self.layout():
            # Tworzenie układu QFormLayout
            form_layout = self.customer_data()

            # Przypisanie układu do głównego widgetu CustomersWindow
            self.setLayout(form_layout)
        

        

       
    def customer_data(self):
        form_layout = QFormLayout()
        
        self.label_customer = QLabel("Klient: ")
        self.customer_combo = QComboBox()
        self.customer_combo.setStyleSheet("margin-bottom: 50px; max-width: 300px;")  
        form_layout.addRow(self.label_customer, self.customer_combo)

        self.label_name = QLabel("Nazwa:")
        self.name_edit = QLineEdit()
        self.name_edit.setStyleSheet("max-width: 100px;")  
        form_layout.addRow(self.label_name, self.name_edit)

        self.label_post_code = QLabel("Kod Pocztowy:")
        self.post_code_edit = QLineEdit()
        self.post_code_edit.setStyleSheet("max-width: 100px;")  
        form_layout.addRow(self.label_post_code, self.post_code_edit)

        self.label_city = QLabel("Miasto:")
        self.city_edit = QLineEdit()
        self.city_edit.setStyleSheet("max-width: 100px;")  
        form_layout.addRow(self.label_city, self.city_edit)

        self.label_address = QLabel("Adres:")
        self.address_edit = QLineEdit()
        self.address_edit.setStyleSheet("max-width: 100px;")  
        form_layout.addRow(self.label_address, self.address_edit)

        self.label_no = QLabel("Numer budynku/lokalu:")
        self.no_edit = QLineEdit()
        self.no_edit.setStyleSheet("max-width: 100px;")  
        form_layout.addRow(self.label_no, self.no_edit)

        self.label_phone = QLabel("Telefon:")
        self.phone_edit = QLineEdit()
        self.phone_edit.setStyleSheet("max-width: 100px;")  
        form_layout.addRow(self.label_phone, self.phone_edit)
        
        # Przycisk "Dodaj" do dodawania danych do bazy
        self.add_button = QPushButton("Dodaj")
        self.add_button.clicked.connect(self.add_customer_to_db)
        form_layout.addRow(self.add_button)
        
        return form_layout
        


    def add_customer_to_db(self):
        
        name = self.name_edit.text()
        post_code = self.post_code_edit.text()
        city = self.city_edit.text()
        address = self.address_edit.text()
        build_no = self.no_edit.text() 
        phone = self.phone_edit.text() 
        print("name:", name)
        print("post_code:", post_code)
        print("city:", city)
        print("address:", address)
        print("build_no:", build_no)
        print("phone:", phone)
        # Połącz z bazą danych
        db = sqlite3.connect("simple.db")
        cursor = db.cursor()

        try:
            cursor.execute("""INSERT INTO customers 
                           (company_name, post_code, city, address,  no_building, phone)
                           VALUES (?,?,?,?,?,?)""", (name, post_code, city, address, build_no, phone))
        except Exception as e:
            # Obsłuż błędy przy wstawianiu danych do bazy
            print(f"Błąd przy wstawianiu danych do bazy: {e}")

        finally:
            # Zamknij kursor i połączenie z bazą danych
            db.commit()
            db.close()
            
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setText("Klient został dodany.")
            msg.setWindowTitle("Jest Git!")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()    

class EditProductWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window 
        self.initUi()
        self.main_window.send_id_order.connect(self.receive_id_order)
    def initUi(self):
        layout = QGridLayout()
        self.setWindowTitle('Wysyłka SAP-Polska')
        self.setGeometry(100, 100, 800, 600)
        if not self.layout():
            form_layout = self.edit_tools_fields()
            self.setLayout(form_layout)
        
    @pyqtSlot(int)
    def receive_id_order(self, id_order):
        # Tutaj możesz wykonać odpowiednie operacje z przekazanym id_order
        print(f"ID zamówienia otrzymane w EditProductWindow: {id_order}")
        self.fill_fields_from_db(id_order)
        self.order_id = int(id_order)
    
    def edit_tools_fields(self):
        fields_layout = QHBoxLayout()
        left_column_layout = QFormLayout()
        right_column_layout = QFormLayout()

        self.label_date = QLabel("Data:")
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True) 
        today = QDate.currentDate()
        self.date_edit.setDate(today)
        self.date_edit.setStyleSheet("QCalendarWidget {width: 300px; height: 200px;}")
        self.date_edit.setStyleSheet("max-width: 200px;")  
        left_column_layout.addRow(self.label_date, self.date_edit)

        self.label_order_no = QLabel("Zlecenie:")
        self.order_no_edit = QSpinBox()
        self.order_no_edit.setRange(0, 9999)
        self.order_no_edit.setStyleSheet("max-width: 200px;")  
        self.order_no_edit.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        left_column_layout.addRow(self.label_order_no, self.order_no_edit)

        self.label_customer = QLabel("Klient:")
        self.customer_combo = QComboBox()
        self.load_customers()
        self.customer_combo.currentIndexChanged.connect(self.add_order_to_db)
        self.customer_combo.setEditable(True)
        self.customer_combo.setStyleSheet("max-width: 200px;")  
        left_column_layout.addRow(self.label_customer, self.customer_combo)

        self.label_product = QLabel("Produkt:")
        self.product_edit = QLineEdit()
        self.product_edit.setStyleSheet("max-width: 200px;")  
        right_column_layout.addRow(self.label_product, self.product_edit)

        self.label_count = QLabel("Ilość:")
        self.count_edit = QSpinBox()
        self.count_edit.setStyleSheet("max-width: 200px;")
        self.count_edit.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)  
        right_column_layout.addRow(self.label_count, self.count_edit)

        self.label_employer = QLabel("Pracownik:")
        self.employer_combo = QComboBox()
        self.load_employers()
        self.employer_combo.setEditable(False)
        self.employer_combo.setStyleSheet("max-width: 200px;")  
        right_column_layout.addRow(self.label_employer, self.employer_combo)

        self.label_info = QLabel("Informacje:")
        self.info_edit = QLineEdit()
        self.info_edit.setStyleSheet("max-width: 200px;")  
        left_column_layout.addRow(self.label_info, self.info_edit)

        self.add_button = QPushButton("Zapisz zmiany")
        self.add_button.setStyleSheet("max-width: 265px;")
        self.add_button.clicked.connect(self.add_order_to_db)  
        right_column_layout.addRow(self.add_button)


        fields_layout.addLayout(left_column_layout)
        fields_layout.addLayout(right_column_layout)

        return fields_layout
    def fill_fields_from_db(self, id_order):
        db = sqlite3.connect('simple.db')
        cursor = db.cursor()
        query = """
        SELECT
            ordered_products.shipping_date, 
            ordered_products.order_number, 
            customers.company_name,
            ordered_products.product, 
            ordered_products.count,
            employers.name,
            ordered_products.informations
        FROM ordered_products
        JOIN customers ON customer_id = customers.id
        JOIN employers ON employer_id = employers.id
        WHERE ordered_products.id = ?
        """
        cursor.execute(query, (id_order,))
        data = cursor.fetchone()  # Użyj fetchone, aby pobrać jedno konkretne zamówienie
        db.close()
        
        if data:
            # Wypełnij pola danymi z bazy danych
            self.date_edit.setDate(QDate.fromString(data[0], 'yyyy-MM-dd'))
            self.order_no_edit.setValue(data[1])
            self.customer_combo.setCurrentText(data[2])
            self.product_edit.setText(data[3])
            self.count_edit.setValue(data[4])
            self.employer_combo.setCurrentText(data[5])
            self.info_edit.setText(data[6])
        else:
            print("Brak danych w bazie dla ID zamówienia:", id_order)
        
    

    def load_employers(self):
        db = sqlite3.connect('simple.db')
        cursor = db.cursor()
        cursor.execute('SELECT DISTINCT name FROM employers')
        employers = cursor.fetchall()
        for employer in employers:
            self.employer_combo.addItem(employer[0])
        
    def load_customers(self):
        db = sqlite3.connect('simple.db')
        cursor = db.cursor()
        self.customer_combo.clear()
        cursor.execute('SELECT DISTINCT company_name FROM customers')
        customers = cursor.fetchall()
        for customer in customers:
            self.customer_combo.addItem(customer[0])

    
    def add_order_to_db(self):
        selected_customer = self.customer_combo.currentText()
        db = sqlite3.connect('simple.db')
        cursor = db.cursor()
        customer_query = "SELECT company_name FROM customers WHERE company_name = ?"
        cursor.execute(customer_query, (selected_customer,))
        result = cursor.fetchone()
        if result:
            sending_date = self.date_edit.date().toString("yyyy-MM-dd")
            order_number = self.order_no_edit.value()
            customer_id = "SELECT id FROM customers WHERE company_name = ?"
            cursor.execute(customer_id, (selected_customer,))
            customer_touple = cursor.fetchone()
            customer = customer_touple[0]
            product = self.product_edit.text()
            count = self.count_edit.value()
            selected_employer = self.employer_combo.currentText() 
            employer_id = "SELECT id FROM employers WHERE name = ?"
            cursor.execute(employer_id, (selected_employer,))
            employer_touple = cursor.fetchone()
            employer = employer_touple[0]
            information = self.info_edit.text()
            print("-----------")
            print(self.order_id)
            try:
                
                query = """UPDATE ordered_products
                        SET shipping_date = ?, product = ?, count = ?, customer_id = ?, employer_id = ?, informations = ?
                        WHERE ordered_products.id = ?"""
                data = (sending_date, product, count, customer, employer, information, self.order_id)
                cursor.execute(query, data)

            except Exception as e:
            # Obsłuż błędy przy wstawianiu danych do bazy
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Critical)
                msg.setText(f"Wystąpił błąd podczas dodawania zamówienia: {e}")
                msg.setWindowTitle("Jest Git!")
                msg.setStandardButtons(QMessageBox.StandardButton.Ok)
                msg.exec()    
                return

            finally:
                # Zamknij kursor i połączenie z bazą danych
                db.commit()
                db.close()
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setText("Zamówienie zostało dodane.")
                msg.setWindowTitle("Jest Git!")
                msg.setStandardButtons(QMessageBox.StandardButton.Ok)
                msg.exec()    
        else:
            print(f"Dane '{selected_customer}' nie istnieją w bazie danych.")

        # Zamknij połączenie z bazą danych
        db.close()
        
    
       
class EmployersWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window 
        self.initUi()

    def initUi(self):
        
        self.setWindowTitle('Wysyłka SAP-Polska')
        self.setGeometry(100, 100, 800, 600)

        # Sprawdź, czy widget nie ma jeszcze przypisanego układu
        if not self.layout():
            # Tworzenie układu QFormLayout
            form_layout = self.employers_data()

            # Przypisanie układu do głównego widgetu CustomersWindow
            self.setLayout(form_layout)
        

        

       
    def employers_data(self):
        form_layout = QFormLayout()
        

        self.label_name = QLabel("Imię:")
        self.name_edit = QLineEdit()
        self.name_edit.setStyleSheet("max-width: 100px;")  
        form_layout.addRow(self.label_name, self.name_edit)


        # Przycisk "Dodaj" do dodawania danych do bazy
        self.add_button = QPushButton("Dodaj")
        self.add_button.clicked.connect(self.add_employer_to_db)
        form_layout.addRow(self.add_button)
        
        return form_layout
    def add_employer_to_db(self):
        name = self.name_edit.text()
        
        db = sqlite3.connect('simple.db')
        cursor = db.cursor()

        try:
            cursor.execute("INSERT INTO employers (name) VALUES (?)", (name,))
        except Exception as e:
            # Obsłuż błędy przy wstawianiu danych do bazy
            print(f"Błąd przy wstawianiu danych do bazy: {e}")
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setText(f"Błąd: {e}")
            msg.setWindowTitle("Błąd!")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
            return
        
        # Zamknij kursor i połączenie z bazą danych
        db.commit()
        db.close()
        
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText("Pracownik został dodany.")
        msg.setWindowTitle("Jest Git!")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

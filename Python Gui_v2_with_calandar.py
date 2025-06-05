import os
import sys
import cx_Oracle
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QTableWidget, QTableWidgetItem,
    QComboBox, QPushButton, QMessageBox,
    QHBoxLayout, QVBoxLayout, QLabel, QDateEdit
)
from PySide6.QtCore import Qt

# --- Oracle client & environment setup ---
os.environ["TNS_ADMIN"] = r"C:\Users\yberj\Wallet_OWATERDB1"
cx_Oracle.init_oracle_client(lib_dir=r"C:\instantclient_19_5")

# Connection helper
def get_connection():
    user = os.getenv("ORACLE_USER")
    pwd  = os.getenv("ORACLE_PASSWORD")
    dsn  = os.getenv("CONNECT", "owaterdb1_high")
    return cx_Oracle.connect(user=user, password=pwd, dsn=dsn)

class FinancialsTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.load_categories()
        self.load_financials()

    def init_ui(self):
        # Top controls layout
        ctrl_layout = QHBoxLayout()

        # Date range pickers using QDateEdit with popup calendar
        ctrl_layout.addWidget(QLabel('From:'))
        self.start_date = QDateEdit(calendarPopup=True)
        self.start_date.setDate(self.start_date.date().currentDate().addDays(-720))
        ctrl_layout.addWidget(self.start_date)

        ctrl_layout.addWidget(QLabel('To:'))
        self.end_date = QDateEdit(calendarPopup=True)
        self.end_date.setDate(self.end_date.date().currentDate())
        ctrl_layout.addWidget(self.end_date)

        # Apply date filter button
        self.reload_btn = QPushButton('Apply Date Filter')
        self.reload_btn.clicked.connect(self.load_financials)
        ctrl_layout.addWidget(self.reload_btn)

        # Category selector and update button
        self.cat_combo = QComboBox()
        self.cat_combo.setEditable(True)
        ctrl_layout.addWidget(self.cat_combo)
        update_btn = QPushButton('Update Category')
        update_btn.clicked.connect(self.update_category)
        ctrl_layout.addWidget(update_btn)

        # Financials table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        headers = [
            'Date', 'Description', 'Sub-Description',
            'Type', 'Amount', 'Category', 'ROWID'
        ]
        self.table.setHorizontalHeaderLabels(headers)
        self.table.hideColumn(6)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.MultiSelection)
        self.table.setSortingEnabled(True)
        self.table.horizontalHeader().setStretchLastSection(True)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.addLayout(ctrl_layout)
        main_layout.addWidget(self.table)

    def load_categories(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT DISTINCT CATEGORY FROM SUB_DESCRIPTION_MAPPING ORDER BY CATEGORY")
            cats = [row[0] for row in cur.fetchall()]
            cur.close(); conn.close()
            self.cat_combo.clear()
            self.cat_combo.addItems(cats)
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to load categories: {e}')

    def load_financials(self):
        start = self.start_date.date().toPython()
        end   = self.end_date.date().toPython()
        try:
            conn = get_connection()
            cur = conn.cursor()
            sql = """
SELECT
  t.TRANSACTION_DATE,
  t.DESCRIPTION,
  t.SUB_DESCRIPTION,
  t.TRANSACTION_TYPE,
  t.AMOUNT,
  COALESCE(
    (SELECT m.category FROM SUB_DESCRIPTION_MAPPING m
       WHERE REGEXP_LIKE(t.SUB_DESCRIPTION, m.pattern)
         AND m.pattern != '.*'
         AND ROWNUM = 1),
    (SELECT m.category FROM SUB_DESCRIPTION_MAPPING m WHERE m.pattern = '.*')
  ) AS CATEGORY,
  t.ROWID AS ROW_ID
FROM BANK_TRANSACTIONS t
WHERE t.TRANSACTION_DATE BETWEEN :1 AND :2
ORDER BY t.TRANSACTION_DATE
"""
            cur.execute(sql, [start, end])
            rows = cur.fetchall()
            cur.close(); conn.close()
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to load financials: {e}')
            return

        self.table.setRowCount(len(rows))
        for r, row in enumerate(rows):
            for c, val in enumerate(row):
                item = QTableWidgetItem(str(val))
                if c == 4:
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.table.setItem(r, c, item)

    def update_category(self):
        new_cat = self.cat_combo.currentText().strip()
        if not new_cat:
            QMessageBox.warning(self, 'Input Error', 'Please select or enter a category.')
            return
        selected = self.table.selectionModel().selectedRows()
        if not selected:
            QMessageBox.warning(self, 'Selection Error', 'No rows selected.')
            return
        try:
            conn = get_connection()
            cur = conn.cursor()
            for idx in selected:
                row = idx.row()
                sub_desc = self.table.item(row, 2).text()
                pattern = sub_desc.replace('"', '""') + '.*'
                cur.callproc('ADD_SUB_DESCRIPTION_CATEGORY', [pattern, new_cat])
                self.table.item(row, 5).setText(new_cat)
            conn.commit()
            cur.close(); conn.close()
        except Exception as e:
            QMessageBox.critical(self, 'DB Error', f'Failed to update mapping: {e}')
            return
        if self.cat_combo.findText(new_cat) == -1:
            self.cat_combo.addItem(new_cat)
        QMessageBox.information(self, 'Success', 'Category mapping updated.')

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Financial Statement Categorizer')
        self.resize(1000, 700)
        self.setCentralWidget(FinancialsTab(self))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())

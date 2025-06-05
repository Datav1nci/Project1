import os
import sys
import cx_Oracle
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QTableWidget, QTableWidgetItem,
    QComboBox, QPushButton, QMessageBox,
    QHBoxLayout, QVBoxLayout
)
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDateEdit, QLineEdit

# --- Oracle client & environment setup ---
os.environ["TNS_ADMIN"] = r"C:\Users\yberj\Wallet_OWATERDB1"
cx_Oracle.init_oracle_client(lib_dir=r"C:\instantclient_19_5")

# Helper to get a new connection
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
        # Controls: category selection and update button
        ctrl_layout = QHBoxLayout()
        self.cat_combo = QComboBox()
        self.cat_combo.setEditable(True)
        update_btn = QPushButton("Update Category")
        update_btn.clicked.connect(self.update_category)
        ctrl_layout.addWidget(self.cat_combo)
        ctrl_layout.addWidget(update_btn)

        # Financials table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        headers = [
            'Date', 'Description', 'Sub-Description',
            'Type', 'Amount', 'Category', 'ROWID'
        ]
        self.table.setHorizontalHeaderLabels(headers)
        self.table.hideColumn(6)  # hide ROWID
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.MultiSelection)
        self.table.horizontalHeader().setStretchLastSection(True)
        # Enable clickable sorting with visual indicators
        self.table.setSortingEnabled(True)
        self.table.horizontalHeader().setSectionsClickable(True)
        self.table.horizontalHeader().setSortIndicatorShown(True)

        # Layout
        layout = QVBoxLayout(self)
        layout.addLayout(ctrl_layout)
        layout.addWidget(self.table)

    def load_categories(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT DISTINCT CATEGORY FROM SUB_DESCRIPTION_MAPPING ORDER BY CATEGORY")
            cats = [row[0] for row in cur.fetchall()]
            cur.close()
            conn.close()
            self.cat_combo.clear()
            self.cat_combo.addItems(cats)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load categories: {e}")

    def load_financials(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
SELECT 
    t.TRANSACTION_DATE,
    t.DESCRIPTION,
    t.SUB_DESCRIPTION,
    t.TRANSACTION_TYPE,
    t.AMOUNT,
    COALESCE(
        (SELECT m.category 
         FROM SUB_DESCRIPTION_MAPPING m 
         WHERE REGEXP_LIKE(t.SUB_DESCRIPTION, m.pattern)
         AND m.pattern != '\.*' -- Exclude fallback pattern
         AND ROWNUM = 1),
        (SELECT category 
         FROM SUB_DESCRIPTION_MAPPING m 
         WHERE pattern = '\.*') -- Use fallback if no other match
    ) AS CATEGORY
FROM BANK_TRANSACTIONS t order by CATEGORY
""")
            rows = cur.fetchall()
            cur.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load financials: {e}")
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
            QMessageBox.warning(self, "Input Error", "Please select or enter a category.")
            return

        selected = self.table.selectionModel().selectedRows()
        if not selected:
            QMessageBox.warning(self, "Selection Error", "No rows selected.")
            return

        try:
            conn = get_connection()
            cur = conn.cursor()
            for idx in selected:
                row = idx.row()
                sub_desc = self.table.item(row, 2).text()
                pattern = sub_desc.replace('"', '""') + '.*'
                # Call stored procedure to add mapping
                cur.callproc('ADD_SUB_DESCRIPTION_CATEGORY', [pattern, new_cat])
                # Update UI
                self.table.item(row, 5).setText(new_cat)
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "DB Error", f"Failed to update mapping: {e}")
            return

        if self.cat_combo.findText(new_cat) == -1:
            self.cat_combo.addItem(new_cat)
        QMessageBox.information(self, "Success", "Category mapping updated.")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Financial Statement Categorizer")
        self.resize(900, 600)
        self.setCentralWidget(FinancialsTab(self))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())

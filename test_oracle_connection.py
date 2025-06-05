import os
import cx_Oracle

# Set Oracle wallet path and instant client path
os.environ["TNS_ADMIN"] = r"C:\Users\yberj\Wallet_OWATERDB1"
os.environ["CONNECT"] = "OWATERDB1"  # Must match alias in tnsnames.ora 
cx_Oracle.init_oracle_client(lib_dir=r"C:\instantclient_19_5")

# Print environment variables for debugging
print("=== Environment Variables ===")
print("TNS_ADMIN =", os.getenv("TNS_ADMIN"))
print("ORACLE_USER =", os.getenv("ORACLE_USER"))
print("ORACLE_PASSWORD =", os.getenv("ORACLE_PASSWORD"))
print("CONNECT =", os.getenv("CONNECT"))
print("=============================")

# Attempt to connect
try:
    conn = cx_Oracle.connect(
        user=os.getenv("ORACLE_USER"),
        password=os.getenv("ORACLE_PASSWORD"),
        dsn= "owaterdb1_high" #os.getenv("CONNECT")
    )
    print("Connected!", conn.version)
    conn.close()
except cx_Oracle.DatabaseError as e:
    error, = e.args
    print("Oracle-Error-Code:", error.code)
    print("Oracle-Error-Message:", error.message)

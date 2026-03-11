# SQLite → SQL Server Migrator

Herramienta simple en **Python** para migrar bases de datos **SQLite** (.db) a **Microsoft SQL Server** de forma automática.

La aplicación:

- Detecta todas las tablas de SQLite
- Crea las tablas automáticamente en SQL Server
- Convierte tipos de datos básicos
- Inserta los registros en batches para mayor velocidad
- Muestra una barra de progreso durante la migración

---

# Metodo de USO
Create the empty database in SQL Server
![image alt](https://github.com/leandrogallo-dev/img-url-repository/blob/main/1.png?raw=true)

Edit the Python file database name:
  SQL_DATABASE = "master"
  "DATABASE=master;"

Execute the Python file:
  python -u sqlite-to-sqlserver.py <database.db>
![image alt](https://github.com/leandrogallo-dev/img-url-repository/blob/main/2.png?raw=true)

---

# Requisitos

Antes de ejecutar el script debes tener instalado:

- Python 3.8+
- Microsoft SQL Server
- ODBC Driver 17 for SQL Server

---

# Instalación

### 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/TU-USUARIO/sqlite-to-sqlserver-migrator.git
cd sqlite-to-sqlserver-migrator

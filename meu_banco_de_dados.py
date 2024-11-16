import sqlite3

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """Cria a tabela 'pacientes' se não existir."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS pacientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                idade INTEGER,
                contato TEXT
            )
        ''')
        self.conn.commit()

    def insert_patient(self, nome, idade, contato):
        """Insere um paciente na tabela."""
        self.cursor.execute('''
            INSERT INTO pacientes (nome, idade, contato) 
            VALUES (?, ?, ?)
        ''', (nome, idade, contato))
        self.conn.commit()

    def insert_patients(self, patients_data):
        """Insere múltiplos pacientes na tabela."""
        self.cursor.executemany('''
            INSERT INTO pacientes (nome, idade, contato) 
            VALUES (?, ?, ?)
        ''', patients_data)
        self.conn.commit()

    def fetch_patients(self):
        """Recupera todos os pacientes."""
        self.cursor.execute('SELECT * FROM pacientes')
        return self.cursor.fetchall()

    def close(self):
        """Fecha a conexão com o banco de dados."""
        self.conn.close()

def get_database():
    """Retorna uma nova instância do banco de dados."""
    return Database('meu_banco_de_dados.db')

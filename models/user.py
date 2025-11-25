from database import criar_conexao

class User:

    def __init__(self, id=None, nome=None, email=None, senha=None):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha

    # CREATE
    def save(self):
       
        con = criar_conexao()
        cursor = con.cursor()
        cursor.execute("""
        INSERT INTO users (nome, email, senha)
        VALUES (?, ?, ?)
    """, (self.nome, self.email, self.senha))
        con.commit()

        print("Usuário salvo no banco:", self.nome, self.email)

        con.close()

    # READ ALL
    @staticmethod
    def get_all():
        con = criar_conexao()
        cursor = con.cursor()
        cursor.execute("SELECT id, nome, email, senha FROM users")
        rows = cursor.fetchall()
        con.close()
        return [User(*row) for row in rows]

    # READ ONE
    @staticmethod
    def get(user_id):
        con = criar_conexao()
        cursor = con.cursor()
        cursor.execute("SELECT id, nome, email, senha FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        con.close()
        return User(*row) if row else None

    # READ BY EMAIL
    @staticmethod
    def get_by_email(email):
        con = criar_conexao()
        cursor = con.cursor()
        cursor.execute("SELECT id, nome, email, senha FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        con.close()
        return User(*row) if row else None

    # UPDATE
    def update(self):
        con = criar_conexao()
        cursor = con.cursor()
        cursor.execute("""
            UPDATE users
            SET nome = ?, email = ?, senha = ?
            WHERE id = ?
        """, (self.nome, self.email, self.senha, self.id))
        con.commit()
        con.close()

    # DELETE
    @staticmethod
    def delete(user_id):
        con = criar_conexao()
        cursor = con.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        con.commit()
        con.close()

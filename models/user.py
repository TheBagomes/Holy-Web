from database import criar_conexao

class User:

    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha

    def save(self):
        con = criar_conexao()
        cursor = con.cursor()
        cursor.execute(
            "INSERT INTO users (nome, email, senha) VALUES (?, ?, ?)",
            (self.nome, self.email, self.senha)
        )
        con.commit()
        con.close()

    @staticmethod
    def get_by_email(email):
        con = criar_conexao()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        con.close()
        return user

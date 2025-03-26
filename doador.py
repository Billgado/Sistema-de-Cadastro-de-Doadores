import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

# Função para conectar ao banco e obter informações do doador
def verificar_doador():
    cpf = entry_cpf.get().strip()
    senha = entry_senha.get().strip()
    
    if not cpf or not senha:
        messagebox.showwarning("Erro", "Por favor, preencha todos os campos!")
        return

    try:
        # Conexão com o banco de dados
        conn = sqlite3.connect('banco_de_sangue.db')
        cursor = conn.cursor()

        # Consulta ao banco de dados incluindo nome e data_nascimento
        cursor.execute("""
            SELECT nome, data_nascimento, cpf, email, telefone, cep, numero_casa, data_cadastro, tipo_sanguineo, senha, apto
            FROM doadores
            WHERE cpf = ? AND senha = ?
        """, (cpf, senha))
        
        dados = cursor.fetchone()
        conn.close()

        if dados:
            exibir_informacoes_doador(dados)
        else:
            messagebox.showerror("Erro", "CPF ou senha incorretos. Tente novamente.")

    except sqlite3.Error as e:
        messagebox.showerror("Erro de Banco de Dados", f"Ocorreu um erro ao acessar o banco de dados: {e}")

# Função para exibir as informações do doador
def exibir_informacoes_doador(dados):
    nome = dados[0]
    data_nascimento = dados[1]
    apto = dados[10]
    
    # Ajusta o cálculo da idade para o formato correto da data de nascimento
    data_nascimento = datetime.strptime(data_nascimento, "%d/%m/%Y")
    hoje = datetime.now()
    idade = hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))
    
    # Criando a janela de informações do doador
    info_window = tk.Toplevel(app)
    info_window.title("Informações do Doador")
    info_window.geometry("400x500")
    info_window.configure(bg="#2F2F2F")
    
    # Exibindo as informações do doador
    tk.Label(info_window, text="Informações do Doador", font=("Arial", 14, "bold"), bg="#2F2F2F", fg="white").pack(pady=10)
    tk.Label(info_window, text=f"Nome: {nome}", bg="#2F2F2F", fg="white").pack(pady=5)
    tk.Label(info_window, text=f"Idade: {idade} anos", bg="#2F2F2F", fg="white").pack(pady=5)
    tk.Label(info_window, text=f"CPF: {dados[2]}", bg="#2F2F2F", fg="white").pack(pady=5)
    tk.Label(info_window, text=f"Email: {dados[3]}", bg="#2F2F2F", fg="white").pack(pady=5)
    tk.Label(info_window, text=f"Telefone: {dados[4]}", bg="#2F2F2F", fg="white").pack(pady=5)
    tk.Label(info_window, text=f"CEP: {dados[5]}", bg="#2F2F2F", fg="white").pack(pady=5)
    tk.Label(info_window, text=f"Número da Casa: {dados[6]}", bg="#2F2F2F", fg="white").pack(pady=5)
    tk.Label(info_window, text=f"Data de Cadastro: {dados[7]}", bg="#2F2F2F", fg="white").pack(pady=5)
    tk.Label(info_window, text=f"Tipo Sanguíneo: {dados[8]}", bg="#2F2F2F", fg="white").pack(pady=5)
    
    # Exibe o status de aptidão
    if apto == "sim":
        tk.Label(info_window, text="Status de Aptidão: Apto para Doar", font=("Arial", 12, "bold"), bg="lightgreen", fg="green").pack(pady=10)
    elif apto == "não":
        tk.Label(info_window, text="Status de Aptidão: Inapto para Doar", font=("Arial", 12, "bold"), bg="red", fg="white").pack(pady=10)
    else:
        tk.Label(info_window, text="Status de Aptidão: Aptidão Futuramente", bg="#2F2F2F", fg="white").pack(pady=10)

# Interface principal do aplicativo
app = tk.Tk()
app.title("Verificação de Aptidão")
app.geometry("400x300")
app.configure(bg="#2F2F2F")

# Campos de entrada e botão
tk.Label(app, text="CPF:", bg="#2F2F2F", fg="white").pack(pady=10)
entry_cpf = tk.Entry(app)
entry_cpf.pack(pady=5)

tk.Label(app, text="Senha:", bg="#2F2F2F", fg="white").pack(pady=10)
entry_senha = tk.Entry(app, show="*")
entry_senha.pack(pady=5)

tk.Button(app, text="Verificar Aptidão", command=verificar_doador, bg="#FF6666", fg="white").pack(pady=20)

# Executar o aplicativo
app.mainloop()
import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

# Função para conectar ao banco e obter informações do doador
def verificar_doador():
    cpf = entry_cpf.get().strip()
    senha = entry_senha.get().strip()
    
    if not cpf or not senha:
        messagebox.showwarning("Erro", "Por favor, preencha todos os campos!")
        return

    try:
        # Conexão com o banco de dados
        conn = sqlite3.connect('banco_de_sangue.db')
        cursor = conn.cursor()

        # Consulta ao banco de dados incluindo nome e data_nascimento
        cursor.execute("""
            SELECT nome, data_nascimento, cpf, email, telefone, cep, numero_casa, data_cadastro, tipo_sanguineo, senha, apto
            FROM doadores
            WHERE cpf = ? AND senha = ?
        """, (cpf, senha))
        
        dados = cursor.fetchone()
        conn.close()

        if dados:
            exibir_informacoes_doador(dados)
        else:
            messagebox.showerror("Erro", "CPF ou senha incorretos. Tente novamente.")

    except sqlite3.Error as e:
        messagebox.showerror("Erro de Banco de Dados", f"Ocorreu um erro ao acessar o banco de dados: {e}")

# Função para exibir as informações do doador
def exibir_informacoes_doador(dados):
    nome = dados[0]
    data_nascimento = dados[1]
    apto = dados[10]
    
    # Ajusta o cálculo da idade para o formato correto da data de nascimento
    data_nascimento = datetime.strptime(data_nascimento, "%d/%m/%Y")
    hoje = datetime.now()
    idade = hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))
    
    # Criando a janela de informações do doador
    info_window = tk.Toplevel(app)
    info_window.title("Informações do Doador")
    info_window.geometry("400x500")
    info_window.configure(bg="#2F2F2F")
    
    # Exibindo as informações do doador
    tk.Label(info_window, text="Informações do Doador", font=("Arial", 14, "bold"), bg="#2F2F2F", fg="white").pack(pady=10)
    tk.Label(info_window, text=f"Nome: {nome}", bg="#2F2F2F", fg="white").pack(pady=5)
    tk.Label(info_window, text=f"Idade: {idade} anos", bg="#2F2F2F", fg="white").pack(pady=5)
    tk.Label(info_window, text=f"CPF: {dados[2]}", bg="#2F2F2F", fg="white").pack(pady=5)
    tk.Label(info_window, text=f"Email: {dados[3]}", bg="#2F2F2F", fg="white").pack(pady=5)
    tk.Label(info_window, text=f"Telefone: {dados[4]}", bg="#2F2F2F", fg="white").pack(pady=5)
    tk.Label(info_window, text=f"CEP: {dados[5]}", bg="#2F2F2F", fg="white").pack(pady=5)
    tk.Label(info_window, text=f"Número da Casa: {dados[6]}", bg="#2F2F2F", fg="white").pack(pady=5)
    tk.Label(info_window, text=f"Data de Cadastro: {dados[7]}", bg="#2F2F2F", fg="white").pack(pady=5)
    tk.Label(info_window, text=f"Tipo Sanguíneo: {dados[8]}", bg="#2F2F2F", fg="white").pack(pady=5)
    
    # Exibe o status de aptidão
    if apto == "sim":
        tk.Label(info_window, text="Status de Aptidão: Apto para Doar", font=("Arial", 12, "bold"), bg="lightgreen", fg="green").pack(pady=10)
    elif apto == "não":
        tk.Label(info_window, text="Status de Aptidão: Inapto para Doar", font=("Arial", 12, "bold"), bg="red", fg="white").pack(pady=10)
    else:
        tk.Label(info_window, text="Status de Aptidão: Aptidão Futuramente", bg="#2F2F2F", fg="white").pack(pady=10)

# Interface principal do aplicativo
app = tk.Tk()
app.title("Verificação de Aptidão")
app.geometry("400x300")
app.configure(bg="#2F2F2F")

# Campos de entrada e botão
tk.Label(app, text="CPF:", bg="#2F2F2F", fg="white").pack(pady=10)
entry_cpf = tk.Entry(app)
entry_cpf.pack(pady=5)

tk.Label(app, text="Senha:", bg="#2F2F2F", fg="white").pack(pady=10)
entry_senha = tk.Entry(app, show="*")
entry_senha.pack(pady=5)

tk.Button(app, text="Verificar Aptidão", command=verificar_doador, bg="#FF6666", fg="white").pack(pady=20)

# Executar o aplicativo
app.mainloop()

import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta
import sqlite3
import random
import string
import pyperclip

# Função para gerar senha aleatória
def gerar_senha():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

# Função para criar a tabela doadores no banco de dados
def criar_tabela():
    conn = sqlite3.connect('banco_de_sangue.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS doadores (
        cpf TEXT PRIMARY KEY,
        nome TEXT,
        data_nascimento TEXT,
        idade INTEGER,
        email TEXT,
        telefone TEXT,
        cep TEXT,
        numero_casa TEXT,
        data_cadastro TEXT,
        tipo_sanguineo TEXT,
        senha TEXT,
        apto TEXT
    )
    ''')
    conn.commit()
    conn.close()

# Função para calcular restrições temporárias
def calcular_restricoes_temporarias(condicoes):
    restricoes = {
        'Febre ou infecção recente': timedelta(days=7),
        'Gripes e resfriados': timedelta(days=7),
        'Uso de Antibióticos': timedelta(days=7),
        'Uso de Antiinflamatórios': timedelta(days=2),
        'Cirurgias de pequeno porte': timedelta(days=180),
        'Cirurgias de grande porte': timedelta(days=365),
        'Vacina contra a febre amarela': timedelta(weeks=4),
        'Vacinas de vírus vivos atenuados': timedelta(weeks=4),
        'Viagens para áreas endêmicas': timedelta(days=180),
        'Tatuagens, piercings e acupuntura': timedelta(days=180),
        'Gestação e amamentação': timedelta(days=180),
        'Endoscopia e outros exames invasivos': timedelta(days=180),
        'Transfusão de sangue': timedelta(days=365),
        'Exposição a doenças transmissíveis': timedelta(days=365)
    }

    result = []
    for condicao, marcado in condicoes.items():
        if marcado.get():
            prazo = restricoes[condicao]
            data_permitida = datetime.today() + prazo
            result.append(f'{condicao}: Pode doar a partir de {data_permitida.strftime("%d/%m/%Y")}')
    
    return result

# Função para verificar as restrições permanentes
def verificar_restricoes_permanentes(condicoes):
    restricoes_permanentes = [
        'Doenças crônicas graves',
        'Histórico de câncer',
        'Doenças autoimunes',
        'Doenças infecciosas crônicas',
        'Uso de drogas injetáveis ilícitas',
        'Comportamentos de risco elevado',
        'Recebimento de transplante de órgãos ou de medula óssea',
        'Malária',
        'Doenças neurodegenerativas'
    ]
    return any(condicoes[condicao].get() for condicao in restricoes_permanentes)

# Função para exibir mensagem de aptidão em verde
def mostrar_mensagem_aptidao(senha, apto):
    apto_window = tk.Toplevel(app)
    apto_window.title("Apto para Doar!")
    apto_window.geometry("300x200")
    apto_window.configure(bg="lightgreen")
    label_msg = tk.Label(apto_window, text=f"Parabéns! Você está apto para doar!", font=("Arial", 14, "bold"), fg="green", bg="lightgreen")
    label_msg.pack(expand=True, pady=10)
    label_senha = tk.Label(apto_window, text=f"Sua senha é: {senha}", font=("Arial", 12), bg="lightgreen")
    label_senha.pack(expand=True, pady=10)
    tk.Button(apto_window, text="Fechar", command=apto_window.destroy).pack(pady=10)
    copiar_para_area_de_transferencia(senha)

# Função para responder sobre as restrições
def responder_restricoes(senha):
    window = tk.Toplevel(app)
    window.title("Restrições Temporárias e Permanentes")
    window.geometry("550x700")
    window.configure(bg="#2F2F2F")

    # Checkbuttons para restrições temporárias e permanentes
    frame_temp = tk.Frame(window, bg="#2F2F2F")
    frame_temp.pack(pady=10)
    
    condicoes_temp = {
        'Febre ou infecção recente': tk.BooleanVar(),
        'Gripes e resfriados': tk.BooleanVar(),
        'Uso de Antibióticos': tk.BooleanVar(),
        'Uso de Antiinflamatórios': tk.BooleanVar(),
        'Cirurgias de pequeno porte': tk.BooleanVar(),
        'Cirurgias de grande porte': tk.BooleanVar(),
        'Vacina contra a febre amarela': tk.BooleanVar(),
        'Vacinas de vírus vivos atenuados': tk.BooleanVar(),
        'Viagens para áreas endêmicas': tk.BooleanVar(),
        'Tatuagens, piercings e acupuntura': tk.BooleanVar(),
        'Gestação e amamentação': tk.BooleanVar(),
        'Endoscopia e outros exames invasivos': tk.BooleanVar(),
        'Transfusão de sangue': tk.BooleanVar(),
        'Exposição a doenças transmissíveis': tk.BooleanVar()
    }
    
    condicoes_perm = {
        'Doenças crônicas graves': tk.BooleanVar(),
        'Histórico de câncer': tk.BooleanVar(),
        'Doenças autoimunes': tk.BooleanVar(),
        'Doenças infecciosas crônicas': tk.BooleanVar(),
        'Uso de drogas injetáveis ilícitas': tk.BooleanVar(),
        'Comportamentos de risco elevado': tk.BooleanVar(),
        'Recebimento de transplante de órgãos ou de medula óssea': tk.BooleanVar(),
        'Malária': tk.BooleanVar(),
        'Doenças neurodegenerativas': tk.BooleanVar()
    }
    
    tk.Label(frame_temp, text="Restrições Temporárias", bg="#2F2F2F", fg="#FF6666", font=("Arial", 10, "bold")).pack(anchor=tk.W)
    for condicao, var in condicoes_temp.items():
        tk.Checkbutton(frame_temp, text=condicao, variable=var, bg="#2F2F2F", fg="white", selectcolor="#FF6666").pack(anchor=tk.W)
    
    tk.Label(frame_temp, text="Restrições Permanentes", bg="#2F2F2F", fg="#FF6666", font=("Arial", 10, "bold")).pack(anchor=tk.W)
    for condicao, var in condicoes_perm.items():
        tk.Checkbutton(frame_temp, text=condicao, variable=var, bg="#2F2F2F", fg="white", selectcolor="#FF6666").pack(anchor=tk.W)

    def confirmar_restricoes(senha):
        if verificar_restricoes_permanentes(condicoes_perm):
            apto = "não"
            messagebox.showwarning("Restrições Permanentes", "Você possui restrições permanentes e não pode doar sangue.")
            salvar_doador(cpf, nome, data_nascimento, idade, email, telefone, cep, numero_casa, data_cadastro, tipo_sanguineo, senha, apto)
            window.destroy()
            return

        resultado_temp = calcular_restricoes_temporarias(condicoes_temp)
        if resultado_temp:
            apto = "fapto"  # Futuro apto
            messagebox.showinfo("Restrições Temporárias", "\n".join(resultado_temp))
        else:
            apto = "sim"  # Apto
            mostrar_mensagem_aptidao(senha, apto)  # Exibe mensagem verde se o doador está apto
        
        # Salvar no banco de dados
        salvar_doador(cpf, nome, data_nascimento, idade, email, telefone, cep, numero_casa, data_cadastro, tipo_sanguineo, senha, apto)
        window.destroy()
    
    tk.Button(window, text="Confirmar", command=lambda: confirmar_restricoes(senha), bg="#FF6666", fg="white").pack(pady=10)

# Função para calcular a idade a partir da data de nascimento
def calcular_idade(data_nascimento):
    data_nascimento = datetime.strptime(data_nascimento, "%d/%m/%Y")
    hoje = datetime.today()
    idade = hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))
    return idade

# Função para salvar ou atualizar doador no banco de dados
def salvar_doador(cpf, nome, data_nascimento, idade, email, telefone, cep, numero_casa, data_cadastro, tipo_sanguineo, senha, apto):
    conn = sqlite3.connect('banco_de_sangue.db')
    cursor = conn.cursor()
    
    # Verifica se o CPF já está cadastrado
    cursor.execute("SELECT * FROM doadores WHERE cpf = ?", (cpf,))
    existe = cursor.fetchone()
    
    try:
        if existe:
            # Atualiza os dados do doador existente
            cursor.execute('''
                UPDATE doadores 
                SET nome = ?, data_nascimento = ?, idade = ?, email = ?, telefone = ?, 
                    cep = ?, numero_casa = ?, data_cadastro = ?, tipo_sanguineo = ?, 
                    senha = ?, apto = ?
                WHERE cpf = ?
            ''', (nome, data_nascimento, idade, email, telefone, cep, numero_casa, data_cadastro, tipo_sanguineo, senha, apto, cpf))
            conn.commit()
            messagebox.showinfo("Atualização Completa", "Cadastro atualizado com sucesso! Nova senha gerada e copiada.")
        else:
            # Insere novo doador
            cursor.execute('''
                INSERT INTO doadores (cpf, nome, data_nascimento, idade, email, telefone, cep, numero_casa, data_cadastro, tipo_sanguineo, senha, apto)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (cpf, nome, data_nascimento, idade, email, telefone, cep, numero_casa, data_cadastro, tipo_sanguineo, senha, apto))
            conn.commit()
            messagebox.showinfo("Cadastro Completo", "Doador cadastrado com sucesso!")
        
        copiar_para_area_de_transferencia(senha)
    
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
    finally:
        conn.close()


# Função para copiar senha para a área de transferência
def copiar_para_area_de_transferencia(senha):
    pyperclip.copy(senha)
    messagebox.showinfo("Senha Copiada", "A senha foi copiada para a área de transferência!")

# Função para cadastrar doador
def cadastrar_doador():
    global cpf, nome, data_nascimento, idade, email, telefone, cep, numero_casa, data_cadastro, tipo_sanguineo  # Variáveis globais para acesso na função responder_restricoes
    cpf = entry_cpf.get()
    nome = entry_nome.get()
    data_nascimento = entry_data_nascimento.get()
    idade = calcular_idade(data_nascimento)
    email = entry_email.get()
    telefone = entry_telefone.get()
    cep = entry_cep.get()
    numero_casa = entry_numero.get()
    data_cadastro = datetime.today().strftime("%d/%m/%Y")
    tipo_sanguineo = var_tipo_sanguineo.get()
    senha = gerar_senha()
    
    if any([cpf == "", nome == "", data_nascimento == "", email == "", telefone == "", cep == "", numero_casa == "", tipo_sanguineo == ""]):
        messagebox.showwarning("Erro", "Todos os campos devem ser preenchidos!")
        return
    
    # Chama a função para verificar restrições antes de cadastrar
    responder_restricoes(senha)

# Interface principal
app = tk.Tk()
app.title("Cadastro de Doadores")
app.geometry("400x600")
app.configure(bg="#2F2F2F")

# Componentes da interface com tema
tk.Label(app, text="CPF:", bg="#2F2F2F", fg="white").pack(pady=5)
entry_cpf = tk.Entry(app)
entry_cpf.pack(pady=5)

tk.Label(app, text="Nome:", bg="#2F2F2F", fg="white").pack(pady=5)
entry_nome = tk.Entry(app)
entry_nome.pack(pady=5)

tk.Label(app, text="Data de Nascimento (dd/mm/yyyy):", bg="#2F2F2F", fg="white").pack(pady=5)
entry_data_nascimento = tk.Entry(app)
entry_data_nascimento.pack(pady=5)

tk.Label(app, text="Email:", bg="#2F2F2F", fg="white").pack(pady=5)
entry_email = tk.Entry(app)
entry_email.pack(pady=5)

tk.Label(app, text="Telefone:", bg="#2F2F2F", fg="white").pack(pady=5)
entry_telefone = tk.Entry(app)
entry_telefone.pack(pady=5)

tk.Label(app, text="CEP:", bg="#2F2F2F", fg="white").pack(pady=5)
entry_cep = tk.Entry(app)
entry_cep.pack(pady=5)

tk.Label(app, text="Número da Casa:", bg="#2F2F2F", fg="white").pack(pady=5)
entry_numero = tk.Entry(app)
entry_numero.pack(pady=5)

tk.Label(app, text="Tipo Sanguíneo:", bg="#2F2F2F", fg="white").pack(pady=5)
var_tipo_sanguineo = tk.StringVar(app)
var_tipo_sanguineo.set("")  # valor padrão vazio
tipo_sanguineo_opcoes = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
ttk.Combobox(app, textvariable=var_tipo_sanguineo, values=tipo_sanguineo_opcoes).pack(pady=5)

# Botão para cadastrar doador
tk.Button(app, text="Cadastrar Doador", command=cadastrar_doador, bg="#FF6666", fg="white").pack(pady=15)

# Inicializa a tabela do banco de dados
criar_tabela()

# Iniciar a interface
app.mainloop()

import tkinter as tk
from tkinter import messagebox, ttk

# Função para calcular os valores de fri
def calcular_fri():
    try:
        k = int(entry_k.get())  # Obtém o valor de k
        if k <= 0:
            messagebox.showerror("Erro", "O valor de k deve ser maior que zero!")
            return

        # Limpa a lista de entradas de fi, se houver
        for widget in frame_fi.winfo_children():
            widget.destroy()

        # Criando um canvas com barra de rolagem
        canvas_fi = tk.Canvas(frame_fi, bg="#2d2d2d", highlightthickness=0)
        scrollbar_fi = ttk.Scrollbar(frame_fi, orient="vertical", command=canvas_fi.yview)
        scrollable_frame_fi = tk.Frame(canvas_fi, bg="#2d2d2d")

        scrollable_frame_fi.bind("<Configure>", lambda e: canvas_fi.configure(scrollregion=canvas_fi.bbox("all")))

        canvas_fi.create_window((0, 0), window=scrollable_frame_fi, anchor="center")
        canvas_fi.configure(yscrollcommand=scrollbar_fi.set)

        canvas_fi.pack(side="left", fill="both", expand=True)
        scrollbar_fi.pack(side="right", fill="y")

        # Lista para armazenar os campos de entrada
        global entries_fi
        entries_fi = []
        for i in range(1, k + 1):
            frame_item = tk.Frame(scrollable_frame_fi, bg="#2d2d2d")
            frame_item.pack(pady=5)

            label = tk.Label(frame_item, text=f"Digite o valor de fi{i}:", bg="#2d2d2d", fg="white")
            label.pack(side="left", padx=5)
            
            entry = tk.Entry(frame_item, bg="#3d3d3d", fg="white", insertbackground="white", justify="center")
            entry.pack(side="left")
            entries_fi.append(entry)

        # Botão para calcular os resultados
        botao_calcular = tk.Button(scrollable_frame_fi, text="Calcular", bg="#4CAF50", fg="white", command=exibir_resultados)
        botao_calcular.pack(pady=20)

    except ValueError:
        messagebox.showerror("Erro", "O valor de k deve ser um número inteiro!")

# Função para exibir os resultados em uma tabela
def exibir_resultados():
    try:
        fi = [float(entry.get()) for entry in entries_fi]  # Obtém os valores de fi
        somatoria_fi = sum(fi)  # Calcula a soma dos valores de fi

        # Limpa a área de resultados
        for widget in frame_resultados.winfo_children():
            widget.destroy()

        # Criando a tabela com Treeview
        colunas = ("fi", "fri", "%fri", "Graus fri", "Fi", "Fri", "%Fri", "Graus Fri")
        tabela = ttk.Treeview(frame_resultados, columns=colunas, show="headings", height=10)

        # Definindo os cabeçalhos das colunas
        for coluna in colunas:
            tabela.heading(coluna, text=coluna)
            tabela.column(coluna, width=80, anchor="center")

        # Adicionando uma barra de rolagem vertical
        scrollbar_tabela = ttk.Scrollbar(frame_resultados, orient="vertical", command=tabela.yview)
        tabela.configure(yscrollcommand=scrollbar_tabela.set)

        # Posicionando a tabela e a barra de rolagem
        tabela.pack(side="left", fill="both", expand=True)
        scrollbar_tabela.pack(side="right", fill="y")

        # Preenchendo a tabela com os resultados
        frequencia_acumulada = 0
        frequencia_acumulada_fi = 0  # Fi da frequência acumulada
        for i in range(len(fi)):
            fri = fi[i] / somatoria_fi
            percent_fri = fri * 100
            graus_fri = fri * 360

            # Cálculo da frequência acumulada (Fai)
            frequencia_acumulada += fri
            percent_fai = frequencia_acumulada * 100  # Porcentagem da frequência acumulada
            graus_fai = frequencia_acumulada * 360  # Graus da frequência acumulada

            # Cálculo do Fi da frequência acumulada
            frequencia_acumulada_fi += fi[i]

            # Adicionando os valores na tabela
            tabela.insert("", "end", values=(
                f"{fi[i]:.2f}",
                f"{fri:.4f}",
                f"{percent_fri:.2f}%",
                f"{graus_fri:.2f}°",
                f"{frequencia_acumulada_fi:.2f}",
                f"{frequencia_acumulada:.4f}",
                f"{percent_fai:.2f}%",
                f"{graus_fai:.2f}°"
            ))

    except ValueError:
        messagebox.showerror("Erro", "Todos os valores de fi devem ser números!")

# Configuração da janela principal
root = tk.Tk()
root.title("Cálculo de FRI")
root.geometry("800x600")
root.configure(bg="#2d2d2d")

# Centralizar a janela na tela
largura_janela = 800
altura_janela = 600
largura_tela = root.winfo_screenwidth()
altura_tela = root.winfo_screenheight()
x = (largura_tela - largura_janela) // 2
y = (altura_tela - altura_janela) // 2
root.geometry(f"{largura_janela}x{altura_janela}+{x}+{y}")

# Frame para o valor de k
frame_k = tk.Frame(root, bg="#2d2d2d")
frame_k.pack(pady=20)

label_k = tk.Label(frame_k, text="Digite o valor de k:", bg="#2d2d2d", fg="white")
label_k.pack(pady=5)

entry_k = tk.Entry(frame_k, bg="#3d3d3d", fg="white", insertbackground="white", justify="center")
entry_k.pack(pady=5)

botao_confirmar_k = tk.Button(frame_k, text="Confirmar", bg="#4CAF50", fg="white", command=calcular_fri)
botao_confirmar_k.pack(pady=10)

# Frame para os valores de fi (com barra de rolagem)
frame_fi = tk.Frame(root, bg="#2d2d2d", height=250)
frame_fi.pack(pady=20, fill="both", expand=True)

# Frame para os resultados (com barra de rolagem)
frame_resultados = tk.Frame(root, bg="#2d2d2d", height=250)
frame_resultados.pack(pady=20, fill="both", expand=True)

# Executar a aplicação
root.mainloop()
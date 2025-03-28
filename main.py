import tkinter as tk
from tkinter import messagebox, ttk

# Variáveis globais
entries_fi = []
entry_h = None
entry_li_inicial = None
tabela = None  # Variável global para a tabela

def calcular_fri():
    try:
        k = int(entry_k.get())
        if k <= 0:
            messagebox.showerror("Erro", "O valor de k deve ser maior que zero!")
            return

        for widget in frame_fi.winfo_children():
            widget.destroy()

        canvas_fi = tk.Canvas(frame_fi, bg="#2d2d2d", highlightthickness=0)
        scrollbar_fi = ttk.Scrollbar(frame_fi, orient="vertical", command=canvas_fi.yview)
        scrollable_frame_fi = tk.Frame(canvas_fi, bg="#2d2d2d")

        scrollable_frame_fi.bind("<Configure>", lambda e: canvas_fi.configure(scrollregion=canvas_fi.bbox("all")))
        canvas_fi.create_window((0, 0), window=scrollable_frame_fi, anchor="center")
        canvas_fi.configure(yscrollcommand=scrollbar_fi.set)

        canvas_fi.pack(side="left", fill="both", expand=True)
        scrollbar_fi.pack(side="right", fill="y")

        frame_parametros = tk.Frame(scrollable_frame_fi, bg="#2d2d2d")
        frame_parametros.pack(pady=10)

        label_h = tk.Label(frame_parametros, text="Amplitude (h):", bg="#2d2d2d", fg="white")
        label_h.pack(side="left", padx=5)
        
        global entry_h
        entry_h = tk.Entry(frame_parametros, bg="#3d3d3d", fg="white", insertbackground="white", justify="center", width=10)
        entry_h.pack(side="left", padx=5)

        label_li = tk.Label(frame_parametros, text="Li inicial:", bg="#2d2d2d", fg="white")
        label_li.pack(side="left", padx=5)
        
        global entry_li_inicial
        entry_li_inicial = tk.Entry(frame_parametros, bg="#3d3d3d", fg="white", insertbackground="white", justify="center", width=10)
        entry_li_inicial.pack(side="left", padx=5)

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

        botao_calcular = tk.Button(scrollable_frame_fi, text="Calcular", bg="#4CAF50", fg="white", command=exibir_resultados)
        botao_calcular.pack(pady=20)

    except ValueError:
        messagebox.showerror("Erro", "O valor de k deve ser um número inteiro!")

def copiar_tabela():
    if tabela is None:
        messagebox.showwarning("Aviso", "Nenhuma tabela para copiar!")
        return
    
    # Obter todos os itens da tabela
    dados = []
    
    # Adicionar cabeçalhos
    cabecalhos = [tabela.heading(col)["text"] for col in tabela["columns"]]
    dados.append("\t".join(cabecalhos))
    
    # Adicionar linhas de dados
    for child in tabela.get_children():
        valores = [tabela.item(child)["values"][i] for i in range(len(tabela["columns"]))]
        dados.append("\t".join(map(str, valores)))
    
    # Juntar tudo com quebras de linha
    texto_copiado = "\n".join(dados)
    
    # Copiar para a área de transferência
    root.clipboard_clear()
    root.clipboard_append(texto_copiado)
    root.update()  # Necessário para garantir que a cópia seja mantida
    
    messagebox.showinfo("Sucesso", "Tabela copiada para a área de transferência!\nAgora você pode colar no Excel ou em outro programa.")

def exibir_resultados():
    try:
        fi = [float(entry.get()) for entry in entries_fi]
        somatoria_fi = sum(fi)
        h = float(entry_h.get())
        li_inicial = float(entry_li_inicial.get())

        # Limpa o frame de resultados completamente
        for widget in frame_resultados.winfo_children():
            widget.destroy()

        # Frame principal para tabela e medidas
        frame_principal = tk.Frame(frame_resultados, bg="#2d2d2d")
        frame_principal.pack(fill="both", expand=True)

        # Frame para o botão de copiar (no canto superior direito)
        frame_botoes = tk.Frame(frame_principal, bg="#2d2d2d")
        frame_botoes.pack(fill="x", padx=10, pady=5, anchor="ne")

        botao_copiar = tk.Button(
            frame_botoes, 
            text="Copiar Tabela", 
            bg="#2196F3", 
            fg="white", 
            command=copiar_tabela
        )
        botao_copiar.pack(side="right")

        # Frame para a tabela
        frame_tabela = tk.Frame(frame_principal, bg="#2d2d2d")
        frame_tabela.pack(fill="both", expand=True)

        # Criando a tabela
        colunas = ("i", "AIC/AID", "xi", "fi", "fi.xi", "fri", "%fri", "Graus fri", "Fi", "Fri", "%Fri", "Graus Fri")
        global tabela
        tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings", height=10)

        for coluna in colunas:
            tabela.heading(coluna, text=coluna)
            tabela.column(coluna, width=80, anchor="center")

        tabela.column("AIC/AID", width=120)
        tabela.column("xi", width=80)
        tabela.column("fi.xi", width=80)

        scrollbar_tabela = ttk.Scrollbar(frame_tabela, orient="vertical", command=tabela.yview)
        tabela.configure(yscrollcommand=scrollbar_tabela.set)

        tabela.pack(side="left", fill="both", expand=True)
        scrollbar_tabela.pack(side="right", fill="y")

        somatoria_fi_xi = 0
        frequencia_acumulada = 0
        frequencia_acumulada_fi = 0
        dados = []  # Armazenar dados para cálculos posteriores

        for i in range(len(fi)):
            li = li_inicial + i * h
            ls = li + h
            xi = (li + ls) / 2
            intervalo = f"{li} - {ls}"

            fi_xi = fi[i] * xi
            somatoria_fi_xi += fi_xi

            fri = fi[i] / somatoria_fi
            percent_fri = fri * 100
            graus_fri = fri * 360

            frequencia_acumulada += fri  # Acumula as frequências relativas
            percent_fai = frequencia_acumulada * 100
            graus_fai = frequencia_acumulada * 360

            frequencia_acumulada_fi += fi[i]

            tabela.insert("", "end", values=(
                i+1,
                intervalo,
                f"{xi:.2f}",
                f"{fi[i]:.2f}",
                f"{fi_xi:.2f}",
                f"{fri:.3f}",
                f"{percent_fri:.2f}%",
                f"{graus_fri:.2f}°",
                f"{frequencia_acumulada_fi:.2f}",
                f"{frequencia_acumulada:.3f}",
                f"{percent_fai:.2f}%",
                f"{graus_fai:.2f}°"
            ))

            # Armazenar dados para cálculos de moda e mediana
            dados.append({
                'li': li,
                'fi': fi[i],
                'Fi': frequencia_acumulada_fi,
                'xi': xi
            })

        # Linha da somatória
        tabela.insert("", "end", values=(
            "",
            "",
            "",
            f"{somatoria_fi:.2f}",
            f"{somatoria_fi_xi:.2f}",
            "",
            "",
            "",
            "",
            "",
            "",
            ""
        ))

        # Cálculo da Média (ME)
        ME = somatoria_fi_xi / somatoria_fi

        # Cálculo da Moda (MO)
        # Encontrar classe modal (maior fi)
        classe_modal = max(dados, key=lambda x: x['fi'])
        index_modal = dados.index(classe_modal)
        
        # Calcular D1 e D2
        fi_modal = classe_modal['fi']
        f_anterior = dados[index_modal-1]['fi'] if index_modal > 0 else 0
        f_posterior = dados[index_modal+1]['fi'] if index_modal < len(dados)-1 else 0
        
        D1 = fi_modal - f_anterior
        D2 = fi_modal - f_posterior
        
        MO = classe_modal['li'] + (D1/(D1+D2)) * h if (D1+D2) != 0 else classe_modal['li']

        # Cálculo da Mediana (MD)
        # Encontrar classe mediana (onde Fi >= n/2)
        n_meio = somatoria_fi / 2
        classe_mediana = None
        Fi_anterior = 0
        
        for i, dado in enumerate(dados):
            if dado['Fi'] >= n_meio:
                classe_mediana = dado
                if i > 0:
                    Fi_anterior = dados[i-1]['Fi']
                break
        
        if classe_mediana:
            MD = classe_mediana['li'] + ((n_meio - Fi_anterior) / classe_mediana['fi']) * h
        else:
            MD = 0

        # Frame para as medidas (ME, MO, MD)
        frame_medidas = tk.Frame(frame_principal, bg="#2d2d2d", pady=10)
        frame_medidas.pack(fill="x")

        # Configuração do estilo para os labels das medidas
        estilo_medida = {
            'bg': '#2d2d2d',
            'fg': 'white',
            'font': ('Arial', 12, 'bold'),
            'padx': 20,
            'pady': 10
        }

        # Média
        label_me = tk.Label(frame_medidas, text=f"MÉDIA (ME) = {ME:.2f}", **estilo_medida)
        label_me.pack(side="left")

        # Moda
        label_mo = tk.Label(frame_medidas, text=f"MODA (MO) = {MO:.2f}", **estilo_medida)
        label_mo.pack(side="left")

        # Mediana
        label_md = tk.Label(frame_medidas, text=f"MEDIANA (MD) = {MD:.2f}", **estilo_medida)
        label_md.pack(side="left")

    except ValueError:
        messagebox.showerror("Erro", "Todos os valores devem ser números válidos!")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

# Configuração da janela principal
root = tk.Tk()
root.title("Cálculo de FRI com Intervalos de Classe")
root.geometry("1100x750")
root.configure(bg="#2d2d2d")

# Centralizar a janela
largura_janela = 1100
altura_janela = 750
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

# Frame para os valores de fi
frame_fi = tk.Frame(root, bg="#2d2d2d", height=250)
frame_fi.pack(pady=20, fill="both", expand=True)

# Frame para os resultados
frame_resultados = tk.Frame(root, bg="#2d2d2d")
frame_resultados.pack(pady=20, fill="both", expand=True)

root.mainloop()
import tkinter as tk
from tkinter import messagebox, ttk

def format_number(value, decimals=2):
    """Formata o número para remover .00 quando não necessário"""
    if isinstance(value, float) and value.is_integer():
        return f"{int(value)}"
    return f"{value:.{decimals}f}"

# Variáveis globais
entries_fi = []
entry_h = None
entry_li_inicial = None
tabela = None
frame_separatrizes_input = None
var_q = var_k = var_d = var_p = None
entry_percentis = None

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

        scrollable_frame_fi.bind(
            "<Configure>", lambda e: canvas_fi.configure(scrollregion=canvas_fi.bbox("all")))
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

        # Frame para entrada de separatrizes
        global frame_separatrizes_input, var_q, var_k, var_d, var_p, entry_percentis
        frame_separatrizes_input = tk.Frame(scrollable_frame_fi, bg="#2d2d2d")
        frame_separatrizes_input.pack(pady=20)

        label_sep = tk.Label(frame_separatrizes_input, text="Selecione as separatrizes que deseja calcular:", 
                           bg="#2d2d2d", fg="white")
        label_sep.config(font=('Arial', 10, 'bold'))
        label_sep.pack(anchor='w')

        # Variáveis de controle para os checkboxes
        var_q = tk.BooleanVar()
        var_k = tk.BooleanVar()
        var_d = tk.BooleanVar()
        var_p = tk.BooleanVar()

        # Checkboxes para seleção
        cb_q = tk.Checkbutton(frame_separatrizes_input, text="Quartis (Q1, Q2, Q3)", 
                            variable=var_q, bg="#2d2d2d", fg="white", selectcolor="#3d3d3d")
        cb_q.pack(anchor='w')
        
        cb_k = tk.Checkbutton(frame_separatrizes_input, text="Quintis (K1, K2, K3, K4)", 
                             variable=var_k, bg="#2d2d2d", fg="white", selectcolor="#3d3d3d")
        cb_k.pack(anchor='w')
        
        cb_d = tk.Checkbutton(frame_separatrizes_input, text="Decis (D1 a D9)", 
                            variable=var_d, bg="#2d2d2d", fg="white", selectcolor="#3d3d3d")
        cb_d.pack(anchor='w')
        
        cb_p = tk.Checkbutton(frame_separatrizes_input, text="Percentis (P10, P25, etc.)", 
                            variable=var_p, bg="#2d2d2d", fg="white", selectcolor="#3d3d3d")
        cb_p.pack(anchor='w')

        # Campo para percentis personalizados
        frame_percentis = tk.Frame(frame_separatrizes_input, bg="#2d2d2d")
        frame_percentis.pack(pady=5, anchor='w')
        
        label_p = tk.Label(frame_percentis, text="Percentis específicos (separados por vírgula):", 
                         bg="#2d2d2d", fg="white")
        label_p.pack(side='left')
        
        entry_percentis = tk.Entry(frame_percentis, bg="#3d3d3d", fg="white", 
                                 insertbackground="white", width=30)
        entry_percentis.pack(side='left', padx=5)

        botao_calcular = tk.Button(scrollable_frame_fi, text="Calcular", bg="#4CAF50", fg="white", command=exibir_resultados)
        botao_calcular.pack(pady=20)

    except ValueError:
        messagebox.showerror("Erro", "O valor de k deve ser um número inteiro!")

def copiar_tabela():
    if tabela is None:
        messagebox.showwarning("Aviso", "Nenhuma tabela para copiar!")
        return
    
    dados = []
    cabecalhos = [tabela.heading(col)["text"] for col in tabela["columns"]]
    dados.append("\t".join(cabecalhos))
    
    for child in tabela.get_children():
        valores = [tabela.item(child)["values"][i] for i in range(len(tabela["columns"]))]
        dados.append("\t".join(map(str, valores)))
    
    texto_copiado = "\n".join(dados)
    root.clipboard_clear()
    root.clipboard_append(texto_copiado)
    root.update()
    messagebox.showinfo("Sucesso", "Tabela copiada para a área de transferência!")

def calcular_separatriz(k, divisor, dados, somatoria_fi, h):
    """Calcula uma separatriz genérica (quartil, quintil, decil ou percentil)"""
    posicao = (k * somatoria_fi) / divisor
    classe_separatriz = None
    Fi_anterior = 0
    
    for i, dado in enumerate(dados):
        if dado['Fi'] >= posicao:
            classe_separatriz = dado
            if i > 0:
                Fi_anterior = dados[i-1]['Fi']
            break
    
    if classe_separatriz:
        return classe_separatriz['li'] + ((posicao - Fi_anterior) / classe_separatriz['fi']) * h
    return 0

def exibir_resultados():
    try:
        fi = [float(entry.get()) for entry in entries_fi]
        somatoria_fi = sum(fi)
        h = float(entry_h.get())
        li_inicial = float(entry_li_inicial.get())

        # Limpa o frame de resultados
        for widget in frame_resultados.winfo_children():
            widget.destroy()

        # Frame principal
        frame_principal = tk.Frame(frame_resultados, bg="#2d2d2d")
        frame_principal.pack(fill="both", expand=True)

        # Botão de copiar
        frame_botoes = tk.Frame(frame_principal, bg="#2d2d2d")
        frame_botoes.pack(fill="x", padx=10, pady=5, anchor="ne")

        botao_copiar = tk.Button(frame_botoes, text="Copiar Tabela", bg="#2196F3", fg="white", command=copiar_tabela)
        botao_copiar.pack(side="right")

        # Tabela
        frame_tabela = tk.Frame(frame_principal, bg="#2d2d2d")
        frame_tabela.pack(fill="both", expand=True)

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

        # Preencher tabela
        somatoria_fi_xi = 0
        frequencia_acumulada = 0
        frequencia_acumulada_fi = 0
        dados = []

        for i in range(len(fi)):
            li = li_inicial + i * h
            ls = li + h
            xi = (li + ls) / 2
            intervalo = f"{format_number(li)} - {format_number(ls)}"

            fi_xi = fi[i] * xi
            somatoria_fi_xi += fi_xi

            fri = fi[i] / somatoria_fi
            percent_fri = fri * 100
            graus_fri = fri * 360

            frequencia_acumulada += fri
            percent_fai = frequencia_acumulada * 100
            graus_fai = frequencia_acumulada * 360

            frequencia_acumulada_fi += fi[i]

            tabela.insert("", "end", values=(
                i+1,
                intervalo,
                format_number(xi),
                format_number(fi[i]),
                format_number(fi_xi),
                f"{fri:.3f}",
                f"{percent_fri:.2f}%",
                f"{graus_fri:.2f}°",
                format_number(frequencia_acumulada_fi),
                f"{frequencia_acumulada:.3f}",
                f"{percent_fai:.2f}%",
                f"{graus_fai:.2f}°"
            ))

            dados.append({
                'li': li,
                'fi': fi[i],
                'Fi': frequencia_acumulada_fi,
                'xi': xi
            })

        # Linha da somatória
        tabela.insert("", "end", values=(
            "", "", "", format_number(somatoria_fi), format_number(somatoria_fi_xi),
            "", "", "", "", "", "", ""
        ))

        # Cálculo das medidas básicas
        ME = somatoria_fi_xi / somatoria_fi
        
        # Moda
        classe_modal = max(dados, key=lambda x: x['fi'])
        index_modal = dados.index(classe_modal)
        fi_modal = classe_modal['fi']
        f_anterior = dados[index_modal-1]['fi'] if index_modal > 0 else 0
        f_posterior = dados[index_modal+1]['fi'] if index_modal < len(dados)-1 else 0
        D1 = fi_modal - f_anterior
        D2 = fi_modal - f_posterior
        MO = classe_modal['li'] + (D1/(D1+D2)) * h if (D1+D2) != 0 else classe_modal['li']

        # Mediana (Q2)
        MD = calcular_separatriz(2, 4, dados, somatoria_fi, h)

        # Frame para medidas básicas
        frame_medidas = tk.Frame(frame_principal, bg="#2d2d2d", pady=10)
        frame_medidas.pack(fill="x")

        estilo_medida = {
            'bg': '#2d2d2d',
            'fg': 'white',
            'padx': 20,
            'pady': 10
        }

        label_me = tk.Label(frame_medidas, text=f"MÉDIA (ME) = {format_number(ME)}", **estilo_medida)
        label_me.config(font=('Arial', 12, 'bold'))
        label_me.pack(side="left")

        label_mo = tk.Label(frame_medidas, text=f"MODA (MO) = {format_number(MO)}", **estilo_medida)
        label_mo.config(font=('Arial', 12, 'bold'))
        label_mo.pack(side="left")

        label_md = tk.Label(frame_medidas, text=f"MEDIANA (MD) = {format_number(MD)}", **estilo_medida)
        label_md.config(font=('Arial', 12, 'bold'))
        label_md.pack(side="left")

        # Cálculo das separatrizes selecionadas
        frame_separatrizes = tk.Frame(frame_principal, bg="#2d2d2d", pady=10)
        frame_separatrizes.pack(fill="x")

        estilo_sep = {
            'bg': '#2d2d2d',
            'fg': 'white',
            'padx': 5,
            'pady': 2
        }

        # Quartis
        if var_q.get():
            frame_q = tk.Frame(frame_separatrizes, bg="#2d2d2d")
            frame_q.pack(anchor='w', pady=5)
            tk.Label(frame_q, text="Quartis:", **estilo_sep, font=('Arial', 10, 'bold')).pack(side='left')
            for q in [1, 2, 3]:
                valor = calcular_separatriz(q, 4, dados, somatoria_fi, h)
                tk.Label(frame_q, text=f"Q{q} = {format_number(valor)}", **estilo_sep).pack(side='left', padx=10)

        # Quintis
        if var_k.get():
            frame_k = tk.Frame(frame_separatrizes, bg="#2d2d2d")
            frame_k.pack(anchor='w', pady=5)
            tk.Label(frame_k, text="Quintis:", **estilo_sep, font=('Arial', 10, 'bold')).pack(side='left')
            for k in [1, 2, 3, 4]:
                valor = calcular_separatriz(k, 5, dados, somatoria_fi, h)
                tk.Label(frame_k, text=f"K{k} = {format_number(valor)}", **estilo_sep).pack(side='left', padx=10)

        # Decis
        if var_d.get():
            frame_d = tk.Frame(frame_separatrizes, bg="#2d2d2d")
            frame_d.pack(anchor='w', pady=5)
            tk.Label(frame_d, text="Decis:", **estilo_sep, font=('Arial', 10, 'bold')).pack(side='left')
            for d in range(1, 10):
                valor = calcular_separatriz(d, 10, dados, somatoria_fi, h)
                tk.Label(frame_d, text=f"D{d} = {format_number(valor)}", **estilo_sep).pack(side='left', padx=5)

        # Percentis
        if var_p.get():
            percentis = []
            # Percentis padrão
            for p in [10, 25, 50, 75, 90]:
                percentis.append(p)
            
            # Percentis personalizados
            if entry_percentis.get():
                try:
                    personalizados = [int(p.strip()) for p in entry_percentis.get().split(',') if p.strip().isdigit()]
                    for p in personalizados:
                        if 1 <= p <= 99:
                            percentis.append(p)
                except:
                    pass
            
            # Remover duplicados e ordenar
            percentis = sorted(list(set(percentis)))
            
            if percentis:
                frame_p = tk.Frame(frame_separatrizes, bg="#2d2d2d")
                frame_p.pack(anchor='w', pady=5)
                tk.Label(frame_p, text="Percentis:", **estilo_sep, font=('Arial', 10, 'bold')).pack(side='left')
                
                for p in percentis:
                    valor = calcular_separatriz(p, 100, dados, somatoria_fi, h)
                    tk.Label(frame_p, text=f"P{p} = {format_number(valor)}", **estilo_sep).pack(side='left', padx=5)

        # Correspondências
        frame_corr = tk.Frame(frame_principal, bg="#2d2d2d", pady=10)
        frame_corr.pack(fill="x")

        tk.Label(frame_corr, text="Correspondências:", bg="#2d2d2d", fg="white", 
               font=('Arial', 12, 'bold')).pack(anchor='w')

        correspondencias = [
            "Q₂ = D₅ = P₅₀ = Mediana",
            "Q₁ = P₂₅",
            "Q₃ = P₇₅",
            "K₁ = D₂ = P₂₀",
            "K₂ = D₄ = P₄₀",
            "K₃ = D₆ = P₆₀",
            "K₄ = D₈ = P₈₀"
        ]

        frame_colunas = tk.Frame(frame_corr, bg="#2d2d2d")
        frame_colunas.pack(anchor='w')

        metade = len(correspondencias) // 2
        frame_col_esq = tk.Frame(frame_colunas, bg="#2d2d2d")
        frame_col_esq.pack(side='left', padx=10)
        for corr in correspondencias[:metade]:
            tk.Label(frame_col_esq, text=corr, **estilo_sep).pack(anchor='w')

        frame_col_dir = tk.Frame(frame_colunas, bg="#2d2d2d")
        frame_col_dir.pack(side='left', padx=10)
        for corr in correspondencias[metade:]:
            tk.Label(frame_col_dir, text=corr, **estilo_sep).pack(anchor='w')

    except ValueError:
        messagebox.showerror("Erro", "Todos os valores devem ser números válidos!")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

# Configuração da janela principal
root = tk.Tk()
root.title("Cálculo de Frequências e Separatrizes")
root.geometry("1200x800")
root.configure(bg="#2d2d2d")

# Centralizar a janela
largura_janela = 1200
altura_janela = 800
largura_tela = root.winfo_screenwidth()
altura_tela = root.winfo_screenheight()
x = (largura_tela - largura_janela) // 2
y = (altura_tela - altura_janela) // 2
root.geometry(f"{largura_janela}x{altura_janela}+{x}+{y}")

# Frame para o valor de k
frame_k = tk.Frame(root, bg="#2d2d2d")
frame_k.pack(pady=20)

label_k = tk.Label(frame_k, text="Digite o número de classes (k):", bg="#2d2d2d", fg="white")
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
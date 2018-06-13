#!/usr/bin/env python3
from xbee_manager import coordinator, readRouterEndDevices
import tkinter as tk
import witkets as wtk

# Abrindo comm. do xbee coordenador

root = tk.Tk()
root.title("LOGAH Manager")
style = wtk.Style()
style.theme_use('clam')
style.apply_default()
builder = wtk.TkBuilder(root)
builder.build_from_file("xbee_manager/gui/main_window.ui")

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=0)

combo_setor = builder.nodes['combo-setor']
combo_setor.current(0)
combo_equipamento = builder.nodes['combo-equipamento']
combo_equipamento.current(0)

button_setor = builder.nodes['button-setor']
button_equipamento = builder.nodes['button-equipamento']
text_equipamento = builder.nodes['text-dispositivo-encontrado']
text_equipamento.config(state=tk.DISABLED)
text_setor = builder.nodes['text-setor-encontrado']
text_setor.config(state=tk.DISABLED)


def show_sector():
    # Setor
    # text_setor.config(state=tk.NORMAL)
    # print(combo_setor.get())
    # text_setor.insert(tk.END, combo_setor.get() + "\n")
    # text_setor.config(state=tk.DISABLED)
    setor_roteador = combo_setor.get()
    if setor_roteador == "Neurologia":
        dispositivos_encontrados = readRouterEndDevices("R1")
        print(combo_setor.get())
        for d in dispositivos_encontrados:
            text_equipamento.config(state=tk.NORMAL)
            text_equipamento.insert(tk.END, d + "\n")
            text_equipamento.config(state=tk.DISABLED)
    else:
        dispositivos_encontrados = readRouterEndDevices("R2")
        print(combo_setor.get())
        for d in dispositivos_encontrados:
            text_equipamento.config(state=tk.NORMAL)
            text_equipamento.insert(tk.END, d + "\n")
            text_equipamento.config(state=tk.DISABLED)


def show_equipamento():
    # Setor
    # text_equipamento.config(state=tk.NORMAL)
    print(combo_equipamento.get())
    # text_equipamento.insert(tk.END, combo_equipamento.get() + "\n")
    # text_equipamento.config(state=tk.DISABLED)


# Acao no botao setor
button_setor["command"] = show_sector
# Acao no botao Equipamento
button_equipamento['command'] = show_equipamento

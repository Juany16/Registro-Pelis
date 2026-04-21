#! /usr/bin/python3

import customtkinter as ctk
from CTkTable import *
import pandas as pd
import pywal as pyw

import Notificaciones as notis

def coloresPywal():
    colores = pyw.colors.file("/home/juani/.cache/wal/colors.json")
    return colores

def aplicarColores(vnt, frameT, tabla, frame_btn, entry_pelicula, entry_fecha, entry_director, chk_vista, btn_add, btn_del, btn_save, 
                   frame_editar, entry_fila, entry_columna, entry_editar, btn_editar, btn_borrar, colores):
    global fondo, bordes, animaciones, botones
    fondo = colores["special"]["background"]
    bordes = colores["colors"]["color7"]
    animaciones = colores["colors"]["color8"]
    botones = colores["colors"]["color1"]

    vnt.configure(fg_color=fondo)
    frameT.configure(fg_color=fondo, border_color=bordes, scrollbar_fg_color=fondo,
                     scrollbar_button_color=botones, scrollbar_button_hover_color=animaciones,
                     label_fg_color=botones, label_text_color=COLORLETRA)
    tabla.configure(header_color=botones, colors=[fondo, fondo], hover_color=animaciones)
    frame_btn.configure(fg_color=fondo, border_color=bordes)
    entry_pelicula.configure(fg_color=fondo, text_color=COLORLETRA, border_color=bordes, placeholder_text_color=COLORLETRA)
    entry_fecha.configure(fg_color=fondo, text_color=COLORLETRA, border_color=bordes, placeholder_text_color=COLORLETRA)
    entry_director.configure(fg_color=fondo, text_color=COLORLETRA, border_color=bordes, placeholder_text_color=COLORLETRA)
    chk_vista.configure(fg_color=fondo, border_color=bordes, hover_color=animaciones, text_color=COLORLETRA)
    btn_add.configure(fg_color=botones, hover_color=animaciones, text_color=COLORLETRA)
    btn_del.configure(fg_color=botones, hover_color=animaciones, text_color=COLORLETRA)
    btn_save.configure(fg_color=botones, hover_color=animaciones, text_color=COLORLETRA)
    frame_editar.configure(fg_color=fondo, border_color=bordes)
    entry_fila.configure(fg_color=fondo, text_color=COLORLETRA, border_color=bordes, placeholder_text_color=COLORLETRA)
    entry_columna.configure(fg_color=fondo, text_color=COLORLETRA, border_color=bordes, placeholder_text_color=COLORLETRA)
    entry_editar.configure(fg_color=fondo, text_color=COLORLETRA, border_color=bordes, placeholder_text_color=COLORLETRA)
    btn_editar.configure(fg_color=botones, hover_color=animaciones, text_color=COLORLETRA)
    btn_borrar.configure(fg_color=botones, hover_color=animaciones, text_color=COLORLETRA)

archivo = "/home/juani/Documentos/Aplicaciones/RegistroPelis/Peliculas.xlsx"

# --- cargar datos iniciales ---
try:
    df = pd.read_excel(archivo)
except FileNotFoundError:
    df = pd.DataFrame(columns=["Película", "Año", "Director", "Vista"])

data = [df.columns.tolist()] + df.values.tolist()
# print(data)

def scrollRuedita(event):
    global frameT
    if event.num == 4:
        frameT._parent_canvas.yview_scroll(-1, "units")
    elif event.num == 5:
        frameT._parent_canvas.yview_scroll(1, "units")

# --- interfaz ---
vnt = ctk.CTk()
vnt.title("Registro de películas")
vnt.geometry("1000x600")

ESQ = 5
COLORLETRA = "white"
LETRA = "TkDefaultFont"
TLN = 14

# --- funciones ---
def borrar_entradas():
    entry_fila.delete(0, "end")
    entry_columna.delete(0, "end")
    entry_editar.delete(0, "end")

def obtenerCelda(info):
    fila = info["row"]
    columna = info["column"]
    valor = info["value"]
    if valor == "Sí":
        tabla.insert(fila, columna, "No")
    elif valor == "No":
        tabla.insert(fila, columna, "Sí")
    else:
        borrar_entradas()
        entry_fila.insert(0, fila)
        entry_columna.insert(0, columna)
        entry_editar.insert(0, valor)
        entry_editar.focus()

def agregar_fila():
    pelicula = entry_pelicula.get().strip().capitalize()
    fecha = entry_fecha.get().strip().capitalize()
    director = entry_director.get().strip().capitalize()
    vista = "Sí" if var_vista.get() else "No"

    if pelicula == "": # or fecha == "" or director == "":
        notis.mandarNotificaciones("Error!\nTenés que escribir algo en película y director")
        return  # no agregar si falta info

    nueva = [pelicula, fecha, director, vista]
    tabla.add_row(nueva)

    # limpiar los inputs
    entry_pelicula.delete(0, "end")
    entry_fecha.delete(0, "end")
    entry_director.delete(0, "end")
    var_vista.set(False)

def eliminar_fila():
    if len(tabla.values) > 1:
        tabla.delete_row(len(tabla.values)-1)

def guardar():
    datos = tabla.values
    headers = datos[0]
    filas = datos[1:]
    df_out = pd.DataFrame(filas, columns=headers)
    df_out.to_excel(archivo, index=False)
    notis.mandarNotificaciones("Exito!\nTabla guardada")

def borrar_celda():
    try:
        fil = int(entry_fila.get())
        col = int(entry_columna.get())

        # tabla.delete(fil, col)
        tabla.insert(fil, col, "-")
        tabla_actualizada = tabla.get()

        notis.mandarNotificaciones("Exito!\nTabla actualizada!")
        borrar_entradas()
    except:
        notis.mandarNotificaciones("Error!\nTabla no actualizada")
        borrar_entradas()


def editar_celda():
    try:
        fil = int(entry_fila.get())
        col = int(entry_columna.get())
        val = entry_editar.get()

        tabla.insert(fil, col, val.capitalize())
        tabla_actualizada = tabla.get()
        # guardar()
        notis.mandarNotificaciones("Exito!\nTabla actualizada!")
        borrar_entradas()
    except Exception as e:
        notis.mandarNotificaciones("Error!")

# --- tabla ---
frameT = ctk.CTkScrollableFrame(vnt, label_font=(LETRA, 18, "bold"), label_text="Registro de películas", corner_radius=ESQ)
frameT.pack(expand=True, fill="both", padx=10, pady=10)

tabla = CTkTable(master=frameT, padx=2, pady=2, corner_radius=ESQ, font=(LETRA, TLN), justify="center", hover_color="gray",
                 row=len(data), column=len(data[0]), values=data, command=obtenerCelda)
tabla.pack(expand=True, fill="both", padx=0, pady=5)

# --- botones ---
frame_btn = ctk.CTkFrame(vnt, corner_radius=ESQ)
frame_btn.pack(fill="x", padx=10, pady=0)

entry_pelicula = ctk.CTkEntry(frame_btn, font=(LETRA, TLN), placeholder_text="Película", corner_radius=ESQ)
entry_pelicula.pack(side="left", padx=5, pady=5, expand=True, fill="x")

entry_fecha = ctk.CTkEntry(frame_btn, font=(LETRA, TLN), placeholder_text="Año", corner_radius=ESQ)
entry_fecha.pack(side="left", padx=5, pady=5, expand=True, fill="x")

entry_director = ctk.CTkEntry(frame_btn, font=(LETRA, TLN), placeholder_text="Director", corner_radius=ESQ)
entry_director.pack(side="left", padx=5, pady=5, expand=True, fill="x")

var_vista = ctk.BooleanVar()
chk_vista = ctk.CTkCheckBox(frame_btn, font=(LETRA, TLN), text="Vista", variable=var_vista, corner_radius=ESQ)
chk_vista.pack(side="left", padx=5, pady=5, expand=True, fill="x")

btn_add = ctk.CTkButton(frame_btn, font=(LETRA, TLN), text="   Agregar", corner_radius=ESQ, command=agregar_fila)
btn_add.pack(side="left", padx=5, expand=True, fill="x")

btn_del = ctk.CTkButton(frame_btn, font=(LETRA, TLN), text="󰗨   Eliminar última", corner_radius=ESQ, command=eliminar_fila)
btn_del.pack(side="left", padx=5, expand=True, fill="x")

btn_save = ctk.CTkButton(frame_btn, font=(LETRA, TLN), text="󰆓   Guardar", corner_radius=ESQ, command=guardar)
btn_save.pack(side="left", padx=5, expand=True, fill="x")

frame_editar = ctk.CTkFrame(vnt, corner_radius=ESQ)
frame_editar.pack(fill="x", padx=10, pady=10)

entry_fila = ctk.CTkEntry(frame_editar, font=(LETRA, TLN), placeholder_text="Nº de Fila", corner_radius=ESQ)
entry_fila.pack(side="left", padx=5, pady=5, expand=True, fill="x")

entry_columna = ctk.CTkEntry(frame_editar, font=(LETRA, TLN), placeholder_text="Nº de Columna", corner_radius=ESQ)
entry_columna.pack(side="left", padx=5, pady=5, expand=True, fill="x")

entry_editar = ctk.CTkEntry(frame_editar, font=(LETRA, TLN), placeholder_text="Dato a Editar", corner_radius=ESQ)
entry_editar.pack(side="left", padx=5, pady=5, expand=True, fill="x")

btn_editar = ctk.CTkButton(frame_editar, font=(LETRA, TLN), text="   Editar", corner_radius=ESQ, command=editar_celda)
btn_editar.pack(side="left", padx=5, expand=True, fill="x")

btn_borrar = ctk.CTkButton(frame_editar, font=(LETRA, TLN), text="   Borrar", corner_radius=ESQ, command=borrar_celda)
btn_borrar.pack(side="left", padx=5, expand=True, fill="x")

frameT._parent_canvas.bind_all("<Button-4>", scrollRuedita)
frameT._parent_canvas.bind_all("<Button-5>", scrollRuedita)

colores = coloresPywal()
aplicarColores(vnt, frameT, tabla, frame_btn, entry_pelicula, entry_fecha, entry_director, chk_vista, btn_add, btn_del, btn_save,
               frame_editar, entry_fila, entry_columna, entry_editar, btn_editar, btn_borrar, colores)

vnt.mainloop()


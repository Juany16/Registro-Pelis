#! /usr/bin/python3

from notifypy import Notify

def mandarNotificaciones(msj):
    notificacion = Notify()
    notificacion.title = "Registro de Pelis"
    notificacion.message = msj
    notificacion.icon = "/home/juani/.config/dunst/iconos/normal.png"
    notificacion.audio = "/home/juani/Documentos/Aplicaciones/RegistroPelis/NotificationPy.wav"
    notificacion.send()

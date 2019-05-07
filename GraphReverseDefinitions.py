##1234567890223456789033345678904444567890555556789066666678907777777890
##72 caracteres de ancho. Tratar de mostrar todo este texto si podemos.


def avadakedabra(argh):
    return 2*argh
##Un prototipo para tener en claro como funciona definir cosas.
##def noimportaelnombre(argumentos):
##  indentación
##  return explícito QUE ESTO NO ES RUBY

def new_function(ICON, NOMBRE, TECL, DESC, OBJ, MENU):
    from PyQt5.QtGui import QIcon
    from PyQt5.QtWidgets import QAction
    NEW = QAction(QIcon(ICON), NOMBRE, OBJ)
    NEW.setShortcut(TECL)
    NEW.setStatusTip(DESC)
    MENU.addAction(NEW)
    return NEW

##Esto acorta la definición de las funciones a 2 líneas, en vez de 4.

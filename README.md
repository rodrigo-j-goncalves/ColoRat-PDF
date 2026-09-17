# ColoRat-PDF

Ahorrá dinero al imprimir documentos que tengan páginas color.

**Para qué es ColoRat-PDF:**

- Imprimir en color cuesta más caro que imprimir en blanco y negro.
- Si tengo un documento de 150 páginas y solo algunas tienen color:
    - ¿por qué pagar impresión color por las 150 páginas?
    - ¿no sería mejor imprimir las páginas color por separado y así pagar menos?
- Pero para eso habría que dividir el PDF en [páginas color] por un lado y [páginas blanco y negro] por otro!

Para eso es **ColoRat** (color + rata + PDF)


**ColoRat-PDF** separa tu PDF en [páginas color] + [páginas en blanco y negro], para que puedas imprimirlas por separado y no pagar de más.

## Cómo se usa (Windows / macOS / Linux)

1. Poné el PDF (también se pueden hacer muchos a la vez) en la carpeta llamada `01_input`
2. Abrí una terminal en esta carpeta y ejecutá: `python 02_process/script.py`
3. Los resultados estarán en la carpeta `03_output`

Supongamos que vamos a imprimir `tesis.pdf`. Luego de ejecutar el script se generan 3 PDFs:
- `tesis-summary.pdf`
    - Esto es una página con un breve resumen que te informa: 
        - Cantidad total de páginas que tiene el PDF de la tesis
        - Cantidad de páginas a color
        - Cantidad de páginas en blanco y negro
        - También muestra un mensaje si es que hubo algún error con el PDF.
- `tesis_color_pages.pdf`
    - Este PDF contiene **todas las páginas de la tesis que tienen color**. Se puede imprimir pagando más caro :)
    - Si no hay páginas con color (`tesis-summary.pdf` te pone que hay 0 páginas con color), este PDF no se crea 
- `tesis_bw_pages.pdf`
    - Este PDF tiene **todas las páginas que NO tienen color**. Este PDF lo pagamos más barato!
    - Si no hay páginas en blanco y negro (`tesis-summary.pdf` te pone que hay 0 páginas black and white), este PDF no se crea.


---


## Instalación

### Antes de instalar

Necesitás tener dos cosas en tu computadora (si no sabés pedile ayuda a tu compi):

1. **Python** (un programa que sirve para ejecutar otros programas). Si no sabés si lo tenés, abrí una terminal y escribí `python --version`.

2. **Poppler**, un pequeño programa auxiliar. Buscá en internet "instalar poppler" junto con el nombre de tu sistema operativo, y seguí las instrucciones.


### Instalar

- Por las dudas, antes de usarlo hay que instalar algunas dependencias. Se hace con un solo comando en la terminal: `pip install -r requirements.txt`


Por cada PDF que le des, el programa crea:

- Un resumen breve: cuántas páginas tiene el documento, cuántas son a color y cuántas son en blanco y negro.
- Un PDF con solo las páginas a color (solo se crea si hay alguna).
- Un PDF con solo las páginas en blanco y negro (solo se crea si hay alguna).

Si algún archivo tiene algún problema y no se puede procesar, el resumen explica qué pasó, en vez de detener todo el programa.

---

## Licence & Credits

- MIT License — Rodrigo J. Gonçalves. Ver [LICENSE](LICENSE) para el texto completo.
- Esto lo he _Claudesarrolado_ ;)
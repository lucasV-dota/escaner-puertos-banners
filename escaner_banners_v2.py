import argparse
import concurrent.futures
import socket
import threading

candado = threading.Lock()

def obtener_banner(s, target, puerto):
    try:
        if puerto in [80, 8080]:
            peticion = f"HEAD / HTTP/1.1\r\nHost: {target}\r\n\r\n"
            s.send(peticion.encode("utf-8"))
        banner = s.recv(1024).decode("utf-8", errors="ignore").strip()
        for linea in banner.split("\n"):
            if "Server" in linea:
                return linea.strip()
        return banner.split("\n")[0] if banner else "sin banner"
    except:
        return "Sin banner(Timeout)"

def probar_puerto(target, puerto, archivo_salida):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3.0)
    resultado = s.connect_ex((target, puerto))
    if resultado == 0:
        banner = obtener_banner(s, target, puerto)
        linea_resultado = f"[+] Puerto {puerto}: ABIERTO | {banner}"
        with candado:
            print(linea_resultado)
            if archivo_salida:
                with open(archivo_salida, "a", encoding="utf-8") as f:
                    f.write(linea_resultado + "\n")
    s.close()

parser = argparse.ArgumentParser(description="Integrador Total")
parser.add_argument("-t", "--target", required=True)
parser.add_argument("-p", "--puerto", default="21,22,80,443")
parser.add_argument("-o", "--output", help="Archivos para guardaar resultados(ej: reporte.txt)")
args = parser.parse_args()

lista_puertos = []
for item in args.puerto.split(","):
    item = item.strip()
    if "-" in item:
        inicio, fin = item.split("-")
        for p in range(int(inicio), int(fin) + 1):
            lista_puertos.append(p)
    else:
        lista_puertos.append(int(item))
print(f"Escaneando {len(lista_puertos)} puertos en {args.target}...\n")

with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
    for p in lista_puertos:
        executor.submit(probar_puerto, args.target, p, args.output)

if args.output:
    print(f"\n[*]Resultados guardados en: {args.output}")

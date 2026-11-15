cat << 'EOF' > README.md
# Escáner de Puertos y Banners Multihilo (Python)

Herramienta CLI escrita en Python para reconocimiento de red, detección de puertos abiertos mediante sockets TCP concurrentes y extracción de banners (pasivo y activo HTTP).

## Características
- **Concurrencia:** Escaneo rápido mediante `ThreadPoolExecutor`.
- **Banner Grabbing:** Detección pasiva (ej. SSH, FTP) y activa mediante peticiones `HEAD` para servicios HTTP (`80`, `8080`).
- **Flexibilidad CLI:** Soporte para puertos individuales, listas separadas por comas y rangos (`1-100`).
- **Exportación segura:** Guardado de resultados en archivo de texto protegido contra condiciones de carrera con `threading.Lock()`.

## Uso

```bash
# Escaneo con puertos por defecto (21, 22, 80, 443)
python3 escaner_banners_v2.py -t scanme.nmap.org

# Escaneo de un rango de puertos
python3 escaner_banners_v2.py -t scanme.nmap.org -p 1-100

# Escaneo guardando el reporte en un archivo
python3 escaner_banners_v2.py -t scanme.nmap.org -p 22,80,8080 -o resultados.txt

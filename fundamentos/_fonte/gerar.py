"""Monta modulo-N a partir de _fonte/mN/*.html e gera o PDF com o Chrome headless.
Uso: python3 _fonte/gerar.py 2 "Testes e CI" modulo-2-testes-ci
"""
import glob, os, subprocess, sys
n, titulo, saida = sys.argv[1], sys.argv[2], sys.argv[3]
base = os.path.dirname(os.path.abspath(__file__))
raiz = os.path.dirname(base)
cab = open(os.path.join(base, 'cabecalho.html'), encoding='utf-8').read()
cab = cab.replace('{TITLE}', f'Módulo {n}: {titulo}').replace('{FOOTER}', f'Módulo {n} · {titulo}')
partes = [open(f, encoding='utf-8').read() for f in sorted(glob.glob(os.path.join(base, f'm{n}', '*.html')))]
html = os.path.join(raiz, saida + '.html')
open(html, 'w', encoding='utf-8').write(cab + ''.join(partes) + '\n</body>\n</html>\n')
pdf = os.path.join(raiz, saida + '.pdf')
subprocess.run(['google-chrome', '--headless=new', '--disable-gpu', '--no-pdf-header-footer',
                f'--print-to-pdf={pdf}', 'file://' + html], check=True, capture_output=True)
print(subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout.split('Pages:')[1].split('\n')[0].strip(), 'páginas ->', pdf)

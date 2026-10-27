"""Iniciador local do SafeFlow Map.

Execute este arquivo com dois cliques. Ele inicia um servidor somente no
computador local e abre o mapa automaticamente no navegador padrão.
"""

from __future__ import annotations

import http.server
import ctypes
import sys
import threading
import urllib.request
import webbrowser
from ctypes import wintypes
from functools import partial
from pathlib import Path


PASTA_DO_MAPA = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
ENDERECO_LOCAL = "127.0.0.1"
_WINDOW_CALLBACK = None


class SafeFlowHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        # Mantém a janela limpa; erros HTTP continuam aparecendo no navegador.
        return


def abrir_navegador(url: str) -> None:
    webbrowser.open(url, new=2)


def executar_como_aplicativo(servidor: http.server.ThreadingHTTPServer, url: str) -> int:
    """Exibe uma janela de controle quando empacotado como aplicativo Windows."""
    global _WINDOW_CALLBACK

    thread = threading.Thread(target=servidor.serve_forever, daemon=True)
    thread.start()
    teste_interface = "--teste-interface" in sys.argv
    if not teste_interface:
        abrir_navegador(url)

    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32
    user32.CreateWindowExW.restype = wintypes.HWND
    user32.DefWindowProcW.argtypes = [wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]
    user32.DefWindowProcW.restype = ctypes.c_ssize_t
    kernel32.GetModuleHandleW.restype = wintypes.HMODULE
    WM_COMMAND, WM_DESTROY, WM_CLOSE = 0x0111, 0x0002, 0x0010
    BOTAO_ABRIR, BOTAO_ENCERRAR = 1001, 1002
    WS_VISIBLE, WS_CHILD = 0x10000000, 0x40000000
    WS_OVERLAPPEDWINDOW = 0x00CF0000
    CW_USEDEFAULT = -2147483648

    WNDPROC = ctypes.WINFUNCTYPE(
        ctypes.c_ssize_t, wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM
    )

    class WNDCLASSW(ctypes.Structure):
        _fields_ = [
            ("style", wintypes.UINT),
            ("lpfnWndProc", WNDPROC),
            ("cbClsExtra", ctypes.c_int),
            ("cbWndExtra", ctypes.c_int),
            ("hInstance", wintypes.HINSTANCE),
            ("hIcon", wintypes.HICON),
            ("hCursor", wintypes.HANDLE),
            ("hbrBackground", wintypes.HBRUSH),
            ("lpszMenuName", wintypes.LPCWSTR),
            ("lpszClassName", wintypes.LPCWSTR),
        ]

    user32.CreateWindowExW.argtypes = [
        wintypes.DWORD,
        wintypes.LPCWSTR,
        wintypes.LPCWSTR,
        wintypes.DWORD,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int,
        wintypes.HWND,
        wintypes.HMENU,
        wintypes.HINSTANCE,
        wintypes.LPVOID,
    ]
    user32.RegisterClassW.argtypes = [ctypes.POINTER(WNDCLASSW)]
    user32.RegisterClassW.restype = wintypes.ATOM
    user32.LoadCursorW.argtypes = [wintypes.HINSTANCE, wintypes.LPCWSTR]
    user32.LoadCursorW.restype = wintypes.HANDLE
    user32.PostMessageW.argtypes = [wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]
    user32.PostMessageW.restype = wintypes.BOOL

    def procedimento(hwnd, mensagem, wparam, lparam):
        if mensagem == WM_COMMAND:
            identificador = wparam & 0xFFFF
            if identificador == BOTAO_ABRIR:
                abrir_navegador(url)
                return 0
            if identificador == BOTAO_ENCERRAR:
                user32.DestroyWindow(hwnd)
                return 0
        if mensagem == WM_DESTROY:
            user32.PostQuitMessage(0)
            return 0
        return user32.DefWindowProcW(hwnd, mensagem, wparam, lparam)

    _WINDOW_CALLBACK = WNDPROC(procedimento)
    nome_classe = "SafeFlowMapaHistoricoWindow"
    instancia = kernel32.GetModuleHandleW(None)
    classe = WNDCLASSW()
    classe.lpfnWndProc = _WINDOW_CALLBACK
    classe.hInstance = instancia
    classe.hCursor = user32.LoadCursorW(None, ctypes.cast(32512, wintypes.LPCWSTR))
    classe.hbrBackground = ctypes.c_void_p(6)
    classe.lpszClassName = nome_classe
    user32.RegisterClassW(ctypes.byref(classe))

    janela = user32.CreateWindowExW(
        0, nome_classe, "SafeFlow — Mapa Histórico", WS_OVERLAPPEDWINDOW | WS_VISIBLE,
        CW_USEDEFAULT, CW_USEDEFAULT, 520, 260, None, None, instancia, None
    )
    user32.CreateWindowExW(
        0, "STATIC", "SAFEFLOW — MAPA HISTÓRICO DE VERIFICAÇÕES",
        WS_CHILD | WS_VISIBLE, 30, 28, 450, 28, janela, None, instancia, None
    )
    user32.CreateWindowExW(
        0, "STATIC", "Aplicativo ativo. Mantenha esta janela aberta durante o uso.",
        WS_CHILD | WS_VISIBLE, 30, 67, 450, 24, janela, None, instancia, None
    )
    user32.CreateWindowExW(
        0, "BUTTON", "Abrir mapa", WS_CHILD | WS_VISIBLE,
        30, 120, 180, 42, janela, wintypes.HMENU(BOTAO_ABRIR), instancia, None
    )
    user32.CreateWindowExW(
        0, "BUTTON", "Encerrar SafeFlow", WS_CHILD | WS_VISIBLE,
        280, 120, 180, 42, janela, wintypes.HMENU(BOTAO_ENCERRAR), instancia, None
    )

    if teste_interface:
        threading.Timer(1.0, lambda: user32.PostMessageW(janela, WM_CLOSE, 0, 0)).start()

    mensagem = wintypes.MSG()
    while user32.GetMessageW(ctypes.byref(mensagem), None, 0, 0) > 0:
        user32.TranslateMessage(ctypes.byref(mensagem))
        user32.DispatchMessageW(ctypes.byref(mensagem))

    servidor.shutdown()
    servidor.server_close()
    return 0


def testar_pacote(servidor: http.server.ThreadingHTTPServer, url: str) -> int:
    """Valida silenciosamente os arquivos essenciais dentro do executável."""
    thread = threading.Thread(target=servidor.serve_forever, daemon=True)
    thread.start()
    alvos = {
        "pagina": "index.html",
        "pontos": "data/pontos_classe_a.geojson",
        "sede": "data/sede.geojson",
        "rotas": "data/sede_para_locais.json",
        "fiscais": "data/fiscais_dias.json",
        "limites": "data/limites_municipais.geojson",
        "fonte_limites": "data/limites_municipais_fonte.json",
    }

    try:
        for caminho in alvos.values():
            with urllib.request.urlopen(f"{url}{caminho}", timeout=10) as resposta:
                if resposta.status != 200 or not resposta.read(64):
                    return 1
        return 0
    except Exception:
        return 1
    finally:
        servidor.shutdown()
        servidor.server_close()


def main() -> int:
    if not (PASTA_DO_MAPA / "index.html").is_file():
        print("ERRO: o arquivo index.html não foi encontrado.")
        print(f"Pasta procurada: {PASTA_DO_MAPA}")
        input("Pressione Enter para fechar...")
        return 1

    handler = partial(SafeFlowHandler, directory=str(PASTA_DO_MAPA))

    try:
        # Porta zero pede ao Windows uma porta livre, evitando conflito com 8000.
        servidor = http.server.ThreadingHTTPServer((ENDERECO_LOCAL, 0), handler)
    except OSError as erro:
        print(f"ERRO ao iniciar o SafeFlow: {erro}")
        input("Pressione Enter para fechar...")
        return 1

    porta = servidor.server_address[1]
    url = f"http://{ENDERECO_LOCAL}:{porta}/"

    if "--teste-pacote" in sys.argv:
        return testar_pacote(servidor, url)

    if getattr(sys, "frozen", False):
        return executar_como_aplicativo(servidor, url)

    print("=" * 58)
    print(" SAFEFLOW MAP — servidor local iniciado")
    print("=" * 58)
    print(f" Mapa: {url}")
    print(" O navegador será aberto automaticamente.")
    print(" Mantenha esta janela aberta enquanto estiver usando o mapa.")
    print(" Para encerrar, feche esta janela ou pressione Ctrl+C.")
    print("=" * 58)

    if "--sem-navegador" not in sys.argv:
        threading.Timer(0.6, abrir_navegador, args=(url,)).start()

    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nSafeFlow encerrado.")
    finally:
        servidor.server_close()

    return 0


if __name__ == "__main__":
    sys.exit(main())

from src.main import App
import win32gui
import win32con

class SystemTray:
    def __init__(self):
        self.app = App()
        icone = "computer_pc_10894.ico"
        self.icon = win32gui.LoadIcon(0, icone)  # Carregue o ícone
        self.window = win32gui.CreateWindowEx(
            0,
            "SystemTrayWindow",
            "Controle de Despesas",
            win32con.WS_OVERLAPPEDWINDOW,
            0, 0, 100, 100,
            0, 0, 0, 0
        )
        win32gui.SetWindowLong(self.window, win32con.GWL_STYLE, win32con.WS_CLIPCHILDREN)
        win32gui.ShowWindow(self.window, win32con.SW_HIDE)

    def OnTaskbarIconActivated(self, event):
        if event.message == win32con.WM_LBUTTONDOWN:
            x, y = win32gui.GetCursorPos()
            menu = win32gui.CreatePopupMenu()
            win32gui.AppendMenu(menu, win32con.MF_STRING, 1, "Maximizar")
            win32gui.AppendMenu(menu, win32con.MF_STRING, 2, "Fechar")
            win32gui.TrackPopupMenu(menu, win32con.TPM_LEFTALIGN, x, y, 0, self.window, None)

    def OnMenuCommand(self, menu, id):
        if id == 1:
          self.app.ShowWindow(win32con.SW_MAXIMIZE)
        if id == 2:
          self.app.Close()


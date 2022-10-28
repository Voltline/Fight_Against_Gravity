if __name__ == '__main__':
    HOST = '47.100.27.66'
    PORT = 25555
    ADDR = (HOST, PORT)
    ENCODING = 'utf-8'
    BUFFSIZE = 1024
    UI = ui.UI_Main("Fight Against Gravity", HOST, PORT, HOST, PORT)
    UI.show()
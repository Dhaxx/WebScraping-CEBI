import fdb

conexao_destino = fdb.connect(dsn="D:\Fiorilli\SCPI_8\Cidades\SAEMJA\ARQ2022\SCPI2022.FDB", user='FSCSCPI8', password='scpi',
                            port=3050, charset='WIN1252', fb_library_name='C:\\Program Files\\Firebird\\Firebird_2_5\\bin\\fbclient.dll')

def commit():
    conexao_destino.commit()
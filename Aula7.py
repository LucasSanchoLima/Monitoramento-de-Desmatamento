import cv2
from pathlib import Path

def CorPixel(pixel, numero):
     if pixel > numero: return "desmatada"
     return "nada"

caminhoVideo = str(Path(__file__).with_name("Imagens de satelite mostram desmatamento na Amazônia.mp4"))

video = cv2.VideoCapture(caminhoVideo)

if video.isOpened() == False:
    print("Erro ao abrir o arquivo de video")
    exit()

arquivo = open("resultado.txt", 'w')

videoProcessado = cv2.VideoWriter("videoProcessado.mp4", cv2.VideoWriter_fourcc(*'mp4v'), 1.0, (int(video.get(3)), int(video.get(4))))

qtdFrame = 0
corMediaAntiga = 0


while video.isOpened():

    for ax in range(12):
        retorno, frame = video.read()
        if not retorno: break

    corMedia = [0,0,0]
    
    x = 0

    frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frameGray = cv2.blur(frameGray, (9,9))

    tamanhoTela = (frame.shape[0]*frame.shape[1])

    while x < frame.shape[0]:
        y = 0

        while y < frame.shape[1]:
            
            if frameGray[x][y] < 120:
                corMedia = corMedia+frameGray[x][y]

            y += 1

        x += 1

    corMedia = int(corMedia[0]/(frame.shape[0]*frame.shape[1]))+7

    #print(corMedia)

    if corMediaAntiga != 0:

        if qtdFrame == 0 or qtdFrame == 16 or qtdFrame == 36 or qtdFrame == 60 or qtdFrame == 79:
            if qtdFrame == 16: ano = 2017
            elif qtdFrame == 36: ano = 2018
            elif qtdFrame == 60: ano = 2019
            elif qtdFrame == 79: ano = 2020

            if qtdFrame != 0:
                print("Ano: ", ano , "| minDes: ", round(minDesMata/tamanhoTela * 100, 2), "| maxDes ", round(maxDesMata/tamanhoTela * 100, 2))
                arquivo.write("Ano: " + str(ano) + " | minDes: " + str(round(minDesMata/tamanhoTela * 100, 2)) + " | maxDes " + str(round(maxDesMata/tamanhoTela * 100, 2)) + "\n")

            elif qtdFrame == 79: break

            maxDesMata = 0
            minDesMata = 1000000

        backupFrame = frame.copy()

        qtdDesMata = 0        
        x = 0

        while x < frame.shape[0]:
            y = 0

            while y < frame.shape[1]:
                resultado = CorPixel(frameGray[x][y], corMedia)

                if resultado == CorPixel(frameAntigo[x][y], corMediaAntiga):
                    if resultado == "desmatada":
                        frame[x][y] = [0,0,0]
                        qtdDesMata += 1
                    else: 
                        frame[x][y] = [0,255,0]

                else: frame[x][y] = [0,255,0]

                y += 1

            x += 1
        
        if minDesMata > qtdDesMata: minDesMata = qtdDesMata
        if maxDesMata < qtdDesMata: maxDesMata = qtdDesMata

        #print("Frame: ", qtdFrame, "| min: ", round(minDesMata/tamanhoTela * 100, 2), "| max ", round(maxDesMata/tamanhoTela * 100, 2), "| qtd ", qtdDesMata, "| des: ", round(qtdDesMata/tamanhoTela * 100, 2), "| mata", round((tamanhoTela - qtdDesMata)/tamanhoTela * 100, 2))

        cv2.imshow("videoOriginal", backupFrame)
        cv2.imshow("videoProcessado", frame)
        videoProcessado.write(frame)

        qtdFrame+=1

    if qtdFrame == 79: break

    frameAntigo = frameGray
    corMediaAntiga = corMedia

    if cv2.waitKey(1) == ord('q'):
            break
    
    retorno, frame = video.read()
    if not retorno: break
    
arquivo.close()

videoProcessado.release()

cv2.destroyAllWindows()
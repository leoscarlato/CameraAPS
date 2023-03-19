import numpy as np
import cv2 as cv

def criar_indices(min_i, max_i, min_j, max_j):
    import itertools
    L = list(itertools.product(range(min_i, max_i), range(min_j, max_j)))
    idx_i = np.array([e[0] for e in L])
    idx_j = np.array([e[1] for e in L])
    idx = np.vstack( (idx_i, idx_j) )
    return idx

def main():

    # Acessa a câmera
    camera = cv.VideoCapture(0)

    # Define a largura e altura do vídeo (tamanho pequeno para melhorar a performance)
    largura = 320
    altura = 240
    
    # Define o ângulo inicial de rotação
    grau = 0

    while True:
        
        # Captura um quadro da câmera
        captura_ok, quadro = camera.read()

        # Redimensiona o quadro para o tamanho definido
        quadro = cv.resize(quadro, (largura, altura))

        # Calcula as coordenadas do centro da imagem
        cy, cx = int(largura / 2), int(altura / 2)
        
        # Define a matriz de translação que leva o centro da imagem para a origem
        M_translacao = np.array([[1, 0, -cx], [0, 1, -cy], [0, 0, 1]])  # leva para esquerda e para cima
        
        # Define a matriz de rotação atual
        rotacao = np.array([[np.cos(np.radians(grau)), -np.sin(np.radians(grau)), 0], 
                        [np.sin(np.radians(grau)), np.cos(np.radians(grau)), 0], 
                        [0, 0, 1]])
        
        # Define a matriz de translação que leva a origem de volta ao centro da imagem
        M_inv_translacao = np.array([[1, 0, cx], [0, 1, cy], [0, 0, 1]])    # leva para direita e para baixo
        
        # Aplica as matrizes de transformação para girar a imagem no centro
        M_combinada = M_inv_translacao @ rotacao @ M_translacao

        # Calcula as coordenadas dos pixels da imagem rotacionada
        destino = criar_indices(0, altura, 0, largura)  # cria uma matriz com as coordenadas dos pixels da imagem rotacionada
        destino = np.vstack( (destino, np.ones((1, destino.shape[1]))) )    # acrescenta uma linha com 1s
        
        # Calcula as coordenadas dos pixels da imagem origina
        
        A = np.linalg.inv(M_combinada) @ destino    # calcula as coordenadas dos pixels da imagem original
        A = A.astype(int)  # converte para int32

        # Aplica o filtro para manter apenas os pixels dentro da imagem
        filtro = (A[0, :] >= 0) & (A[0, :] < altura) & (A[1, :] >= 0) & (A[1, :] < largura)
        
        A = A[:, filtro]    # aplica o filtro
        destino = destino[:, filtro]    # aplica o filtro

        # Cria uma imagem preta
        quadro_rotacionado = np.zeros((altura, largura, 3), dtype=np.uint8)

        # Copia os pixels da imagem original para a imagem rotacionada
        quadro_rotacionado[destino[0, :].astype(int), destino[1, :].astype(int)] = quadro[A[0, :], A[1, :]]
        
        # Decrementa o ângulo de rotação
        grau -= 3

        # Mostra a imagem
        cv.imshow('Imagem', quadro_rotacionado)

        # Aguarda uma tecla ser pressionada
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    # Libera a câmera
    camera.release()

    # Fecha todas as janelas
    cv.destroyAllWindows()

if __name__ == '__main__':
    main()

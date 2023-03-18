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

    # Define a largura e altura do vídeo
    largura = 640
    altura = 480
    
    # Define o ângulo inicial de rotação
    grau = 0

    while True:
        # Captura um quadro da câmera
        captura_ok, quadro = camera.read()
        
        # Calcula as coordenadas do centro da imagem
        cx, cy = int(largura/2), int(altura/2)
        
        # Define a matriz de translação que leva o centro da imagem para a origem
        M_translacao = np.array([[1, 0, -cx], [0, 1, -cy], [0, 0, 1]])  # leva para esquerda e para cima
        
        # Decrementa o ângulo de rotação
        grau -= 1

        # Define a matriz de rotação atual
        rotacao = np.array([[np.cos(np.radians(grau)), -np.sin(np.radians(grau)), 0], 
                        [np.sin(np.radians(grau)), np.cos(np.radians(grau)), 0], 
                        [0, 0, 1]])
        
        # Define a matriz de translação que leva a origem de volta ao centro da imagem
        M_inv_translacao = np.array([[1, 0, cx], [0, 1, cy], [0, 0, 1]])    # leva para direita e para baixo
        
        # Aplica as matrizes de transformação para girar a imagem no centro
        M_combinada = M_inv_translacao @ rotacao @ M_translacao
        quadro_rotacionado = cv.warpAffine(quadro, M_combinada[:2], (largura, altura))  # transformação afim -> 2x3
        
        # Exibe o quadro com a imagem rotacionada
        cv.imshow("Camera", quadro_rotacionado)
        
        # Verifica se a tecla 'q' foi pressionada para sair do loop
        if cv.waitKey(1) == ord('q'):
            break
        
    # Libera a câmera e fecha todas as janelas
    camera.release()
    cv.destroyAllWindows()
    
if __name__ == "__main__":
    main()

# APS3 - Efeitos de vídeo em tempo real

## Descrição

Neste projeto, deveríamos capturar a câmera do computador e fazer com que, usando os conceitos de Álgebra Linear, a imagem da câmera exibida na janela gerada quando o código é executado, realizasse um movimento de rotação contínua em torno do ponto central do quadro de exibição.

## Equações implementadas

No projeto tivemos que encontrar uma maneira que pudessemos fazer com que a imagem da câmera se movimentasse em torno do ponto central do quadro de exibição. Para isso, utilizamos as seguintes equações:

### Matriz de rotação

$$
R = 
\begin{bmatrix}
\cos (\theta) & -\sin (\theta) & 0 \\
\cos (\theta) & \cos (\theta) & 0 \\
0 & 0 & 1
\end{bmatrix}
$$

Essa foi a matriz que utilizamos para realizar a rotação da imagem. A cada iteração do loop principal do programa, o ângulo de rotação é decrementado em 3 graus, fazendo com que a imagem gire em torno do ponto central do quadro de exibição.

### Matriz de translação

$$
T =
\begin{bmatrix}
1 & 0 & \frac{- imagem_y}{2} \\
0 & 1 & \frac{- imagem_x}{2} \\
0 & 0 & 1
\end{bmatrix}
$$

Essa matriz foi utilizada para transladar a imagem para o centro do quadro de exibição.

### Matriz de translação inversa

$$
T2 = 
\begin{bmatrix}
1 & 0 & \frac{imagem_y}{2} \\
0 & 1 & \frac{imagem_x}{2} \\
0 & 0 & 1
\end{bmatrix}
$$

Essa matriz foi utilizada para transladar a imagem de volta para a posição original.

### Matriz combinada

$$
M = T2 \cdot R \cdot T
$$

Essa matriz foi utilizada para realizar a rotação da imagem em torno do ponto central do quadro de exibição.


![](girando.gif)

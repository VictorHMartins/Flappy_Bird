FLAPPY BIRD CLONE
  
  Este projeto é uma recriação do famoso jogo Flappy Bird utilizando a biblioteca Pygame. O objetivo do jogo é controlar um pássaro que deve passar entre os canos sem colidir.

1.REQUISITOS:

    -Antes de executar o jogo, certifique-se de ter os seguintes requisitos instalados:

        Python 3.x
  
        Biblioteca Pygame

2.INSTALAÇÂO DO PYGAME:

    -Caso ainda não tenha o Pygame instalado, utilize o seguinte comando:

         pip install pygame

3.COMO JOGAR:

    -Execute o jogo com o seguinte comando:

          python FleppyBird.py
  
    -Pressione a barra de espaço para fazer o pássaro pular.

    -O objetivo é evitar colisões com os canos e com o chão.

    -O jogo mostra sua pontuação na tela.

4.ESTRUTURA DO CÓDIGO

    -O jogo é composto pelas seguintes classes:
    
        Passaro: Controla o movimento e a animação do pássaro.
    
        Cano: Responsável por gerar e movimentar os canos.
    
        Chao: Gera e move o chão para dar a sensação de movimento.
    
        Função main(): Gerencia a lógica principal do jogo, incluindo colisões e pontuação.

5.RECURSOS UTILIZADOS

-O jogo utiliza imagens e fontes para criar uma interface visual amigável. As imagens são carregadas a partir da pasta imgs/ e incluem:

    bg.png (plano de fundo)
    
    base.png (chão)
    
    pipe.png (cano)
    
    bird1.png, bird2.png, bird3.png (animação do pássaro)

6.MELHORIAS FUTURAS

    -Botão de reinicio

    -Melhorar a detecção de colisão.

    -Criar um sistema de recorde.

    -Implementar diferentes dificuldades.


7.LICENÇA

    -Este projeto é de uso livre para aprendizado e melhorias pessoais. Sinta-se à vontade para modificar e compartilhar!

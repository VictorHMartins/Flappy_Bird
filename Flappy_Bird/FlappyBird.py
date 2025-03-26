import pygame #criação de jogos
import os #integrar os arquivos do computador com o codigo
import random #geração de numeros aleatorios

TELA_LARGURA = 500 #constantes- configurações do jogo
TELA_ALTURA = 800 #constantes- configurações do jogo

IMAGEM_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png'))) #carregar a imagem e duplicar em 2x para não ficar pequeno
IMAGEM_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png'))) #carregar a imagem e duplicar em 2x para não ficar pequeno
IMAGEM_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png'))) #carregar a imagem e duplicar em 2x para não ficar pequeno
IMAGENS_PASSARO = [ #lista das imagens do passaro
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png'))),
]

pygame.font.init() #configuração de texto para fonte da pontuação 
FONTE_PONTOS = pygame.font.SysFont('arial', 50) #fonte e tamanho

class Passaro:#classe passaro
    IMGS = IMAGENS_PASSARO #constantes do passaro- informações fixas
    ROTACAO_MAXIMA = 25 #animações da rotação
    VELOCIDADE_ROTACAO = 20 #animações da rotação
    TEMPO_ANIMACAO = 5 #animações da rotação
    
    #configurando um objeto com varios atributos
    def __init__(self, x, y):#método especial usado para inicializar os objetos
        self.x = x #atributos do objeto
        self.y = y #atributos do objeto
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y #tributo altura
        self.tempo = 0
        self.contagem_imagem = 0#quando a contagem bater 5 trocar a imagem
        self.imagem = self.IMGS[0]
        
    def pular(self): #função de pular
        self.velocidade = -10.5 #velocidade para subir
        self.tempo = 0 #conforme desloca faz a conta de velocidade
        self.altura = self.y
        
    def mover(self):
    #calcular o deslocamento
        self.tempo += 1
        #formula do deslocamento
        deslocamento = 1.5 * (self.tempo**2) + self.velocidade * self.tempo#S = so + vot + at2 / 2
    #restringir o deslocamento
        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2 #velocidade do deslocamento aqui
    #deslocar o passaro
        self.y += deslocamento
        
    #angulo do passaro
        if deslocamento < 0 or self.y < (self.altura + 50): # se tiver a cima da posição inicial continuar com o mesmo angulo, depois de cair alterar para angulo para baixo
            if self.angulo < self.ROTACAO_MAXIMA:
                self.angulo = self.ROTACAO_MAXIMA
        else:#quando estiver caindo -90 trocar o angulo do passaro
            if self.angulo > -90:
                self.angulo -= self.VELOCIDADE_ROTACAO
    
    def desenhar(self, tela):#como o passaro sera desenhado
        #definir qual imagem o passaro vai usar
        self.contagem_imagem += 1 
        
        if self.contagem_imagem < self.TEMPO_ANIMACAO:#se a contagem da imagem for maior que o tempo de animação de 5s trocar a imagem para a prox da lista
            self.imagem = self.IMGS[0] #asa para cima
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*2:
            self.imagem = self.IMGS[1] #asa pro meio
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*3:
            self.imagem = self.IMGS[2]#asa para baixo
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*4: 
            self.imagem = self.IMGS[1]#asa pro meio
        elif self.contagem_imagem >= self.TEMPO_ANIMACAO*4 +1 :
            self.imagem = self.IMGS[0]#asa para cima
            self.contagem_imagem = 0
            
            
         #se o passaro tiver caindo usar a imagem fixa para cair
        if self.angulo <= 80:
             self.imagem = self.IMGS[1]#cair parado
             self.contagem_imagem = self.TEMPO_ANIMACAO*2#quando tiver caindo, a primeira batida de asa sera para baixo
                 
        #desenhar a imagem
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)#recebe uma imagem e um ângulo (em graus) e rotaciona a imagem nesse ângulo.
        pos_centro_imagem = self.imagem.get_rect(topleft=(self.x, self.y)).center#ccria um retângulo ao redor da imagem usando a posição superior esquerda definida por self.x e self.y
        retangulo = imagem_rotacionada.get_rect(center=pos_centro_imagem)#cria um novo retângulo ao redor da imagem rotacionada, mas agora com o centro alinhado à posição calculada anteriormente (pos_centro_imagem)
        tela.blit(imagem_rotacionada, retangulo.topleft)# desenha a imagem rotacionada na tela. O blit é usado para colocar a imagem na superfície de destino
        
    def get_mask(self):#função para pegar a mascara do passaro
        return pygame.mask.from_surface(self.imagem)#pega a mascara do passaro e a mascara do cano e verifica se tem algump pixel em comum- se tiver, bateu
        
class Cano:
    DISTANCIA = 200 #constante, cano base e cano do too
    VELOCIDADE = 5# velocidade de mov do cano, anda de 5 em 5 para o ladp
    
    def __init__(self, x):
        self.x = x
        self.altura = 0 #altura do cano
        self.pos_topo = 0 # posição do topo
        self.pos_base = 0 #posição da base
        self.CANO_TOPO = pygame.transform.flip(IMAGEM_CANO, False, True)#inverte a imagem do cano de cabeça para baixo
        self.CANO_BASE= IMAGEM_CANO #imagem do cano
        self.passou = False #parametro para ver se o passaro ja passou
        self.definir_altura()
        
    def definir_altura(self):#define as alturas dos canos aleatoriamente
        self.altura = random.randrange(50, 450) #gera os canos entre 50 a 450
        self.pos_topo = self.altura - self.CANO_TOPO.get_height() #desenhando o cano do topo para cima
        self.pos_base = self.altura + self.DISTANCIA #para desenhar o cano de baixo pega a altura + a a distancia de um cano e outro
        
    def mover(self):
        self.x -= self.VELOCIDADE #mover de forma negativa
        
    def desenhar(self, tela):
        tela.blit(self.CANO_TOPO, (self.x, self.pos_topo)) #desenhar o cano de cima
        tela.blit(self.CANO_BASE, (self.x, self.pos_base)) #desenhar o cano de baixo
        
    def colidir(self, passaro):
        passaro_mask = passaro.get_mask() #mascara do passaro
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO) #mascara do topo
        base_mask = pygame.mask.from_surface(self.CANO_BASE) #mascara da base
        
        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y)) #calcula a distancia entre o topo e o passaro
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y)) #calcula a distancia entre a base e o passaro
        
        topo_ponto = passaro_mask.overlap(topo_mask, distancia_base) #verifica se a mask do passararo colide ou sobrepoe a do objeto
        base_ponto = passaro_mask.overlap(base_mask, distancia_base) #verifica se a mask do passararo colide ou sobrepoe a do objeto
        
        if base_ponto or topo_ponto:#se houver colisão retorna verdadeiro
            return True
        else:
            return False
    
class Chao:
    VELOCIDADE = 5 #constante da velocidade do chão
    LARGURA = IMAGEM_CHAO.get_width()#largura do chão
    IMAGEM = IMAGEM_CHAO #variavel imagem
    
    def __init__(self, y):
        self.y = y
        self.x0 = 0 #primeiro chão
        self.x1 = self.LARGURA #segundo chão
        
    def mover(self): #função para mover os dois chão
        self.x0 -= self.VELOCIDADE
        self.x1 -= self.VELOCIDADE
        
        #verificar se os elementos sairam completamente da tela pela esquerda
        if self.x0 + self.LARGURA < 0:
            self.x0 = self.x1 + self.LARGURA   
        if self.x1 + self.LARGURA < 0:
            self.x1 = self.x0 + self.LARGURA
            
    def desenhar(self, tela):
            tela.blit(self.IMAGEM, (self.x0, self.y)) #desenhar o chão
            tela.blit(self.IMAGEM, (self.x1, self.y))
            
def desenhar_tela(tela, passaros, canos, chao, pontos):
    tela.blit(IMAGEM_BACKGROUND, (0, 0)) #desenhar o fundo da tela
    for passaro in passaros: #para cada passaro na lista, retornar desenhar na tela
        passaro.desenhar(tela)
    for cano in canos:#desenhar o cano aleatoriamente
        cano.desenhar(tela)
        
    texto = FONTE_PONTOS.render(f"Pontuação: {pontos}", 1, (255, 255, 255))#renderizar o texto na tela
    tela.blit(texto, (TELA_LARGURA - 10 - texto.get_width(), 10))#desenhar pontuação na tela
    chao.desenhar(tela) #desenhar o chão
    
    pygame.display.update() #atualizar a tela
    
#logica de funcionamento do jogo
def main ():
    passaros = [Passaro(230, 350)]
    chao = Chao(730)
    canos = [Cano(700)]
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    pontos = 0
    relogio = pygame.time.Clock()
    
    rodando = True
    while rodando:
        relogio.tick(30)#FPS
        
        #forma de interagir com o jogo - interação com o usuario
        for evento in pygame.event.get():#eventos do jogo
            if evento.type == pygame.QUIT: #fechar o jogo
                rodando = False
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN: #evento de apertar uma tecla 
                if evento.key == pygame.K_SPACE: #quando apertar no espaço
                    for passaro in passaros: #pular
                        passaro.pular()
                        
        #mover as coisas              
        for passaro in passaros: #movimentar o passaro
            passaro.mover()
        chao.mover()#mover o chao
        
        adicionar_cano = False
        remover_canos = []
        for cano in canos: #para cada cano na lista
            for i, passaro in enumerate(passaros): #percorro a lista de passaros
                if cano.colidir(passaro): #se bateu com o cano, eu tiro o passaro
                    passaros.pop(i)
                if not cano.passou and passaro.x > cano.x: # se o x do passaro for maior que o x do cano
                    cano.passou = True #passou
                    adicionar_cano = True # adicionar novo cano
            cano.mover()
            if cano.x + cano.CANO_TOPO.get_width() < 0: #posição do x somar a largura e for menor que 0 sera removido
                remover_canos.append(cano) #adiciona na lista de canos removidos
                
        if adicionar_cano:
              pontos += 1 # se passou do cano ganha 1 ponto
              canos.append(Cano(600)) # adiciona outro cano na tela
              
        for cano in remover_canos:
            canos.remove(cano)
            
        for i, passaro in enumerate(passaros):
            if (passaro.y + passaro.imagem.get_height()) > 730 or passaro.y <0:
                passaros.pop(i)
        
        desenhar_tela(tela, passaros, canos, chao, pontos)
        
if __name__ == '__main__':#serve para garantir que o código dentro da função main() (ou qualquer código no bloco) será executado apenas quando o script for executado diretamente.
    main()
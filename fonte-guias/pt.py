BODY = {}

BODY["comecar"] = """
<p>Footfall se joga andando de verdade. O mapa é a sua cidade pelo GPS, e você só avança quando anda. Este guia leva você do primeiro toque até a primeira sessão na rua.</p>

<h2>Conta</h2>
<p>O jogo precisa de uma conta com e-mail e senha: é ela que guarda o seu personagem, a base e o progresso na nuvem. Na tela inicial, toque em <kbd>ENTRAR / CRIAR CONTA</kbd>. A senha tem pelo menos 8 caracteres e o cadastro é confirmado com um código de 6 dígitos enviado por e-mail.</p>

<h2>O seu sobrevivente</h2>
<ol class="steps">
<li><b>Antes de sair andando:</b> leia os avisos de segurança e toque em <kbd>ENTENDI, VAMOS</kbd>.</li>
<li><b>Aparência:</b> rosto, cabelo, pele e roupa.</li>
<li><b>Profissão e traços:</b> cada profissão dá habilidades e um saldo de pontos. Traços positivos gastam pontos; negativos devolvem.</li>
</ol>
<p>Algumas profissões para começar:</p>
<ul>
<li><b>Desempregado(a):</b> nenhum bônus, mas o maior saldo de pontos para traços.</li>
<li><b>Policial</b> e <b>Militar veterano(a):</b> melhores com armas de fogo (o militar já vem dessensibilizado ao pânico).</li>
<li><b>Enfermeiro(a)</b> e <b>Médico(a):</b> tratam feridas mais rápido e com menos falhas.</li>
<li><b>Marceneiro(a):</b> constrói e conserta a base melhor.</li>
<li><b>Entregador(a):</b> já começa com o bairro descoberto no mapa, e a distância andada rende mais.</li>
<li><b>Arrombador(a):</b> vasculha 1,5× mais rápido e faz menos barulho.</li>
</ul>
<p>Traços úteis: <b>Passos leves</b> (menos barulho), <b>Olhos de águia</b> (vê mais longe), <b>Organizado</b> (mochila maior), <b>Pele grossa</b> (golpes viram menos feridas). Cuidado com <b>Caseiro</b> (cansa longe da base) e <b>Fumante</b> (precisa de cigarro).</p>
<p>Você começa com o kit básico na mochila: taco, revólver com balas, bandagens, água, comida, calça jeans e mochila escolar.</p>
<div class="tip warn"><b>A morte é permanente</b>Se o personagem morrer, ele e as habilidades dele se vão. A base, os baús e o depósito do rádio ficam para o próximo.</div>

<h2>A primeira noite</h2>
<p>Antes do mapa, o jogo oferece <b>A última entrega</b>: você é um carteiro numa noite de tempestade, e ela ensina a andar agachado, vasculhar, golpear, empurrar e atirar. Dá para pular com <kbd>IR DIRETO PARA A CIDADE</kbd> e jogar depois pela estante de memórias.</p>

<h2>Sessão</h2>
<p>No mapa, toque em <kbd>INICIAR SESSÃO</kbd> na barra de baixo. A partir daí o seu personagem anda com você. Para parar, abra o menu <kbd>⋯</kbd>:</p>
<ul>
<li><kbd>Dormir (encerrar aqui)</kbd> na base, num posto avançado ou numa barraca: o personagem descansa e recupera cansaço e vida.</li>
<li><kbd>Encerrar sessão</kbd> em qualquer outro lugar: você não perde nada, mas o descanso é ruim.</li>
</ul>

<h2>Ver e ser visto</h2>
<ul>
<li>Você enxerga num cone de 110° à sua frente, até 120 m de dia e 40 m à noite. Prédios tapam a visão.</li>
<li>O cone segue o topo do celular (bússola). Se a bússola atrapalhar, desligue em Ajustes e use o analógico para olhar.</li>
<li>Zumbis te veem a uns 15 m de dia e 8 m à noite, mas a lanterna acesa faz você ser visto a 30 m.</li>
<li>Andar faz pouco barulho; correr faz muito mais. O barulho chama quem está por perto.</li>
</ul>

<h2>Quanto mais anda, melhor o saque</h2>
<p>A distância andada na sessão aumenta a chance de achar itens raros (até 15%). Só conta andando a pé: acima de uns 25 km/h por alguns segundos o jogo entende que é veículo, a distância para de contar e o barulho vai ao máximo.</p>

<div class="tip"><b>Atravessando a rua</b>Em avenidas, os zumbis param e não começa luta: aparece "Atravesse com atenção". Olhe a rua de verdade, não a tela. Nunca jogue dirigindo.</div>
"""

BODY["saque"] = """
<p>Mercados, farmácias, delegacias, postos, escolas, lojas e casas do seu bairro estão no jogo. Cada tipo de lugar tem os seus achados e os seus perigos.</p>

<h2>Pela porta ou entrando</h2>
<p>Chegando a até 35 m de um lugar (casas: encostado nelas), toque em <kbd>Saquear</kbd>. Você escolhe:</p>
<ul>
<li><b>Pela porta:</b> rápido, só os móveis da entrada e sem itens raros.</li>
<li><b>Entrar:</b> abre a tela de ação dentro do prédio. Mais móveis, mais chance de raro e mais zumbis. Prédios podem ter andares (<kbd>SUBIR</kbd> / <kbd>DESCER</kbd>).</li>
</ul>
<p>Se você se afastar mais de 20 m no meio do saque, ele é interrompido.</p>

<h2>Móveis e barulho</h2>
<p>Cada móvel tem um tempo para vasculhar e um nível de barulho: <b>silencioso</b>, <b>barulho médio</b> ou <b>barulho alto</b>. Uma gaveta leva 1 s; um caixa registradora, 2,5 s e faz barulho; um arsenal trancado, 5 s e muito barulho. Fique parado enquanto vasculha e toque em <kbd>Pegar tudo</kbd> no fim.</p>
<ul>
<li>Às vezes o móvel está vazio.</li>
<li>Vasculhar vidro e lata pode cortar a mão (estilhaço).</li>
<li>Portas trancadas abrem com pé de cabra (3 s, com barulho) ou quando um zumbi lá dentro quebra a porta.</li>
</ul>

<h2>Estoque toda semana</h2>
<p>Um lugar saqueado fica marcado como "já saqueado" por 7 dias; depois ele enche de novo. O estoque é o mesmo para todos: se aparecer "Outro sobrevivente pegou antes", alguém chegou primeiro.</p>

<h2>Corpos</h2>
<p>Zumbis abatidos ficam no chão por 2 horas. Cada luta vira uma pilha de corpos: <kbd>Revistar todos</kbd> passa por todos de uma vez. Corpos trazem coisas do bolso, panos e, às vezes, selos. Zumbis de uniforme (polícia, bombeiro, médico…) carregam o que usavam em vida, e às vezes o uniforme inteiro.</p>

<h2>Mochila e peso</h2>
<p>O quanto você carrega é a soma dos bolsos das roupas e da mochila:</p>
<ul>
<li>Bolsos do corpo: 4 kg, mais os bolsos de calças, coletes, pochete e bolsa de coxa.</li>
<li>Mochilas: escolar 6 kg, academia 5, caminhada 10, tática 12, cargueira 16.</li>
<li>Força, Organizado e Desorganizado mudam esse limite.</li>
</ul>
<p>Acima do limite aparece <b>Carga pesada</b>: você fica mais lento na luta e mais barulhento no mapa.</p>
<p>O cinto tem 2 vagas para o que você precisa na mão rápido (a 3ª com colete tático ou mochila tática). Armas longas vão nas costas.</p>
<div class="tip"><b>Dica</b>Remédios, munição, coisas de arremessar e pilhas vão primeiro para os bolsos. Na luta, tirar qualquer outra coisa do fundo da mochila leva 2,5 s.</div>

<h2>Bunkers militares</h2>
<p>Todo mês, algumas praças viram bunkers com 3 a 6 andares para baixo, cada vez mais escuros e mais perigosos, e com saque cada vez melhor. Cada andar começa numa sala segura, onde os zumbis não entram. O gerador de um andar acende a luz com 1 biodiesel. A porta-cofre do fundo abre com o cartão de acesso, ou com pé de cabra em 60 s e muito barulho. O bunker reabastece no mês seguinte.</p>
"""

BODY["combate"] = """
<p>Quando um zumbi que está atrás de você chega a 25 m, o jogo pede que você pare num lugar seguro e abre a <b>tela de ação</b>: a cena em pixel art do lugar onde você está, com as ruas, os carros e os prédios de verdade. Também dá para abrir pelo botão grande <kbd>Tela de ação</kbd> do mapa.</p>
<p>Zumbis a até 120 m entram na luta, alguns de cada vez. Na base em segurança ou atravessando uma avenida, não começa luta.</p>

<h2>Os três controles</h2>
<p>Escolha em Ajustes → <kbd>CONTROLES</kbd> (ou tocando no cartão de status durante a luta):</p>
<ul>
<li><b>Simples</b> (padrão): um analógico para andar e o botão <kbd>LUTAR</kbd>. Com ele ligado, você encara o zumbi mais perto; toque na metade direita da tela para golpear ou atirar e na esquerda para empurrar. Correr desliga.</li>
<li><b>Dois analógicos:</b> o direito mira; toque na tela golpeia e empurra.</li>
<li><b>Automático:</b> só o analógico de andar; golpe, tiro e empurrão saem sozinhos.</li>
</ul>

<h2>Empurrar</h2>
<p>O empurrão é a sua melhor defesa: derruba ou desequilibra, solta você de quem te agarrou e baixa o pânico. Ele gasta fôlego e tem uma pequena espera entre um e outro.</p>

<h2>Mirar e acertar</h2>
<ul>
<li>Escolha o <kbd>ALVO</kbd>: cabeça, corpo ou pernas.</li>
<li>Na cabeça, o golpe dá mais dano, mas pode escorregar para o ombro (menos com mais habilidade). Tiro na cabeça dá 2,5× de dano.</li>
<li>Pernas destruídas fazem o zumbi rastejar.</li>
<li>Acertos com a ponta da arma podem ser críticos.</li>
</ul>

<h2>Fôlego</h2>
<p>Correr gasta fôlego rápido; parado ele volta. Com pouco fôlego, os golpes perdem força. Cansaço, febre, frio, calor e dor diminuem o fôlego máximo.</p>

<h2>Agachar</h2>
<p><kbd>AGACHAR</kbd> deixa você lento e sem correr, mas os zumbis distraídos demoram o dobro para te notar e precisam estar bem mais perto. Por trás, fora da visão deles, dá para abater em silêncio.</p>

<h2>Armas</h2>
<ul>
<li><b>Brancas</b> (faca, taco, facão, machado, marreta, katana…): gastam a cada golpe que acerta e quebram. Dá para consertar na bancada ou com fita e prego.</li>
<li><b>De fogo</b> (pistola, revólver, escopeta, carabina, rifle, submetralhadora, fuzil): não gastam, mas cada tiro chama zumbis num raio de 150 m. O silenciador abafa alguns tiros de pistola.</li>
<li><b>Arco e besta:</b> quase silenciosos; parte das flechas volta depois da luta.</li>
<li><b>Arremesso:</b> garrafa, pedra, despertador e rojão distraem; o molotov põe fogo no chão.</li>
</ul>
<p>Recarregar com munição no bolso é rápido; se ela estiver só na mochila, demora o dobro.</p>

<h2>Zumbis diferentes</h2>
<p>Além do comum, há zumbis de uniforme: o <b>presidiário</b> é rápido, o <b>militar</b> e o <b>bombeiro</b> aguentam muito (o bombeiro não pega fogo), o <b>policial</b> tem colete, o <b>mochileiro</b> carrega mais coisas. O <b>Brutamontes</b> é enorme, lento e aguenta seis vezes mais.</p>

<h2>Sair da luta</h2>
<ul>
<li>O ícone da porta (<kbd>Sair</kbd>) aparece quando ninguém está a menos de 10 m e ninguém está atrás de você.</li>
<li>Fique a 40 m de todos que te viram por alguns segundos e eles perdem você.</li>
<li>Ou corra para a borda vermelha da cena.</li>
</ul>
<div class="tip"><b>Outros sobreviventes</b>Quem estiver perto de você no mundo real aparece na mesma cena, e o mapa avisa quando alguém está lutando ali perto.</div>
"""

BODY["saude"] = """
<p>O corpo do seu sobrevivente funciona como um corpo. Cada golpe de zumbi pode virar uma ferida numa parte do corpo, e cada ferida tem o seu tratamento. Tudo fica em <b>Personagem → Saúde</b>.</p>

<h2>Feridas</h2>
<ul>
<li><b>Arranhão:</b> sangra pouco, fecha em 1 dia.</li>
<li><b>Laceração:</b> sangra mais, 3 dias. Às vezes vira <b>hemorragia</b>, que sangra muito rápido.</li>
<li><b>Mordida:</b> sangra e quase sempre infecta.</li>
<li><b>Corte profundo:</b> precisa de sutura.</li>
<li><b>Estilhaço:</b> do vidro ao vasculhar; tire com pinça.</li>
<li><b>Fratura:</b> precisa de tala, 7 dias.</li>
<li><b>Queimadura:</b> pomada e faixa.</li>
</ul>

<h2>Tratar passo a passo</h2>
<ol class="steps">
<li><b>Torniquete</b> (hemorragia): pare o sangue com torniquete ou pano. Não deixe mais de 2 horas sem suturar.</li>
<li><b>Limpar e desinfetar:</b> soro, álcool ou cachaça.</li>
<li><b>Tirar o estilhaço</b> com pinça, quando houver.</li>
<li><b>Suturar</b> com kit de sutura (cortes profundos e hemorragias).</li>
<li><b>Enfaixar:</b> atadura, gaze, bandagem ou pano.</li>
</ol>
<p>A ferida só cicatriza com todos os passos feitos. Curativos sujam depois de 12 horas (24 com esparadrapo) e precisam ser trocados; pano já conta como sujo. Ferida suja infecciona, e infecção comum se cura com antibiótico.</p>

<h2>A infecção zumbi</h2>
<div class="tip warn"><b>Não tem cura</b>Uma mordida infecta quase sempre; laceração e arranhão, às vezes. A infecção corre no tempo real: alguns dias sem nada, depois febre, depois delírio, e em 7 dias o personagem morre.</div>

<h2>Fome e sede</h2>
<p>O personagem gasta comida e água como uma pessoa, e mais quando anda. Os avisos aparecem em três níveis ("Com fome", "Faminto", "Passando mal de fome"). Só no último nível ele perde vida, e só durante a sessão: com o app fechado ninguém morre de fome.</p>
<p>Comida cozida rende mais e dura mais. Para cozinhar, acenda uma fogueira ou o fogão a lenha (isqueiro e tábua). Água de chuva pode dar enjoo: ferva antes.</p>

<h2>Frio e calor</h2>
<p>A temperatura é a da sua cidade agora. Na chuva sem capa e à noite faz mais frio; abaixo de 16 °C você precisa de roupa quente. No calor, roupa pesada cansa e o boné ajuda. Frio gasta comida; calor gasta água.</p>

<h2>Cansaço e sono</h2>
<p>Andar, correr e lutar cansam. Encerrar a sessão com <kbd>Dormir</kbd> na base, num posto ou numa barraca recupera o cansaço e a vida enquanto você está fora. Com cama na base o descanso é bem melhor; fora dela, saco de dormir ajuda.</p>

<h2>A cabeça também</h2>
<p>Pânico na luta tira a precisão; empurrar alivia. Ficar muito tempo parado na base deixa o personagem entediado, e passar por muita coisa ruim o deixa triste. Sair para andar ajuda.</p>

<h2>Roupas</h2>
<p>Roupas protegem a parte do corpo que cobrem. Roupa rasgada protege pela metade: costure com agulha, linha e um pano.</p>

<h2>Quando ele morre</h2>
<p>O personagem e as habilidades se vão. Tudo o que ele carregava fica numa pilha onde caiu: por 24 horas só você vê, depois qualquer um, e um zumbi com o rosto dele vigia. A carteira perde 15% dos selos. A base, os baús, o depósito do rádio e as roupas do armário ficam. Toque em <kbd>Novo sobrevivente</kbd> e volte para a rua.</p>
"""

BODY["base"] = """
<p>A base é o lugar onde você guarda o que juntou, dorme e cozinha. Toda noite os mortos batem nas paredes.</p>

<h2>Demarcar</h2>
<ol class="steps">
<li>Com a sessão ligada, abra o menu da base e toque em <kbd>Demarcar base</kbd>.</li>
<li>Toque na grade para marcar os cantos (até 60 m de você). Toque no primeiro canto de novo para fechar.</li>
<li>Toque em <kbd>Demarcar base</kbd> para confirmar.</li>
</ol>
<p>Começa com 50 m², e cresce com kits de expansão e com gente no grupo. Precisa estar a pelo menos 30 m de outra base.</p>
<div class="tip warn"><b>Privacidade</b>A base fica visível para quem passa perto. Não demarque a base onde você mora. Em casa, use um posto avançado.</div>

<h2>Paredes, portas e janelas</h2>
<ul>
<li>Paredes de prédio são de graça e não caem.</li>
<li>Paredes suas: 1 tábua e 1 prego a cada 4 m. Dá para reforçar com chapa e depois com concreto.</li>
<li>Porta: 3 tábuas e 2 pregos. Janela: 2 tábuas e 1 prego (tábuas pregadas reforçam).</li>
<li><kbd>Consertar a parede mais fraca</kbd> gasta 1 tábua e 1 prego.</li>
</ul>
<p>Porta aberta ou parede caída = base aberta.</p>

<h2>Móveis</h2>
<p>Na tela de ação, dentro da base, use o martelo para montar e <kbd>USAR</kbd> para usar:</p>
<ul>
<li><b>Baú:</b> 40 kg cada. Nada entra sozinho: guarde você.</li>
<li><b>Bancada:</b> receitas e consertos.</li>
<li><b>Cama:</b> descanso bem melhor. <b>Maca:</b> feridas tratadas cicatrizam mais rápido.</li>
<li><b>Mesa</b>, <b>fogueira</b> (luz e barulho à noite), <b>fogão a lenha</b> (quase sem luz).</li>
<li><b>Barril de chuva:</b> junta água quando chove de verdade.</li>
<li><b>Torre de vigia:</b> enxerga mais longe perto da base. <b>Holofote:</b> precisa de gerador e gasolina.</li>
<li><b>Caixa de correio:</b> o mercado (veja o guia de grupo).</li>
</ul>

<h2>Horta</h2>
<p>Até 4 canteiros: <kbd>Plantar</kbd> as sementes, <kbd>Regar</kbd> (cada rega dura um dia) e <kbd>Colher</kbd> depois de uns 3 dias regados.</p>

<h2>Armadilhas</h2>
<ul>
<li><b>Estacas</b> e <b>buraco coberto:</b> pegam atacantes e precisam ser rearmados.</li>
<li><b>Arame com latas:</b> alarme que avisa e reduz o estrago.</li>
</ul>

<h2>O ataque de toda noite</h2>
<p>À 1h da manhã a base é atacada, mesmo com o app fechado (até 3 noites perdidas são resolvidas quando você volta). Paredes maiores, fogueira acesa e holofote ligado atraem mais gente. As armadilhas pegam alguns; os outros batem nas paredes, portas e janelas.</p>
<p>Se alguma parede cair ou porta ficar aberta, os baús perdem parte do que tem dentro (roupas ficam). A horda da semana também passa pela base se a rota chegar perto.</p>
<div class="tip"><b>Estar lá ajuda</b>Se você estiver na base com a sessão ligada, o estrago cai pela metade.</div>

<h2>O depósito do rádio e os postos</h2>
<p>O depósito do rádio é só seu, com 300 kg, e você chega nele de qualquer posto avançado ou barraca. Lá ficam o depósito, a bancada, o rádio para voltar à base, o correio (mercado e armazém), o armário de roupas e a estante de memórias. As roupas do armário ficam mesmo depois da morte.</p>
<p>Você pode ter até 10 postos avançados, entre 200 m e 20 km da base e a 100 m uns dos outros. O primeiro é de graça; os outros pedem um rádio de posto.</p>
"""

BODY["grupo"] = """
<h2>Grupo</h2>
<p>No ícone <kbd>Grupo</kbd>, crie um grupo ou entre num com o código. Até 10 pessoas.</p>
<ul>
<li>Avisos rápidos no mapa: <kbd>HORDA AQUI</kbd>, <kbd>LOOT AQUI</kbd> e <kbd>SOCORRO!</kbd>.</li>
<li>Conversa do grupo, e troca de itens lado a lado.</li>
<li>Uma base só para o grupo, com baús compartilhados. Ao entrar num grupo, a sua base é desmontada e o que tinha vai para o depósito do rádio.</li>
<li>Papéis no grupo dão mais experiência: <b>Médico</b>, <b>Construtor</b> e <b>Batedor</b>.</li>
</ul>
<p>Ninguém fora do grupo vê o seu nome. Para trocar com qualquer pessoa perto (até 40 m), use <kbd>Trocar com alguém aqui</kbd> no menu.</p>

<h2>Selos e mercado</h2>
<p>A moeda do apocalipse é o <b>selo</b>. O mercado de todo mundo fica na <b>caixa de correio</b> da base ou do depósito do rádio:</p>
<ul>
<li><kbd>Mercado</kbd>: compre e venda com outros sobreviventes. Você tem 6 vagas; pôr uma oferta custa 1 selo e quem vende paga uma pequena taxa. Ninguém vê o que os outros negociam, só o preço de referência.</li>
<li><kbd>Armazém</kbd>: o balcão vende o básico e compra qualquer coisa barato, funciona mesmo sem internet.</li>
</ul>
<p>Selos parados demais acima de 300 perdem um pouco por semana. Morrer custa 15% deles.</p>

<h2>Pontos dominados</h2>
<p>Lugares grandes (saúde, mercado, restaurante, construção, posto, polícia, bombeiros, escola) têm bandeira. Toque em <kbd>Tomar o ponto</kbd> e vença quem está lá numa arena com carros e barricadas: no começo são bandidos, muitos armados.</p>
<p>Ganhou, o ponto é seu (ou do grupo) e paga 4 selos por dia. Deixe até 6 guardas: cada um leva uma arma sua (e a munição). Guarda que cai some com a arma. Sem guardas, qualquer um toma sem luta.</p>

<h2>Sinalizadores de resgate</h2>
<p>Acenda um sinalizador e aguente as ondas: fácil (3), médio (4) ou difícil (5, com o Brutamontes no fim). Vencendo, cai uma caixa de resgate e você tem 30 minutos para pegar o que der.</p>
"""

BODY["corvo"] = """
<h2>O corvo</h2>
<p>Quando você põe a primeira porta na base, um corvo pousa nela. Ele fica. Só você o vê.</p>
<ul>
<li><b>Avisa a horda:</b> quando muitos zumbis vêm atrás de você, ele chega voando daquela direção, grasnando.</li>
<li><b>Mostra corpos:</b> rodeia pilhas de corpos que ainda não foram revistadas.</li>
<li><b>Um lugar por dia:</b> pousa num lugar não saqueado ali perto que ganha um item raro a mais.</li>
<li>Voa da direção dos avisos do seu grupo, e foge de barulho alto.</li>
</ul>
<p>No botão <kbd>Corvo</kbd> do mapa, dê comida para criar laço. Com mais confiança ele leva coisas leves até o depósito, aponta zumbis especiais, busca um item pequeno do depósito e, no último nível, grasna para distrair até 3 zumbis por um tempo. Com fome, ele não voa.</p>

<h2>A Rádio Corvo</h2>
<p>Com um rádio na mochila, nos baús ou no depósito, abra o menu → <kbd>Rádio</kbd>:</p>
<ul>
<li><b>A horda da semana:</b> anunciada desde segunda, de 30 a 60 zumbis vindos de uma direção, numa noite entre quarta e domingo. Ela atravessa a região em linha reta, e o rádio diz se passa perto da sua base.</li>
<li><b>Caixas de suprimento:</b> 2 por semana na região, de dia. Ficam 24 horas e o barulho delas chama zumbis por um tempo. Sem rádio, você só fica sabendo das muito perto.</li>
<li><b>Dica do dia:</b> um lugar não saqueado com um item raro a mais.</li>
<li><b>Missão da semana:</b> abater, saquear, andar ou guardar tábuas, e ganhar selos.</li>
<li>A frase do dia, e alarmes que disparam pela cidade e puxam os zumbis.</li>
</ul>

<h2>Clima e hora reais</h2>
<ul>
<li><b>Chuva:</b> abafa o seu barulho, encurta a visão, esfria e enche o barril.</li>
<li><b>Neblina:</b> encurta muito a visão.</li>
<li><b>Tempestade:</b> abafa mais o barulho, mas deixa os zumbis agitados.</li>
<li><b>Noite:</b> começa no pôr do sol de verdade. Na madrugada eles ficam agitados e ouvem melhor.</li>
<li><b>Lua cheia:</b> você vê mais longe à noite, mas eles também, e mais deles saem andando.</li>
</ul>
"""

BODY["memorias"] = """
<p>Pela cidade há livros raros que guardam os últimos dias de quem veio antes. Cada um é uma <b>memória</b>: uma história jogável, com começo, meio e fim, e uma roupa de recompensa.</p>

<h2>Onde achar</h2>
<p>Os livros (<i>Memória: …</i>) são lendários e aparecem muito raramente nos móveis <b>de dentro</b> dos lugares: só entrando, nunca pela porta. Cada memória sai de um tipo de lugar:</p>
<ul>
<li><b>Seu Jorge:</b> casas</li>
<li><b>O plantão:</b> lugares de saúde</li>
<li><b>A voz do corvo:</b> lojas de eletrônicos</li>
<li><b>Plantão de quinta:</b> delegacias</li>
<li><b>O cofre:</b> bunkers militares</li>
</ul>
<p>Quem já leu um livro não acha outro igual. Se achar repetido, ele vira 3 selos.</p>

<h2>Jogar</h2>
<ol class="steps">
<li>Na mochila, toque no livro e em <kbd>Pôr na estante</kbd>.</li>
<li>Vá a um posto avançado ou barraca e entre no depósito do rádio.</li>
<li>Abra a <kbd>ESTANTE DE MEMÓRIAS</kbd>, toque na lombada e em <kbd>JOGAR</kbd>. A sessão é encerrada para a memória começar.</li>
</ol>
<p>Na memória você joga com outra pessoa, com o kit dela; o seu personagem fica guardado e nada do que acontece lá mexe nele. Se cair antes do fim, a memória falhou: recomece <kbd>DESTE PONTO</kbd> ou <kbd>DO COMEÇO</kbd>. A estante guarda o seu recorde de abates.</p>

<h2>As sete memórias</h2>
<ul>
<li><b>A última entrega:</b> o carteiro na noite da tempestade. Roupa de Carteiro.</li>
<li><b>Seu Jorge:</b> o porteiro que fechou o prédio. Roupa de Porteiro.</li>
<li><b>O plantão:</b> a enfermeira Lúcia no último plantão do pronto-socorro. Roupa de Enfermeira.</li>
<li><b>A voz do corvo:</b> a radialista Rosa, que não saiu do ar. Fone de radialista, e a frase do dia da rádio passa a ser assinada por ela.</li>
<li><b>Plantão de quinta:</b> o soldado Ramos segurando a delegacia. Farda de Policial.</li>
<li><b>O cofre:</b> o soldado Nunes descendo o bunker andar por andar. Farda Militar.</li>
<li><b>O corvo:</b> só voar e ler. Aparece na estante depois que as outras seis forem jogadas.</li>
</ul>
<div class="tip"><b>Fitas na pata</b>Terminando O corvo, o seu corvo passa a usar uma fita de cada memória.</div>
"""

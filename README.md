# twitter_cliente-servidor

Introdução

Neste trabalho iremos implementar um servidor e clientes para troca de mensagens de forma similar ao serviço da plataforma Twitter. Clientes enviam mensagens para o servidor informando em quais mensagens estão interessados. O servidor recebe mensagens de clientes e repassa cada mensagem para todos os clientes que estão interessados naquela mensagem. O tópico de uma mensagem é definido pelos tags que ela contém. Cada cliente envia ao servidor em quais tags está interessado, e o servidor irá repassar ao cliente todas as mensagens que contém pelo menos uma tag de seu interesse. Esse paradigma de comunicação é conhecido como publish/subscribe.

Protocolo
Servidores e clientes trocam mensagens curtas de até 500 bytes usando o protocolo TCP.  Mensagens carregam texto codificado segundo a tabela ASCII. Apenas letras, números, os caracteres de pontuação ,.?!:;+-*/=@#$%()[]{} e espaços podem ser transmitidos. (Caracteres acentuados não podem ser transmitidos.)

Clientes informam ao servidor que estão interessados em receber mensagens com um tag enviando uma mensagem contendo o caractere + (mais) seguido do identificador do tag.  Clientes podem informar ao servidor que não estão mais interessados num tag enviando uma mensagem contendo o caractere - (menos) seguido do identificador da tag.  Identificadores de tag são qualquer sequência de letras (sem números e sem pontuação).  O servidor deve confirmar mensagens de declaração de interesse “+tag” com uma mensagem de texto contendo “subscribed +tag”; de forma similar, o servidor deve confirmar mensagens de declaração de desinteresse “-tag” com uma mensagem de texto contendo “unsubscribed -tag”. Por exemplo, abaixo segue um exemplo de comunicação do cliente com o servidor, onde linhas começando com > são enviadas pelo cliente e linhas começando com < foram recebidas do servidor:

> +dota
< subscribed +dota
> -overwatch
< unsubscribed -overwatch

Clientes podem enviar mensagens com um tag colocando um caractere # (tralha) seguido do identificador do tag.  Uma mensagem pode ter mais de um tag. O servidor replica uma mensagem para todos os clientes que informaram interesse em qualquer um dos tags de uma mensagem. Por exemplo, o cliente acima poderia poderia receber as seguintes mensagens:

< bloodcyka noob hero #dota
< perdeu eh culpa do suporte #dota #overwatch

Caso um cliente informe interesse em um tag pro qual já tenha informado interesse antes, o servidor deve responder com uma mensagem contendo “already subscribed +tag”. Caso um cliente declare desinteresse por uma tag pra qual não tenha informado interesse, o servidor deve responder com uma mensagem “not subscribed -tag”. A sequência abaixo exemplifica esses casos:

> +dota
< subscribed +dota
> +dota
< already subscribed +dota
> -dota
< unsubscribed -dota
> -dota
< not subscribed -dota

Uma mensagem sem um tag pode ser enviada ao servidor, mas não será repassada a nenhum cliente.

Detalhes de implementação do protocolo:

O servidor deve enviar no máximo uma cópia de cada mensagem a um cliente independente do número de tags na mensagem nas quais o cliente informou interesse.
As mensagens de interesse (+tag) e desinteresse (-tag) devem ter o sinal (+ ou -) no primeiro caractere e apenas um tag, sem nenhum texto adicional.
O servidor deve esquecer todas as tags de interesse de um cliente quando o cliente desconectar-se do sistema. (Em outras palavras, quando um cliente conecta-se ao servidor, ele precisa enviar para os servidor em quais tags tem interesse.)

Tags e especificações de interesse e desinteresse devem estar precedidas e sucedidas por espaço, início da mensagem, ou término da mensagem. Em outras palavras, um string como “#dota#overwatch” não será considerado como tags.

As mensagens são terminadas com um caractere de quebra de linha ‘\n’.

O servidor deve descartar mensagens com caractere(s) inválido(s). O servidor pode desconectar o cliente que enviou a mensagem com caractere inválido, mas precisa continuar a operação sem impacto para os demais clientes conectados. Em outras palavras, o servidor não deve fechar ao receber uma mensagem com caracteres inválidos. Clientes podem simplesmente abortar operação caso recebam mensagens com caractere(s) inválido(s) do servidor.

Para funcionamento do sistema de correção semi-automática (descrito abaixo), seu servidor deve fechar todas as conexões e terminar execução ao receber uma mensagem contendo apenas “##kill” de qualquer um dos clientes.


Como especificado acima, mensagens podem ter até 500 bytes e o fim de uma mensagem é identificado com um caractere ‘\n’. Uma mensagem não pode ultrapassar 500 bytes (i.e., um caractere ‘\n’ deve aparecer entre os primeiros 500 bytes). Caso essas condições sejam violadas, o servidor pode inferir que há um bug no cliente e desconectá-lo.

Qualquer incoerência ou ambiguidade na especificação deve ser apontada para o professor; se confirmada a incoerência ou ambiguidade, o aluno que a apontou receberá um ou dois pontos extras dependendo da gravidade da incoerência ou ambiguidade.  

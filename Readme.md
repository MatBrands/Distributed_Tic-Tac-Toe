# Distributed Tic-Tac-Toe

- Instituição: Universidade Estadual de Santa Cruz
- Curso: Ciência da Computação
- Disciplina: CET100 - Sistemas Distribuídos
- Docente: Paulo Andre Sperandio Giacomin
- Discente: Matheus Miranda Brandão

Este projeto tem como objetivo a conclusão da avaliação prática para a disciplina. Deve-se implementar um jogo da velha 7x7 utilizando os conceitos de sistemas distribuídos, dois jogadores em máquinas distintas devem conectar-se a um servidor para poder jogar. Um jogador ganha quando enfileira 4 peças de mesmo valor, na mesma linha, na mesma coluna, ou em diagonal.

## Conteúdo
- Tecnologias
- Instalação/Execução
- Organização do projeto
- Middleware
- License

## Tecnologias
Esse projeto utiliza as seguintes bibliotecas:

python=3.11.3
numpy=1.24.3
pyro5=5.14
sys
os

## Instalação/Execução
Foi utilizado o Python v3.11.3.

### Conda
No desenvolvimento foi utilizado o gerenciador de pacotes e ambientes Conda. Portanto para prosseguir necessita-se de sua instalação.

Navegar até a pasta de destino
```sh
cd utils
```

Instalar dependências
```sh
conda env create -f environment.yml
```

Ativar
```sh
conda activate tic_tac_toe_venv
```

Desativar
```sh
conda deactivate
```

### Requirements
Pode-se utilizar o arquivo requirements.txt para criar o ambiente virtual.

Criar ambiente virtual
```sh
python -m venv tic_tac_toe_venv
```

Ativar
```sh
source ./tic_tac_toe_venv/bin/activate
```

Navegar até a pasta de destino
```sh
cd utils
```

Instalar dependências
```sh
pip install -r requirements.txt
```

Desativar
```sh
deactivate
```

### Execução
As dependências devem ser instaladas em ambos os lados, cliente e servidor. As instruções de instalação já foram descritas acima. Lembrando de **ativar** o ambiente virtual antes de executar o programa.

A execução do programa é feita em duas etapas, inicialmente deve-se executar o servidor e em seguida os clientes.

#### Server
Para funcionamento, inicialmente deve-se inicializar o servidor

Navegar até a pasta de destino
```sh
cd tic_tac_toe/server
```

Execute o programa
```sh
python __init__.py
```

O servidor ficará aguardando por conexões de clientes.

### Client
Após o servidor estar ativo, pode-se executar o cliente. O cliente pode ser executado em quantas máquinas forem necessárias. O programa irá solicitar o IP e a Porta do servidor, que deve ser informado para que o cliente possa se conectar.

Navegar até a pasta de destino
```sh
cd tic_tac_toe/client
```

Execute o programa
```sh
python __init__.py
```

## Organização do projeto

```sh
.
├── License
├── Readme.md
├── tic_tac_toe
│   ├── client
│   │   └── __init__.py
│   └── server
│       ├── __init__.py
│       └── src
│           ├── Lobby.py
│           └── TicTac.py
└── utils
    ├── environment.yml
    └── requirements.txt
```

## Middleware
Na resolução do projeto foi proposto a utilização do middleware RPC (Remote Procedure Call) que é um modelo de comunicação que permite que um programa execute um procedimento em outro computador ou processo, como se estivesse chamando uma função local. O objetivo do RPC é tornar a comunicação entre sistemas distribuídos mais transparente e fácil de usar.

Para implementação do RPC em Python foi utilizada a biblioteca Pyro5. Com o Pyro, é possível expor objetos Python em um servidor, permitindo que clientes remotos chamem métodos nesses objetos como se estivessem chamando métodos locais. O Pyro utiliza um protocolo de comunicação transparente para serializar e desserializar objetos Python, permitindo que eles sejam transferidos através da rede.

## License
Mit.
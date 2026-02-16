# CifraGlub

Uma aplicação CLI para conseguir tocar violão sem esperar horas pro site da palheta laranja carregar. O site da palheta laranja poderá ser referido como "site laranja", "glub", "cc", ou como qualquer adjetivo pejorativo a partir daqui.

## Como usar

Instale as dependências descritas no requirements.py (não testei o comando abaixo. Se não funcionar, é só olhar as mensagens de erro e instalar as dependências manualmente):
```
>>> python -m venv venv         // cria o ambiente virtual
>>> source venv/bin/activate    // no Linux, procura aí como ativa o venv no Windows
>>> pip install -r requirements.py
```

Execute o main.py da seguinte forma:

```
>>> python main.py "nome do artista" "nome da musica"
```

O nome do artista precisa ser escrito **entre aspas** exatamente como na URL do site laranja (geralmente sem acentos ou cedilhas), sem distinção entre maiúsculas e minúsculas (```"caetano veloso"``` funcionaria). O nome da música não precisa ser exato -- o script te ajuda com isso.

Caso o nome da música inserido não seja idêntico à URL do site laranja, o script te dará opções de nomes parecidos. Basta escolher um número de 1 a 5 correspondente à música que você procura.

O script criará um diretório ```artistas/``` para salvar um arquivo .json com a lista de músicas do artista. Esse processo é feito para evitar ter que baixar a página desnecessariamente imensa que o site laranja tem para cada artista. Uma opção ```--no-cache``` será adicionada em breve.

As cores na cifra são baseadas em linhas pares e ímpares e as cores estão definidas na variável "config" no main.py, caso queira alterá-las.

## Próximas alterações

- [x] Adicionar opção --no-cache
- [ ] Fazer fuzzy finding no nome do artista
- [ ] Tirar necessidade das aspas nos nomes
- [x] Adicionar opção --no-tabs (sem tablaturas)
- [x] Colorir somente os acordes de fato
- [ ] Melhorar UX
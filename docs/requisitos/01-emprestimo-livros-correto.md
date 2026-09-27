# Módulo: Empréstimo de livros

Sistema: Biblioteca Comunitária

## HU-01 — Reservar um livro emprestado

### História de usuário

Como leitor cadastrado, quero reservar um livro que está emprestado para outra pessoa, para que eu seja o próximo a retirá-lo quando ele for devolvido.

### Critérios de aceitação

- O botão "Reservar" aparece apenas para livros com situação "Emprestado".
- Cada leitor pode ter no máximo 3 reservas ativas ao mesmo tempo.
- Quando o livro é devolvido, o leitor com a reserva mais antiga recebe um e-mail em até 10 minutos.
- A reserva é cancelada automaticamente se o leitor não retirar o livro em até 2 dias úteis após o e-mail.

## HU-02 — Renovar um empréstimo

### História de usuário

Como leitor cadastrado, quero renovar o prazo de um livro que está comigo, para que eu possa terminar a leitura sem pagar multa por atraso.

### Critérios de aceitação

- A renovação só pode ser feita até a data de devolução, inclusive.
- Cada renovação adiciona 7 dias corridos ao prazo atual.
- Um mesmo empréstimo pode ser renovado no máximo 2 vezes.
- A renovação é bloqueada se existir uma reserva ativa para o livro, e o sistema exibe a mensagem "Este livro está reservado por outro leitor".

## HU-03 — Consultar histórico de empréstimos

### História de usuário

Como leitor cadastrado, quero ver a lista dos livros que já peguei emprestado, para que eu lembre o que já li e possa indicar para outras pessoas.

### Critérios de aceitação

- A lista mostra título, autor, data de retirada e data de devolução de cada empréstimo.
- A lista é ordenada da data de retirada mais recente para a mais antiga.
- São exibidos 20 empréstimos por página.
- O leitor vê apenas o próprio histórico.

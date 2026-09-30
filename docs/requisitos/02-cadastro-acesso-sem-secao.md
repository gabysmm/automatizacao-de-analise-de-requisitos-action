# Módulo: Cadastro e acesso de usuários

Sistema: Portal do Aluno

## HU-01 — Criar conta

### História de usuário

Como aluno matriculado, quero criar uma conta usando meu número de matrícula, para que eu possa acessar minhas notas pelo portal.

### Critérios de aceitação

- O cadastro exige número de matrícula, e-mail e senha.
- A senha deve ter no mínimo 8 caracteres, com pelo menos uma letra e um número.
- O cadastro é recusado se o número de matrícula não existir na base da secretaria.
- Após o cadastro, o aluno recebe um e-mail de confirmação em até 5 minutos.

## HU-02 — Recuperar senha

### História de usuário

Como aluno cadastrado, quero receber um link para criar uma nova senha, para que eu consiga voltar a acessar o portal se esquecer a senha atual.

## HU-03 — Bloquear acesso após tentativas erradas

### Critérios de aceitação

- Após 5 tentativas seguidas com senha errada, a conta é bloqueada por 15 minutos.
- Durante o bloqueio, o sistema exibe a mensagem "Conta bloqueada temporariamente. Tente novamente em 15 minutos".
- O contador de tentativas volta a zero após um login com sucesso.
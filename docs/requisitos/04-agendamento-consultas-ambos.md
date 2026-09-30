# Módulo: Agendamento de consultas

Sistema: Clínica Médica

## HU-01 — Agendar consulta

### História de usuário

Como paciente, quero agendar uma consulta pela internet, para que eu não precise ligar para a clínica.

### Critérios de aceitação

- A busca por médico deve ser eficiente.
- O sistema deve mostrar os horários disponíveis em um calendário adequado.
- O paciente só pode ter 1 consulta agendada por especialidade ao mesmo tempo.
- Após o agendamento, o paciente recebe uma confirmação por e-mail com data, horário e nome do médico.

## HU-02 — Cancelar consulta

### História de usuário

Como paciente, quero um cancelamento rápido da minha consulta, para que outro paciente possa usar o horário.

## HU-03 — Receber lembrete da consulta

### História de usuário

Como paciente, quero receber um lembrete antes da consulta, para que eu não esqueça o compromisso.

### Critérios de aceitação

- O lembrete é enviado por SMS 24 horas antes do horário da consulta.
- O lembrete informa data, horário, endereço da clínica e nome do médico.
- Consultas canceladas não geram lembrete.
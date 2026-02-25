# Life-Alert

## Sobre o Sistema:  

  O **_life Alert_** é uma plataforma de registro e controle de emergências civis em diversos âmbitos (ambiental, criminal, de saúde, etc.), com o objetivo de permitir que os órgãos públicos tenham uma resposta mais rápida aos eventos que ameaçam a segurança da população, como desastres naturais, incêndios, acidentes, epidemias, entre outros, além de notificar os civis afetados e proporcionar um melhor controle dos alertas. 
  
  O programa permite que o civil possa registrar uma ocorrência coletiva junto ao atendente responsável pelos registros, relatando as informações iniciais do ocorrido (descrição do problema, geolocalização, tipo de ocorrência, população afetada, etc.) e encaminhando-os aos setores responsáveis (SAMU, SUS, Polícia Ambiental, Bombeiros, ...), para que a ocorrência seja atendida pelos órgãos corretos e aprimorar a resposta no resgate da população. Quando necessário, com base na gravidade da ocorrência, o sistema emite alertas de emergência aos civis cadastrados no sistema mais próximos ou que se localizam na área do ocorrido, permitindo informar a toda a população da área sobre o evento e o que fazer para garantir a segurança da região.
  
  Por padrão, o sistema permite acionar o resgate rápido em casos que demandam menor tempo de resposta, como invasões, pandemias etc., além de gerenciar as vítimas de cada ocorrência, possibiltando o acompanhamento do perfil médico e socioeconômico de cada civil afetado pelo poder público, permitindo maior organização e eficiência no atendimento às emergências e na aplicação de políticas públicas.
  
  Este projeto é desenvolvido e efetuado por estudantes da graduação de Engenharia de Software, na Universidade Federal do Cariri (UFCA), como componente da disciplina de **Programação Orientada a Objetos**, ministrada pelo professor **Jayr Alencar Pereira**.

## Estrutura do código:

```

life_alert/
|
├── src/life_alert/           
|   ├── ocorrencias/
|   |   ├── Ocorrencia.py
|   |   ├── OcorrenciaMedica.py
|   |   ├── OcorrenciaPolicial.py
|   |   └── __init__.py
|   |
|   ├── usuarios/
|   |   ├── Usuario.py
|   |   ├── UsuarioAgente.py
|   |   ├── UsuarioAtendente.py
|   |   ├── UsuarioCivil.py
|   |   └── __init__.py
|   |
|   ├── Alerta.py
|   ├── Atendimento.py
|   ├── EquipeResgate.py
|   ├── PerfilMedico.py
|   ├── Relatorio.py
|   ├── Regate.py
|   ├── Vitima.py
|   ├── __init__.py
|   └── menu.py
|
├── tests/           
|   └── __init__.py
|
├── README.md
├── poetry.lock
└── pypoject.toml

```


# Sistema de Ponto de Venda (PDV)

Um sistema de Ponto de Venda (PDV) moderno para gerenciamento de vendas, estoque, clientes e relatórios, desenvolvido com Electron e JavaScript modular.

## Características

- **Login de Vendedor:** Sistema de autenticação para controle de acesso
- **Vendas:** Interface para registrar novas vendas e consultar vendas realizadas
- **Estoque:** Gestão completa de produtos e inventário
- **Clientes:** Cadastro e gerenciamento de clientes
- **Relatórios:** Visualização de dados de desempenho e estatísticas de vendas
- **Interface Responsiva:** Funciona em diferentes tamanhos de tela

## Tecnologias Utilizadas

- **Electron:** Framework para desenvolvimento de aplicações desktop multiplataforma
- **JavaScript Modular:** Organização do código em módulos ES6 para melhor manutenibilidade
- **HTML5 & CSS3:** Interface moderna e responsiva

## Estrutura do Projeto

```
src/
├── css/
│   └── styles.css
├── js/
│   ├── app.js
│   ├── components/
│   │   └── loginModal.js
│   ├── modules/
│   │   ├── cart.js
│   │   └── navigation.js
│   ├── services/
│   │   └── auth.js
│   └── utils/
│       ├── formatters.js
│       └── ui.js
├── index.html
├── main.js
└── preload.js
```

## Padrões de Projeto

- **Modular:** Código organizado em módulos especializados
- **Serviços:** Camada para manipulação de dados e regras de negócio
- **Componentes:** Elementos de UI reutilizáveis
- **Utilitários:** Funções auxiliares para operações comuns

## Como Executar

1. Clone o repositório
2. Instale as dependências:
   ```
   npm install
   ```
3. Execute o aplicativo:
   ```
   npm start
   ```

## Credenciais de Teste

- **Usuário:** vendedor
- **Senha:** 123

## Para Desenvolvedores

### Instalação de Dependências de Desenvolvimento

```
npm install --save-dev electron electron-builder
```

### Build para Produção

```
npm run build
```

## Licença

Este projeto está licenciado sob a licença MIT. 
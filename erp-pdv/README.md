# ERP-PDV

Sistema ERP com foco em PDV (Ponto de Venda) desenvolvido com Electron, Node.js e MySQL.

## Funcionalidades

- Sistema de login seguro
- Gestão de vendas
- Controle de estoque
- Gestão financeira
- Relatórios gerenciais
- Controle de usuários e permissões
- Backup automático

## Requisitos

- Node.js 18.x ou superior
- MySQL 8.x ou superior
- Windows 10 ou superior (para desenvolvimento)

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/erp-pdv.git
cd erp-pdv
```

2. Instale as dependências:
```bash
npm install
```

3. Configure o arquivo `.env`:
- Copie o arquivo `.env.example` para `.env`
- Ajuste as variáveis de ambiente conforme sua configuração

4. Crie o banco de dados:
```bash
mysql -u root -p
CREATE DATABASE erp_pdv;
```

5. Execute as migrações do banco de dados:
```bash
npm run migrate
```

## Desenvolvimento

Para iniciar o aplicativo em modo de desenvolvimento:

```bash
npm run dev
```

## Produção

Para criar o instalador do aplicativo:

```bash
npm run build
```

O instalador será gerado na pasta `dist`.

## Estrutura do Projeto

```
erp-pdv/
├── src/
│   ├── assets/         # Imagens e recursos
│   ├── css/           # Arquivos CSS
│   ├── js/
│   │   ├── components/ # Componentes reutilizáveis
│   │   ├── db/        # Configuração do banco de dados
│   │   ├── modules/   # Módulos do sistema
│   │   └── utils/     # Funções utilitárias
│   ├── index.html    # Página principal
│   └── preload.js    # Script de preload do Electron
├── main.js           # Processo principal do Electron
├── server.js         # Servidor Express
└── package.json      # Dependências e scripts
```

## Testes

Para executar os testes:

```bash
npm test
```

## Contribuição

1. Faça o fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Crie um Pull Request

## Licença

Este projeto está licenciado sob a licença ISC - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Suporte

Para suporte, envie um email para seu-email@exemplo.com ou abra uma issue no GitHub.

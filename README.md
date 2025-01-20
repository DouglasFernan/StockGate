# Configurando o Ambiente Virtual e Instalando Dependências

Este tutorial mostra como configurar um ambiente virtual e instalar as dependências do projeto em diferentes sistemas operacionais.

---

## 1. Criar o Ambiente Virtual

### Windows
1. Abra o terminal (PowerShell ou CMD).
2. Execute o comando: `python -m venv venv`
3. Ative o ambiente virtual: `.\venv\Scripts\activate`
   - O nome do ambiente (`venv`) aparecerá no início da linha de comando.

### Linux/Mac
1. Abra o terminal.
2. Execute o comando: `python3 -m venv venv`
3. Ative o ambiente virtual: `source venv/bin/activate`
   - O nome do ambiente (`venv`) aparecerá no início da linha de comando.

---

## 2. Instalar as Dependências

Com o ambiente virtual ativado, instale as dependências do projeto listadas no arquivo `requirements.txt`:

`pip install -r requirements.txt`

---

## 3. Verificar a Instalação

Para garantir que tudo foi instalado corretamente, você pode listar as dependências instaladas:

`pip freeze`

---

## 4. Desativar o Ambiente Virtual

Quando terminar de trabalhar no projeto, desative o ambiente virtual:

`deactivate`

---

## 5. Atualizar o `requirements.txt`

### Por que é importante?
Sempre que novas dependências forem adicionadas ao projeto, o arquivo `requirements.txt` precisa ser atualizado para que outros desenvolvedores possam recriar o ambiente virtual corretamente.

### Como atualizar?
Com o ambiente virtual ativado, use o seguinte comando para recriar o `requirements.txt`:

`pip freeze > requirements.txt`

Este comando sobrescreverá o arquivo atual com as dependências instaladas no ambiente virtual. Certifique-se de fazer o commit das alterações no arquivo `requirements.txt` para mantê-lo atualizado no repositório.

---

## Observações

- Certifique-se de ter o Python instalado em sua máquina.
  - No Windows, você pode verificar com: `python --version`
  - No Linux/Mac, use: `python3 --version`
- Recrie o ambiente virtual sempre que necessário usando os passos acima.

Agora você está pronto para começar a desenvolver no projeto!

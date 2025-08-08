# cbpi4-BrewPiLessAdvancedFermentationController

Plugin de controle avançado de fermentação para CraftBeerPi 4 inspirado no BrewPiLess, com PID dinâmico, máquina de estados, proteção anti-congelamento e controle robusto de compressor e aquecedor.

---

## Funcionalidades principais

- Controle PID dinâmico para temperatura do fermentador
- Máquina de estados com modos IDLE, COOLING, HEATING, WAIT e ERROR
- Proteção anti-congelamento para evitar temperaturas abaixo do limite seguro
- Gerenciamento robusto dos atuadores de aquecimento e resfriamento
- Configuração via interface do CraftBeerPi 4 com parâmetros ajustáveis
- Notificações internas para estados e mudanças importantes

---

## Requisitos

- CraftBeerPi 4 (CBPi4) instalado e funcionando
- Python >= 3.7
- Ambiente com acesso a sensores e atores configurados no CBPi4

---

## Instalação

Instale diretamente via pip pelo GitHub:

pip install git+https://github.com/Zimer-Gbz/cbpi4-BrewPiLessAdvancedFermentationController.git



Após a instalação, reinicie o CraftBeerPi 4 para carregar o plugin:

Se estiver usando systemd
sudo systemctl restart cbpi4

Ou reinicie manualmente, se não usar systemd
cbpi stop
cbpi start


Verifique se o plugin está ativo com:

cbpi plugins


---

## Configuração

Após instalação, o plugin aparecerá na interface web do CBPi4 na categoria de controladores de fermentação. Configure os seguintes parâmetros:

- **Sensor de Fermentador**: Sonda de temperatura na cerveja
- **Sensor da Câmara**: Sonda dentro da câmara ou geladeira
- **Aquecedor**: Atuador responsável por aquecer o fermentador
- **Resfriador**: Atuador responsável por resfriar o fermentador
- **Setpoint de Fermentação**: Temperatura alvo desejada para a fermentação (°C)
- **Parâmetros PID**: Kp, Ki, Kd para ajuste do controlador
- **Tempos e proteções**: Ciclo de controle, tempos mínimos ligado/desligado, dead time, limite anti-congelamento

---

## Uso

- O plugin executa a lógica de controle automática com base na temperatura da cerveja e da câmara.
- A máquina de estados gerencia liga/desliga do aquecedor e resfriador, com proteções integradas.
- Notificações aparecem na interface para informar mudanças de estado ou erros.

---

## Desenvolvimento

Código fonte, arquivos de configuração, e scripts estão disponíveis no repositório GitHub.

Contribuições e sugestões são bem-vindas!

---
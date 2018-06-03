/* Programa para exibir dados recebidos de XBee.

   Possibilidades atuais:
      1 - Receber o endereco (SL )de um End Device cadastrado

   Possibilidades a serem implementadas:
   1 - Montar o pacote:
    1.1 - Pegar COMPRIMENTO
    1.2 - Pegar TIPO DE FRAME
    1.3 - Pegar o END. 64-bit
    1.4 - Pegar o END. 16-bit (MY)
    1.5 - Pegar o COMANDO (hex)
    1.6 - Calcular o CHECKSUM
   2 - Enviar o pacote
   3 - Verificar porta serial. Se disponivel, armazenar em um vetor o valor retornado
   4 - Enviar o vetor para o programa em Python.
*/

uint8_t option;
int response[4] = {};

int sl_frames[3][19] = { // Array de frames
  {0x7E, 0x00, 0x0F, 0x17, 0x01, 0x00, 0x13, 0xA2, 0x00, 0x40, 0x7C, 0x48, 0xFF, 0xFF, 0xFE, 0x02, 0x53, 0x4C, 0x91}, //E1
  {0x7E, 0x00, 0x0F, 0x17, 0x01, 0x00, 0x13, 0xA2, 0x00, 0x40, 0x7C, 0x49, 0x27, 0xFF, 0xFE, 0x02, 0x53, 0x4C, 0x68}, // E2
  {0x7E, 0x00, 0x0F, 0x17, 0x01, 0x00, 0x13, 0xA2, 0x00, 0x40, 0x7C, 0x48, 0xFE, 0xFF, 0xFE, 0x02, 0x53, 0x4C, 0x92}  //E3
};

void setup() {
  Serial.begin(9600);
}

void send_frame(int frame[19]) {
  for (int i = 0; i < sizeof(frame) / sizeof(int); i++) {
    Serial.write((int) frame[i]);
  }
}

void loop() {
  if (Serial.available() == 1) {
    option = Serial.read();
    switch (option) {
      case 1: // Retorna o SL do 1
        send_frame(sl_frames[0]);
        break;
      case 2: // Retorna o SL do 2
        send_frame(sl_frames[1]);
        break;
      case 3: // Retorna o SL do 2
        send_frame(sl_frames[2]);
        break;
    }
  } else if (Serial.available() > 21) {
    if (Serial.read() == 0x7E) { // se for o inicio do pacote
      for (int i = 0; i < 17; i++) { //loop sobre a resposta
        uint8_t waste = Serial.read();
      }
      for (int i = 0; i < 4; i++) { // loop para armazenar o SL recebido
        response[i] = Serial.read();
        Serial.print(response[i]);
      }
    }
    Serial.println();
  }
}


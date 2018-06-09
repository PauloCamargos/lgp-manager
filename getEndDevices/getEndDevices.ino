/*
Get's all End Devices conected to a specified router.
Uses external library 'SoftwareSerial.h'

Recebe o NI do roteador (R1, R2)
Monta o frame para MY do roteador especificado
Envia o frame
Recebe a resposta
Armazena o MY em um vetor

Monta um frame para cada ED cadastrado, solicitando o MP
Envia o frame para cada ED
Recebe a resposta de cada ED
Armazena o MP de cada ED em um vetor
Se um MP diferente de MY, descarta
Para cada MP remanescente, retorna
*/

#include "SoftwareSerial.h"
SoftwareSerial xbee_serial(2, 3); //(RX, TX). Pins connected to Xbee serial

// String router_ni; //String representing "R1" or "R2
// byte router_my[2] = {}; //Array representing a router's MY number(16-bit address)
// byte end_device_mp[2] = {};//Array representing a router's MP number
// bool flag_my_mp = true; //Flag signaling if MY=MP

/* SH e SL
R1: 00 13 A2 00 40 7C 49 27
R2: 00 13 A2 00 40 7C 48 FE
*/

/* Tipos de atributos
SL: Ox53 Ox4C
MP: 0x4D 0x50
NI: 0x4E 0x49
MY: 0x4D 0x59
*/
byte waste, status;

// Frame para os EDs
byte mp_frames[][19] = {
    {}, //E1
    {}, //E2
    {}, //E3
    {}, //E4
};

//Ex. resp. SL: 7E 00 13 97 01 00 13 A2 00 40 7C 48 FF FE 59 53 4C 00 40 7C 48 FF B6
//Ex. resp. MP: 7E 00 11 97 01 00 13 A2 00 40 7C 48 FF FE 59 4D 50 00 00 00 BB

// Frames para os Routers
byte my_frames[][19] = {
    {0x7E, 0x00, 0x0F, 0x17, 0x01, 0x00, 0x13, 0xA2, 0x00, 0x40, 0x7C, 0x49, 0x27, 0xFF, 0xFE, 0x02, 0x4D, 0x59, 0x61},//R1
    {0x7E, 0x00, 0x0F, 0x17, 0x01, 0x00, 0x13, 0xA2, 0x00, 0x40, 0x7C, 0x48, 0xFE, 0xFF, 0xFE, 0x02, 0x4D, 0x59, 0x8B} //R2
};

byte mp_response[4][2] = {}; // Armazena a resposta de MP de todos os EDs
byte my_response[2] = {};    // Armazena a responsta de MY do Routers especificado

byte response_type[2] = {}
void setup(){
    Serial.begin(9600); // Internal serial initialization
    xbee_serial.begin(9600); //Pins connecter to Xbee serial initialization
}

void loop(){
    if(Serial.available() > 0  && Serial.available() < 3){ //if R1 or R2
        router = Serial.read();
        if(router == "R1"){
            send_frame(my_frames[0]); // envia frame para R1 solicitando MY
        }else if(router == "R2"){
            send_frame(my_frames[1]) // envia frame para R2 solicitando MY
        }
    }else if(xbee_serial.available() > 21){
        if(xbee_serial.read() == 0x7E){ //Se for o inicio do pacote
            // Recebendo o tipo da resposta
            for(int i=0; i < 15; i++){
                waste = xbee_serial.read();
            }
            response_type[0] = xbee_serial.read();
            response_type[1] = xbee_seiral.read();
            if(response_type[0] == 0x4D && response_type[1] == 0x59){ // Se a resp for para MY
                status = Serial.read();
                if(status == 0x00){ //Se o status da resposta estiver ok
                    my_response[0] = xbee_serial.read(); // Lendo o MY
                    my_response[1] = xbee_serial.read();
                }
            }else if(response_type[0] == 0x4D && response_type[1] == 0x50){ // Se a resp for pra MP
                status = Serial.read();
                if(status == 0x00){ // Se o status da resposta estiver ok

                }
            }
        }
    }
}

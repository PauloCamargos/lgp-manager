/*
    Get's all End Devices conected to a specified router.
    Uses external library 'SoftwareSerial.h'
*/

#include "SoftwareSerial.h"
SoftwareSerial xbee_serial(2, 3); //(RX, TX). Pins connecter to Xbee serial initialization

String router; //String representing "R1" or "R2
byte router_my[2] = {}; //Array representing a router's MY number(16-bit address)
byte end_device_mp[2] = {};//Array representing a router's MP number
bool flag_my_mp = true; //Flag signaling if MY=MP

void setup(){
    Serial.begin(9600); // Internal serial initialization
    xbee_serial.begin(9600); //Pins connecter to Xbee serial initialization
}

void loop(){
    if(Serial.available() > 0  && Serial.available() < 2){ //if R1 or R2
        router = Serial.read();
        if(router == "R1"){
            getRouterMy("R1"); //Set router_my
            getEndDeviceMp();; //Set end_device_mp

            for(int i=0; i<2; i++){ //Loop checking if MY=MP
                if(router_my[i] != end_device_mp[i]){
                    flag_my_mp = false;
                    break;
                }
            }

            if(flag_my_mp){ // if MY=MP
                
            }
        }else if(router == "R2"){

        }
    }else if(Serial.availabe() < 21){

    }
}

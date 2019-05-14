#include <Servo.h>

#define HEAD_PAN  3
#define HEAD_TILT 5
#define EYES_PAN  6
#define EYES_TILT 9

#define HEAD_PAN_KEY  'p'
#define HEAD_TILT_KEY 't'
#define EYES_PAN_KEY  'e'
#define EYES_TILT_KEY 'f'

#define LED 13

#define RV_BUFFER_SIZE 12
#define NU_BUFFER_SIZE 4

#define V_MAX 1200.0 //deg par seconde
#define V_MIN 10 //deg par seconde
#define ACCEL 100.0 //deg par seconde^2

#define DELTA_T 16

Servo servo_hp;
Servo servo_ht;
Servo servo_ep;
Servo servo_et;

int i;
char rvbuf[RV_BUFFER_SIZE];
char numbuf[NU_BUFFER_SIZE];
int nb;
int lu;

int isReady = 1;
int etat = 0;
int frame = 0;

float pos[4];
float vitesse[4];
float consigne[4];

void setup()
{
  servo_hp.attach(HEAD_PAN);
  servo_ht.attach(HEAD_TILT);
  servo_ep.attach(EYES_PAN);
  servo_et.attach(EYES_TILT);

  Serial.begin(115200);
  Serial.setTimeout(50);

  nb = 0;
  lu = 0;
  for (i = 0; i < NU_BUFFER_SIZE; i++) numbuf[i] = '\0';
  for (i = 0; i < RV_BUFFER_SIZE; i++) rvbuf[i] = '\0';
  i = 0;

  vitesse[0] = 0;
  vitesse[1] = 0;
  vitesse[2] = 0;
  vitesse[3] = 0;

  pos[0] = 100;
  pos[1] = 60;
  pos[2] = 90;
  pos[3] = 90;

  consigne[0] = 100;
  consigne[1] = 60;
  consigne[2] = 90;
  consigne[3] = 90;
}

float distance(float vec[]) {
  float tot = 0;
  for (int k = 0; k < 4; k++) {
    tot += pow(vec[k], 4);
  }
  return pow(tot, 1.0 / 4.0);
}

void minus(float a[], float b[], float resultat[]) {
  for (int k = 0; k < 4; k++) {
    resultat[k] = a[k] - b[k];
  }
}

void calculAngle() {

  

  float chemin[4];
  minus(consigne, pos, chemin);
  float v = distance(chemin);
  float coef[4];
  for (int k = 0; k < 4; k++) {
    coef[k] = abs(chemin[k]) / v;
  }
  if (distance(chemin) < distance(vitesse) / (ACCEL * (DELTA_T / 1000.0))) {
    etat = 1;
    for (int k = 0; k < 4; k++) {
      if (vitesse[k] > V_MIN) {
        vitesse[k] -= coef[k] * ACCEL * (DELTA_T / 1000.0);
      } else {
        vitesse[k] = V_MIN;
        pos[k] = consigne[k];
      }
    }
  } else {
    if (distance(vitesse) < V_MAX) {
      for (int k = 0; k < 4; k++) {
        if(etat == 0){
          vitesse[k] += coef[k] * ACCEL * (DELTA_T / 1000.0);
        }else{
          vitesse[k] = V_MIN;
          pos[k] = consigne[k];
        }
      }
    }
  }

  for (int k = 0; k < 4; k++) {

    if (consigne[k] < pos[k]) {
      pos[k] -= vitesse[k] * (DELTA_T / 1000.0);
    }
    if (consigne[k] > pos[k]) {
      pos[k] += vitesse[k] * (DELTA_T / 1000.0);
    }

  }

}


void resetBuffer() {
  for (i = 0; i < RV_BUFFER_SIZE; i++) rvbuf[i] = '\0';
  nb = 0;
}

void lireCommande() {
  if (nb <= RV_BUFFER_SIZE) {
    for (int k = 0; k < 4; k++) {
      char angleBuffer[3];
      for (int i = 0; i < 3; i++) {
        angleBuffer[i] = rvbuf[3 * k + i];
      }
      consigne[k] = atoi(angleBuffer);
    }
    float difference[4];
    minus(consigne, pos, difference);
    float dist = distance(difference);
    vitesse[0] = 0;
    vitesse[1] = 0;
    vitesse[2] = 0;
    vitesse[3] = 0;
  } else {
    Serial.print("Commande trop longue ! ");
    Serial.print(nb);
    Serial.print("\n");
  }
  resetBuffer();
  etat = 0;
  isReady = 0;
}

void msg_fini() {
  Serial.print("f");
}

void loop()
{
  if ( Serial.available() )
  {
    lu = Serial.read();
    if (lu != '\n') {
      rvbuf[nb++] = lu;
    } else {
      lireCommande();
    }
  }

  calculAngle();
  
  servo_hp.write( int(pos[0]) );
  servo_ht.write( int(pos[1]) );
  servo_ep.write( int(pos[2]) );
  servo_et.write( int(pos[3]) );
  
  if (frame % 20 == 0) {
    Serial.print("p");
    Serial.print(pos[0]);
    Serial.print("\n");
  }
  if ((frame + 10) % 20 == 0) {
    Serial.print("t");
    Serial.print(pos[1]);
    Serial.print("\n");
  }
  frame++;
  delay(DELTA_T);

}

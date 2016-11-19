byte sensorPin = 2;
int trigPin = 11;
int echoPin = 12;
int buzzerPin = 3;
int crowd = 0;
long denominator = 0;
float index = 0;
long distance, cm,duration;

void setup()
{
  pinMode(sensorPin,INPUT);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(buzzerPin, OUTPUT);
  Serial.begin(9600);
}

void loop()
{
  distance = get_distance();
  byte state = digitalRead(sensorPin);
  denominator += 1;
  if(state == 1)
  {
    crowd += 1;
    if(distance < 50){
      digitalWrite(buzzerPin, HIGH);
      delay(100);
      digitalWrite(buzzerPin, LOW);
      delay(30);
      digitalWrite(buzzerPin, HIGH);
      delay(100);
      digitalWrite(buzzerPin, LOW);
    }else{
      delay(200);
    }
    //Serial.println("Somebody is in this area!");
   }else{
    delay(200);
   }
  if (denominator == 100){
    index =  10.0 * (float)crowd / (float)denominator ;
    crowd = 0;
    denominator = 0;
    delay(200);
  }
  communicate(distance,index);
}

int get_distance()
{
  digitalWrite(trigPin, LOW);
  delayMicroseconds(5);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
 
  // Read the signal from the sensor: a HIGH pulse whose
  // duration is the time (in microseconds) from the sending
  // of the ping to the reception of its echo off of an object.
  pinMode(echoPin, INPUT);
  duration = pulseIn(echoPin, HIGH);
 
  // convert the time into a distance
  cm = (duration/2) / 29.4;
  return cm;
}

void communicate(int distance,int index)
{
  if (distance < 50){
    Serial.print("True;");
  }else{
    Serial.print("False;");
  }
  //Serial.print(crowd);
  Serial.println(index);
}

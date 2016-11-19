byte sensorPin = 2;
int trigPin = 11;
int echoPin = 12;
int buzzerPin = 3;
int crowd = 0;
long denominator = 0;
float index = 0;
long cm,duration;
int bufferTrash[11]={};
int bufferArray[11]={};

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
  bool judgeTrash;
  for(int i=1; i<11; i++){
    judgeTrash = find_trash();
    if (judgeTrash){
      bufferTrash[i] = bufferTrash[i-1] + 1;      
    }else{
      bufferTrash[i] = bufferTrash[i-1];
    }
    bool judgePasserby = is_passerby();
    denominator += 1;
    if(judgePasserby)
    {
      crowd += 1;
      if(judgeTrash){
        bufferArray[i] = bufferArray[i-1] + 1;
        if (bufferArray[i] > 6){
          digitalWrite(buzzerPin, HIGH);
          delay(100);
          digitalWrite(buzzerPin, LOW);
        }else{
          delay(100);
        }
      }else{
        bufferArray[i] = bufferArray[i-1];
        delay(100);
      }
      //Serial.println("Somebody is in this area!");
     }else{
      delay(100);
      }
    }

    if (denominator == 100){
      index =  100.0 * (float)crowd / (float)denominator ;
      crowd = 0;
      denominator = 0;
    }
    if (bufferTrash[10] < 7){
        judgeTrash = false;
    }
    communicate(judgeTrash,index);

}

bool find_trash()
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
  duration = pulseIn(echoPin, HIGH );
      //Serial.println(duration);
  if (duration == 0){
    duration = 10000;
  }
    //Serial.println(duration);
  // convert the time into a distance
  cm = (duration/2) / 29.4;
  if (cm<50){
    return true;
  }else{
    return false;
  }
}

bool is_passerby()
{
  byte state = digitalRead(sensorPin);
  if (state == 1){
    return true;
  }else{
    return false;
  }
}


void communicate(bool judgeTrash,int index)
{
  if (judgeTrash){
    Serial.print("True;");
  }else{
    Serial.print("False;");
  }
  //Serial.print(crowd);
  Serial.println(index);
}

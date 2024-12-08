
const int trigPin1 = 9;  // First sensor trigger pin
const int echoPin1 = 10; // First sensor echo pin

const int trigPin2 = 11;  // Second sensor trigger pin
const int echoPin2 = 12;  // Second sensor echo pin

void setup() {
  // Initialize serial communication
  Serial.begin(9600);

  // Initialize the pins for the first sensor
  pinMode(trigPin1, OUTPUT);
  pinMode(echoPin1, INPUT);

  // Initialize the pins for the second sensor
  pinMode(trigPin2, OUTPUT);
  pinMode(echoPin2, INPUT);
}

void loop() {
  // For Sensor 1
  long duration1, distance1;
  
  // Clear the trigger pin
  digitalWrite(trigPin1, LOW);
  delayMicroseconds(2);

  // Send the trigger signal
  digitalWrite(trigPin1, HIGH);
  delayMicroseconds(10); // 10-microsecond pulse
  digitalWrite(trigPin1, LOW);

  // Read the echo pin
  duration1 = pulseIn(echoPin1, HIGH);

  // Calculate the distance
  distance1 = duration1 * 0.034 / 2;

  // For Sensor 2
  long duration2, distance2;

  // Clear the trigger pin
  digitalWrite(trigPin2, LOW);
  delayMicroseconds(2);

  // Send the trigger signal
  digitalWrite(trigPin2, HIGH);
  delayMicroseconds(10); // 10-microsecond pulse
  digitalWrite(trigPin2, LOW);

  // Read the echo pin
  duration2 = pulseIn(echoPin2, HIGH);

  // Calculate the distance
  distance2 = duration2 * 0.034 / 2;

  // Output the distance readings to the Serial Monitor
  Serial.print("Sensor 1 Distance: ");
  Serial.print(distance1);
  Serial.print(" cm   |   Sensor 2 Distance: ");
  Serial.print(distance2);
  Serial.println(" cm");

  // Small delay to avoid overwhelming the Serial Monitor
  delay(100);
}
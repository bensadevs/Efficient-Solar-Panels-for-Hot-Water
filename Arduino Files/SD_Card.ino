#include <SD.h>
#include <SPI.h>
File myFile;
char fileName[] = "simple.txt";
const int chipSelect = 10;
char charRead;
char pangram_1[] = "The five boxing wizards jump quickly";
char pangram_2[] = "Pack my box with five dozen liquor jugs";
char pangram_3[] = "The quick brown fox jumps over the lazy dog";

void setup()
{
  Serial.begin(9600);
  Serial.println("Simple SD Card Demo");

   if (SD.begin(chipSelect))
    {
    Serial.println("SD card is present & ready");
    } 
    else
    {
    Serial.println("SD card missing or failure");
    while(1);  //wait here forever
    }
    Serial.println("Enter w for write, r for read or d for delete");
}

void loop() 
{
  //Create a loop to read a command character from the keyboard
  //This will be 'r' for read, 'w' for write and 'd' for delete.

  if (Serial.available()) 
     {
      charRead = tolower(Serial.read());  //force ucase
      Serial.write(charRead); //write it back to Serial window
      Serial.println();
     }
     
  //get command from keyboard:
   switch(charRead)
   {
    case 'r':
        readFromFile();   //read
        break;
    case 'w':
        writeToFile(); //write to file
        break;
    case 'd':
        deleteFile();  //delete
        break;
   }
}

void readFromFile()
{
  byte i=0; //counter
  char inputString[100]; //string to hold read string
  
  //now read it back and show on Serial monitor 
  // Check to see if the file exists:
  if (!SD.exists(fileName)) 
      Serial.println("simple.txt doesn't exist."); 
  Serial.println("Reading from simple.txt:");
  myFile = SD.open(fileName);

  while (myFile.available()) 
  {   
   char inputChar = myFile.read(); // Gets one byte from serial buffer
    if (inputChar == '\n') //end of line (or 10)
    {
      inputString[i] = 0;  //terminate the string correctly
      Serial.println(inputString);
      i=0;
    }
    else
    {
      inputString[i] = inputChar; // Store it
      i++; // Increment where to write next
      if(i> sizeof(inputString))
        {
        Serial.println("Incoming string longer than array allows");
        Serial.println(sizeof(inputString));
        while(1);
        }
    }
  }
 }

void writeToFile()
{
  myFile = SD.open(fileName, FILE_WRITE);
  if (myFile) // it opened OK
    {
    Serial.println("Writing to simple.txt");
    myFile.println(pangram_1);
    myFile.println(pangram_2);
    myFile.println(pangram_3);
    myFile.close(); 
    Serial.println("Done");
    }
  else 
    Serial.println("Error opening simple.txt");
}

void deleteFile()
{
 //delete a file:
  if (SD.exists(fileName)) 
    {
    Serial.println("Removing simple.txt");
    SD.remove(fileName);
    Serial.println("Done");
   } 
}

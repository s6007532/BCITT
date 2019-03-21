PFont font ;
int state = 1;
int count = 0;
String Seq = "ABCDEFGHI"; 
String svm;
String Blinkold;
String [] result = {"A", "AB", "ABC", "ABCD"}; //test for showing alphabet
String reci;
int times=3; //changethenumberofsequenceshere
float x = 150;
float y = 150;
int size = 100;
int char_dist = 300;
int color_bg = 255;
int color_letter = 0;
int count_show = 0;
int position = 1000;
int count_blink=0;
int count_layout;
int color_blink = 255;
int run = 1;
String [] Blink;
String S;
int BlinkAt;
import processing.net.*;
Client myClient;

void setup() {
  font = createFont("Arial", size);
  size(1500, 900);
  background(color_bg);
  //S represents how we blink
  //7 is when we update the keyboard(upper left corner)
  S = "0,1,0,2,0,3,0,4,0,5,0,6,0,7,0,1,0,2,0,3,0,4,0,5,0,6,0,7,0,1,0,2,0,3,0,4,0,5,0,6,0,7";
  Blink = split(S, ',');
}
void draw() {
  //run will be 1 when P300 is running and will be 0 when it is off
  if (run==1) {
    BlinkAt = int(Blink[count_blink]);
    if (BlinkAt == 1) {
      int count_layout = 0;
      background(color_bg);
      for (int k = 0; k < 3; k++) {
        for (int i = 0; i < 3; i++) {
          if (i == 0) {
            fill(color_blink);
          } else {
            fill(color_letter);
          }
          textFont(font, size);
          text(Seq.charAt(count_layout), x + i * char_dist, y + k * char_dist);
          count_layout = count_layout+1;
          show();
        }
      }
    } else if (BlinkAt == 2) {
      int count_layout = 0;
      background(color_bg);
      for (int k = 0; k < 3; k++) {
        for (int i = 0; i < 3; i++) {
          if (i == 1) {
            fill(color_blink);
          } else {
            fill(color_letter);
          }
          textFont(font, size);
          text(Seq.charAt(count_layout), x + i * char_dist, y + k * char_dist);
          count_layout = count_layout+1;
          show();
        }
      }
    } else if (BlinkAt== 3) {
      int count_layout = 0;
      background(color_bg);
      for (int k = 0; k < 3; k++) {
        for (int i = 0; i < 3; i++) {
          if (i == 2) {
            fill(color_blink);
          } else {
            fill(color_letter);
          }
          textFont(font, size);
          text(Seq.charAt(count_layout), x + i * char_dist, y + k * char_dist);
          count_layout = count_layout+1;
          show();
        }
      }
    } else if (BlinkAt == 4) {
      int count_layout = 0;
      background(color_bg);
      for (int k = 0; k < 3; k++) {
        for (int i = 0; i < 3; i++) {
          if (k == 0) {
            fill(color_blink);
          } else {
            fill(color_letter);
          }
          textFont(font, size);
          text(Seq.charAt(count_layout), x + i * char_dist, y + k * char_dist);
          count_layout = count_layout+1;
          show();
        }
      }
    } else if (BlinkAt == 5) {
      int count_layout = 0;
      background(color_bg);
      for (int k = 0; k < 3; k++) {
        for (int i = 0; i < 3; i++) {
          if (k == 1) {
            fill(color_blink);
          } else {
            fill(color_letter);
          }
          textFont(font, size);
          text(Seq.charAt(count_layout), x + i * char_dist, y + k * char_dist);
          count_layout = count_layout+1;
          show();
        }
      }
    } else if (BlinkAt == 6) {
      int count_layout = 0;
      background(color_bg);
      for (int k = 0; k < 3; k++) {
        for (int i = 0; i < 3; i++) {
          if (k == 2) {
            fill(color_blink);
          } else {
            fill(color_letter);
          }
          textFont(font, size);
          text(Seq.charAt(count_layout), x + i * char_dist, y + k * char_dist);
          count_layout = count_layout+1;
          show();
        }
      }
    } else if (BlinkAt == 0) {
      int count_layout = 0;
      fill(color_letter);
      for (int k = 0; k < 3; k++) {
        for (int i = 0; i < 3; i++) {
          textFont(font, size);
          text(Seq.charAt(count_layout), x + i * char_dist, y + k * char_dist);
          count_layout = count_layout+1;
          show();
        }
      }
      //every time we meet 7 we will update the upper left keyboard
    }else if (BlinkAt==7) {
      show();
      count_show = count_show+1;
      if (count_show>=4) {
        count_show = 0;
      }
    }
    show();
    delay(80);
    //This part is try to receiving the signal to collect data
    count_layout = count_layout+1;
    count_blink = count_blink+1;
  }
  if (count_blink>=Blink.length) {
    //if we are at the end of array "Blink" we will stop P300
    run = 0;
    background(color_bg);
  }
  //run should be 0 by now
  if (run==0){
  //recei = myClient.readString(); 
   reci = "11,0,2,0,3,0,4,0,5,0,6,0,7,0,8,0"; //example of received string
   run = int(reci.substring(0,1)); //recei should consist be like this : 11,0,2,0,3,0,4,0
   S = reci.substring(1);
   Blink = split(S,',');  
}
}

//just function to show alphabet on upper left keyboard
void show() {
  textFont(font, size);
  text(result[count_show], 1000, 150);
}
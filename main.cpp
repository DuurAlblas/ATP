#include "hwlib.hpp"

extern "C" void print(int x){
    hwlib::cout << x << "\n";
    return;
};

extern "C" int coco(int x, int y);
extern "C" int loopysum(int x);
extern "C" int even(int x);

int main() {
    hwlib::wait_ms(2000);    
    int result = 0;
    
    hwlib::cout << "Starting Testing...\n";
    // Loopsum will return the sum of the input and all of its lower integers.
    // 5 + 4 + 3 + 2 + 1 = 15
    hwlib::cout << "loopysum(5) result: ";
    result = loopysum(5);
    if(result == 15){
        hwlib::cout << "TEST Success : loopysum value 5 result 15.\n";
    } else {
        hwlib::cout << "TEST Failed : loopysum value 5 result " << result << "\n";
    };
    
    // 6 + 5 + 4 + 3 + 2 + 1 = 21
    hwlib::cout << "Execute loopysum(6) output:\n";
    result = loopysum(6);
    if(result == 21){
        hwlib::cout << "TEST Success : loopysum value 6 result 21.\n";
    } else {
        hwlib::cout << "TEST Failed : loopysum value 6 result " << result << "\n";
    }
    
    // even checks whether a input is even or not and return a 1 if it is and a 0 if it is not.
    // 4 is even so result would be 1
    hwlib::cout << "Execute even(4) output:\n";
    result = even(4);
    if(result == 1){
        hwlib::cout << "TEST Success : even value 4 result 1.\n";
    } else {
        hwlib::cout << "TEST Failed : even value 4 result " << result << "\n";
    }
    
    // 3 is odd so the result would be 0
    hwlib::cout << "Execute even(3) output:\n";
    result = even(3);
    if(result == 0){
        hwlib::cout << "TEST Success : even value 3 result 0.\n";
    } else {
        hwlib::cout << "TEST Failed : even value 3 result " << result << "\n";
    }
    
    // coco receives 2 values, and prints them then resturn the value that was stored in the place of the memory pointer which is the last printed value.
    // prints 4 then 12 and returns 12.
    hwlib::cout << "Execute coco(4,12) output:\n";
    result = coco(4,12);
    if(result == 12){
        hwlib::cout << "TEST Success : coco value 4, 12 result 12.\n";
    } else {
        hwlib::cout << "TEST Failed : coco value 4, 12 result " << result << "\n";
    }
    
    // prints 7 then 2 and returns 2.
    hwlib::cout << "Execute coco(7,2) output:\n";
    result = coco(7,2);
    if(result == 2){
        hwlib::cout << "TEST Success : coco value 7, 2 result 2.\n";
    } else {
        hwlib::cout << "TEST Failed : coco value 7, 2 result " << result << "\n";
    }
    
};
// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.6.0;

contract samplyArray {

    uint[] public myArray; //this is a dynamic array of type uint
    uint[] public myArray2 = [1, 2, 3]; //this is a dynamic array with 1, 2 and 3 as default values
    uint[10] public myFixedSizeArray; //this is a fixed size array of type uint

    //this will add i to the end of myArray
    function pushistoAdd(uint i) public {
        myArray.push(i);
    }

    function changeArray(uint[] memory array) public returns (bool) {
        myArray = array;
        return true;
    }


    //returns the value in the specified position of the array
    function getIteminArray(uint index) public view returns (uint) {
        return myArray[index];
    }


    //this will update an item in the array
    function updatethearray(uint locationinarray, uint valuetochangeto) public {
        myArray[locationinarray] = valuetochangeto;
    }


    //this is to delete an item stored at a specific index in the array.
    //Once you delete the item the value in the array is set back to 0 for a uint.
    function remove(uint index) public {
        delete myArray[index];
    }


    //this will return the length of myArray
    function getLength() public view returns (uint) {
        return myArray.length;
    }
}

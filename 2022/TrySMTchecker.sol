// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.8.0;
pragma experimental SMTChecker;

contract Monotonic1
{
    // In this case the SMT problem (on the right) is UNSATISFIABLE
    // so the assertion holds
	function f(uint x) public pure    // forall x . (f(x) = x*42) and
		returns (uint) { 
            require(x < type(uint128).max);
			return x * 42;
	}
	function g(uint a, uint b, uint c) public pure {
		require(a >= b);              //            (a >= b) and
		require(b >= c);              //            (b >= c) and
		assert(f(a) >= f(c));         //            (f(a) < f(c))   //the negated of the assert condition
	}
}

contract Monotonic2
{
    // In this case the SMT problem (on the right) is SATISFIABLE
    // so the assertion does not hold
    // There is also an UNDERFLOW problem here
	function f(uint x) public pure
		returns (uint) { 
			return x * 42;           // An underflow may occur
	}
	function g(uint a, uint b, uint c) public pure {
		require(a >= b);
		require(b >= c);
		assert(f(a) == f(c)); 
	}
}

contract C3 {
    uint immutable x;
    uint immutable y;
 
    function subtract(uint _x, uint _y) internal pure returns (uint) {
        return _x - _y;
    }
 
    constructor(uint _x, uint _y) {
        (x, y) = (_x, _y);
    }
 
    function stateAdd() public view returns (uint) {
        return subtract(x, y);
    }
}

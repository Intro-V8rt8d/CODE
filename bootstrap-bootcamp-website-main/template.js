
// Template for Arithmetic Calculations
// Here are some basic templates for different arithmetic operations:
function add(a,b) {
    c = a + b
    return c;
}

function subtractNumbers(a, b) {
    return a - b;
}

function multiplyNumbers(a, b) {
    return a * b;
}

function divideNumbers(a, b) {
    if (b !== 0) {
        return a / b;
    } else {
        return 'Cannot divide by zero';
    }
}

console.log(subtractNumbers(10, 3)); // Output: 7
console.log(multiplyNumbers(4, 5)); // Output: 20
console.log(divideNumbers(20, 4)); // Output: 5
console.log(divideNumbers(20, 0)); // Output: Cannot divide by zero


//Template for Calculating Area (e.g., Rectangle, Circle)
// Area of a rectangle
function rectangleArea(length, width) {
    return length * width;
}

console.log(rectangleArea(5, 3)); // Output: 15

// Area of a circle
function circleArea(radius) {
    return Math.PI * radius * radius;
}

console.log(circleArea(3)); // Output: Approximately 28.27


// Template for Conditional Calculations
// You can use conditions inside functions to decide which calculation to perform:
function calculate(num1, num2, operation) {
    if (operation === 'add') {
        return num1 + num2;
    } else if (operation === 'subtract') {
        return num1 - num2;
    } else if (operation === 'multiply') {
        return num1 * num2;
    } else if (operation === 'divide') {
        return num2 !== 0 ? num1 / num2 : 'Cannot divide by zero';
    } else {
        return 'Unknown operation';
    }
}

console.log(calculate(6, 3, 'add')); // Output: 9
console.log(calculate(6, 3, 'divide')); // Output: 2


//Template for Exponentiation and Square Root
// Exponentiation (e.g., square, cube)
function power(base, exponent) {
    return Math.pow(base, exponent);
}

console.log(power(2, 3)); // Output: 8 (2^3)

// Square root
function squareRoot(number) {
    return Math.sqrt(number);
}

console.log(squareRoot(16)); // Output: 4


//Template for Array Operations (Sum, Average)
// Calculate the sum of an array of numbers
function sumArray(numbers) {
    let sum = 0;
    for (let i = 0; i < numbers.length; i++) {
        sum += numbers[i];
    }
    return sum;
}

console.log(sumArray([1, 2, 3, 4])); // Output: 10

// Calculate the average of an array of numbers
function averageArray(numbers) {
    const total = sumArray(numbers);
    return total / numbers.length;
}

console.log(averageArray([1, 2, 3, 4])); // Output: 2.5


//Template for More Complex Functions (e.g., Factorial)
// Calculate the factorial of a number
function factorial(n) {
    if (n === 0 || n === 1) {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}

console.log(factorial(5)); // Output: 120



//Template for Calculating Percentage
function calculatePercentage(total, percentage) {
    return (total * percentage) / 100;
}

console.log(calculatePercentage(200, 10)); // Output: 20

async function hashPassword(password) {
    const encoder = new TextEncoder(); // Encode string as bytes
    const data = encoder.encode(password); // Convert password string to bytes
  
    // Use the SubtleCrypto API to hash the password
    const hashBuffer = await crypto.subtle.digest('SHA-256', data); // Hash using SHA-256
  
    // Convert hash buffer to a hexadecimal string
    const hashArray = Array.from(new Uint8Array(hashBuffer)); // Convert buffer to byte array
    const hashHex = hashArray.map(byte => byte.toString(16).padStart(2, '0')).join('');
  
    return hashHex; // Return the hexadecimal hash string
  }


   HTTP REQUEST PUT METHOD
    const response = await fetch("http://localhost:3000/users/1");
if (response.ok) {
  const user = await response.json();

  // Modify the specific field
  user.Email = "new.email@example.com";

  // Send the updated resource back
  const updateResponse = await fetch("http://localhost:3000/users/1", {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(user),
  });

  if (updateResponse.ok) {
    const updatedUser = await updateResponse.json();
    console.log("Field updated successfully:", updatedUser);
  } else {
    console.error("Update failed:", updateResponse.statusText);
  }
} else {
  console.error("Failed to fetch the resource:", response.statusText);
}



TRY AND CATCH 
 async function deleteUser(userId) {
  try {
    const response = await fetch(`http://localhost:3000/users/${userId}`, {
      method: 'DELETE',
    });

    if (!response.ok) {
      throw new Error(`Failed to delete user: ${response.status} - ${response.statusText}`);
    }

    console.log(`User with ID ${userId} deleted successfully.`);
  } catch (error) {
    console.error("Error occurred:", error.message);
  }
}

// Call the function
deleteUser(1);
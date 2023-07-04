const firstDropdown = document.getElementById('firstDropdown');
const secondDropdown = document.getElementById('secondDropdown');

firstDropdown.addEventListener('change', function() {
  const selectedValue = firstDropdown.value;
  
  // Clear the options in the second dropdown
  secondDropdown.innerHTML = '';
  
  // Create new options based on the selected value
  if (selectedValue === 'option1') {
    const option3 = document.createElement('option');
    option3.value = 'option3';
    option3.textContent = 'Option 3';
    secondDropdown.appendChild(option3);
    
    const option4 = document.createElement('option');
    option4.value = 'option4';
    option4.textContent = 'Option 4';
    secondDropdown.appendChild(option4);
  } 
  
  else if (selectedValue === 'option2') {
    const option4 = document.createElement('option');
    option4.value = 'option4';
    option4.textContent = 'Option 4';
    secondDropdown.appendChild(option4);
    
    const option5 = document.createElement('option');
    option5.value = 'option5';
    option5.textContent = 'Option 5';
    secondDropdown.appendChild(option5);
  }
});

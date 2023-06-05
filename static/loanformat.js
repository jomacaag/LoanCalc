function formatCurrency(number) {
    const formatter = new Intl.NumberFormat('en-US', {
      style: 'decimal',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    });
    return formatter.format(number);
  }
  
  function formatPercent(number) {
    const formatter = new Intl.NumberFormat('en-US', {
      style: 'decimal',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    });
    return formatter.format(number);
  }
  
  function addDelayedUpdateListener(inputId, rangeId) {
    let timer;
  
    // Update input field value based on the range slider
    document.getElementById(rangeId).addEventListener('input', function() {
      clearTimeout(timer);
      updateInputValue(inputId, this.value);
    });
  
    // Update range slider value based on the input field
    document.getElementById(inputId).addEventListener('input', function() {
      clearTimeout(timer);
      updateRangeValue(rangeId, this.value);
    });
  
    document.getElementById(inputId).addEventListener('blur', function() {
      const numericValue = parseFloat(this.value.replace(/[^0-9.-]+/g, ''));
      const formattedValue = formatCurrency(numericValue);
      this.value = formattedValue;
    });
  
    function updateInputValue(inputId, rangeValue) {
      const numericValue = parseFloat(rangeValue.replace(/[^0-9.-]+/g, ''));
      let formattedValue;
      if (inputId === 'term') {
        formattedValue = numericValue < 10 ? '0' : '';
        formattedValue += numericValue.toString();
      } else {
        formattedValue = formatCurrency(numericValue);
      }
      document.getElementById(inputId).value = formattedValue;
    }
  
    function updateRangeValue(rangeId, inputValue) {
      const numericValue = parseFloat(inputValue.replace(/[^0-9.-]+/g, ''));
      document.getElementById(rangeId).value = numericValue;
    }
  }
  
  // Add delayed update listener for purchasePrice
  addDelayedUpdateListener('purchasePrice', 'purchasePriceRange');
  
  // Add delayed update listener for interestRate
  addDelayedUpdateListener('interestRate', 'interestRateRange');
  
  // Add delayed update listener for downPayment
  addDelayedUpdateListener('downPayment', 'downPaymentRange');
  
  // Add delayed update listener for mortgageInsurance
  addDelayedUpdateListener('mortgageInsurance', 'mortgageInsuranceRange');
  
  // Add delayed update listener for upfrontMI
  addDelayedUpdateListener('upfrontMI', 'upfrontMIRange');
  
  // Add delayed update listener for term
  addDelayedUpdateListener('term', 'termRange');
  
  // Add delayed update listener for income
  addDelayedUpdateListener('income', 'incomeRange');
  
  // Add delayed update listener for monthlyDebt
  addDelayedUpdateListener('monthlyDebt', 'monthlyDebtRange');
  
  // Add delayed update listener for propertyTaxes
  addDelayedUpdateListener('propertyTaxes', 'propertyTaxesRange');
  
  // Add delayed update listener for CondoHOA
  addDelayedUpdateListener('CondoHOA', 'CondoHOARange');
  
  // Add delayed update listener for Hazard
  addDelayedUpdateListener('Hazard', 'HazardRange');
  
  // Add blur event listener to trigger updates when the input fields lose focus
  const inputFields = document.querySelectorAll('input[type="text"]');
  inputFields.forEach(function(input) {
    input.addEventListener('blur', function() {
      const numericValue = parseFloat(this.value.replace(/[^0-9.-]+/g, ''));
      const formattedValue = formatCurrency(numericValue);
      this.value = formattedValue;
    });
  });
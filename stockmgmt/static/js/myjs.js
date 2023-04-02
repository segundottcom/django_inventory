function sum (){






    var selling_price = document.getElementById ('cost').value;
    var quantity = document.getElementById ('quantity').value;
    var amount = parseInt (selling_price) * pasrseInt (quantity);
    if (!isNaN(amount)){
      document.getElementByID ('amount').value=amount;

    }
  
    };
  
  
  
    
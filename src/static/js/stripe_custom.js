$(document).ready(function() {

  // Create a Stripe client.
  var stripe = Stripe('pk_test_6pRNASCoBOKtIshFeQd4XMUh');

  // Create an instance of Elements.
  var elements = stripe.elements();

  // Custom styling can be passed to options when creating an Element.
  // (Note that this demo uses a wider set of styles than the guide below.)
  var style = {
    base: {
      color: '#32325d',
      lineHeight: '18px',
      fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
      fontSmoothing: 'antialiased',
      fontSize: '16px',
      '::placeholder': {
        color: '#aab7c4'
      }
    },
    invalid: {
      color: '#fa755a',
      iconColor: '#fa755a'
    }
  };

  // Create an instance of the card Element.
  var card = elements.create('card', {style: style});

  // Add an instance of the card Element into the `card-element` <div>.
  card.mount('#card-element');

  // Handle real-time validation errors from the card Element.
  card.on('change', function(event) {
    var displayError = $('#card-errors');
    if (event.error) {
      displayError.textContent = event.error.message;
    } else {
      displayError.textContent = '';
    }
  });

  // Handle form submission.
  var form = $('#payment-form');
  form.on('submit', function(event) {
    event.preventDefault();

    stripe.createToken(card).then(function(result) {
      if (result.error) {
        // Inform the user if there was an error.
        var errorElement = $('#card-errors');
        errorElement.textContent = result.error.message;
      } else {
        // Send the token to your server.
        stripeTokenHandler(result.token);
        console.log(result.token)
      }
    });
  });

  function stripeTokenHandler(token) {
    var data = {
      'token': token.id
    }
    var urlEndpoint = '/company/payment/cards'
    console.log(urlEndpoint)

    $.ajax({
      method: 'POST',
      url: urlEndpoint,
      data: data,  
    }).done(function(response) {
      alert('Success! ' + response.msg)
      window.location.reload()
    }).fail(function(response) {
      alert('Failed!' + response.msg)
    })

  }

})







//function to enable update Option
document.addEventListener('DOMContentLoaded', function () {
    const rememberCheckbox = document.getElementById('remember');
    const formFields = document.querySelectorAll('input[id="full_name"], input[id="phone"], input[id="email"], input[id="profile_password"]');
    const updateButton = document.getElementById('update_profile');
    const popover = document.getElementById('popover_password');

    // if (rememberCheckbox.checked) {
    //     popover.style.display="block";
    // }
    rememberCheckbox.addEventListener('change', function () {
        const isChecked = this.checked;
        formFields.forEach(field => field.disabled = !isChecked);
        updateButton.disabled = !isChecked; // Enable/disable the update button based on checkbox status
        
    });
});


document.getElementById('registerButton').addEventListener('click', function() {
    // Get values from the input fields
    var full_name = document.getElementById('full_name').value;
    var phone = document.getElementById('phone').value;
    var email = document.getElementById('email').value;
    var password = document.getElementById('register_password').value;
    
    if (full_name.length>0 && phone.length>0 && email.length>0 && password.length>0 ) {
        // Create a list of values
        var data = [full_name, phone, email, password];

        // Send the data to the Flask endpoint using fetch
        fetch('/register_profile', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data => {
            if (data.message === 'register successful') {
                window.location.href = data.redirect_url;
            } else {
                alert('Register failed');
            } // Display the response message
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }else{
        alert('Please Enter valid input')
    }

});



document.getElementById('LoginButton').addEventListener('click', function() {
    // Get values from the input fields
    var email = document.getElementById('log_email').value;
    var password = document.getElementById('login_password').value;
    
    if (email.length>0 && password.length>0) {
        // Create a list of values
        var data = [email, password];

        // Send the data to the Flask endpoint using fetch
        fetch('/login_profile', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data => {
            if (data.message === 'register successful') {
                window.location.href = data.redirect_url;
            } else {
                alert('Register failed');
            } // Display the response messag
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }else{
        alert('Please enter a valid email and password');
    }
});




document.getElementById('update_profile').addEventListener('click', function() {
    // Get values from the input fields
    var full_name = document.getElementById('full_name').value;
    var phone = document.getElementById('phone').value;
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;

    // Create a list of values
    var data = [full_name, enrollment, phone, email, password, confirm_password];

    // Send the data to the Flask endpoint using fetch
    fetch('/update_profile', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message); // Display the response message
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});




document.getElementById('generateOtpBtn').addEventListener('click', function() {
    var otpStatus = document.getElementById('otpStatus');
    otpStatus.innerHTML = 'Loading...';
    setTimeout(function() {
    otpStatus.innerHTML = 'OTP has been sent!';
    }, 1000);
  });

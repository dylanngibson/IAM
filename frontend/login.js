document.getElementById('loginForm').addEventListener('submit', function(e) {
  e.preventDefault();

  const username = document.getElementById('username').value.trim();
  const password = document.getElementById('password').value.trim();

  // Simple hardcoded credentials (you can change this or connect to a backend later)
  const validUsername = 'admin';
  const validPassword = 'password123';

  if (username === validUsername && password === validPassword) {
    // Redirect to dashboard
    window.location.href = 'index.html'; // Change this to your actual dashboard page
  } else {
    alert('Invalid username or password!');
  }
});

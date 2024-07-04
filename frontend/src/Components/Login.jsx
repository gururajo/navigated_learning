import React from 'react';
import './Auth.css';

function Login() {
  return (
    <div className="auth-form">
      <h2>Sign In</h2>
      <form>
        <input type="email" placeholder="Email" required />
        <input type="password" placeholder="Password" required />
        <button type="submit">Sign In</button>
        <a href="#">Forgot Password?</a>
      </form>
    </div>
  );
}

export default Login;

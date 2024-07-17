import React, { useEffect, useState } from "react";
import "./Auth.css";
import { getResponsePost } from "../lib/utils";

function Login({ setIsLoggedIn }) {
	console.log("is logged in?");
	const [username, setUsername] = useState("username");
	const [password, setPassword] = useState("password");
	const handleForgotPassword = () => {
		// Handle forgot password logic here
		console.log("Forgot Password clicked");
	};
	let storageUsername = localStorage.getItem("username");
	useEffect(() => {
		if (storageUsername) {
			setIsLoggedIn(true);
		}
	}, []);
	const handleLogin = async () => {
		// Handle login logic here
		console.log("Login clicked", username, password);
		const response = await getResponsePost("/login", {
			username: username,
			password: password,
		});
		const loggedin = response?.data;
		console.log(response, loggedin);

		if (loggedin && loggedin.isValid) {
			localStorage.setItem("username", username);
			localStorage.setItem("name", loggedin.name);
			localStorage.setItem("cgpa", loggedin.cgpa);
			localStorage.setItem("id", loggedin.id);
			setIsLoggedIn(true);
		} else {
			alert("Please enter valid Credentials");
		}
	};
	return (
		<div className="auth-form">
			<h2>Sign In</h2>
			<div>
				<input
					type="text"
					placeholder="Email"
					required
					onChange={(e) => {
						setUsername(e.target.value);
					}}
				/>
				<input
					type="password"
					placeholder="Password"
					required
					onChange={(e) => {
						setPassword(e.target.value);
					}}
				/>
				<button type="submit" onClick={handleLogin}>
					Sign In
				</button>
				<label onClick={handleForgotPassword}>Forgot Password</label>
			</div>
		</div>
	);
}

export default Login;

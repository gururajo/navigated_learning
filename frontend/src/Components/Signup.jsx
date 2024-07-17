import React, { useEffect, useState } from "react";
import "./Auth.css";
import { getResponsePost } from "../lib/utils";

function Signup({ setIsLoggedIn }) {
	const [name, setName] = useState("");
	const [password, setPassword] = useState("");
	const [retypePassword, setRetypePassword] = useState("");
	const [email, setEmail] = useState("");
	let storageUsername = localStorage.getItem("username");
	useEffect(() => {
		if (storageUsername) {
			setIsLoggedIn(true);
		}
	}, []);
	const handleSubmit = async () => {
		console.log("signup", name, email, password);
		if (password !== retypePassword) {
			alert("Passwords do not match");
			return;
		}
		let data = {
			name: name,
			username: email,
			password: password,
			cgpa: 4.0,
		};
		const response = await getResponsePost("/learners", data);
		console.log(response);
		const responseData = response?.data;
		if (responseData) {
			setIsLoggedIn(true);
			console.log(
				"this is the data from server for signup",
				responseData
			);

			localStorage.setItem("username", responseData.username);
			localStorage.setItem("name", responseData.name);
			localStorage.setItem("cgpa", responseData.cgpa);
			localStorage.setItem("id", responseData.id);
		}
	};
	return (
		<div className="auth-form">
			<h2>Sign Up</h2>
			<div>
				<input
					type="text"
					placeholder="Name"
					required
					value={name}
					onChange={(e) => setName(e.target.value)}
				/>
				<input
					type="email"
					placeholder="Email"
					required
					value={email}
					onChange={(e) => setEmail(e.target.value)}
				/>
				<input
					type="password"
					placeholder="Password"
					required
					value={password}
					onChange={(e) => setPassword(e.target.value)}
				/>
				<input
					type="password"
					placeholder="Confirm Password"
					required
					value={retypePassword}
					onChange={(e) => setRetypePassword(e.target.value)}
				/>
				<button type="submit" onClick={handleSubmit}>
					Sign Up
				</button>
			</div>
		</div>
	);
}

export default Signup;

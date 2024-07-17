import React, { useState } from "react";
import {
	BrowserRouter as Router,
	Routes,
	Route,
	NavLink,
	Navigate,
} from "react-router-dom";
import Login from "./Components/Login";
import Signup from "./Components/Signup";
import "./App.css";
import Dashboard from "./Components/Dashboard";

function App() {
	const [isLoggedIn, setIsLoggedIn] = useState(false); // Set to false initially for actual use

	return (
		<Router>
			<div className="app">
				{!isLoggedIn ? (
					<div className="auth-card">
						<div className="auth-nav">
							<NavLink
								to="/"
								className={({ isActive }) =>
									isActive ? "active" : ""
								}
							>
								Sign In
							</NavLink>
							<NavLink
								to="/signup"
								className={({ isActive }) =>
									isActive ? "active" : ""
								}
							>
								Sign Up
							</NavLink>
						</div>
						<Routes>
							<Route
								path="/"
								element={
									<Login setIsLoggedIn={setIsLoggedIn} />
								}
							/>
							<Route
								path="/signup"
								element={
									<Signup setIsLoggedIn={setIsLoggedIn} />
								}
							/>
							<Route path="*" element={<Navigate to="/" />} />
						</Routes>
					</div>
				) : (
					<Dashboard setIsLoggedIn={setIsLoggedIn} />
				)}
			</div>
		</Router>
	);
}

export default App;

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
import LearnerActivity from "./Components/LearnerActivity";
import LearnerMap from "./Components/LearnerMap";
import LearnerSummary from "./Components/LearnerSummary";

function App() {
	const [isLoggedIn, setIsLoggedIn] = React.useState(false); // Set to false initially for actual use
	const activitiesState = useState([]);
	const learnerPosState = useState([0.1, 0.1]);

	const containerStyle = {
		width: "100%",
		height: "100vh",
		display: "flex",
		flexDirection: "column",
		backgroundColor: "white",
		boxSizing: "border-box",
	};

	const rowStyle = {
		display: "flex",
		justifyContent: "space-between",
		flexWrap: "wrap",
	};

	const colStyleLeft = {
		flex: "1 1 70%", // Adjust width for responsiveness
		boxSizing: "border-box",
		padding: "10px",
		minWidth: "300px", // Ensure a minimum width for each column
	};

	const colStyleRight = {
		flex: "1 1 30%", // Adjust width for responsiveness
		boxSizing: "border-box",
		padding: "10px",
		minWidth: "300px", // Ensure a minimum width for each column
	};

	const colFullWidthStyle = {
		width: "100%",
	};

	return (
		<Router>
			<div className="app">
				{!isLoggedIn && (
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
							<Route path="/signup" element={<Signup />} />
							<Route path="*" element={<Navigate to="/" />} />
						</Routes>
					</div>
				)}
				{isLoggedIn && (
					<>
						<div style={containerStyle}>
							<h1>Learning Map (Discrete Mathematics)</h1>
							<div style={rowStyle}>
								<div style={colStyleLeft}>
									<LearnerMap
										activitiesState={activitiesState}
										learnerPosState={learnerPosState}
									/>
								</div>
								<div style={colStyleRight}>
									<LearnerActivity
										activitiesState={activitiesState}
									/>
								</div>
							</div>
							<div style={colFullWidthStyle}>
								<LearnerSummary
									activitiesState={activitiesState}
									learnerPosState={learnerPosState}
								/>
							</div>
						</div>
					</>
				)}
			</div>
		</Router>
	);
}

export default App;

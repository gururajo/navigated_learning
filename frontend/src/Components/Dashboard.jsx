import * as d3 from "d3";
import { useEffect, useRef, useState } from "react";
import LearnerActivity from "./LearnerActivity";
import LearnerMap from "./LearnerMap";
import LearnerSummary from "./LearnerSummary";
import { Button, Dropdown, DropdownButton } from "react-bootstrap";
import { getResponseGet } from "../lib/utils";

const containerStyle = {
	width: "100%",
	height: "100vh",
	display: "flex",
	flexDirection: "column",
	backgroundColor: "white",
	boxSizing: "border-box",
};

const headerStyle = {
	display: "flex",
	justifyContent: "space-between",
	alignItems: "center",
	padding: "10px 10px",
	borderBottom: "1px solid #ccc",
	backgroundColor: "rgb(225, 225, 225)",
};

const titleSectionStyle = {
	display: "flex",
	alignItems: "center",
	justifyContent: "space-between",
	width: "60%",
};

const dropdownSectionStyle = {
	marginTop: "10px",
	display: "flex",
	flexDirection: "column",
};

const usernameStyle = {
	marginLeft: "10px",
	fontSize: "1.5rem",
};

const logoutStyle = {
	marginLeft: "auto",
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

const Dashboard = ({ setIsLoggedIn }) => {
	const activitiesState = useState([]);
	const learnerPosState = useState([0.1, 0.1]);
	const learnerId = localStorage.getItem("id");
	var resetMap = [false];
	const [enrolledCourses, setEnrolledCourses] = useState([]);

	const svgRef = useRef(null);
	const zoomRef = useRef(null);

	const setCourses = async (learnerId) => {
		const response = await getResponseGet(`enrolledCourses/${learnerId}`);
		if (response?.data) {
			console.log("Enrolled courses", response.data);
			setEnrolledCourses(response.data);
		} else {
			console.error("Failed to fetch enrolled courses", response);
		}
	};
	useEffect(() => {
		setCourses(learnerId);
	}, []);
	return (
		<>
			<div style={containerStyle}>
				<div className="header" style={headerStyle}>
					<div style={titleSectionStyle}>
						<h1>Navigated Learning </h1>
						<h5 style={usernameStyle}>
							Welcome, {localStorage.getItem("name")} !!!!
						</h5>
					</div>
					<Button
						style={logoutStyle}
						onClick={() => {
							setIsLoggedIn(false);
							localStorage.clear();
						}}
					>
						Logout
					</Button>
				</div>
				<div style={{ display: "flex" }}>
					<div style={colStyleLeft}>
						<LearnerMap
							activitiesState={activitiesState}
							learnerPosState={learnerPosState}
							svgRef={svgRef}
							zoomRef={zoomRef}
						/>
					</div>
					<div style={dropdownSectionStyle}>
						{enrolledCourses && (
							<DropdownButton
								id="dropdown-basic-button"
								title="Enrolled Courses"
							>
								{enrolledCourses.map((course) => (
									<Dropdown.Item
										key={course.course_id}
										href={`#/${course.course_id}`}
									>
										<i className="fa fa-book"></i>
										{"  " + course.course_name}
									</Dropdown.Item>
								))}
								<Dropdown.Item key="Enroll new Course">
									<i className="fa fa-plus-square"></i>
									{"  Enroll New Course "}
								</Dropdown.Item>
							</DropdownButton>
						)}
						<br />

						<Button
							onClick={() => {
								const svg = d3.select(svgRef.current);
								svg.transition().duration(750).call(
									zoomRef.current.transform,
									d3.zoomIdentity // Reset to the default transform
								);
							}}
						>
							ReCentre
						</Button>
					</div>

					<div style={colStyleRight}>
						<LearnerActivity activitiesState={activitiesState} />
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
	);
};

export default Dashboard;

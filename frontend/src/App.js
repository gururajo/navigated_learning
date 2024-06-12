import { useState } from "react";
import "./App.css";
import LearnerActivity from "./Components/LearnerActivity";
import LearnerMap from "./Components/LearnerMap";
import LearnerSummary from "./Components/LearnerSummary";

function App() {
	const activitiesState = useState([]);
	const learnerPosState = useState([100, 900]);

	return (
		<>
			<h1>Learning Map(Discrete Mathematics)</h1>
			<div className="row">
				<div className="col-sm-8 align-middle">
					<LearnerMap
						activitiesState={activitiesState}
						learnerPosState={learnerPosState}
					/>
				</div>
				<div className="col-sm-4 align-middle">
					<LearnerActivity activitiesState={activitiesState} />
				</div>
			</div>
			<div className="align-middle">
				<LearnerSummary
					activitiesState={activitiesState}
					learnerPosState={learnerPosState}
				/>
			</div>
		</>
	);
}

export default App;

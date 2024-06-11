import "./App.css";
import LearnerActivity from "./Components/LearnerActivity";
import LearnerMap from "./Components/LearnerMap";
import LearnerSummary from "./Components/LearnerSummary";

function App() {
	return (
		<>
			<h1>Learning Map(Discrete Mathematics)</h1>
			<div className="row">
				<div className="col-sm-8 align-middle">
					<LearnerMap />
				</div>
				<div className="col-sm-4 align-middle">
					<LearnerActivity />
				</div>
			</div>
			<div className="align-middle">
				<LearnerSummary />
			</div>
		</>
	);
}

export default App;

import "./App.css";
import LearnerActivity from "./Components/LearnerActivity";
import LearnerMap from "./Components/LearnerMap";
import LearnerSummary from "./Components/LearnerSummary";

function App() {
  return (
    <>
      <div className="row">
        <div className="col-sm-8 learnerMap align-middle">
          <LearnerMap />
        </div>
        <div className="col-sm-4 leanerActivity align-middle">
          <LearnerActivity />
        </div>
      </div>
      <div className="learnerSummary align-middle">
        <LearnerSummary />
      </div>
    </>
  );
}

export default App;

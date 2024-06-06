import "./App.css";
import LearnerActivity from "./Components/LearnerActivity";
import LearnerMap from "./Components/LearnerMap";
import LearnerSummary from "./Components/LearnerSummary";

function App() {
  return (
    <>
      <div className="row">
        <div className="col-sm-7 align-middle">
          <LearnerMap />
        </div>
        <div className="col-sm-5 align-middle">
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

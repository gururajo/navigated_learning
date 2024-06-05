import "./App.css";
import LearnerActivity from "./Components/LearnerActivity";
import LearnerMap from "./Components/LearnerMap";
import LearnerSummary from "./Components/LearnerSummary";

function App() {
  return (
    <div className="App">
      <LearnerSummary />
      <LearnerActivity />
      <LearnerMap />
    </div>
  );
}

export default App;

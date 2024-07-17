import React, { useState } from "react";
import { Button, Form, InputGroup } from "react-bootstrap";
import { getResponsePost } from "../lib/utils";

const LearnerSummary = ({ activitiesState, learnerPosState }) => {
	const [loading, setLoading] = useState(false);
	const [summary, setSummary] = useState("");
	const updatePosition = async () => {
		let data = {
			summary: summary,
			enroll_id: 1,
			course_id: 1,
		};
		setLoading(true);
		const response = await getResponsePost("/submitsummary", data);
		console.log(response);
		var newPositions = response?.data;
		if (!newPositions) {
			console.log(newPositions, "this the not the expected response");
			return;
		}
		console.log(newPositions);
		learnerPosState[1]([newPositions[0], newPositions[1]]);
		console.log("this is the new position", newPositions);
		setSummary(summary);
		// setCount((c) => (c + 1) % 4);
		activitiesState[1]((activities) => [
			...activities,
			{
				type: "summary",
				name: summary,
				time: Date(),
			},
		]);
		setLoading(false);
	};

	return (
		<div className="learnerSummaryBody">
			<InputGroup className="mb-3 titleText">
				<InputGroup.Text>Title</InputGroup.Text>
				<Form.Control
					as="textarea"
					aria-label="With textarea"
					value={summary}
					onChange={(e) => setSummary(e.target.value)}
				/>
			</InputGroup>
			<InputGroup className="mb-3 summaryText">
				<InputGroup.Text>Summary</InputGroup.Text>
				<Form.Control
					as="textarea"
					aria-label="With textarea"
					value={summary}
					onChange={(e) => setSummary(e.target.value)}
				/>
			</InputGroup>
			<Button
				variant="secondary"
				className="summarySubmitButton"
				onClick={updatePosition}
				disabled={loading}
			>
				Update My Position
			</Button>
		</div>
	);
};

export default LearnerSummary;

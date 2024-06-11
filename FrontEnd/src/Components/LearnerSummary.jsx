import React from "react";
import { Button, Form, InputGroup } from "react-bootstrap";
import { getResponseGet } from "../lib/utils";

const LearnerSummary = () => {
	const updatePosition = async () => {
		// const response = await getResponseGet("/new_positions");
		// var newPositions = response?.data;
		// // Update position of individual point based on the new data
		// g.select("#individual-point")
		// 	.attr("cx", newPositions[currentPositionIndex].x * 1000)
		// 	.attr("cy", 1000 - newPositions[currentPositionIndex].y * 1000);
		// newCx = newPositions[currentPositionIndex].x * 1000;
		// newCy = 1000 - newPositions[currentPositionIndex].y * 1000;
		// descriptionText.text(newPositions[currentPositionIndex].description);
		// currentPositionIndex = (currentPositionIndex + 1) % newPositions.length;
		// //updateMilestone(newPositions)
		// update_summary_Milestone(buttonClickCount);
		// // Increment the button click count
		// buttonClickCount++;
		// const [[x0, y0], [x1, y1]] = g.node().getBBox(); // Get the bounding box of the group element
		// const width = svg.attr("width");
		// const height = svg.attr("height");
		// const newTransform = d3.zoomIdentity
		// 	.translate(width / 2 - newCx, height / 2 - newCy)
		// 	.scale(1);
		// svg.transition().duration(750).call(zoom.transform, newTransform);
	};
	return (
		<div className="learnerSummaryBody">
			<InputGroup className="mb-3 summaryText">
				<InputGroup.Text>Summary</InputGroup.Text>
				<Form.Control as="textarea" aria-label="With textarea" />
			</InputGroup>
			<Button
				variant="secondary"
				className="summarySubmitButton"
				onClick={updatePosition}
			>
				Update My Position
			</Button>
		</div>
	);
};

export default LearnerSummary;

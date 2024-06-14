import React, { useEffect, useRef } from "react";
import { getResponseGet } from "../lib/utils";
import * as d3 from "d3";

const SVGComponent = ({ children }) => {
	const svgRef = useRef(null);

	useEffect(() => {
		const svg = d3.select(svgRef.current);
		const g = svg.select("g");

		const zoom = d3
			.zoom()
			.scaleExtent([0.5, 5])
			.on("zoom", (event) => {
				g.attr("transform", event.transform);
			});

		svg.call(zoom);
	}, []);

	return (
		<svg ref={svgRef} width="auto" height="auto">
			<g>{children}</g>
		</svg>
	);
};

const GroupComponent = ({ children }) => {
	return <>{children}</>;
};

const CircleComponent = ({ data, activitiesState }) => {
	return (
		<a href={data.video_url} target="_blank" rel="noopener noreferrer">
			<circle
				cx={data.x * 8000 - 2800}
				cy={3650 - data.y * 8000}
				r={5}
				fill="steelblue"
				onClick={(event) => {
					event.currentTarget.setAttribute("fill", "orange");
					activitiesState[1]((activities) => [
						...activities,
						{
							type: "resource",
							name: data.name,
							link: data.video_url,
							time: new Date().toString(),
						},
					]);
				}}
				onMouseOver={(event) => {
					const g = d3.select(event.currentTarget.parentNode);
					g.append("text")
						.attr("x", event.currentTarget.getAttribute("cx"))
						.attr("y", event.currentTarget.getAttribute("cy") - 10)
						.text(data.name)
						.attr("fill", "black")
						.attr("font-size", "12px")
						.attr("font-family", "sans-serif")
						.attr("id", "name-label");
				}}
				onMouseOut={(event) => {
					const g = d3.select(event.currentTarget.parentNode);
					g.select("#name-label").remove();
				}}
			/>
		</a>
	);
};

const LearnerPositionComponent = ({ learnerPosState }) => {
	const pos = learnerPosState[0];
	return (
		<rect
			x={pos[0] * 1000}
			y={1000 - pos[1] * 1000}
			width={20}
			height={20}
			fill="red"
			id="individual-point"
			onMouseOver={(event) => {
				const g = d3.select(event.currentTarget.parentNode);
				g.append("text")
					.attr("x", event.currentTarget.getAttribute("x"))
					.attr("y", event.currentTarget.getAttribute("y") - 10)
					.text("Learner")
					.attr("fill", "black")
					.attr("font-size", "12px")
					.attr("font-family", "sans-serif")
					.attr("id", "learner-label");
			}}
			onMouseOut={(event) => {
				const g = d3.select(event.currentTarget.parentNode);
				g.select("#learner-label").remove();
			}}
		/>
	);
};

const LearnerMap = ({ activitiesState, learnerPosState }) => {
	const [data, setData] = React.useState([]);

	useEffect(() => {
		const loadMap = async () => {
			const response = await getResponseGet("/data");
			if (response) {
				setData(response.data);
			}
		};

		loadMap();
	}, []);

	return (
		<div className="learnerMapBody">
			<SVGComponent>
				<GroupComponent>
					<rect
						x={0}
						y={0}
						width={1000}
						height={1000}
						fill="none"
						stroke="black"
						strokeWidth={2}
					/>
					{data.map((d) => (
						<CircleComponent
							key={d.index}
							data={d}
							activitiesState={activitiesState}
						/>
					))}
					<LearnerPositionComponent
						learnerPosState={learnerPosState}
					/>
					{data.map((d) => (
						<text
							key={d.index}
							x={d.x * 8000 - 2800 + 10}
							y={3650 - d.y * 8000}
							fill="black"
							fontSize="12px"
							fontFamily="sans-serif"
						>
							{d.index}
						</text>
					))}
				</GroupComponent>
			</SVGComponent>
		</div>
	);
};

export default LearnerMap;

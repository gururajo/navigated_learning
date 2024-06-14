import React, { useEffect, useRef, useState } from "react";
import { getResponseGet } from "../lib/utils";
import * as d3 from "d3";

// Grid component
const GridComponent = ({ width, height, step }) => {
	const lines = [];
	for (let x = 0; x <= width; x += step) {
		lines.push(
			<line
				key={`v${x}`}
				x1={x}
				y1={0}
				x2={x}
				y2={height}
				stroke="lightgrey"
				strokeWidth="1"
			/>
		);
	}
	for (let y = 0; y <= height; y += step) {
		lines.push(
			<line
				key={`h${y}`}
				x1={0}
				y1={y}
				x2={width}
				y2={y}
				stroke="lightgrey"
				strokeWidth="1"
			/>
		);
	}
	return <>{lines}</>;
};

// SVG component with zoom
const SVGComponent = ({ children, width, height }) => {
	const svgRef = useRef(null);

	useEffect(() => {
		const svg = d3.select(svgRef.current);
		const g = svg.select("g");

		const zoom = d3
			.zoom()
			.scaleExtent([0.1, 1])
			.on("zoom", (event) => {
				g.attr("transform", event.transform);
			});

		svg.call(zoom);
	}, []);

	return (
		<svg ref={svgRef} style={{ width: "100%", height: "100%" }}>
			<g>
				<GridComponent width={1000} height={1000} step={50} />
				{children}
			</g>
		</svg>
	);
};

// Group component
const GroupComponent = ({ children }) => {
	return <>{children}</>;
};

// Circle component
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

// Learner position component
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

// Main LearnerMap component
const LearnerMap = ({ activitiesState, learnerPosState }) => {
	const [data, setData] = useState([]);
	const mapRef = useRef(null);
	const [dimensions, setDimensions] = useState({ width: 0, height: 0 });

	useEffect(() => {
		const loadMap = async () => {
			const response = await getResponseGet("/data");
			if (response) {
				setData(response.data);
			}
		};

		loadMap();
	}, []);

	useEffect(() => {
		const updateDimensions = () => {
			if (mapRef.current) {
				setDimensions({
					width: mapRef.current.offsetWidth,
					height: mapRef.current.offsetHeight,
				});
			}
		};

		updateDimensions();
		window.addEventListener("resize", updateDimensions);
		return () => {
			window.removeEventListener("resize", updateDimensions);
		};
	}, []);

	return (
		<div className="learnerMapBody" ref={mapRef}>
			<SVGComponent width={dimensions.width} height={dimensions.height}>
				<GroupComponent>
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

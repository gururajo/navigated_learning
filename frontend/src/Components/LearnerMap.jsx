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
			.scaleExtent([0.6, 10])
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
const CircleComponent = ({
	data,
	activitiesState,
	tooltipRef,
	learnerPos,
	coverageRadius,
}) => {
	const handleMouseOver = (event) => {
		const tooltip = d3.select(tooltipRef.current);
		tooltip
			.style("visibility", "visible")
			.html(
				`<div>
					<strong>Index:</strong> ${data.index}<br>
					<strong>Name:</strong> ${data.name}
				</div>`
			)
			.style("left", `${event.pageX + 10}px`)
			.style("top", `${event.pageY + 10}px`);

		// Hide the default text
		d3.select(`#text-${data.index}`).style("visibility", "hidden");
	};

	const handleMouseMove = (event) => {
		const tooltip = d3.select(tooltipRef.current);
		tooltip
			.style("left", `${event.pageX + 10}px`)
			.style("top", `${event.pageY + 10}px`);
	};

	const handleMouseOut = () => {
		const tooltip = d3.select(tooltipRef.current);
		tooltip.style("visibility", "hidden");

		// Restore the default text
		d3.select(`#text-${data.index}`).style("visibility", "visible");
	};

	const distance = Math.sqrt(
		Math.pow(data.x * 8000 - 2800 - learnerPos[0] * 1000, 2) +
			Math.pow(3650 - data.y * 8000 - (1000 - learnerPos[1] * 1000), 2)
	);

	const isWithinCoverage = distance <= coverageRadius;

	return (
		<a
			href={isWithinCoverage ? data.video_url : "#"}
			target={isWithinCoverage ? "_blank" : ""}
			rel="noopener noreferrer"
		>
			<circle
				cx={data.x * 8000 - 2800}
				cy={3650 - data.y * 8000}
				r={5}
				fill={isWithinCoverage ? "steelblue" : "gray"}
				onClick={(event) => {
					if (isWithinCoverage) {
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
					} else {
						event.preventDefault();
					}
				}}
				onMouseOver={handleMouseOver}
				onMouseMove={handleMouseMove}
				onMouseOut={handleMouseOut}
			/>
		</a>
	);
};

// Learner position component
const LearnerPositionComponent = ({ learnerPosState, coverageRadius }) => {
	const pos = learnerPosState[0];
	return (
		<>
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
			<circle
				cx={pos[0] * 1000 + 10}
				cy={1000 - pos[1] * 1000 + 10}
				r={coverageRadius}
				fill="none"
				opacity="0.6"
				stroke="red"
				strokeWidth="2"
				strokeDasharray="10,10"
			/>
			<defs>
				<radialGradient
					id="gradient"
					cx="50%"
					cy="50%"
					r="50%"
					fx="50%"
					fy="50%"
				>
					<stop
						offset="0%"
						style={{
							stopColor: "rgba(0, 0, 255, 0)",
							stopOpacity: 0.6,
						}}
					/>
					<stop
						offset="50%"
						style={{
							stopColor: "rgba(0, 50, 255, 0.6)",
							stopOpacity: 0.8,
						}}
					/>
					<stop
						offset="100%"
						style={{
							stopColor: "rgba(0, 100, 255, 0.8)",
							stopOpacity: 1,
						}}
					/>
				</radialGradient>
			</defs>
		</>
	);
};

// Main LearnerMap component
const LearnerMap = ({ activitiesState, learnerPosState }) => {
	const [data, setData] = useState([]);
	const mapRef = useRef(null);
	const [dimensions, setDimensions] = useState({ width: 0, height: 0 });
	const tooltipRef = useRef(null);
	const [coverageRadius] = useState(300); // Define the coverage radius (adjust as needed)

	const loadMap = async () => {
		const response = await getResponseGet("/data");
		if (response) {
			setData(response.data);
		}
	};
	useEffect(() => {
		loadMap();
	}, []);

	const updateDimensions = () => {
		if (mapRef.current) {
			setDimensions({
				width: mapRef.current.offsetWidth,
				height: mapRef.current.offsetHeight,
			});
		}
	};
	useEffect(() => {
		updateDimensions();
		window.addEventListener("resize", updateDimensions);
		return () => {
			window.removeEventListener("resize", updateDimensions);
		};
	}, []);

	const learnerPos = learnerPosState[0];

	return (
		<div
			className="learnerMapBody"
			ref={mapRef}
			style={{ position: "relative" }}
		>
			<SVGComponent width={dimensions.width} height={dimensions.height}>
				<GroupComponent>
					{data.map((d) => (
						<React.Fragment key={d.index}>
							<CircleComponent
								data={d}
								activitiesState={activitiesState}
								tooltipRef={tooltipRef}
								learnerPos={learnerPos}
								coverageRadius={coverageRadius}
							/>
							<text
								id={`text-${d.index}`}
								x={d.x * 8000 - 2800 + 10}
								y={3650 - d.y * 8000}
								fill="black"
								fontSize="12px"
								fontFamily="sans-serif"
							>
								{d.index}
							</text>
						</React.Fragment>
					))}
					<LearnerPositionComponent
						learnerPosState={learnerPosState}
						coverageRadius={coverageRadius}
					/>
				</GroupComponent>
			</SVGComponent>
			<div
				ref={tooltipRef}
				style={{
					position: "absolute",
					backgroundColor: "rgba(255, 255, 255, 0.9)",
					border: "1px solid #ccc",
					padding: "8px",
					borderRadius: "4px",
					boxShadow: "0px 4px 8px rgba(0, 0, 0, 0.1)",
					pointerEvents: "none",
					visibility: "hidden",
					transition: "opacity 0.2s ease",
					fontSize: "12px",
					zIndex: 10,
				}}
			/>
		</div>
	);
};

export default LearnerMap;

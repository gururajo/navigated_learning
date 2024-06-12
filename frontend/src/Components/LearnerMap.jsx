import { useEffect } from "react";
import { getResponseGet } from "../lib/utils";
import * as d3 from "d3";

const LearnerMap = ({ activitiesState, learnerPosState }) => {
	useEffect(() => {
		loadMap();
	}, []);

	const loadMap = async () => {
		var response = await getResponseGet("/data");
		if (response) {
			const data = response.data;
			console.log(data);

			const svg = d3
				.select(".learnerMapBody")
				.append("svg")
				.attr("width", 1559)
				.attr("height", 650);

			const g = svg.append("g");
			console.log("this is g 1", g);
			// Define zoom behavior
			const zoom = d3
				.zoom()
				.scaleExtent([0.5, 5]) // Set limits to the zoom level
				.on("zoom", (event) => {
					g.attr("transform", event.transform);
				});

			svg.call(zoom);

			// Bind data to circles
			const circles = g
				.selectAll("circle")
				.data(data)
				.enter()
				// .append("a") // Make each point a link
				// .attr("xlink:href", (d) => d.video_url)
				// .attr("target", "_blank")
				.append("circle")
				.attr("cx", (d) => d.x * 8000 - 2800) //d.x * 1000)
				.attr("cy", (d) => 3650 - d.y * 8000) //1000 - d.y * 1000)
				.attr("r", 5)
				.attr("fill", "steelblue")
				.on("click", function (event, d) {
					// Change color of clicked circle
					d3.select(this).attr("fill", "orange");
					activitiesState[1]((activities) => [
						...activities,
						{
							type: "resource",
							name: d.name,
							link: d.video_url,
							time: Date(),
						},
					]);
				})
				.on("mouseover", function (event, d) {
					// Display name of the data point
					g.append("text")
						.attr("x", d3.select(this).attr("cx")) // Position text relative to the circle
						.attr("y", d3.select(this).attr("cy") - 10) // Adjust the position of the text slightly above the circle
						.text(d.name)
						.attr("fill", "black")
						.attr("font-size", "12px")
						.attr("font-family", "sans-serif")
						.attr("id", "name-label");
				})
				.on("mouseout", function (event, d) {
					// Remove the name label when mouse moves out
					g.selectAll("text").remove();
				});
			console.log("this is the learnerPos", learnerPosState);
			g.append("rect")
				.attr("x", learnerPosState[0][0]) // Adjust x-coordinate
				.attr("y", learnerPosState[0][1])
				.attr("width", 20)
				.attr("height", 20)
				.attr("fill", "red")
				.attr("id", "individual-point")
				.on("mouseover", function (event, d) {
					g.append("text")
						.attr("x", d3.select(this).attr("x"))
						.attr("y", d3.select(this).attr("y") - 10)
						.text("Learner") // Set text content to "Learner"
						.attr("fill", "black")
						.attr("font-size", "12px")
						.attr("font-family", "sans-serif")
						.attr("id", "learner-label");
				})
				.on("mouseout", function (event, d) {
					// Remove the name label when mouse moves out
					g.selectAll("text").remove();
				});

			const texts = g
				.selectAll("text")
				.data(data)
				.enter()
				.append("text")
				.attr("x", (d) => d.x * 8000 - 2800 + 10) // Adjust x-coordinate to position text beside the circle
				.attr("y", (d) => 3650 - d.y * 8000) // Adjust y-coordinate if needed
				.text((d) => d.index)
				.attr("fill", "black")
				.attr("font-size", "12px")
				.attr("font-family", "sans-serif");

			console.log("this is g", g);
		}
	};

	return (
		<>
			<div className="learnerMapBody"></div>
		</>
	);
};

export default LearnerMap;

// import React, { useState, useEffect } from "react";
// import ReactMapGL, { Marker } from "react-map-gl";

// const mapData = [
// 	{ id: 1, latitude: 37.7749, longitude: -122.4194 },
// 	{ id: 2, latitude: 37.7849, longitude: -122.4094 },
// 	{ id: 3, latitude: 37.7649, longitude: -122.4294 },
// 	{ id: 4, latitude: 37.7549, longitude: -122.4394 },
// 	{ id: 5, latitude: 37.7449, longitude: -122.4494 },
// ];
// export default function LearnerMap() {
// 	const [viewport, setViewport] = useState({
// 		latitude: 37.7833,
// 		longitude: -122.4167,
// 		zoom: 13,
// 	});
// 	return (
// 		<ReactMapGL
// 			{...viewport}
// 			width="100%"
// 			height="400px"
// 			mapStyle="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json"
// 			onViewportChange={(newViewport) => setViewport(newViewport)}
// 		>
// 			{mapData.map((marker) => (
// 				<Marker
// 					key={marker.id}
// 					latitude={marker.latitude}
// 					longitude={marker.longitude}
// 				>
// 					<img
// 						src="https://upload.wikimedia.org/wikipedia/commons/e/ed/Map_pin_icon.svg"
// 						alt="Marker"
// 						style={{ width: "20px", height: "20px" }}
// 					/>
// 				</Marker>
// 			))}
// 		</ReactMapGL>
// 	);
// }

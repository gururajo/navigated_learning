import { useEffect } from "react";
import { getResponseGet } from "../lib/utils";
import * as d3 from "d3";

const LearnerMap = () => {
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
        .attr("width", 950)
        .attr("height", 600);

      const g = svg.append("g");

      // Define zoom behavior
      const zoom = d3
        .zoom()
        .scaleExtent([0.5, 5]) // Set limits to the zoom level
        .on("zoom", (event) => {
          g.attr("transform", event.transform);
        });

      svg.call(zoom);

      // Border
      g.append("rect")
        .attr("x", 0)
        .attr("y", 0)
        .attr("width", 1000) // Same as SVG width
        .attr("height", 1000) // Same as SVG height
        .attr("fill", "none")
        .attr("stroke", "black")
        .attr("stroke-width", 2);

      // Bind data to circles
      const circles = g
        .selectAll("circle")
        .data(data)
        .enter()
        .append("a") // Make each point a link
        .attr("xlink:href", (d) => d.video_url)
        .attr("target", "_blank")
        .append("circle")
        .attr("cx", (d) => d.x * 8000 - 2800) //d.x * 1000)
        .attr("cy", (d) => 3650 - d.y * 8000) //1000 - d.y * 1000)
        .attr("r", 5)
        .attr("fill", "steelblue")
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
      g.append("rect")
        .attr("x", 100) // Adjust x-coordinate
        .attr("y", 900)
        .attr("width", 10)
        .attr("height", 10)
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
    }
  };

  return (
    <>
      <div className="learnerMapBody"></div>
    </>
  );
};

export default LearnerMap;

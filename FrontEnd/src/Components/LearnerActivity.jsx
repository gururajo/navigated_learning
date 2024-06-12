import Timeline from "@mui/lab/Timeline";
import TimelineItem from "@mui/lab/TimelineItem";
import TimelineSeparator from "@mui/lab/TimelineSeparator";
import TimelineConnector from "@mui/lab/TimelineConnector";
import TimelineContent from "@mui/lab/TimelineContent";
import TimelineOppositeContent from "@mui/lab/TimelineOppositeContent";
import TimelineDot from "@mui/lab/TimelineDot";
import MenuBookIcon from "@mui/icons-material/MenuBook";
import PublishIcon from "@mui/icons-material/Publish";
import HotelIcon from "@mui/icons-material/Hotel";
import RepeatIcon from "@mui/icons-material/Repeat";
import Typography from "@mui/material/Typography";
import { useEffect } from "react";

const LearnerActivity = ({ activitiesState }) => {
	console.log("sthis is activitiesState", activitiesState[0]);

	return (
		<div className="learnerActivityBody">
			<Timeline position="right">
				{/* <TimelineItem>
					<TimelineOppositeContent
						sx={{ m: "auto 0" }}
						align="right"
						variant="body2"
						color="text.secondary"
					>
						9:30 am
					</TimelineOppositeContent>
					<TimelineSeparator>
						<TimelineConnector />
						<TimelineDot>
							<FastfoodIcon />
						</TimelineDot>
						<TimelineConnector />
					</TimelineSeparator>
					<TimelineContent sx={{ py: "12px", px: 2 }}>
						<Typography variant="h6" component="span">
							Eat
						</Typography>
						<Typography>Because you need strength</Typography>
					</TimelineContent>
				</TimelineItem> */}

				{activitiesState[0].map((activity, index) => (
					<TimelineItem key={index}>
						<TimelineOppositeContent
							sx={{ m: "auto 0" }}
							align="right"
							variant="body2"
							color="text.secondary"
						>
							{activity.time}
						</TimelineOppositeContent>
						<TimelineSeparator>
							<TimelineConnector />
							<TimelineDot>
								{activity.type === "resource" ? (
									<MenuBookIcon />
								) : (
									<PublishIcon />
								)}
							</TimelineDot>
							<TimelineConnector />
						</TimelineSeparator>
						<TimelineContent sx={{ py: "12px", px: 2 }}>
							<Typography variant="h6" component="span">
								{activity.name.slice(0, 50)}
							</Typography>
							<Typography>
								<a
									href={activity.link}
									target="_blank"
									rel="noopener noreferrer"
								>
									{activity.link}
								</a>
							</Typography>
						</TimelineContent>
					</TimelineItem>
				))}
			</Timeline>
		</div>
	);
};

export default LearnerActivity;

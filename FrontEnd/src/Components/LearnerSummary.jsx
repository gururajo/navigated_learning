import React from "react";
import { Button, Form, InputGroup } from "react-bootstrap";

const LearnerSummary = () => {
  return (
    <div className="learnerSummaryBody">
      <InputGroup className="mb-3 summaryText">
        <InputGroup.Text>Summary</InputGroup.Text>
        <Form.Control as="textarea" aria-label="With textarea" />
      </InputGroup>
      <Button variant="secondary" className="summarySubmitButton">
        Update My Position
      </Button>
    </div>
  );
};

export default LearnerSummary;

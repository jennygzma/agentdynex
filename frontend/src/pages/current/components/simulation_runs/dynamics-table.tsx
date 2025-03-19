import React, { useEffect, useState } from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
} from "@mui/material";
import axios from "axios";
import { SERVER_URL } from "../..";

type DynamicsData = {
  milestone: string;
  dynamics: string;
  timestamp: string;
};

const Dynamics = () => {
  const [dynamicsData, setDynamicsData] = useState<DynamicsData[]>([
    {
      milestone: "Assignment 1 announced and completed",
      dynamics:
        "- Alex convinced Betty to try to be a better student, \n - Charlie started badmouthing the professor",
      timestamp: "2024-03-19T12:00:00Z",
    },
    {
      milestone: "Assignment 1 announced and completed",
      dynamics:
        "- Alex convinced Betty to try to be a better student, \n - Charlie started badmouthing the professor",
      timestamp: "2024-03-19T13:00:00Z",
    },
  ]);

  console.log(dynamicsData);
  useEffect(() => {
    // getRubric();
  }, []);

  //   const getRubric = () => {
  //     updateIsLoading(true);
  //     axios({
  //       method: "GET",
  //       url: `${SERVER_URL}/get_rubric`,
  //     })
  //       .then((response) => {
  //         console.log("/get_rubric request successful:", response.data);
  //         console.log(`rubric ${response.data}`);
  //         setRubricData(response.data.rubric);
  //       })
  //       .catch((error) => {
  //         console.error("Error calling /get_rubric request:", error);
  //       })
  //       .finally(() => {
  //         updateIsLoading(false);
  //       });
  //   };

  return (
    <TableContainer component={Paper}>
      <Table>
        <TableHead>
          <TableRow sx={{ backgroundColor: "#6a4c9cff" }}>
            <TableCell sx={{ color: "white" }}>MILESTONE</TableCell>
            <TableCell sx={{ color: "white" }}>DYNAMICS</TableCell>
            <TableCell sx={{ color: "white" }}>TIMESTAMP</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {dynamicsData.map((row, index) => (
            <TableRow key={index}>
              <TableCell>{row.milestone}</TableCell>
              <TableCell>{row.dynamics}</TableCell>
              <TableCell>{row.timestamp}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default Dynamics;

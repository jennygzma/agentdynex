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
import { SERVER_URL } from ".";
import { useAppContext } from "./hooks/app-context";
import axios from "axios";

type RubricItem = {
  category: string;
  rubric_type: string;
  description: string;
  example: string;
};

const Rubric = () => {
  const [rubricData, setRubricData] = useState<RubricItem[]>([]);
  const { updateIsLoading } = useAppContext();
  console.log(rubricData);
  useEffect(() => {
    console.log("hi jenny");
    getRubric();
  }, []);

  const getRubric = () => {
    updateIsLoading(true);
    axios({
      method: "GET",
      url: `${SERVER_URL}/get_rubric`,
    })
      .then((response) => {
        console.log("/get_rubric request successful:", response.data);
        console.log(`rubric ${response.data}`);
        setRubricData(response.data.rubric);
      })
      .catch((error) => {
        console.error("Error calling /get_rubric request:", error);
      })
      .finally(() => {
        updateIsLoading(false);
      });
  };

  return (
    <TableContainer component={Paper}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Category</TableCell>
            <TableCell>Rubric Type</TableCell>
            <TableCell>Description</TableCell>
            <TableCell>Example</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {rubricData.map((row, index) => (
            <TableRow key={index}>
              <TableCell>{row.category}</TableCell>
              <TableCell>{row.rubric_type}</TableCell>
              <TableCell>{row.description}</TableCell>
              <TableCell>{row.example}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default Rubric;

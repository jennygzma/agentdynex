import React, { useEffect, useState } from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Checkbox,
} from "@mui/material";
import axios from "axios";
import { SERVER_URL } from "../..";
import { useAppContext } from "../../hooks/app-context";
import Button from "../../../../components/Button";
import TextField from "../../../../components/TextField";

type FixData = {
  problem: string;
  problem_example: string;
  solution: string;
  solution_example: string;
};

const UserSpecifiedFixes = () => {
  const [fixesData, setFixesData] = useState<FixData[]>([{problem: "hi", problem_example: "hi bitch", solution: "bye", solution_example: "bye bitch"}, {problem:"fuck me", problem_example: "fuck me bitch", solution:"fuck you", solution_example: "fuck you bitch"}]);
  const [selectedFixes, setSelectedFixes] = useState<Set<number>>(new Set());
    const [userInput, setUserInput] = useState<string>("");
  const { isRunningSimulation, currentPrototype, currentRunId, updateIsLoading } =
    useAppContext();

  const identifyNewListEntries = () => {
    updateIsLoading(true);
    axios({
      method: "POST",
      url: `${SERVER_URL}/identify_new_list_entry`,
      data: {
        input: userInput,
      },
    })
      .then((response) => {
        console.log("/identify_new_list_entry request successful:", response.data);
        setFixesData(response.data.fixes);
      })
      .catch((error) => {
        console.error("Error calling /identify_new_list_entry request:", error);
      })
      .finally(() => {
        updateIsLoading(false);
      });
  };

  useEffect(() => {
  }, [currentRunId, currentPrototype]);

  // Toggle selected fixes
  const handleCheckboxChange = (index: number) => {
    setSelectedFixes((prev) => {
      const newSelected = new Set(prev);
      if (newSelected.has(index)) {
        newSelected.delete(index);
      } else {
        newSelected.add(index);
      }
      return newSelected;
    });
  };

  if (!fixesData) return <></>;
  return (
    <TableContainer component={Paper} elevation={0} sx={{ boxShadow: "none" }}>
        <TextField
            label="User Identified Error"
            className="User Identified Error"
            rows={4}
            value={userInput}
            onChange={(e) => { setUserInput(e.target.value)}}
        />
      <Button
        variant="contained"
        color="primary"
        fullWidth
        onClick={()=>identifyNewListEntries()}
      >
        Get Fixes for Identified Issues
      </Button>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell sx={{ fontWeight: "bold" }}>Problem</TableCell>
            <TableCell sx={{ fontWeight: "bold" }}>Solution</TableCell>
            <TableCell sx={{ fontWeight: "bold" }}>Apply</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {fixesData.map((fix, index) => (
            <TableRow key={index}>
              <TableCell>{fix.problem}</TableCell>
              <TableCell>{fix.solution}</TableCell>
              <TableCell>
                <Checkbox
                  checked={selectedFixes.has(index)}
                  onChange={() => handleCheckboxChange(index)}
                  sx={{
                    color: "purple",
                    "&.Mui-checked": {
                      color: "purple",
                    },
                  }}
                />
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
      <Button
        variant="contained"
        color="primary"
        fullWidth
        onClick={()=>{}}
        disabled={selectedFixes.size === 0}
      >
        Submit Selected Fixes
      </Button>
    </TableContainer>
  );
};

export default UserSpecifiedFixes;

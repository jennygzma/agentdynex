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

type FixData = {
  problem: string;
  solution: string;
};

const Fixes = () => {
  const [fixesData, setFixesData] = useState<FixData[]>([{problem: "hi", solution: "bye"}, {problem:"fuck me", solution:"fuck you"}]);
  const [selectedFixes, setSelectedFixes] = useState<Set<number>>(new Set());

  const { isRunningSimulation, currentPrototype, currentRunId, updateIsLoading } =
    useAppContext();

  const generateFixes = () => {
    updateIsLoading(true);
    axios({
      method: "GET",
      url: `${SERVER_URL}/generate_fixes`,
    })
      .then((response) => {
        console.log("/generate_fixes request successful:", response.data);
        setFixesData(response.data.fixes);
      })
      .catch((error) => {
        console.error("Error calling /generate_fixes request:", error);
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
      <Button
        variant="contained"
        color="primary"
        fullWidth
        onClick={()=>generateFixes()}
      >
        Get Fixes
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

export default Fixes;

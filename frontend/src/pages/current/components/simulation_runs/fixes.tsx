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
  problem_example: string;
  solution: string;
  solution_example: string;
};

const Fixes = () => {
  const [fixesData, setFixesData] = useState<FixData[]>([
    {
      problem: "hi",
      problem_example: "hi bitch",
      solution: "bye",
      solution_example: "bye bitch",
    },
    {
      problem: "fuck me",
      problem_example: "fuck me bitch",
      solution: "fuck you",
      solution_example: "fuck you bitch",
    },
  ]);
  const [selectedFixes, setSelectedFixes] = useState<Set<FixData>>(new Set());

  const {
    isRunningSimulation,
    currentPrototype,
    currentRunId,
    updateIsLoading,
  } = useAppContext();

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

  const setFixesToApply = () => {
    updateIsLoading(true);
    axios({
      method: "POST",
      url: `${SERVER_URL}/set_fixes_to_apply`,
      data: {
        fixes: Array.from(selectedFixes),
      },
    })
      .then((response) => {
        console.log("/set_fixes_to_apply request successful:", response.data);
      })
      .catch((error) => {
        console.error("Error calling /set_fixes_to_apply request:", error);
      })
      .finally(() => {
        updateIsLoading(false);
      });
  };

  const getFixesToApply = () => {
    updateIsLoading(true);
    axios({
      method: "GET",
      url: `${SERVER_URL}/get_fixes_to_apply`,
    })
      .then((response) => {
        console.log("/get_fixes_to_apply request successful:", response.data);
        setFixesData(response.data.fixes_to_apply);
        setSelectedFixes(new Set<FixData>(response.data.fixes_to_apply));
      })
      .catch((error) => {
        console.error("Error calling /get_fixes_to_apply request:", error);
      })
      .finally(() => {
        updateIsLoading(false);
      });
  };

  useEffect(() => {
    getFixesToApply();
  }, [currentRunId, currentPrototype]);

  // Toggle selected fixes
  const handleCheckboxChange = (fix: FixData) => {
    setSelectedFixes((prev) => {
      const newSelected = new Set(prev);
      if (newSelected.has(fix)) {
        newSelected.delete(fix);
      } else {
        newSelected.add(fix);
      }
      return newSelected;
    });
  };

  return (
    <TableContainer component={Paper} elevation={0} sx={{ boxShadow: "none" }}>
      <Button
        variant="contained"
        color="primary"
        fullWidth
        onClick={() => generateFixes()}
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
          {fixesData?.map((fix, index) => (
            <TableRow key={index}>
              <TableCell>{fix.problem}</TableCell>
              <TableCell>{fix.solution}</TableCell>
              <TableCell>
                <Checkbox
                  checked={selectedFixes.has(fix)}
                  onChange={() => handleCheckboxChange(fix)}
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
        onClick={() => {
          setFixesToApply();
        }}
        disabled={selectedFixes?.size === 0}
      >
        Submit Selected Fixes
      </Button>
    </TableContainer>
  );
};

export default Fixes;

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
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from "@mui/material";
import axios from "axios";
import { SERVER_URL } from "../..";
import { useAppContext } from "../../hooks/app-context";
import Button from "../../../../components/Button";
import InputWithButton from "../../../../components/InputWithButton";
import TextField from "../../../../components/TextField";

type FixData = {
  problem: string;
  problem_example: string;
  solution: string;
  solution_example: string;
};

type EditableFixData = FixData & { index: number };

const UserSpecifiedFixes = () => {
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
  const [userInput, setUserInput] = useState<string>("");
  const [hasSubmitted, setHasSubmitted] = useState(true);
  const [openEdit, setOpenEdit] = useState(false);
  const [editData, setEditData] = useState<EditableFixData | null>(null);
  const { currentPrototype, currentRunId, updateIsLoading } = useAppContext();

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
        console.log(
          "/identify_new_list_entry request successful:",
          response.data,
        );
        setFixesData(response.data.new_fixes);
      })
      .catch((error) => {
        console.error("Error calling /identify_new_list_entry request:", error);
      })
      .finally(() => {
        updateIsLoading(false);
      });
  };

  const addToList = () => {
    updateIsLoading(true);
    axios({
      method: "POST",
      url: `${SERVER_URL}/add_to_iterative_list`,
      data: {
        elements: Array.from(selectedFixes),
      },
    })
      .then((response) => {
        console.log(
          "/add_to_iterative_list request successful:",
          response.data,
        );
      })
      .catch((error) => {
        console.error("Error calling /add_to_iterative_list request:", error);
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
        user_specified: true,
      },
    })
      .then((response) => {
        console.log("/set_fixes_to_apply request successful:", response.data);
        setHasSubmitted(true);
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
      params: {
        user_specified: true,
      },
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
    setUserInput("");
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
    setHasSubmitted(false);
  };

  const handleRowClick = (fix: FixData, index: number) => {
    setEditData({ ...fix, index });
    setOpenEdit(true);
  };

  const handleEditChange = (field: keyof FixData, value: string) => {
    setEditData((prev) => (prev ? { ...prev, [field]: value } : null));
  };

  const handleEditSubmit = () => {
    if (editData !== null && editData.index !== undefined) {
      setFixesData((prev) =>
        prev.map((fix, idx) =>
          idx === editData.index ? { ...editData } : fix,
        ),
      );
      setOpenEdit(false);
    }
  };

  return (
    <TableContainer component={Paper} elevation={0} sx={{ boxShadow: "none" }}>
      <InputWithButton
        label="User Identified Error"
        input={userInput}
        setInput={setUserInput}
        onClick={() => {
          identifyNewListEntries();
        }}
        direction="column"
        rows={4}
      />
      <Table>
        <TableHead>
          <TableRow>
            <TableCell width="20%" sx={{ fontWeight: "bold" }}>
              Problem
            </TableCell>
            <TableCell width="20%" sx={{ fontWeight: "bold" }}>
              Problem Example
            </TableCell>
            <TableCell width="20%" sx={{ fontWeight: "bold" }}>
              Solution
            </TableCell>
            <TableCell width="20%" sx={{ fontWeight: "bold" }}>
              Solution Example
            </TableCell>
            <TableCell width="20%" sx={{ fontWeight: "bold" }}>
              Apply
            </TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {fixesData?.map((fix, index) => (
            <TableRow key={index}>
              <TableCell
                onClick={() => handleRowClick(fix, index)}
                style={{ cursor: "pointer" }}
              >
                {fix.problem}
              </TableCell>
              <TableCell
                onClick={() => handleRowClick(fix, index)}
                style={{ cursor: "pointer" }}
              >
                {fix.problem_example}
              </TableCell>
              <TableCell
                onClick={() => handleRowClick(fix, index)}
                style={{ cursor: "pointer" }}
              >
                {fix.solution}
              </TableCell>
              <TableCell
                onClick={() => handleRowClick(fix, index)}
                style={{ cursor: "pointer" }}
              >
                {fix.solution_example}
              </TableCell>
              <TableCell>
                <Checkbox
                  checked={selectedFixes?.has(fix)}
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
      <Dialog open={openEdit} onClose={() => setOpenEdit(false)}>
        <DialogTitle>Edit Fix</DialogTitle>
        <DialogContent>
          {editData && (
            <>
              <TextField
                fullWidth
                margin="dense"
                label="Problem"
                value={editData.problem}
                onChange={(e) => handleEditChange("problem", e.target.value)}
              />
              <TextField
                fullWidth
                margin="dense"
                label="Problem Example"
                value={editData.problem_example}
                onChange={(e) =>
                  handleEditChange("problem_example", e.target.value)
                }
              />
              <TextField
                fullWidth
                margin="dense"
                label="Solution"
                value={editData.solution}
                onChange={(e) => handleEditChange("solution", e.target.value)}
              />
              <TextField
                fullWidth
                margin="dense"
                label="Solution Example"
                value={editData.solution_example}
                onChange={(e) =>
                  handleEditChange("solution_example", e.target.value)
                }
              />
            </>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenEdit(false)}>Cancel</Button>
          <Button
            onClick={handleEditSubmit}
            variant="contained"
            color="primary"
          >
            Save
          </Button>
        </DialogActions>
      </Dialog>
      <Button
        variant="contained"
        color="primary"
        fullWidth
        onClick={() => {
          addToList();
          setFixesToApply();
        }}
        disabled={selectedFixes?.size === 0 || hasSubmitted}
      >
        Submit Selected Fixes
      </Button>
    </TableContainer>
  );
};

export default UserSpecifiedFixes;

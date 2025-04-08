import React, { useEffect, useRef, useState } from "react";
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
import { useAppContext } from "../../hooks/app-context";

type ChangeLogData = {
  where: string;
  what: string;
  change: string;
  milestone: string;
};

const ChangeLog = ({ expand }: { expand: boolean }) => {
  const [changeLogData, setChangeLogData] = useState<ChangeLogData[]>([]);

  const { isRunningSimulation, currentPrototype, currentRunId } =
    useAppContext();

  const fetchChanges = () => {
    // updateIsLoading(true);
    axios({
      method: "GET",
      url: `${SERVER_URL}/fetch_changes`,
    })
      .then((response) => {
        console.log("/fetch_changes request successful:", response.data);
        setChangeLogData(response.data.changes_data);
      })
      .catch((error) => {
        console.error("Error calling /fetch_changes request:", error);
      })
      .finally(() => {
        // updateIsLoading(false);
      });
  };

  const getChanges = () => {
    // updateIsLoading(true);
    axios({
      method: "GET",
      url: `${SERVER_URL}/get_changes`,
    })
      .then((response) => {
        console.log("/get_changes request successful:", response.data);
        setChangeLogData(response.data.changes_data);
      })
      .catch((error) => {
        console.error("Error calling /get_changes request:", error);
      })
      .finally(() => {
        // updateIsLoading(false);
      });
  };

  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    if (isRunningSimulation) {
      intervalRef.current = setInterval(fetchChanges, 60000);
    } else {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null; // Ensure it's reset
      }
    }

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
    };
  }, [isRunningSimulation]);

  useEffect(() => {
    getChanges();
  }, [expand, currentRunId, currentPrototype]);

  useEffect(() => {
    getChanges();
  }, []);

  if (!changeLogData) return <></>;
  return (
    <TableContainer component={Paper}>
      <Table>
        <TableHead>
          <TableRow sx={{ backgroundColor: "#6a4c9cff" }}>
            <TableCell sx={{ color: "white" }}>MILESTONE</TableCell>
            <TableCell sx={{ color: "white" }}>WHERE</TableCell>
            <TableCell sx={{ color: "white" }}>WHAT</TableCell>
            <TableCell sx={{ color: "white" }}>CHANGE</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {changeLogData
            .filter((row) => row.change.trim() !== "")
            .map((row, index, array) => {
              const showMilestone =
                index === 0 || row.milestone !== array[index - 1].milestone;
              return (
                <TableRow key={index}>
                  <TableCell>{showMilestone ? row.milestone : ""}</TableCell>
                  <TableCell>{row.where}</TableCell>
                  <TableCell>{row.what}</TableCell>
                  <TableCell>{row.change}</TableCell>
                </TableRow>
              );
            })}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default ChangeLog;

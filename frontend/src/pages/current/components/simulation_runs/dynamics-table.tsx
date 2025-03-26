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

type DynamicsData = {
  milestone: string;
  dynamic: string;
};

const Dynamics = ({ expand }: { expand: boolean }) => {
  const [dynamicsData, setDynamicsData] = useState<DynamicsData[]>([]);
  const { isRunningSimulation, currentRunId, currentPrototype } =
    useAppContext();

  console.log(dynamicsData);

  const fetchDynamics = () => {
    // updateIsLoading(true);
    axios({
      method: "GET",
      url: `${SERVER_URL}/fetch_dynamics`,
    })
      .then((response) => {
        console.log("/fetch_dynamics request successful:", response.data);
        setDynamicsData(response.data.dynamics_data);
      })
      .catch((error) => {
        console.error("Error calling /fetch_dynamics request:", error);
      })
      .finally(() => {
        // updateIsLoading(false);
      });
  };
  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    if (isRunningSimulation) {
      intervalRef.current = setInterval(fetchDynamics, 60000);
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
    if (expand) fetchDynamics();
  }, [currentRunId, currentPrototype]);

  return (
    <TableContainer component={Paper}>
      <Table>
        <TableHead>
          <TableRow sx={{ backgroundColor: "#6a4c9cff" }}>
            <TableCell sx={{ color: "white" }}>MILESTONE</TableCell>
            <TableCell sx={{ color: "white" }}>DYNAMICS</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {dynamicsData
            .filter((row) => row?.dynamic?.trim() !== "")
            .map((row, index, array) => {
              const showMilestone =
                index === 0 || row.milestone !== array[index - 1].milestone;

              return (
                <TableRow key={index}>
                  <TableCell>{showMilestone ? row.milestone : ""}</TableCell>
                  <TableCell>{row.dynamic}</TableCell>
                </TableRow>
              );
            })}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default Dynamics;

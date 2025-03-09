import { Stack } from "@mui/material";
import React from "react";
import RunsNavBar from "./runs-nav-bar";
import Run from "./run";
import { useAppContext } from "../../hooks/app-context";
import ConfigCreation from "./config_creation";

const SimulationRuns = () => {
  const { updateIsLoading, currentRunId, currentRunTree } = useAppContext();
  if (!currentRunTree) {
    return <ConfigCreation />;
  }
  return (
    <Stack direction="row" spacing="20px">
      <RunsNavBar />
      {currentRunId !== undefined && currentRunId !== "initial" ? (
        <Run />
      ) : (
        <ConfigCreation />
      )}
    </Stack>
  );
};

export default SimulationRuns;

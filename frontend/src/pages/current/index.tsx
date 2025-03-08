import { Stack } from "@mui/material";
import React, { useEffect, useState } from "react";
import { useAppContext } from "./hooks/app-context";
import Spinner from "./components/spinner";
import { MatrixProvider } from "./hooks/matrix-context";
import Matrix from "./components/matrix";
import Header from "./components/header";
import SetMatrix from "./components/set-matrix";
import SimulationRuns from "./components/simulation_runs";

const local = true;
export const SERVER_URL = local
  ? ""
  : "https://dynexbackend-nmingl5go-jenny-mas-projects.vercel.app/";

// This prototype focuses on planning and getting a fully planned out version with the code ready
const Home = () => {
  const { isLoading, currentPrototype } = useAppContext();
  useEffect(() => {}, [isLoading]);
  const [expand, setExpand] = useState(true);

  return (
    <div className={"home"}>
      {isLoading && <Spinner />}
      <MatrixProvider>
        <Header />
        {!currentPrototype && <Matrix />}
      </MatrixProvider>
      {currentPrototype && (
        <Stack
          spacing="10px"
          sx={{
            padding: "40px",
            height: "100%",
            minHeight: "100vh",
          }}
        >
          <SetMatrix />
          <SimulationRuns />
        </Stack>
      )}
    </div>
  );
};

export default Home;

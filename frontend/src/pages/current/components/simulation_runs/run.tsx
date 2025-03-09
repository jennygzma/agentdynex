import { Stack, Typography } from "@mui/material";
import React, { useEffect, useState } from "react";
import axios from "axios";
import { useAppContext } from "../../hooks/app-context";
import { SERVER_URL } from "../..";
import Button from "../../../../components/Button";
import TextField from "../../../../components/TextField";
import Reflection from "./reflection";
import { ExpandLess, ExpandMore } from "@mui/icons-material";

const Run = () => {
  const { updateIsLoading, currentPrototype, currentRunId } = useAppContext();
  const [config, setConfig] = useState("");
  const [logs, setLogs] = useState("");
  const [summary, setSummary] = useState("");
  const [updatedConfig, setUpdatedConfig] = useState(false);
  const [isRunningSimulation, setIsRunningSimulation] = useState(false);
  const [hasReflection, setHasReflection] = useState(false);
  const [expand, setExpand] = useState(true);

  const saveConfig = () => {
    updateIsLoading(true);
    axios({
      method: "POST",
      url: `${SERVER_URL}/save_config`,
      data: {
        config,
        type: "initial",
      },
    })
      .then((response) => {
        console.log("/save_config request successful:", response.data);
        getConfig();
        setUpdatedConfig(false);
      })
      .catch((error) => {
        console.error("Error calling /save_config request:", error);
      })
      .finally(() => {
        updateIsLoading(false);
      });
  };

  const getConfig = () => {
    updateIsLoading(true);
    axios({
      method: "GET",
      url: `${SERVER_URL}/get_config`,
      params: {
        type: "initial",
      },
    })
      .then((response) => {
        console.log("/get_config request successful:", response.data);
        setConfig(response.data.config);
      })
      .catch((error) => {
        console.error("Error calling /get_config request:", error);
      })
      .finally(() => {
        updateIsLoading(false);
      });
  };

  const generateReflection = () => {
    updateIsLoading(true);
    axios({
      method: "POST",
      url: `${SERVER_URL}/generate_reflection`,
    })
      .then((response) => {
        console.log("/generate_reflection request successful:", response.data);
      })
      .catch((error) => {
        console.error("Error calling /generate_reflection request:", error);
      })
      .finally(() => {
        updateIsLoading(false);
      });
  };

  const getLogs = () => {
    updateIsLoading(true);
    axios({
      method: "GET",
      url: `${SERVER_URL}/get_logs`,
    })
      .then((response) => {
        console.log("/get_logs request successful:", response.data);
        setLogs(response.data.logs);
      })
      .catch((error) => {
        console.error("Error calling /get_logs request:", error);
      })
      .finally(() => {
        updateIsLoading(false);
      });
  };

  const getSummary = () => {
    updateIsLoading(true);
    axios({
      method: "GET",
      url: `${SERVER_URL}/get_summary`,
    })
      .then((response) => {
        console.log("/get_summary request successful:", response.data);
        setSummary(response.data.summary);
      })
      .catch((error) => {
        console.error("Error calling /get_summary request:", error);
      })
      .finally(() => {
        updateIsLoading(false);
      });
  };

  useEffect(() => {
    if (!currentPrototype) return;
    getConfig();
    setIsRunningSimulation(false);
    setHasReflection(false);
    // this may need to change
    setLogs("");
    setSummary("");
  }, [currentPrototype, currentRunId]);

  if (!currentPrototype) return <></>;
  return (
    <Stack spacing="20px" width="85%">
      {hasReflection && <Reflection />}
      {!expand ? (
        <Stack direction="row" spacing="10px">
          <Button onClick={() => setExpand(true)}>
            <ExpandMore />
          </Button>
          <Typography variant="h6" sx={{ fontWeight: "bold" }}>
            SIMULATION RUN
          </Typography>
        </Stack>
      ) : (
        <Stack spacing="20px">
          <Stack direction="row" spacing="10px">
            <Button onClick={() => setExpand(false)}>
              <ExpandLess />
            </Button>
            <Typography
              variant="h6"
              sx={{
                fontWeight: "bold",
              }}
            >
              SIMULATION RUN
            </Typography>
          </Stack>
          <Stack spacing="20px" direction="row">
            {isRunningSimulation ? (
              <Button
                onClick={() => {
                  setIsRunningSimulation(false);
                  // call endpoint to stop simulation
                }}
              >
                Stop Running Simulation
              </Button>
            ) : (
              <Button
                onClick={() => {
                  setIsRunningSimulation(true);
                  // call endpoint to run simulation
                }}
              >
                Run Simulation
              </Button>
            )}
            {!isRunningSimulation && logs && summary && (
              <Button
                onClick={() => {
                  setHasReflection(true);
                  generateReflection();
                }}
              >
                REFLECT
              </Button>
            )}
          </Stack>
          <Stack spacing="20px" width="100%" direction="row">
            {config && (
              <Stack spacing="25px" width="100%">
                <Typography
                  variant="h6"
                  sx={{
                    fontWeight: "bold",
                  }}
                >
                  Original Configuration
                </Typography>
                <TextField
                  className={"code"}
                  rows={50}
                  value={config}
                  onChange={(e) => {
                    setConfig(e.target.value);
                    setUpdatedConfig(true);
                  }}
                  code={true}
                />
                <Button
                  disabled={!updatedConfig}
                  onClick={saveConfig}
                  sx={{ width: "100%" }}
                >
                  Update Config
                </Button>
              </Stack>
            )}
            {(isRunningSimulation || logs) && (
              <Stack width="33%" spacing="20px">
                <Stack direction="row" sx={{ justifyContent: "space-between" }}>
                  <Typography
                    variant="h6"
                    sx={{
                      fontWeight: "bold",
                    }}
                  >
                    Logs
                  </Typography>
                  <Button
                    onClick={() => {
                      getLogs();
                    }}
                  >
                    Get Logs
                  </Button>
                </Stack>
                <TextField
                  className={"Logs"}
                  value={logs}
                  readOnly={true}
                  code={true}
                />
              </Stack>
            )}
            {(isRunningSimulation || logs) && (
              <Stack width="33%" spacing="20px">
                <Stack direction="row" sx={{ justifyContent: "space-between" }}>
                  <Typography
                    variant="h6"
                    sx={{
                      fontWeight: "bold",
                    }}
                  >
                    Summary
                  </Typography>
                  <Button
                    onClick={() => {
                      getSummary();
                    }}
                  >
                    Get Summary
                  </Button>{" "}
                </Stack>
                <TextField
                  className={"Summary"}
                  value={summary}
                  readOnly={true}
                  code={true}
                />
              </Stack>
            )}
          </Stack>
        </Stack>
      )}
    </Stack>
  );
};

export default Run;
